#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from abc import abstractmethod, ABCMeta
from collections import deque
from typing import TypeVar, Iterable, Generic, Deque, TYPE_CHECKING, Union

T = TypeVar('T')
U = TypeVar('U')

__all__ = ["TraversalQueue"]


class FIFODeque(deque):
    def pop(self):
        return self.popleft()

    def peek(self) -> T:
        return self[-1]


class LIFODeque(deque):
    def peek(self) -> T:
        return self[0]


class TraversalQueue(Generic[T], metaclass=ABCMeta):
    """
    Basic queue object, implementing some methods to align it with the kotlin sdk syntax,
    """
    @abstractmethod
    def __len__(self):
        """:return: the length of the queue"""

    @classmethod
    def breadth_first(cls) -> TraversalQueue[T]:
        """ Creates a new instance backed by a breadth first (FIFO) queue. """
        return BasicQueue(FIFODeque())

    @classmethod
    def depth_first(cls) -> TraversalQueue[T]:
        """ Creates a new instance backed by a depth first (LIFO) queue. """
        return BasicQueue(LIFODeque())

    @abstractmethod
    def has_next(self) -> bool:
        """:return: True if the queue has more items."""

    @abstractmethod
    def pop(self):
        """:return: The next item in the queue"""

    @abstractmethod
    def append(self, item: T) -> bool:
        """
        Adds an item to the queue

        :param item: The item to be added to the queue

        :return: True if the item was added
        """

    @abstractmethod
    def extend(self, items: Iterable[T]):
        """
        Adds the items to the queue

        :param items: The items to be added to the queue
        """

    @abstractmethod
    def peek(self) -> T:
        """:return: The next item on the queue without removing it"""

    @abstractmethod
    def clear(self):
        """Clears the queue"""


class BasicQueue(TraversalQueue, Generic[T]):

    def __init__(self, queue: Union[FIFODeque, LIFODeque]):
        self.queue = queue

    def __iter__(self):
        return self.queue.__iter__()

    def __len__(self):
        return len(self.queue)

    def has_next(self) -> bool:
        return len(self.queue) > 0

    def pop(self):
        return self.queue.pop()

    def append(self, item: T) -> bool:
        self.queue.append(item)
        return True

    def extend(self, items: Iterable[T]) -> None:
        self.queue.extend(items)

    def peek(self) -> T:
        return self.queue.peek()

    def clear(self):
        self.queue.clear()
