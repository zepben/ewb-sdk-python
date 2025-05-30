#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import TypeVar, Generic

from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext

T = TypeVar('T')

__all__ = ['ComputeData', 'ComputeDataWithPaths']


class ComputeData(Generic[T]):
    """
    Functional interface used to compute contextual data stored on a NetworkTraceStep.
    """
    def __init__(self, func):
        self._func = func

    def compute_next(self, current_step: NetworkTraceStep[T], current_context: StepContext, next_path: NetworkTraceStep.Path) -> T:
        """
        Called for each new NetworkTraceStep in a NetworkTrace. The value returned from this function
        will be stored against the next step within NetworkTraceStep. data.

        `currentStep` - The current step of the trace.
        `currentContext` - The context of teh current step in the trace.
        `nextPath` - The next path of the next NetworkTraceStep that the data will be associated with.

        Returns The data to associate with the next NetworkTraceStep.
        """
        return self._func(current_step, current_context, next_path)

class ComputeDataWithPaths(Generic[T]):
    """
    Functional interface used to compute contextual data stored on a NetworkTraceStep. This can be used when the
    contextual data can only be computed by knowing all the next paths that can be stepped to from a given step.
    """
    def __init__(self, func):
        self._func = func or (lambda *args: None)

    def compute_next(self, current_step: NetworkTraceStep[T], current_context: StepContext, next_path: NetworkTraceStep.Path, next_paths: list[NetworkTraceStep.Path]) -> T:
        """
        Called for each new NetworkTraceStep in a NetworkTrace. The value returned from this function
        will be stored against the next step within NetworkTraceStep. data.

        `currentStep` - The current step of the trace.
        `currentContext` - The context of teh current step in the trace.
        `nextPath` - The next path of the next NetworkTraceStep that the data will be associated with.
        `nextPaths` - A list of all the next paths that the current step can trace to.

        Returns The data to associate with the next NetworkTraceStep.
        """
        return self._func(current_step, current_context, next_path, next_paths)
