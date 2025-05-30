#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections import defaultdict
from typing import TypeVar, Callable, Iterable

from zepben.evolve.services.network.tracing.traversal.traversal import Traversal
from zepben.evolve.services.network.tracing.traversal.queue import TraversalQueue

T = TypeVar('T')
U = TypeVar('U')

__all__ = ['WeightedPriorityQueue']


class SortedDefaultDict(defaultdict):
    def keys(self):
        return sorted(super().keys())

    def items(self):
        return sorted(super().items())


class WeightedPriorityQueue(TraversalQueue[T]):
    """
    A traversal queue which uses a weighted order. The higher the weight, the higher the priority.

    :param queue_provider: A queue provider. This allows you to customise the priority of items with the same weight.
    :param get_weight:     A method to extract the weight of an item being added to the queue.
    """

    def __init__(self, queue_provider: Callable[[], TraversalQueue[T]], get_weight: Callable[[T], int]):
        self._queue_provider = queue_provider
        self._get_weight = get_weight

        self.queue: SortedDefaultDict[int, TraversalQueue[T]] = SortedDefaultDict(self._queue_provider)

    def __len__(self) -> int:
        """need to aggregate the lengths of all queues"""
        return sum(len(v) for v in self.queue.values())

    def pop(self):
        for weight in reversed(self.queue.keys()):
            if self.queue[weight].has_next():
                return self.queue[weight].pop()

    def append(self, item: T) -> bool:
        weight = self._get_weight(item)
        self.queue[weight].append(item)
        return True

    def extend(self, items: Iterable[T]) -> bool:
        raise NotImplementedError()

    @classmethod
    def process_queue(cls, get_weight: Callable[[T], int]) -> TraversalQueue[T]:
        """Special priority queue that queues items with the largest weight as the highest priority."""
        return cls(TraversalQueue.depth_first, get_weight)

    @classmethod
    def branch_queue(cls, get_weight: Callable[[T], int]) -> TraversalQueue[T]:
        """Special priority queue that queues branch items with the largest weight on the starting item as the highest priority"""
        def condition(traversal: Traversal):
            items = traversal.start_items
            if len(items) == 0:
                return -1
            return get_weight(items[0]) or -1

        return cls(TraversalQueue.breadth_first, condition)

    def has_next(self) -> bool:
        for weight in self.queue.keys():
            _next = self.queue.get(weight)
            if _next:
                return True
        return False


    def peek(self) -> T:
        raise Exception

    def clear(self):
        self.queue.clear()
