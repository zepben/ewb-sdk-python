#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import abstractmethod
from typing import TypeVar, Generic, Callable

from zepben.evolve.services.network.tracing.traversal.context_value_computer import ContextValueComputer
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext

T = TypeVar('T')
U = TypeVar('U')

__all__ = ['StepAction', 'StepActionWithContextValue', 'StepActionFunc']

StepActionFunc = Callable[[T, StepContext], None]


class StepAction(Generic[T]):
    """
    Functional interface representing an action to be performed at each step of a traversal.
    This allows for custom operations to be executed on each item during traversal.

    `T` The type of items being traversed.
    """
    def __init__(self, _func: StepActionFunc):
        self._func = _func

    def apply(self, item: T, context: StepContext):
        """
        Applies the action to the specified [item].

        :param item: The current item in the traversal.
        :param context: The context associated with the current traversal step.
        """
        return self._func(item, context)

class StepActionWithContextValue(StepAction[T], ContextValueComputer[T]):
    """
    Interface representing a step action that utilises a value stored in the [StepContext].

    `T` The type of items being traversed.
    `U` The type of the context value computed and used in the action.
    """
    def __init__(self, _func: StepActionFunc, key: str):
        StepAction.__init__(self, _func)
        ContextValueComputer.__init__(self, key)

    @abstractmethod
    def compute_initial_value(self, item: T):
        raise NotImplemented

    @abstractmethod
    def compute_next_value(self, next_item: T, current_item: T, current_value):
        raise NotImplemented
