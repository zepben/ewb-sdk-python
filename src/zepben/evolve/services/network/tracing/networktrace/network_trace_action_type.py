#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Callable, Set, Any
from enum import Enum

from zepben.evolve import Terminal, SinglePhaseKind
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext

HasTracked = Callable[[Terminal, Set[SinglePhaseKind]], bool]
CanActionItem = Callable[[NetworkTraceStep[Any], StepContext, HasTracked], bool]


def _all_steps(item: NetworkTraceStep, context: StepContext, has_tracked: HasTracked) -> bool:
    return True


def _first_step_on_equipment(item: NetworkTraceStep[Any], context: StepContext, has_tracked: HasTracked) -> bool:
    phases = item.path.to_phases_set()
    return not any(has_tracked(it, phases) for it in item.path.to_terminal.other_terminals())


class NetworkTraceActionType(Enum):
    """
    Options to configure when a [NetworkTrace] actions a [NetworkTraceStep].
    """
    def __call__(self, *args, **kwargs) -> bool:
        return self.value(*args, **kwargs)

    ALL_STEPS: CanActionItem = _all_steps
    """
    All steps visited during a [NetworkTrace] will be actioned.
    """

    FIRST_STEP_ON_EQUIPMENT: CanActionItem = _first_step_on_equipment
    """
    Only actions steps where the `toEquipment` on the [NetworkTraceStep.path] has not been visited before on the phases within the [NetworkTraceStep.path].
    This means that all [NetworkTraceStep.type] of [NetworkTraceStep.Type.INTERNAL] will never be actioned as a first visit will always occur on an
    external step, except if the step is a start item in the trace.
    """
