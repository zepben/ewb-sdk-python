#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations
from collections import deque
from abc import abstractmethod, ABC
from typing import TypeVar, Generic, Iterable
from heapq import heappush, heappop

__all__ = ["Queue", "FifoQueue", "LifoQueue", "PriorityQueue", "depth_first", "breadth_first"]
T = TypeVar('T')


def depth_first():
    return LifoQueue()


def breadth_first():
    return FifoQueue()


class Queue(Generic[T], ABC):
    def __init__(self, queue=None):
        if queue is None:
            self.queue = deque()
        else:
            self.queue = queue

    @abstractmethod
    def put(self, item: T):
        raise NotImplementedError()

    @abstractmethod
    def extend(self, items: Iterable[T]):
        raise NotImplementedError()

    @abstractmethod
    def get(self) -> T:
        """
        Pop an item off the queue.
        Raises `IndexError` if the queue is empty.
        """
        raise NotImplementedError()

    @abstractmethod
    def empty(self) -> bool:
        """
        Check if queue is empty
        Returns True if empty, False otherwise
        """
        raise NotImplementedError()

    @abstractmethod
    def peek(self) -> T:
        """
        Retrieve next item on queue, but don't remove from queue.
        Returns Next item on the queue
        """
        raise NotImplementedError()

    @abstractmethod
    def clear(self):
        """Clear the queue."""
        raise NotImplementedError()

    @abstractmethod
    def copy(self) -> Queue[T]:
        """Create a copy of this Queue"""
        raise NotImplementedError()


class FifoQueue(Queue[T]):
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


class LifoQueue(Queue[T]):
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


class PriorityQueue(Queue[T]):
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
