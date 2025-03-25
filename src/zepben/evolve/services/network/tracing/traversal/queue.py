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
from typing import TypeVar, Iterable
from heapq import heappush, heappop

__all__ = ["FifoQueue", "LifoQueue", "PriorityQueue", "TraversalQueue"]

T = TypeVar('T')


class TraversalQueue[T]:
    """
    Basic queue object, implementing some methods to align it with the kotlin sdk syntax,
    """
    def __init__(self, queue=None):
        if queue is None:
            self.queue = deque()
        else:
            self.queue = queue

    def len(self):
        return self.__len__()

    def __len__(self):
        return len(self.queue)

    @classmethod
    @property
    def depth_first(cls):
        return cls(FifoQueue())

    @classmethod
    @property
    def breadth_first(cls):
        return cls(LifoQueue())

    def has_next(self) -> bool:
        return len(self.queue) > 0

    def next(self):
        self.queue.get()

    def get(self, item: T) -> U:
        return self.queue.get(item)

    def put(self, item: T) -> bool:
        return self.queue.put(item)

    def extend(self, items: Iterable[T]) -> bool:
        return self.queue.extend(items)

    def peek(self) -> T:
        return self.queue.peek()

    def clear(self):
        return self.queue.clear()


class FifoQueue(TraversalQueue[T]):
    """Used for Breadth-first Traversal's"""

    def put(self, item: T):
        self.queue.append(item)

    def extend(self, items: Iterable[T]):
        self.queue.extend(items)

    def get(self) -> T:
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

    def peek(self) -> T:
        """
        Retrieve next item on queue, but don't remove from queue.
        Returns Next item on the queue
        """
        return self.queue[0]

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

    def get(self) -> T:
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

    def peek(self) -> T:
        """
        Retrieve next item on queue, but don't remove from queue.
        Returns Next item on the queue
        """
        return self.queue[-1]

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

    def get(self) -> T:
        """
        Get the next item in the queue, removing it from the queue.
        Returns The next item in the queue by priority.
        Raises `IndexError` if the queue is empty
        """
        return heappop(self.queue)

    def peek(self) -> T:
        """
        Retrieve the next item in the queue, but don't remove it from the queue.
        Note that you shouldn't modify the returned item after using this function, as you could change its
        priority and thus corrupt the queue. Always use `get` if you intend on modifying the result.
        Returns The next item in the queue
        """
        return self.queue[0]

    def empty(self) -> bool:
        return len(self) == 0

    def clear(self):
        """Clear the queue."""
        self.queue.clear()

    def copy(self) -> PriorityQueue[T]:
        return PriorityQueue(self.queue.copy())

