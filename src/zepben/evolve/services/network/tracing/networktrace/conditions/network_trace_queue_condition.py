#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import TypeVar, Generic

from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.traversal.queue_condition import QueueCondition, ShouldQueue
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext

T = TypeVar('T')

__all__ = ['NetworkTraceQueueCondition']


class NetworkTraceQueueCondition(QueueCondition[NetworkTraceStep[T]], Generic[T]):
    """
    A special queue condition implementation that allows only checking `should_queue` when a [NetworkTraceStep] matches a given
    [NetworkTraceStep.Type]. When [step_type] is:
    *[NetworkTraceStep.Type.ALL]: [should_queue] will be called for every step.
    *[NetworkTraceStep.Type.INTERNAL]: [shouldQueue] will be called only when [NetworkTraceStep.type] is [NetworkTraceStep.Type.INTERNAL].
    *[NetworkTraceStep.Type.EXTERNAL]: [shouldQueue] will be called only when [NetworkTraceStep.type] is [NetworkTraceStep.Type.EXTERNAL].

    If the step does not match the given step type, `true` will always be returned.
    """

    def __init__(self, step_type: NetworkTraceStep.Type, condition: ShouldQueue=None):
        """
        :param step_type: The step type to match to check `should_queue`.
        :param condition: function with the signature of `ShouldQueue` to be called when step_type matches the current items step
        """
        super().__init__(self.should_queue)
        if condition is not None:
            self.should_queue_matched_step = condition
        self.should_queue = self._should_queue_func(step_type)

    def should_queue(self, next_item: T, next_context: StepContext, current_item: T, current_context: StepContext) -> bool:
        raise NotImplementedError()

    def should_queue_matched_step(self, next_item: NetworkTraceStep[T], next_context: StepContext, current_item: NetworkTraceStep[T], current_context: StepContext) -> bool:
        """
        The logic you would normally put in `should_queue`. However, this will only be called when a step matches the `step_type`
        """
        raise NotImplementedError()

    def should_queue_internal_step(self, next_item: NetworkTraceStep[T], next_context: StepContext, current_item: NetworkTraceStep[T], current_context: StepContext) -> bool:
        if next_item.type() == NetworkTraceStep.Type.INTERNAL:
            return self.should_queue_matched_step(next_item, next_context, current_item, current_context)
        return True

    def should_queue_external_step(self, next_item: NetworkTraceStep[T], next_context: StepContext, current_item: NetworkTraceStep[T], current_context: StepContext) -> bool:
        if next_item.type() == NetworkTraceStep.Type.EXTERNAL:
            return self.should_queue_matched_step(next_item, next_context, current_item, current_context)
        return True

    def _should_queue_func(self, step_type: NetworkTraceStep.Type) -> ShouldQueue:
        if step_type == NetworkTraceStep.Type.ALL:
            return self.should_queue_matched_step
        elif step_type == NetworkTraceStep.Type.INTERNAL:
            return self.should_queue_internal_step
        elif step_type == NetworkTraceStep.Type.EXTERNAL:
            return self.should_queue_external_step
        raise ValueError(f"INTERNAL ERROR: step type [{step_type}] didn't match expected")
