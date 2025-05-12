#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import  annotations

from collections.abc import Callable
from typing import TypeVar, TYPE_CHECKING

from zepben.evolve.services.network.tracing.traversal.queue_condition import QueueCondition
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep

if TYPE_CHECKING:
    from zepben.evolve import Terminal, StepContext
    from zepben.evolve.services.network.tracing.feeder.feeder_direction import FeederDirection

T = TypeVar('T')


class DirectionCondition[T](QueueCondition[NetworkTraceStep[T]]):

    def __init__(self, direction: FeederDirection, get_direction: Callable[[Terminal], FeederDirection]):
        self.direction = direction
        self.get_direction = get_direction

    def should_queue(self, next_item: NetworkTraceStep[T], next_context: StepContext, current_item: NetworkTraceStep[T], current_context: StepContext[T]) -> bool:
        if next_item.path.traced_internally:
            return self.should_queue_start_item(next_item)
        else:
            return self.direction.complementary_external_direction in self.get_direction(next_item.path.to_terminal)

    def should_queue_start_item(self, item: NetworkTraceStep[T]) -> bool:
        return self.direction in self.get_direction(item.path.to_terminal)

