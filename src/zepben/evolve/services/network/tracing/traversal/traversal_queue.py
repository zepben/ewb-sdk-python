#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations
from abc import abstractmethod, ABC
from collections import deque
from typing import TypeVar, Iterable, Generic
from queue import LifoQueue

T = TypeVar('T')

__all__ = ['TraversalQueue']


class TraversalQueue(Generic[T], ABC):
    def __init__(self, queue=None):
        if queue is None:
            self.queue = deque()
        else:
            self.queue = queue

    @classmethod
    def depth_first(cls):
        return cls(deque())

    @classmethod
    def breadth_first(cls):
        return cls(LifoQueue())

    @abstractmethod
    def has_next(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get(self) -> T:
        raise NotImplementedError()

    @abstractmethod
    def put(self, item: T) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def extend(self, items: Iterable[T]) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def peek(self) -> T:
        raise NotImplementedError()

    @abstractmethod
    def clear(self):
        raise NotImplementedError()
