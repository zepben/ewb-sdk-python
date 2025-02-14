#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from abc import ABC
from typing import TypeVar

T = TypeVar('T')
U = TypeVar('U')


class ContextValueComputer[T](ABC):
    """
    Interface representing a context value computer used to compute and store values in a [StepContext].
    This interface does not specify a generic return type because the [StepContext] stores its values as `Any?`.
    Implementations compute initial and subsequent context values during traversal steps.

    `T` The type of items being traversed.
    """
    def __init__(self, key: str):
        self.key = key  # A unique key identifying the context value computed by this computer.

    def compute_initial_value(self, item: T):
        """
        Computes the initial context value for the given starting item.

        `item` The starting item for which to compute the initial context value.
        Returns The initial context value associated with the starting item.
        """
        pass

    def compute_next_value(self, next_item: T, current_item: T, current_value):
        """
        Computes the next context value based on the current item, next item, and the current context value.

        `nextItem` The next item in the traversal.
        `currentItem` The current item of the traversal.
        `currentValue` The current context value associated with the current item.
        Returns The updated context value for the next item.
        """
        pass

class TypedContextValueComputer[T, U](ContextValueComputer):
    """
    A typed version of [ContextValueComputer] that avoids unchecked casts by specifying the type of context value.
    This interface allows for type-safe computation of context values in implementations.

    `T` The type of items being traversed.
    `U` The type of the context value computed and stored.
    """
    def compute_initial_value(self, item: T):
        """
        Computes the initial context value of type [U] for the given starting item.

        `item` The starting item for which to compute the initial context value.
        Returns The initial context value associated with the starting item.
        """
        pass

    def compute_next_value(self, next_item: T, current_item: T, current_value) -> U:
        return self.compute_next_value_typed(next_item, current_item, current_value)

    def compute_next_value_typed(self, next_item: T, current_item: T, current_value) -> U:
        """
        Computes the next context value of type [U] based on the current item, next item, and the current context value.

        `nextItem` The next item in the traversal.
        `currentItem` The current item being processed.
        `currentValue` The current context value associated with the current item cast to type [U].
        Returns The updated context value of type for the next item.
        """
        pass
    
    # TODO: implement
    """
    Gets the computed value from the context cast to type [U].
    """
    #  val StepContext.value: U get() = this.getValue<Any?>(key) as U