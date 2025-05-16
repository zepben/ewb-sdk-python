#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.connectors import BusbarSection
from zepben.evolve.model.cim.iec61970.base.wires.power_transformer import PowerTransformer

from zepben.evolve import Feeder, Traversal
from zepben.evolve.services.network.tracing.networktrace.compute_data import ComputeData
from zepben.evolve.services.network.tracing.networktrace.network_trace_action_type import NetworkTraceActionType
from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.evolve.services.network.tracing.networktrace.tracing import Tracing
from zepben.evolve.services.network.tracing.feeder.feeder_direction import FeederDirection
from zepben.evolve.services.network.tracing.networktrace.network_trace import NetworkTrace
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep


if TYPE_CHECKING:
    from zepben.evolve import NetworkService, Switch, ConductingEquipment

__all__ = ["SetDirection"]


class SetDirection:
    """
    Convenience class that provides methods for setting feeder direction on a [NetworkService]
    This class is backed by a [BranchRecursiveTraversal].
    """

    @staticmethod
    def _compute_data(reprocessed_loop_terminals: list[Terminal],
                      state_operators: NetworkStateOperators,
                      step: NetworkTraceStep[FeederDirection],
                      next_path: NetworkTraceStep.Path) -> FeederDirection:

        if next_path.to_equipment is BusbarSection:
            return FeederDirection.CONNECTOR

        direction_applied = step.data

        next_direction = FeederDirection.NONE
        if direction_applied == FeederDirection.UPSTREAM:
            next_direction = FeederDirection.DOWNSTREAM
        elif direction_applied in (FeederDirection.DOWNSTREAM, FeederDirection.CONNECTOR):
            next_direction = FeederDirection.UPSTREAM

        #
        # NOTE: Stopping / short-circuiting by checking that the next direction is already present in the toTerminal,
        #       causes certain looping network configurations not to be reprocessed. This means that some parts of
        #       loops do not end up with BOTH directions. This is done to stop massive computational blowout on
        #       large networks with weird looping connectivity that rarely happens in reality.
        #
        #       To allow these parts of the loop to be correctly processed without the computational blowout, we allow
        #       a single re-pass over the loop, controlled by the `reprocessedLoopTerminals` set.

        next_terminal_direction = state_operators.get_direction(next_path.to_terminal)

        if next_direction == FeederDirection.NONE:
            return FeederDirection.NONE
        elif next_direction not in next_terminal_direction:
            return next_direction
        elif next_terminal_direction == FeederDirection.BOTH:
            reprocessed_loop_terminals.append(next_path.to_terminal)
            return next_direction
        return FeederDirection.NONE

    async def _create_traversal(self, state_operators: NetworkStateOperators) -> NetworkTrace[FeederDirection]:
        reprocessed_loop_terminals: list[Terminal] = []

        def queue_condition(nts: NetworkTraceStep, *args):
            assert isinstance(nts.data, FeederDirection)
            return nts.data != FeederDirection.NONE

        async def step_action(nts: NetworkTraceStep, *args):
            state_operators.add_direction(nts.path.to_terminal, nts.data)

        def stop_condition(nts: NetworkTraceStep, *args):
            return nts.path.to_terminal.is_feeder_head_terminal() or self._reached_substation_transformer(nts.path.to_terminal)

        return (
            Tracing.network_trace_branching(
                network_state_operators=state_operators,
                action_step_type=NetworkTraceActionType.ALL_STEPS,
                compute_data=lambda step, _, next_path: self._compute_data(reprocessed_loop_terminals, state_operators, step, next_path)
            )
            .add_condition(state_operators.stop_at_open())
            .add_stop_condition(stop_condition)
            .add_queue_condition(queue_condition)
            .add_step_action(step_action)
        )

    @staticmethod
    def _reached_substation_transformer(terminal: Terminal) -> bool:
        ce = terminal.conducting_equipment
        if not ce:
            return False

        return isinstance(ce, PowerTransformer) and ce.num_substations() > 0

    @staticmethod
    def _is_normally_open_switch(conducting_equipment: Optional[ConductingEquipment]):
        return isinstance(conducting_equipment, Switch) and conducting_equipment.is_normally_open()

    async def run(self, network: NetworkService, network_state_operators: NetworkStateOperators):
        """
         Apply feeder directions from all feeder head terminals in the network.

         :param network: The network in which to apply feeder directions.
        :param network_state_operators: The `NetworkStateOperators` to be used when setting feeder direction
         """
        for terminal in (f.normal_head_terminal for f in network.objects(Feeder) if f.normal_head_terminal):
            head_terminal = terminal.conducting_equipment

            if head_terminal is not None:
                if not network_state_operators.is_open(head_terminal, None):
                    await self.run_terminal(terminal, network_state_operators)

    async def run_terminal(self, terminal: Terminal, network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL):
        """
         Apply [FeederDirection.DOWNSTREAM] from the [terminal].

         :param terminal: The terminal to start applying feeder direction from.
        :param network_state_operators: The `NetworkStateOperators` to be used when setting feeder direction
         """
        trav = await self._create_traversal(network_state_operators)
        return await trav.run(terminal, FeederDirection.DOWNSTREAM, can_stop_on_start_item=False)

