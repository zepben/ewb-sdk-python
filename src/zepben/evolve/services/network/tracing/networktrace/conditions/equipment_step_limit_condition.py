#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Generic, TypeVar

from zepben.evolve import StepContext, NetworkTraceStep
from zepben.evolve.services.network.tracing.traversal.stop_condition import StopCondition

T = TypeVar('T')


class EquipmentStepLimitCondition(StopCondition, Generic[T]):
    def __init__(self, limit: int):
        super().__init__(self.should_stop)
        self.limit = limit

    def should_stop(self, item: NetworkTraceStep[T], context: StepContext) -> bool:
        return item.num_equipment_steps >= self.limit