#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import abstractmethod
from typing import TypeVar

from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.traversal.queue_condition import QueueCondition
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext

T = TypeVar('T')


class NetworkTraceQueueCondition[T](QueueCondition[NetworkTraceStep[T]]):
    step_type:NetworkTraceStep.Type

    def __init__(self, step_type: NetworkTraceStep.Type):
        self.should_queue_func = {
        #herp = {
            NetworkTraceStep.Type.ALL: self.should_queue_matched_step,
            NetworkTraceStep.Type.INTERNAL: self.should_queue_internal_step,
            NetworkTraceStep.Type.EXTERNAL: self.should_queue_external_step
        }.get(step_type)
        #}
        #return herp.get(step_type)


    def should_queue(self, next_item: T, next_context: StepContext, current_item: T, current_context: StepContext) -> bool:
        self.should_queue_func(next_item, next_context, current_item, current_context)

    def should_queue_func(self):
        pass

    def should_queue_matched_step(self, next_item: NetworkTraceStep[T], next_context: StepContext, current_item: NetworkTraceStep[T], current_context: StepContext) -> bool:
        raise NotImplementedError()

    def should_queue_internal_step(self, next_item: NetworkTraceStep[T], next_context: StepContext, current_item: NetworkTraceStep[T], current_context: StepContext) -> bool:
        if next_item.type == NetworkTraceStep.Type.EXTERNAL:
            self.should_queue_matched_step(next_item, next_context, current_item, current_context)

    def should_queue_external_step(self, next_item: NetworkTraceStep[T], next_context: StepContext, current_item: NetworkTraceStep[T], current_context: StepContext) -> bool:
        if next_item.type == NetworkTraceStep.Type.INTERNAL:
            self.should_queue_matched_step(next_item, next_context, current_item, current_context)

    @staticmethod
    def delegate_to(step_type: NetworkTraceStep.Type, condition: QueueCondition[NetworkTraceStep[T]]) -> 'NetworkTraceQueueCondition[T]':
        return DelegatedNetworkTraceQueueCondition(step_type, condition)


class DelegatedNetworkTraceQueueCondition[T](NetworkTraceQueueCondition[T]):
    def __init__(self, step_type: NetworkTraceStep.Type, delegate: QueueCondition[NetworkTraceStep[T]]):
        super().__init__(step_type)
        self.delegate = delegate

    def should_queue_matched_step(self, next_item: NetworkTraceStep[T], next_context: StepContext, current_item: NetworkTraceStep[T], current_context: StepContext) -> bool:
        return self.delegate.should_queue(next_item, next_context, current_item, current_context)

    def should_queue_start_item(self, item: NetworkTraceStep[T]) -> bool:
        return self.delegate.should_queue_start_item(item)