#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Callable, TypeVar

from zepben.evolve import Traversal, BasicTracker
from zepben.evolve.services.network.tracing.traversals.queue import Queue, depth_first
from zepben.evolve.services.network.tracing.traversals.tracker import Tracker

__all__ = ["BasicTraversal"]
T = TypeVar('T')


class BasicTraversal(Traversal[T]):
    """
    A basic traversal implementation that can be used to traverse any type of item.

    The traversal gets the next items to be traversed to by calling a user provided callback (next_), with the current
    item of the traversal. This function should return a list of ConnectivityResult's, that will get added to the
    process_queue for processing.

    The process queue, an instance of `Queue` is also supplied during construction. This gives the
    flexibility for this trace to be backed by any type of queue: breadth, depth, priority etc.

    The traversal also requires a `zepben.evolve.traversals.tracker.Tracker` to be supplied. This gives flexibility
    to track items in unique ways, more than just "has this item been visited" e.g. visiting more than once,
    visiting under different conditions etc.
    """

    queue_next: Callable[[T, BasicTraversal[T]], None]
    """A function that will be called at each step of the traversal to queue "adjacent" items."""

    process_queue: Queue[T] = depth_first()
    """Dictates the type of search to be performed on the network graph. Breadth-first, Depth-first, and Priority based searches are possible."""

    async def _run_trace(self, can_stop_on_start_item: bool = True):
        """
        Run's the trace. Stop conditions and step_actions are called with await, so you can utilise asyncio when
        performing a trace if your step actions or conditions are IO intensive. Stop conditions and
        step actions will always be called for each item in the order provided.
        `can_stop_on_start_item` Whether the trace can stop on the start_item. Actions will still be applied to
                                       the start_item.
        """
        can_stop = True

        if self.start_item:
            self.process_queue.put(self.start_item)
            can_stop = can_stop_on_start_item

        while not self.process_queue.empty():
            current = self.process_queue.get()
            if self.tracker.visit(current):
                stopping = can_stop and await self.matches_any_stop_condition(current)

                await self.apply_step_actions(current, stopping)
                if not stopping:
                    self.queue_next(current, self)

                can_stop = True

    def reset(self):
        self._reset_run_flag()
        self.process_queue.queue.clear()
        self.tracker.clear()
