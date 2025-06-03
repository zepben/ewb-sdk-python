#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing_extensions import TypeVar

from zepben.evolve.services.network.tracing.networktrace.network_trace_tracker import NetworkTraceTracker
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext
from zepben.evolve.services.network.tracing.traversal.traversal import Traversal, TraversalQueue

T = TypeVar('T')


class BusBranchTraceStep:
    def __init__(self, identified_object: T):
        self.identified_object = identified_object

class BusBranchTrace(Traversal):
    def __init__(self, queue_next: Traversal.QueueNext):
        self._tracker = NetworkTraceTracker()
        queue_type = Traversal.BasicQueueType(
            queue_next=queue_next,
            queue=TraversalQueue.depth_first()
        )
        super().__init__(queue_type)

    def on_reset(self) -> None:
        self._tracker.clear()

    def can_visit_item(self, item: BusBranchTraceStep, context: StepContext) -> bool:
        return self._tracker.visit(item.identified_object)

    def add_start_item(self, item: T) -> 'BusBranchTrace':
        super().add_start_item(BusBranchTraceStep(item))
        return self
