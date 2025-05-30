#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import TypeVar, Generic

from zepben.evolve.services.network.tracing.traversal.step_context import StepContext
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.traversal.stop_condition import StopCondition, ShouldStop

T = TypeVar('T')

__all__ = ['NetworkTraceStopCondition']


class NetworkTraceStopCondition(StopCondition[T], Generic[T]):
    """
    A special stop condition implementation that allows only checking `should_stop` when a [NetworkTraceStep] matches a given
    [NetworkTraceStep.Type]. When [step_type] is:
    *[NetworkTraceStep.Type.ALL]: [should_stop] will be checked for every step.
    *[NetworkTraceStep.Type.INTERNAL]: [should_stop] will be checked only when [NetworkTraceStep.type] is [NetworkTraceStep.Type.INTERNAL].
    *[NetworkTraceStep.Type.EXTERNAL]: [should_stop] will be checked only when [NetworkTraceStep.type] is [NetworkTraceStep.Type.EXTERNAL].

    If the step does not match the given step type, `false` will always be returned.
    """

    def __init__(self, step_type: NetworkTraceStep.Type, condition: ShouldStop):
        """
        :param step_type: The step type to match to check `should_stop`.
        :param condition: function with the signature of `ShouldStop` to be called when step_type matches the current items step
        """
        super().__init__(self.should_stop)
        if condition is not None:
            self.should_stop_matched_step = condition
        self.should_stop = self._should_stop_func(step_type)

    def should_stop(self, item: NetworkTraceStep[T], context: StepContext) -> bool:
        raise NotImplementedError()

    def should_stop_matched_step(self, item: NetworkTraceStep[T], context: StepContext) -> bool:
        """
        The logic you would normally put in `should_stop`. However, this will only be called when a step matches the `step_type`
        """
        raise NotImplementedError()

    def should_stop_internal_step(self, item: NetworkTraceStep[T], context: StepContext) -> bool:
        if item.type() == NetworkTraceStep.Type.INTERNAL:
            return self.should_stop_matched_step(item, context)
        return False

    def should_stop_external_step(self, item: NetworkTraceStep[T], context: StepContext) -> bool:
        # We also need to check start items as they are always marked as internal, but we still want to be able to stop on them.
        if (item.type() == NetworkTraceStep.Type.EXTERNAL) or context.is_start_item:
            return self.should_stop_matched_step(item, context)
        return False

    def _should_stop_func(self, step_type: NetworkTraceStep.Type) -> ShouldStop:
        if step_type == NetworkTraceStep.Type.ALL:
            return self.should_stop_matched_step
        elif step_type == NetworkTraceStep.Type.INTERNAL:
            return self.should_stop_internal_step
        elif step_type == NetworkTraceStep.Type.EXTERNAL:
            return self.should_stop_external_step
        raise ValueError(f"INTERNAL ERROR: step type [{step_type}] didn't match expected")
