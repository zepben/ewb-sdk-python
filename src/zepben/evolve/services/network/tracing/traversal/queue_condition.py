#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import TypeVar, Generic

from zepben.evolve.services.network.tracing.traversal.step_context import StepContext
from zepben.evolve.services.network.tracing.traversal.traversal_condition import TraversalCondition

T = TypeVar('T')
U = TypeVar('U')


class QueueCondition(TraversalCondition[T], Generic[T]):
    """
    Functional interface representing a condition that determines whether a traversal should queue a next item.

    `T` The type of items being traversed.
    """

    def should_queue(self, next_item: T, next_context: StepContext, current_item: T, current_context: StepContext) -> bool:
        """
        Determines whether the [nextItem] should be queued for traversal.

        `nextItem` The next item to be potentially queued.
        `nextContext` The context associated with the [nextItem].
        `currentItem` The current item being processed in the traversal.
        `currentContext` The context associated with the [currentItem].
        Returns `true` if the [nextItem] should be queued; `false` otherwise.
        """
        return self._func(next_item, next_context, current_item, current_context)

    def should_queue_start_item(self, item: T) -> bool:
        """
        Determines whether a traversal startItem should be queued when running a [Traversal].

        `item` The item to be potentially queued.
        Returns `true` if the [item] should be queued; `false` otherwise. Defaults to `true`.
        """
        try:  # this is a filthy hack to avoid this being called on a queue condition function that doesnt match this signature
              # TODO: this absolute hack of a method to use this as a functional interface needs to go..
            return self._func(item)
        except TypeError as e:
            if self._func.__code__.co_argcount == 4:
                return True
            raise e


from zepben.evolve.services.network.tracing.traversal.context_value_computer import TypedContextValueComputer

class QueueConditionWithContextValue(QueueCondition[T], TypedContextValueComputer[T, U], Generic[T, U]):
    """
    Interface representing a queue condition that requires a value stored in the [StepContext] to determine if an item should be queued.

    `T` The type of items being traversed.
    `U` The type of the context value computed and used in the condition.
    """
    pass
