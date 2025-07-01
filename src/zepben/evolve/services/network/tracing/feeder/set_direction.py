#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from functools import singledispatchmethod
from logging import Logger
from typing import Optional, TYPE_CHECKING, Type

from zepben.evolve.model.cim.iec61970.base.core.equipment_container import Feeder
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.connectors import BusbarSection
from zepben.evolve.model.cim.iec61970.base.wires.cut import Cut
from zepben.evolve.model.cim.iec61970.base.wires.power_transformer import PowerTransformer
from zepben.evolve.services.network.tracing.feeder.feeder_direction import FeederDirection
from zepben.evolve.services.network.tracing.networktrace.conditions.conditions import stop_at_open
from zepben.evolve.services.network.tracing.networktrace.network_trace import NetworkTrace
from zepben.evolve.services.network.tracing.networktrace.network_trace_action_type import NetworkTraceActionType
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.evolve.services.network.tracing.networktrace.tracing import Tracing
from zepben.evolve.services.network.tracing.traversal.weighted_priority_queue import WeightedPriorityQueue

if TYPE_CHECKING:
    from zepben.evolve import NetworkService, Switch, ConductingEquipment

__all__ = ["SetDirection"]


class SetDirection:
    """
    Convenience class that provides methods for setting feeder direction on a [NetworkService]
    This class is backed by a [BranchRecursiveTraversal].
    """

    def __init__(self, debug_logger: Logger = None):
        self._debug_logger = debug_logger

    @staticmethod
    def _compute_data(
        reprocessed_loop_terminals: list[Terminal],
        state_operators: Type[NetworkStateOperators],
        step: NetworkTraceStep[FeederDirection],
        next_path: NetworkTraceStep.Path
    ) -> FeederDirection:

        if next_path.to_equipment is BusbarSection:
            return FeederDirection.CONNECTOR

        def next_direction_func():
            if step.data == FeederDirection.NONE:
                return FeederDirection.NONE
            elif next_path.traced_internally:
                return FeederDirection.DOWNSTREAM
            elif isinstance(next_path.to_equipment, Cut):
                return FeederDirection.UPSTREAM
            elif next_path.did_traverse_ac_line_segment:
                return FeederDirection.DOWNSTREAM
            else:
                return FeederDirection.UPSTREAM

        next_direction = next_direction_func()

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

    def _create_traversal(self, state_operators: Type[NetworkStateOperators]) -> NetworkTrace[FeederDirection]:
        reprocessed_loop_terminals: list[Terminal] = []

        return (
            Tracing.network_trace_branching(
                network_state_operators=state_operators,
                action_step_type=NetworkTraceActionType.ALL_STEPS,
                debug_logger=self._debug_logger,
                name=f'SetDirection({state_operators.description})',
                queue_factory=lambda: WeightedPriorityQueue.process_queue(lambda it: it.path.to_terminal.phases.num_phases),
                branch_queue_factory=lambda: WeightedPriorityQueue.branch_queue(lambda it: it.path.to_terminal.phases.num_phases),
                compute_data=lambda step, _, next_path: self._compute_data(reprocessed_loop_terminals, state_operators, step, next_path)
            )
            .add_condition(stop_at_open())
            .add_stop_condition(
                lambda nts, ctx: nts.path.to_terminal.is_feeder_head_terminal() or
                                 self._reached_substation_transformer(nts.path.to_terminal)
            )
            .add_queue_condition(lambda nts, *args: nts.data != FeederDirection.NONE)
            .add_step_action(
                lambda nts, ctx: state_operators.add_direction(nts.path.to_terminal, nts.data)
            )
        )

    @staticmethod
    def _reached_substation_transformer(terminal: Terminal) -> bool:
        if ce := terminal.conducting_equipment:
            return isinstance(ce, PowerTransformer) and ce.num_substations() > 0
        return False

    @staticmethod
    def _is_normally_open_switch(conducting_equipment: Optional[ConductingEquipment]):
        return isinstance(conducting_equipment, Switch) and conducting_equipment.is_normally_open()

    @singledispatchmethod
    async def run(self, network: NetworkService, network_state_operators: Type[NetworkStateOperators]):
        """
         Apply feeder directions from all feeder head terminals in the network.

         :param network: The network in which to apply feeder directions.
         :param network_state_operators: The `NetworkStateOperators` to be used when setting feeder direction
         """

        for terminal in (f.normal_head_terminal for f in network.objects(Feeder) if f.normal_head_terminal):
            if (head_terminal := terminal.conducting_equipment) is not None:
                if not network_state_operators.is_open(head_terminal, None):
                    await self.run_terminal(terminal, network_state_operators)

    @run.register
    async def run_terminal(self, terminal: Terminal, network_state_operators: Type[NetworkStateOperators] = NetworkStateOperators.NORMAL):
        """
         Apply [FeederDirection.DOWNSTREAM] from the [terminal].

         :param terminal: The terminal to start applying feeder direction from.
         :param network_state_operators: The `NetworkStateOperators` to be used when setting feeder direction
         """

        return await (self._create_traversal(network_state_operators)
                      .run(terminal, FeederDirection.DOWNSTREAM, can_stop_on_start_item=False))
