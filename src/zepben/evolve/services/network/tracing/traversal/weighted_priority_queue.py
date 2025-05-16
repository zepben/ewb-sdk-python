#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections import defaultdict
from typing import TypeVar, Callable, Iterable, Any

from zepben.evolve.services.network.tracing.traversal.queue import TraversalQueue


T = TypeVar('T')
U = TypeVar('U')

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
    def __init__(self, queue_provider: Callable[[], TraversalQueue[T]], get_weight: Callable[[Any], int]):
        self._queue_provider = queue_provider
        self._get_weight = get_weight
        super().__init__(queue=SortedDefaultDict(self._queue_provider))

    def __len__(self) -> int:
        """need to aggregate the lengths of all queues"""
        return sum(len(v) for v in self.queue.values())

    def __iter__(self):
        return self

    def __next__(self):
        yield self.pop()

    def pop(self):
        for weight in self.queue.keys():
            if self.queue[weight].has_next():
                return self.queue[weight].pop()

    def put(self, item: T) -> bool:
        weight = self._get_weight(item)
        if weight < 0:
            raise Exception
        self.queue[weight].put(item)
        return True

    def extend(self, items: Iterable[T]) -> bool:
        raise NotImplementedError()

    @classmethod
    def process_queue(cls, get_weight: Callable[[T], int]) -> TraversalQueue:
        """Special priority queue that queues items with the largest weight as the highest priority."""
        return cls(TraversalQueue.depth_first, get_weight)

    @classmethod
    def branch_queue(cls, get_weight: Callable[[T], int]) -> TraversalQueue:
        """Special priority queue that queues branch items with the largest weight on the starting item as the highest priority"""
        def condition(traversal):
            items = traversal.start_items
            if len(items) == 0:
                return None
            return get_weight(items) or -1

        return cls(TraversalQueue.breadth_first, condition)
