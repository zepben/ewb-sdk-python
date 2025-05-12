#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.


from __future__ import annotations

from collections import deque
from typing import TypeVar, Iterable, Generic
from heapq import heappush, heappop

__all__ = ["FifoQueue", "LifoQueue", "PriorityQueue", "TraversalQueue"]

T = TypeVar('T')
U = TypeVar('U')


# TODO: the methods in these classes overlap in a slightly unclear way, this needs to be tidied up.

class TraversalQueue(Generic[T]):
    """
    Basic queue object, implementing some methods to align it with the kotlin sdk syntax,
    """
    def __init__(self, queue=None):
        if queue is None:
            self.queue = deque()
        else:
            self.queue = queue

    def __iter__(self):
        return self.queue.__iter__()

    def __len__(self):
        return len(self.queue)

    @classmethod
    def breadth_first(cls) -> TraversalQueue:
        """ Creates a new instance backed by a breadth first (FIFO) queue. """
        return cls(FifoQueue())

    @classmethod
    def depth_first(cls) -> TraversalQueue:
        """ Creates a new instance backed by a depth first (LIFO) queue. """
        return cls(LifoQueue())

    def has_next(self) -> bool:
        """ :return: True if the queue has more items. """
        return len(self.queue) > 0

    def pop(self):
        return self.queue.pop()

    def put(self, item: T) -> bool:
        self.queue.put(item)
        return True

    def extend(self, items: Iterable[T]) -> bool:
        return self.queue.extend(items)

    def clear(self):
        return self.queue.clear()


class FifoQueue(TraversalQueue[T]):
    """Used for Breadth-first Traversal's"""

    def put(self, item: T):
        return self.queue.append(item)

    def extend(self, items: Iterable[T]):
        return self.queue.extend(items)

    def pop(self) -> T:
        """
        Pop an item off the queue.
        Raises `IndexError` if the queue is empty.
        """
        return self.queue.popleft()

    def empty(self) -> bool:
        """
        Check if queue is empty
        Returns True if empty, False otherwise
        """
        return len(self.queue) == 0

    def clear(self):
        """Clear the queue."""
        self.queue.clear()

    def copy(self) -> FifoQueue[T]:
        return FifoQueue(self.queue.copy())


class LifoQueue(TraversalQueue[T]):
    """Used for Depth-first Traversal's"""

    def put(self, item: T):
        self.queue.append(item)

    def extend(self, items: Iterable[T]):
        self.queue.extend(items)

    def pop(self) -> T:
        """
        Pop an item off the queue.
        Raises `IndexError` if the queue is empty.
        """
        return self.queue.pop()

    def empty(self) -> bool:
        """
        Check if queue is empty
        Returns True if empty, False otherwise
        """
        return len(self.queue) == 0

    def clear(self):
        """Clear the queue."""
        self.queue.clear()

    def copy(self) -> LifoQueue[T]:
        return LifoQueue(self.queue.copy())


class PriorityQueue(TraversalQueue[T]):
    """Used for custom `Traversal`s"""

    def __init__(self, queue=None):
        if queue is None:
            super().__init__([])
        else:
            super().__init__(queue)

    def __len__(self):
        return len(self.queue)

    def put(self, item: T):
        """
        Place an item in the queue based on its priority.
        `item` The item to place on the queue. Must implement `__lt__`
        Returns True if put was successful, False otherwise.
        """
        heappush(self.queue, item)

    def extend(self, items: Iterable[T]):
        for item in items:
            heappush(self.queue, item)

    def pop(self) -> T:
        """
        Get the next item in the queue, removing it from the queue.
        Returns The next item in the queue by priority.
        Raises `IndexError` if the queue is empty
        """
        return heappop(self.queue)

    def empty(self) -> bool:
        return len(self) == 0

    def clear(self):
        """Clear the queue."""
        self.queue.clear()

    def copy(self) -> PriorityQueue[T]:
        return PriorityQueue(self.queue.copy())

