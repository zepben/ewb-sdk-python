#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC
from typing import TypeVar, Callable, Generator, Generic, List, Union

from zepben.evolve.services.network.tracing.networktrace.network_trace_step_path_provider import NetworkTraceStepPathProvider

from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.traversal.traversal import Traversal

T = TypeVar('T')

from zepben.evolve.services.network.tracing.networktrace.compute_data import ComputeData, ComputeDataWithPaths
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext
QueueItem = Callable[[NetworkTraceStep[T]], bool]
QueueBranch = Callable[[NetworkTraceStep[T]], bool]
GetNextSteps = Callable[[NetworkTraceStep[T], StepContext], Generator[NetworkTraceStep[T], None, None]]
GetNextStepsBranching = Callable[[NetworkTraceStep[T], StepContext], List[NetworkTraceStep[T]]]


class NetworkTraceQueueNext(ABC):
    path_provider = NetworkTraceStepPathProvider

    def __init__(self, path_provider: NetworkTraceStepPathProvider):
        self.path_provider = path_provider


    def next_trace_steps(self,
                          current_step: NetworkTraceStep[T],
                          current_context: StepContext,
                          compute_data: Union[ComputeData[T], ComputeDataWithPaths[T]]
                          ) -> Generator[NetworkTraceStep[T], None, None]:
        """ Builds a list of next `NetworkTraceStep` to add to the `NetworkTrace` queue """
        next_paths = self.path_provider.next_paths(current_step.path)
        if isinstance(compute_data, ComputeData):
            compute_next = lambda it: compute_data.compute_next(current_step, current_context, it)
        elif isinstance(compute_data, ComputeDataWithPaths):
            next_paths = list(next_paths)
            compute_next = lambda it: compute_data.compute_next(current_step, current_context, it, next_paths)
        else:
            raise TypeError(f'ComputeData was not of a recognised class: {compute_data.__class__} not in [ComputeData, ComputeDataWithPaths]')

        next_num_terminal_steps = current_step.next_num_terminal_steps()
        for it in next_paths:
            data = compute_next(it)
            yield NetworkTraceStep(it, next_num_terminal_steps, it.next_num_equipment_steps(current_step.num_equipment_steps), data)

    @staticmethod
    def Basic(path_provider: NetworkTraceStepPathProvider, compute_data: Union[ComputeData[T], ComputeDataWithPaths[T]]):
        return Basic(path_provider, compute_data)

    @staticmethod
    def Branching(path_provider: NetworkTraceStepPathProvider, compute_data: Union[ComputeData[T], ComputeDataWithPaths[T]]):
        return Branching(path_provider, compute_data)


class Basic(NetworkTraceQueueNext, Traversal.QueueNext[NetworkTraceStep[T]], Generic[T]):
    def __init__(self, path_provider: NetworkTraceStepPathProvider, compute_data: Union[ComputeData[T], ComputeDataWithPaths[T]]):
        super().__init__(path_provider)

        self._get_next_steps: GetNextSteps = lambda item, context: self.next_trace_steps(item, context, compute_data)

    def __iinit__(self, get_next_steps: GetNextSteps):
        self._get_next_steps: GetNextSteps = get_next_steps

    def accept(self, item: NetworkTraceStep[T], context: StepContext, queue_item: QueueItem):
        for it in self._get_next_steps(item, context):
            queue_item(it)


class Branching(NetworkTraceQueueNext, Traversal.BranchingQueueNext[NetworkTraceStep[T]], Generic[T]):
    def __init__(self, path_provider: NetworkTraceStepPathProvider, compute_data: Union[ComputeData[T], ComputeDataWithPaths[T]]):
        super().__init__(path_provider)
        
        self._get_next_steps: GetNextStepsBranching = lambda item, context: list(self.next_trace_steps(item, context, compute_data))

    def accept(self, item: NetworkTraceStep[T], context: StepContext, queue_item: QueueItem, queue_branch: QueueBranch):
        next_steps = list(self._get_next_steps(item, context))
        if len(next_steps) == 1:
            queue_item(next_steps[0])
        else:
            for step in next_steps:
                queue_branch(step)

