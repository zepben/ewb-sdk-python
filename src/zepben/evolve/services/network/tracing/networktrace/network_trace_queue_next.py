#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import TypeVar, Callable, Sequence

from zepben.protobuf.cim.iec61970.base.core.ConductingEquipment_pb2 import ConductingEquipment

from zepben.evolve.services.network.tracing.traversal.step_context import StepContext
from zepben.evolve.services.network.tracing.networktrace.compute_data import ComputeData, ComputeDataWithPaths
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.traversal.traversal import QueueNext, BranchingQueueNext

T = TypeVar('T')

CheckInService = Callable[[ConductingEquipment], bool]


class NetworkTraceQueueNext:
    def basic(self, is_in_service: CheckInService, compute_data: ComputeData[T]) -> QueueNext[NetworkTraceStep[T]]:
        if isinstance(compute_data, ComputeData):
            return lambda item, context, queue_item: map(queue_item ,self._next_trace_steps(is_in_service, item, context, compute_data))
        elif isinstance(compute_data, ComputeDataWithPaths):
            return lambda item, context, queue_item: map(queue_item, self._next_trace_steps(is_in_service, item, context, compute_data))

    def branching(self, is_in_service: CheckInService, compute_data: ComputeData[T]) -> BranchingQueueNext[NetworkTraceStep[T]]:
        if isinstance(compute_data, ComputeData):
            return lambda item, context, queue_item, queue_branch: self._queue_next_steps_branching(list(self._next_trace_steps(is_in_service, item, context, compute_data)), queue_item, queue_branch)
        elif isinstance(compute_data, ComputeDataWithPaths):
            return lambda item, context, queue_item, queue_branch: self._queue_next_steps_branching(self._next_trace_steps(is_in_service, item, context, compute_data), queue_item, queue_branch)

    @staticmethod
    def _queue_next_steps_branching(next_steps: list[NetworkTraceStep[T]],
                                    queue_item: Callable[[NetworkTraceStep[T]], bool],
                                    queue_branch: Callable[[NetworkTraceStep[T]], bool]):
        queue_item(next_steps[0]) if len(next_steps) == 1 else map(queue_branch, next_steps)

    @staticmethod
    def _next_trace_steps(is_in_service: CheckInService,
                          current_step: NetworkTraceStep[T],
                          current_contrext: StepContext,
                          compute_data: ComputeData[T]
                          ) -> Sequence[NetworkTraceStep[T]]:
        return map()
