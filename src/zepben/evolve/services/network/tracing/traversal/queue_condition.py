#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar, Generic, Callable

from zepben.evolve.services.network.tracing.traversal.step_context import StepContext
from zepben.evolve.services.network.tracing.traversal.traversal_condition import TraversalCondition

T = TypeVar('T')
U = TypeVar('U')

ShouldQueue = Callable[[T, StepContext, T, StepContext], bool]
ShouldQueueStartItem = Callable[[T], bool]

__all__ = ['QueueCondition', 'QueueConditionWithContextValue', 'ShouldQueue', 'ShouldQueueStartItem']


@TraversalCondition.register
class QueueCondition(Generic[T]):
    """
    Functional interface representing a condition that determines whether a traversal should queue a next item.

    `T` The type of items being traversed.
    """
    def __init__(self, should_queue: ShouldQueue=None):
        self.should_queue = should_queue

    @staticmethod
    @abstractmethod
    def should_queue(next_item: T, next_context: StepContext, current_item: T, current_context: StepContext) -> bool:
        """
        Determines whether the [nextItem] should be queued for traversal.

        `nextItem` The next item to be potentially queued.
        `nextContext` The context associated with the [nextItem].
        `currentItem` The current item being processed in the traversal.
        `currentContext` The context associated with the [currentItem].
        Returns `true` if the [nextItem] should be queued; `false` otherwise.
        """
        raise NotImplementedError

    @staticmethod
    def should_queue_start_item(item: T) -> bool:
        """
        Determines whether a traversal startItem should be queued when running a [Traversal].

        `item` The item to be potentially queued.
        Returns `true` if the [item] should be queued; `false` otherwise. Defaults to `true`.
        """
        return True


from zepben.evolve.services.network.tracing.traversal.context_value_computer import TypedContextValueComputer

class QueueConditionWithContextValue(QueueCondition[T], TypedContextValueComputer[T, U], Generic[T, U]):
    """
    Interface representing a queue condition that requires a value stored in the [StepContext] to determine if an item should be queued.

    `T` The type of items being traversed.
    `U` The type of the context value computed and used in the condition.
    """
