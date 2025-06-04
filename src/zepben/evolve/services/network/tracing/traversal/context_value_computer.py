#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from abc import abstractmethod
from typing import TypeVar, Generic

from zepben.evolve.services.network.tracing.traversal.step_context import StepContext

T = TypeVar('T')
U = TypeVar('U')

__all__ = ['ContextValueComputer']


class ContextValueComputer(Generic[T]):
    """
    Interface representing a context value computer used to compute and store values in a `StepContext`.
    Implementations compute initial and subsequent context values during traversal steps.

    `T` The type of items being traversed.
    """

    def __init__(self, key: str):
        self.key = key  # A unique key identifying the context value computed by this computer.

    @abstractmethod
    def compute_initial_value(self, item: T):
        """
        Computes the initial context value for the given starting item.

        :param item: The starting item for which to compute the initial context value.
        :return: The initial context value associated with the starting item.
        """
        raise NotImplemented

    @abstractmethod
    def compute_next_value(self, next_item: T, current_item: T, current_value):
        """
        Computes the next context value based on the current item, next item, and the current context value.

        :param next_item: The next item in the traversal.
        :param current_item: The current item of the traversal.
        :param current_value: The current context value associated with the current item.
        :return: The updated context value for the next item.
        """
        raise NotImplemented

    def get_context_value(self, context: StepContext):
        """
        Gets the computed value from the context cast to type [U].
        """
        return context.get_value(self.key)

    def is_standalone_computer(self):
        return not isinstance(self, (StepAction, StopCondition, QueueCondition))


# these imports are here to stop circular imports
from zepben.evolve.services.network.tracing.traversal.stop_condition import StopCondition
from zepben.evolve.services.network.tracing.traversal.step_action import StepAction
from zepben.evolve.services.network.tracing.traversal.queue_condition import QueueCondition
