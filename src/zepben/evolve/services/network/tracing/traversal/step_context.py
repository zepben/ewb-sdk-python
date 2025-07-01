#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import TypeVar, Generic

T = TypeVar('T')

__all__ = ['StepContext']


class StepContext(Generic[T]):
    """
    Represents the context of a traversal step, holding information about the traversal state and the ability to store arbitrary values with the context.
    This context is passed to conditions and actions during a traversal to provide additional information about each step.
    
    Any `ContextValueComputer` registered with the traversal will put the computed value into this context with the given `ContextValueComputer.key` which can
    be retrieved by using `get_value`.

    :var is_start_item: Indicates whether the current item is a starting item of the traversal.
    :var is_branch_start_item: Indicates whether the current item is the start of a new branch in a branching traversal.
    :var step_number: The number of steps taken in the traversal so far for this traversal path.
    :var branch_depth: The depth of the current branch in a branching traversal.
    :var is_stopping: Indicates whether the traversal is stopping at the current item due to a stop condition.
    """

    def __init__(self, is_start_item: bool, is_branch_start_item: bool, step_number: int = 0, branch_depth: int = 0, values: dict = None):
        self.is_start_item = is_start_item
        self.is_branch_start_item = is_branch_start_item
        self.step_number = step_number
        self.branch_depth = branch_depth
        self._values = values or dict()

        self.is_stopping: bool = False
        self.is_actionable_item: bool = False

    def set_value(self, key: str, value):
        """
        Sets a context value associated with the specified key.

        `key` The key identifying the context value.
        `value` The value to associate with the key.
        """

        self._values[key] = value

    def get_value(self, key: str) -> T:
        """
        Retrieves a context value associated with the specified key.

        `key` The key identifying the context value.
        @return The context value associated with the key, or `None` if not found.
        """

        return self._values.get(key)

    def __str__(self) -> str:
        return f"StepContext({', '.join('{}={}'.format(*i) for i in vars(self).items())})"
