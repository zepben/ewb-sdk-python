#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from zepben.protobuf.cim.iec61970.base.core.Terminal_pb2 import Terminal

from zepben.evolve import require, Feeder, Traversal
from zepben.evolve.services.network.tracing.networktrace.network_trace_action_type import NetworkTraceActionType
from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.evolve.services.network.tracing.networktrace.tracing import Tracing
from zepben.evolve.services.network.tracing.feeder.feeder_direction import FeederDirection
from zepben.evolve.services.network.tracing.networktrace.network_trace import NetworkTrace
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep


if TYPE_CHECKING:
    from zepben.evolve import NetworkService, PowerTransformer, Switch, \
        ConductingEquipment, BusbarSection

__all__ = ["SetDirection"]


class SetDirection:
    """
    Convenience class that provides methods for setting feeder direction on a [NetworkService]
    This class is backed by a [BranchRecursiveTraversal].
    """

    async def _compute_data(self,
                            reprocessed_loop_terminals: list[Terminal],
                            state_operators: NetworkStateOperators,
                            step: NetworkTraceStep[FeederDirection],
                            next_path: NetworkTraceStep.Path) -> FeederDirection:

        if next_path.to_equipment is BusbarSection:
            return FeederDirection.CONNECTOR

        direction_applied = step.data

        next_direction = FeederDirection.NONE
        if direction_applied == FeederDirection.UPSTREAM:
            next_direction = FeederDirection.DOWNSTREAM
        elif direction_applied in (FeederDirection.UPSTREAM, FeederDirection.CONNECTOR):
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
        elif (next_terminal_direction == FeederDirection.BOTH) and reprocessed_loop_terminals.append(next_path.to_terminal):
            return next_direction
        return FeederDirection.NONE

    async def _create_traversal(self, state_operators: NetworkStateOperators) -> NetworkTrace[FeederDirection]:
        reprocessed_loop_terminals: list[Terminal] = []

        def queue_condition(_in, *args):
            _, direction_to_apply = _in
            return direction_to_apply != FeederDirection.NONE

        def step_action(_in, _):
            path, direction_to_apply = _in
            return state_operators.add_direction(path.to_terminal, direction_to_apply)

        def stop_condition(_in, *args):
            path, direction_to_apply = _in
            return path.to_terminal.is_feeder_head_terminal or self._reached_substation_transformer(path.to_terminal)

        return (Tracing.network_trace_branching(
            network_state_operators=state_operators,
            action_step_type=NetworkTraceActionType.ALL_STEPS(),
            compute_data=lambda step, _, next_path: self._compute_data(reprocessed_loop_terminals, state_operators, step, next_path)
            ).add_condition(state_operators.stop_at_open())
               .add_stop_condition(Traversal.stop_condition(stop_condition))
               .add_queue_condition(Traversal.queue_condition(queue_condition))
               .add_step_action(Traversal.step_action(step_action))
        )

    @staticmethod
    def _reached_substation_transformer(terminal: Terminal) -> bool:
        ce = terminal.conducting_equipment
        if not ce:
            return False

        return isinstance(ce, PowerTransformer) and ce.num_substations() > 0

    def _is_normally_open_switch(conducting_equipment: Optional[ConductingEquipment]):
        return isinstance(conducting_equipment, Switch) and conducting_equipment.is_normally_open()

    async def run(self, network: NetworkService, network_state_operators: NetworkStateOperators):
        """
         Apply feeder directions from all feeder head terminals in the network.

         :param network: The network in which to apply feeder directions.
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
         """
        trav = await self._create_traversal(network_state_operators)
        return trav.run(terminal, FeederDirection.DOWNSTREAM, can_stop_on_start_item=False)

