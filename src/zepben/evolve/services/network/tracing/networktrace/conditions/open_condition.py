#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections.abc import Callable
from typing import Generic

from typing_extensions import TypeVar

from zepben.evolve.services.network.tracing.networktrace.network_trace_queue_condition import NetworkTraceQueueCondition
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.model.cim.iec61970.base.wires.switch import Switch


T = TypeVar('T')


class OpenCondition(NetworkTraceQueueCondition[T], Generic[T]):
    def __init__(self, step_type: NetworkTraceStep.Type=NetworkTraceStep.Type.INTERNAL):
        super().__init__(step_type)

    def __call__(self, is_open: Callable[[Switch, SinglePhaseKind], bool], step_type: NetworkTraceStep.Type, phase: SinglePhaseKind = None):
        self.is_open = is_open
        self.phase = phase

    def should_queue_matched_step(self, next_item: NetworkTraceStep[T], next_context: StepContext, current_item: NetworkTraceStep[T], current_context: StepContext) -> bool:
        return not self.is_open(next_item.path.to_equipment, self.phase) if isinstance(next_item.path.to_equipment, Switch) else True

    def should_queue_start_item(self, item: T) -> bool:
        return True
