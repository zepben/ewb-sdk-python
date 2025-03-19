#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List, Optional, Iterable, Set

from zepben.evolve import Terminal, NetworkService, Feeder, PowerTransformer, Switch, ConductingEquipment, FeederDirection, \
    BusbarSection
from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.evolve.services.network.tracing.networktrace.tracing import Tracing

__all__ = ["SetDirection"]

from zepben.evolve.services.network.tracing.networktrace.network_trace import NetworkTrace

from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep


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
        return Tracing

    async def run(self, network: NetworkService):
        """
         Apply feeder directions from all feeder head terminals in the network.

         :param network: The network in which to apply feeder directions.
         """
        await self._run_terminals(
            [f.normal_head_terminal for f in network.objects(Feeder) if
             f.normal_head_terminal and not self._is_normally_open_switch(f.normal_head_terminal.conducting_equipment)])

    async def run_terminal(self, terminal: Terminal, network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL):
        """
         Apply [FeederDirection.DOWNSTREAM] from the [terminal].

         :param terminal: The terminal to start applying feeder direction from.
         """
        await self._create_traversal(network_state_operators).run(terminal, FeederDirection.DOWNSTREAM, can_stop_on_start_item=False)

    @staticmethod
    def _reached_substation_transformer(terminal: Terminal) -> bool:
        ce = terminal.conducting_equipment
        if not ce:
            return False

        return isinstance(ce, PowerTransformer) and ce.num_substations() > 0

    def _is_normally_open_switch(conducting_equipment: Optional[ConductingEquipment]):
        return isinstance(conducting_equipment, Switch) and conducting_equipment.is_normally_open()

