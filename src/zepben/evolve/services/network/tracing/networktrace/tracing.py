#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import TypeVar

from zepben.evolve import TraversalQueue, require
from zepben.evolve.services.network.tracing.networktrace.compute_data import ComputeData
from zepben.evolve.services.network.tracing.networktrace.network_trace import NetworkTrace
from zepben.evolve.services.network.tracing.networktrace.network_trace_action_type import NetworkTraceActionType
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators

T = TypeVar('T')


class Tracing:
    @staticmethod
    def network_trace(network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL,
                      action_step_type: NetworkTraceActionType=NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT,
                      queue: TraversalQueue[NetworkTraceStep[T]]=TraversalQueue.depth_first,
                      compute_data: ComputeData[T]=None
                      ) -> NetworkTrace[T]:
        """
        Creates a `NetworkTrace` that computes contextual data for every step.

        :param network_state_operators: The state operators to make the NetworkTrace state aware. Defaults to `NetworkStateOperators.NORMAL`.
        :param action_step_type: The action step type to be applied when the trace steps. Defaults to `NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT`.
        :param queue: The traversal queue the trace is backed by. Defaults to a depth first queue.
        :param compute_data: The computer that provides the [NetworkTraceStep.data] contextual step data for each step in the trace.

        :returns: a new `NetworkTrace`
        """
        require(compute_data is not None, lambda: f'compute_data cannot be None')  # if we change the signature this check isnt required, but the jvm
                                                                                       # sdk signature has this param last
        return NetworkTrace(network_state_operators, queue, action_step_type, compute_data)

    
