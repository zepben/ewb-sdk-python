#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations
from typing import TypeVar, Iterable, Generic


from zepben.evolve.services.network.tracing.traversal.traversal_queue import TraversalQueue
T = TypeVar('T')

# TODO: i strongly dislike that ive essentially wrapped a pre existing class in 2 layers just so the
#  code reads the same.. *discussion point*


class BasicQueue(TraversalQueue[T]):
    def has_next(self) -> bool:
        return len(self.queue) > 0

    def get(self) -> T:
        """
        Pop an item off the queue.
        Raises `IndexError` if the queue is empty.
        """
        return self.queue.pop()

    def put(self, item: T):
        self.queue.append(item)

    def extend(self, items: Iterable[T]):
        self.queue.extend(items)

    def peek(self) -> T:
        """
        Retrieve next item on queue, but don't remove from queue.
        Returns Next item on the queue
        """
        return self.queue[0]

    def clear(self):
        """Clear the queue."""
        self.queue.clear()
