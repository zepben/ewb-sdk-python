#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing_extensions import TypeVar

from zepben.evolve.services.network.tracing.traversal.step_context import StepContext
from zepben.evolve.services.network.tracing.traversal.traversal import Traversal, TraversalQueue

T = TypeVar('T')


class BusBranchTraceStep:
    def __init__(self, identified_object: T):
        self.identified_object = identified_object


class BusBranchTracker:
    """
    Internal class that tracks the visited state of a Terminal in a BusBranchTrace
    """
    def __init__(self):
        self._visited = list()

    def has_visited(self, item: BusBranchTraceStep):
        """Returns true if this terminal has been visited"""
        return self._get_key(item) in self._visited

    def visit(self, item: BusBranchTraceStep) -> bool:
        """Marks the terminal as visited. returns False if we already have visited it, True otherwise"""
        if self.has_visited(item):
            return False
        self._visited.append(self._get_key(item))
        return True

    def clear(self):
        """Clear the visit state tracker"""
        self._visited.clear()

    @staticmethod
    def _get_key(item: BusBranchTraceStep):
        return item.identified_object


class BusBranchTrace(Traversal):
    def __init__(self, queue_next: Traversal.QueueNext):
        self._tracker = BusBranchTracker()
        queue_type = Traversal.BasicQueueType(
            queue_next=queue_next,
            queue=TraversalQueue.depth_first()
        )
        super().__init__(queue_type)

    def on_reset(self):
        self._tracker.clear()

    def can_visit_item(self, item: BusBranchTraceStep, context: StepContext) -> bool:
        return self._tracker.visit(item)

    def add_start_item(self, item: T) -> 'BusBranchTrace':
        super().add_start_item(BusBranchTraceStep(item))
        return self
