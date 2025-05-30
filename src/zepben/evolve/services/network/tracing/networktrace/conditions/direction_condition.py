#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import  annotations

from typing import TypeVar, TYPE_CHECKING, Generic, Type

from zepben.evolve import require

from zepben.evolve.model.cim.iec61970.base.wires.clamp import Clamp
from zepben.evolve.model.cim.iec61970.base.wires.cut import Cut

from zepben.evolve.services.network.tracing.feeder.feeder_direction import FeederDirection
from zepben.evolve.services.network.tracing.traversal.queue_condition import QueueCondition
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep

if TYPE_CHECKING:
    from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
    from zepben.evolve import StepContext

T = TypeVar('T')

__all__ = ['DirectionCondition']


class DirectionCondition(QueueCondition[NetworkTraceStep[T]], Generic[T]):

    def __init__(self, direction: FeederDirection, state_operators: Type[NetworkStateOperators]):
        require(direction != FeederDirection.CONNECTOR, lambda: 'A direction of CONNECTOR is not currently supported')
        self.direction = direction
        self.state_operators = state_operators
        self.get_direction = self.state_operators.get_direction

    def should_queue(self, next_item: NetworkTraceStep[T], next_context: StepContext[T], current_item: NetworkTraceStep[T], current_context: StepContext[T]) -> bool:
        return self._should_queue(next_item.path)

    def _should_queue(self, path: NetworkTraceStep.Path) -> bool:
        # Cuts do weird things with directions depending on if they are energised from an external connection, or through a "closed" cut. To prevent
        # dealing with this awful mess, it is much simpler to just ask if anything else past it needs queueing. This could be made to short-circuit
        # for traversing downstream, but the code is much more complex to only save one extra step.
        if isinstance(path.to_equipment, Cut):
            return self._should_queue_next_paths(path)
        elif path.traced_internally or path.did_traverse_ac_line_segment:
            return self.direction in self.get_direction(path.to_terminal)
        else:
            return self.direction.complementary_external_direction in self.get_direction(path.to_terminal)

    def should_queue_start_item(self, item: NetworkTraceStep[T]) -> bool:
        if self.direction in self.get_direction(item.path.to_terminal):
            return True
        # Because cuts and clamps behave a bit different with directions than other equipment terminals, we can also check if any further paths needs to be
        # queued, and if they do we queue the start item.
        elif isinstance(item.path.to_equipment, (Clamp, Cut)):
            return self._should_queue_next_paths(item.path)
        return False

    def _should_queue_next_paths(self, path: NetworkTraceStep.Path) -> bool:
        for next_path in self.state_operators.next_paths(path):
            if not(next_path.traced_internally and self.state_operators.is_open(path.to_equipment)):
                if self._should_queue(next_path):
                    return True
        return False
