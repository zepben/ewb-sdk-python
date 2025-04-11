from abc import abstractmethod
from enum import Enum

from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext


class NetworkTraceActionType(Enum):
    """
    Options to configure when a [NetworkTrace] actions a [NetworkTraceStep].
    """
    @staticmethod
    def ALL_STEPS(item: NetworkTraceStep, context: StepContext, has_tracked) -> bool:
        """
        All steps visited during a [NetworkTrace] will be actioned.
        """
        return True

    @staticmethod
    def FIRST_STEP_ON_EQUIPMENT(item: NetworkTraceStep, context: StepContext, has_tracked) -> bool:  # TODO: type def for has_tracked
        """
        Only actions steps where the `toEquipment` on the [NetworkTraceStep.path] has not been visited before on the phases within the [NetworkTraceStep.path].
        This means that all [NetworkTraceStep.type] of [NetworkTraceStep.Type.INTERNAL] will never be actioned as a first visit will always occur on an
        external step, except if the step is a start item in the trace.
        """
        phases = item.path.to_phases_set()
        return not any(filter(lambda it: has_tracked(it, phases), item.path.to_terminal.other_terminals()))  # TODO: make sure i understood this right
