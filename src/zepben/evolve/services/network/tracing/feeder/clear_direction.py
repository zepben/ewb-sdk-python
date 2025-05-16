#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal

from zepben.evolve import FeederDirection, Traversal
from zepben.evolve.services.network.tracing.networktrace.tracing import Tracing
from zepben.evolve.services.network.tracing.traversal.weighted_priority_queue import WeightedPriorityQueue
from zepben.evolve.services.network.tracing.networktrace.network_trace import NetworkTrace
from zepben.evolve.services.network.tracing.networktrace.network_trace_action_type import NetworkTraceActionType
from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators

if TYPE_CHECKING:
    from zepben.evolve import StepContext, NetworkTraceStep


class ClearDirection:

    #
    #NOTE: We used to try and remove directions in a single pass rather than clearing (and the reapplying where needed) to be more efficient.
    #      However, this caused all sorts of pain when trying to determine which directions to remove from dual fed equipment that contains inner loops.
    #      We decided it is so much simpler to just clear the directions and reapply from other feeder heads even if its a bit more computationally expensive.
    #
    async def run(self,
            terminal: Terminal,
            network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL
            ) -> list[Terminal]:
        """
        Clears the feeder direction from a terminal and the connected equipment chain.
        This clears directions even if equipment is dual fed. A set of feeder head terminals encountered while running will be returned and directions
        can be reapplied if required using `set_direction`. Note that if you start on a feeder head terminal, this will be returned in the encountered
        feeder heads set.

        :param terminal: The `Terminal` from which to start the direction removal.
        :param network_state_operators: The `NetworkStateOperators` to be used when removing directions.
        :return : A set of feeder head `terminals` encountered when clearing directions
        """
        feeder_head_terminals: list[Terminal] = []

        trace = self._create_trace(network_state_operators, feeder_head_terminals)
        await trace.run(terminal, can_stop_on_start_item=False)
        return feeder_head_terminals

    @staticmethod
    def _create_trace(state_operators: NetworkStateOperators,
                      visited_feeder_head_terminals: list[Terminal]
                      ) -> NetworkTrace[Any]:
        def queue_condition(step: NetworkTraceStep, context: StepContext, _, __):
            return state_operators.get_direction(step.path.to_terminal) != FeederDirection.NONE

        def step_action(item, context):
            state_operators.set_direction(item.path.to_terminal, FeederDirection.NONE)
            visited_feeder_head_terminals.append(item.path.to_terminal) if item.path.to_terminal.is_feeder_head_terminal() else None

        return (
            Tracing.network_trace(
                network_state_operators=state_operators,
                action_step_type=NetworkTraceActionType.ALL_STEPS,
                queue=WeightedPriorityQueue.process_queue(
                    lambda it: it.path.to_terminal.phases.num_phases),
            )
            .add_condition(state_operators.stop_at_open())
            .add_queue_condition(queue_condition)
            .add_step_action(step_action)
        )