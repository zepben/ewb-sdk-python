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


class QueueCondition(Generic[T], TraversalCondition[T]):
    """
    Functional interface representing a condition that determines whether a traversal should queue a next item.

    `T` The type of items being traversed.
    """

    def __init__(self, condition):
        self.should_queue = condition

    def should_queue(self, next_item: T, next_context: StepContext, current_item: T, current_context: StepContext) -> bool:
        """
        Determines whether the `next_item` should be queued for traversal.

        `next_item` The next item to be potentially queued.
        `next_context` The context associated with the `next_iItem`.
        `current_item` The current item being processed in the traversal.
        `current_context` The context associated with the `current_item`.
        Returns `True` if the `next_tem` should be queued; `False` otherwise.
        """

        raise NotImplemented

    @staticmethod
    def should_queue_start_item(item: T) -> bool:
        """
        Determines whether a traversal start_item should be queued when running a `Traversal`.

        :param item: The item to be potentially queued.
        :eturn: `True` if the `item` should be queued; `False` otherwise. Defaults to `True`.
        """

        return True


from zepben.evolve.services.network.tracing.traversal.context_value_computer import ContextValueComputer


class QueueConditionWithContextValue(QueueCondition[T], ContextValueComputer[T], Generic[T, U]):
    """
    Interface representing a queue condition that requires a value stored in the `StepContext` to determine if an item should be queued.

    `T` The type of items being traversed.
    `U` The type of the context value computed and used in the condition.
    """

    @abstractmethod
    def compute_initial_value(self, item: T):
        raise NotImplemented

    @abstractmethod
    def compute_next_value(self, next_item: T, current_item: T, current_value):
        raise NotImplemented
