#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Generic, TypeVar, TYPE_CHECKING, Type

from zepben.evolve.services.network.tracing.traversal.context_value_computer import ContextValueComputer
from zepben.evolve.services.network.tracing.traversal.stop_condition import StopConditionWithContextValue

if TYPE_CHECKING:
    from zepben.evolve import ConductingEquipment, StepContext, NetworkTraceStep

T = TypeVar('T')
U = TypeVar('U')

__all__ = ['EquipmentTypeStepLimitCondition']


class EquipmentTypeStepLimitCondition(StopConditionWithContextValue[T], Generic[T, U]):
    def __init__(self, limit: int, equipment_type: Type[ConductingEquipment]):
        StopConditionWithContextValue.__init__(self, self.should_stop)
        ContextValueComputer.__init__(self, f'sdk:{equipment_type.name}Count')
        self.limit = limit
        self.equipment_type = equipment_type

    def should_stop(self, item: NetworkTraceStep[T], context: StepContext) -> bool:
        return self.get_context_value(context) >= self.limit

    def compute_initial_value(self, item: NetworkTraceStep[T]) -> int:
        return 0

    def compute_next_value(self, next_item: NetworkTraceStep[T], current_item: NetworkTraceStep[T], current_value: int) -> int:
        if next_item.path.traced_internally:
            return current_value
        if self.matches_equipment_type(next_item.path.to_equipment):
            return current_value + 1
        else:
            return current_value

    def matches_equipment_type(self, conducting_equipment: ConductingEquipment) -> bool:
        return isinstance(conducting_equipment, self.equipment_type)
