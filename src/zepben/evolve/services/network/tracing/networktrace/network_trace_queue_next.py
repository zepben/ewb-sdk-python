#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from abc import ABC
from typing import TypeVar, Callable, Generator, Generic, List, Union, Type

from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.traversal.traversal import Traversal
from zepben.evolve.services.network.tracing.networktrace.compute_data import ComputeData, ComputeDataWithPaths
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext

T = TypeVar('T')

QueueItem = Callable[[NetworkTraceStep[T]], bool]
QueueBranch = Callable[[NetworkTraceStep[T]], bool]
GetNextSteps = Callable[[NetworkTraceStep[T], StepContext], Generator[NetworkTraceStep[T], None, None]]
GetNextStepsBranching = Callable[[NetworkTraceStep[T], StepContext], List[NetworkTraceStep[T]]]


class NetworkTraceQueueNext(ABC):
    state_operators = NetworkStateOperators

    def __init__(self, state_operators: Type[NetworkStateOperators]):
        self.state_operators = state_operators


    def next_trace_steps(self,
                          current_step: NetworkTraceStep[T],
                          current_context: StepContext,
                          compute_data: Union[ComputeData[T], ComputeDataWithPaths[T]]
                          ) -> Generator[NetworkTraceStep[T], None, None]:
        """ Builds a list of next `NetworkTraceStep` to add to the `NetworkTrace` queue """
        next_paths = list(self.state_operators.next_paths(current_step.path))
        if isinstance(compute_data, ComputeData):
            compute_next = lambda _it: compute_data.compute_next(current_step, current_context, _it)
        elif isinstance(compute_data, ComputeDataWithPaths):
            compute_next = lambda _it: compute_data.compute_next(current_step, current_context, _it, next_paths)
        else:
            raise TypeError(f'ComputeData was not of a recognised class: {compute_data.__class__} not in [ComputeData, ComputeDataWithPaths]')

        next_num_terminal_steps = current_step.next_num_terminal_steps()
        for it in next_paths:
            data = compute_next(it)
            yield NetworkTraceStep(it, next_num_terminal_steps, it.next_num_equipment_steps(current_step.num_equipment_steps), data)

    @staticmethod
    def Basic(state_operators: Type[NetworkStateOperators], compute_data: Union[ComputeData[T], ComputeDataWithPaths[T]]):
        return Basic(state_operators, compute_data)

    @staticmethod
    def Branching(state_operators: Type[NetworkStateOperators], compute_data: Union[ComputeData[T], ComputeDataWithPaths[T]]):
        return Branching(state_operators, compute_data)


class Basic(NetworkTraceQueueNext, Traversal.QueueNext[NetworkTraceStep[T]], Generic[T]):
    def __init__(self, state_operators: Type[NetworkStateOperators], compute_data: Union[ComputeData[T], ComputeDataWithPaths[T]]):
        super().__init__(state_operators)

        self._get_next_steps: GetNextSteps = lambda item, context: self.next_trace_steps(item, context, compute_data)

    def __iinit__(self, get_next_steps: GetNextSteps):
        self._get_next_steps: GetNextSteps = get_next_steps

    def accept(self, item: NetworkTraceStep[T], context: StepContext, queue_item: QueueItem):
        for it in self._get_next_steps(item, context):
            queue_item(it)


class Branching(NetworkTraceQueueNext, Traversal.BranchingQueueNext[NetworkTraceStep[T]], Generic[T]):
    def __init__(self, state_operators: Type[NetworkStateOperators], compute_data: Union[ComputeData[T], ComputeDataWithPaths[T]]):
        super().__init__(state_operators)
        
        self._get_next_steps: GetNextStepsBranching = lambda item, context: list(self.next_trace_steps(item, context, compute_data))

    def accept(self, item: NetworkTraceStep[T], context: StepContext, queue_item: QueueItem, queue_branch: QueueBranch):
        next_steps = self._get_next_steps(item, context)
        if len(next_steps) == 1:
            queue_item(next_steps[0])
        else:
            for step in next_steps:
                queue_branch(step)
