from abc import abstractmethod
from enum import Enum

from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext


class NetworkTraceActionType(Enum):
    """
    Options to configure when a [NetworkTrace] actions a [NetworkTraceStep].
    """
    @classmethod
    def ALL_STEPS(cls):
        """
        All steps visited during a [NetworkTrace] will be actioned.
        """
        cls.can_action_item = cls._can_action_item_all_steps

    @classmethod
    def FIRST_STEP_ON_EQUIPMENT(cls):
        """
        Only actions steps where the `toEquipment` on the [NetworkTraceStep.path] has not been visited before on the phases within the [NetworkTraceStep.path].
        This means that all [NetworkTraceStep.type] of [NetworkTraceStep.Type.INTERNAL] will never be actioned as a first visit will always occur on an
        external step, except if the step is a start item in the trace.
        """
        cls.can_action_item = cls._can_action_item_first_step_on_equipment

    @staticmethod
    def can_action_item(item: NetworkTraceStep, context: StepContext, has_tracked) -> bool:  #TODO: type def for has_tracked
        pass

    @staticmethod
    def _can_action_item_all_steps(item: NetworkTraceStep, context: StepContext, has_tracked) -> bool:  # TODO: type def for has_tracked
        return True

    @staticmethod
    def _can_action_item_first_step_on_equipment(item: NetworkTraceStep, context: StepContext, has_tracked) -> bool:  # TODO: type def for has_tracked
        phases = item.path.nominal_phase_paths.to_phases_set()
        return not any(filter(lambda it: has_tracked(it, phases), item.path.to_terminal.other_terminals()))  # TODO: make sure i understood this right
