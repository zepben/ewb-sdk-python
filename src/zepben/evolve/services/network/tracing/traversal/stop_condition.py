#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import abstractmethod
from typing import TypeVar, Generic, Callable

from zepben.evolve.services.network.tracing.traversal.context_value_computer import ContextValueComputer
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext
from zepben.evolve.services.network.tracing.traversal.traversal_condition import TraversalCondition

T = TypeVar('T')
U = TypeVar('U')

ShouldStop = Callable[[T, StepContext], bool]

__all__ = ['StopCondition', 'StopConditionWithContextValue', 'ShouldStop']


class StopCondition(Generic[T], TraversalCondition[T]):
    """
    Functional interface representing a condition that determines whether the traversal should stop at a given item.

    `T` The type of items being traversed.
    """

    def __init__(self, stop_function: ShouldStop = None):
        if stop_function is not None:
            self.should_stop = stop_function

    def should_stop(self, item: T, context: StepContext) -> bool:
        """
        Determines whether the traversal should stop at the specified item.

        :param item: The current item being processed in the traversal.
        :param context: The context associated with the current traversal step.

        :return: `True` if the traversal should stop at this item; `False` otherwise.
        """


class StopConditionWithContextValue(StopCondition[T], ContextValueComputer[T]):
    """
    Interface representing a stop condition that requires a value stored in the StepContext to determine if an item should be queued.

    `T` The type of items being traversed.
    `U` The type of the context value computed and used in the condition.
    """

    @abstractmethod
    def compute_initial_value(self, item: T):
        raise NotImplemented

    @abstractmethod
    def compute_next_value(self, next_item: T, current_item: T, current_value):
        raise NotImplemented
