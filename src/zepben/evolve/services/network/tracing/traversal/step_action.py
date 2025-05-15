#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.


from typing import TypeVar, Generic

from zepben.evolve.services.network.tracing.traversal.context_value_computer import TypedContextValueComputer
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext

T = TypeVar('T')
U = TypeVar('U')


class StepAction(Generic[T]):
    """
    Functional interface representing an action to be performed at each step of a traversal.
    This allows for custom operations to be executed on each item during traversal.

    `T` The type of items being traversed.
    """
    def __init__(self, _func):
        self._func = _func

    def apply(self, item: T, context: StepContext):
        """
        Applies the action to the specified [item].

        `item` The current item in the traversal.
        `context` The context associated with the current traversal step.
        """
        return self._func(item, context)

class StepActionWithContextValue(StepAction[T], TypedContextValueComputer[T, U]):
    """
    Interface representing a step action that utilises a value stored in the [StepContext].

    `T` The type of items being traversed.
    `U` The type of the context value computed and used in the action.
    """
    pass
