from abc import abstractmethod
from enum import Enum, member
from functools import partial
from typing import Callable

from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext


class EnumFunc:
    def __init__(self, func):
        self._func = func

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)


def _all_steps(item: NetworkTraceStep, context: StepContext, has_tracked) -> bool:
    return True


def _first_step_on_equipment(item: NetworkTraceStep, context: StepContext, has_tracked) -> bool:
    return not any(filter(lambda it: has_tracked(it, item.path.to_phases_set()), item.path.to_terminal.other_terminals()))  # TODO: make sure i understood this right


class NetworkTraceActionType(Enum):
    """
    Options to configure when a [NetworkTrace] actions a [NetworkTraceStep].
    """
    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)

    ALL_STEPS = EnumFunc(_all_steps)
    """
    All steps visited during a [NetworkTrace] will be actioned.
    """

    FIRST_STEP_ON_EQUIPMENT = EnumFunc(_first_step_on_equipment)
    """
    Only actions steps where the `toEquipment` on the [NetworkTraceStep.path] has not been visited before on the phases within the [NetworkTraceStep.path].
    This means that all [NetworkTraceStep.type] of [NetworkTraceStep.Type.INTERNAL] will never be actioned as a first visit will always occur on an
    external step, except if the step is a start item in the trace.
    """
