#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import abstractmethod
from typing import TypeVar, Generic, Callable, final

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

    def __init__(self, _func: StepActionFunc = None):
        self._func = _func or self._apply

    def __init_subclass__(cls):
        """
        Due to ``apply`` needing to call ``self._func`` to allow the method wrapping used in
        ``Traversal.if_stopping()`` and ``Traversal.if_not_stopping()`` we **DO NOT** allow this
        method to be overridden directly.

        :raises Exception: If ``cls.apply`` is overridden
        """
        if 'apply' in cls.__dict__.keys():
            raise Exception(f"method 'apply' should not be directly overridden, override '_apply' instead.")
        super().__init_subclass__()

    @final
    def apply(self, item: T, context: StepContext):
        """
        Applies the action to the specified ``item``.

        :param item: The current item in the traversal.
        :param context: The context associated with the current traversal step.
        """

        return self._func(item, context)

    @abstractmethod
    def _apply(self, item: T, context: StepContext):
        """
        Override this method instead of ``self.apply`` directly

        :param item: The current item in the traversal.
        :param context: The context associated with the current traversal step.
        """
        raise NotImplementedError()


class StepActionWithContextValue(StepAction[T], ContextValueComputer[T]):
    """
    Interface representing a step action that utilises a value stored in the :class:`StepContext`.

    `T` The type of items being traversed.
    `U` The type of the context value computed and used in the action.
    """

    def __init__(self, key: str, _func: StepActionFunc = None):
        StepAction.__init__(self, _func)
        ContextValueComputer.__init__(self, key)

    @abstractmethod
    def compute_initial_value(self, item: T):
        raise NotImplementedError()

    @abstractmethod
    def compute_next_value(self, next_item: T, current_item: T, current_value):
        raise NotImplementedError()
