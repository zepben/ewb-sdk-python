#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ['OpenCondition']

from collections.abc import Callable
from typing import Generic, TYPE_CHECKING

from typing_extensions import TypeVar

from zepben.ewb.services.network.tracing.networktrace.conditions.network_trace_queue_condition import NetworkTraceQueueCondition
from zepben.ewb.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.switch import Switch
    from zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
    from zepben.ewb.services.network.tracing.traversal.step_context import StepContext

T = TypeVar('T')


class OpenCondition(NetworkTraceQueueCondition[T], Generic[T]):
    def __init__(self, is_open: Callable[[Switch, SinglePhaseKind], bool], phase: SinglePhaseKind = None):
        super().__init__(NetworkTraceStep.Type.INTERNAL)
        self._is_open = is_open
        self._phase = phase

    def should_queue_matched_step(self, next_item: NetworkTraceStep[T], next_context: StepContext, current_item: NetworkTraceStep[T],
                                  current_context: StepContext) -> bool:
        from zepben.ewb.model.cim.iec61970.base.wires.switch import Switch
        equip = next_item.path.to_equipment
        if isinstance(equip, Switch):
            return not self._is_open(equip, self._phase)
        else:
            return True
