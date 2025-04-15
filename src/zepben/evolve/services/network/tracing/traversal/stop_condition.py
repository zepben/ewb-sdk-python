#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import TypeVar, Generic

from zepben.evolve.services.network.tracing.traversal.context_value_computer import TypedContextValueComputer
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext
from zepben.evolve.services.network.tracing.traversal.traversal_condition import TraversalCondition


T = TypeVar('T')
U = TypeVar('U')


class StopCondition(TraversalCondition[T], Generic[T]):
    """
    Functional interface representing a condition that determines whether the traversal should stop at a given item.

    `T` The type of items being traversed.
    """
    def should_stop(self, item: T, context: StepContext) -> bool:
        """
        Determines whether the traversal should stop at the specified item.

        `item` The current item being processed in the traversal.
        `context` The context associated with the current traversal step.
        Returns `true` if the traversal should stop at this item; `false` otherwise.
        """
        return self._func(item, context)

class StopConditionWithContextValue(StopCondition[T], TypedContextValueComputer[T, U], Generic[T, U]):
    """
    Interface representing a stop condition that requires a value stored in the [StepContext] to determine if an item should be queued.

    `T` The type of items being traversed.
    `U` The type of the context value computed and used in the condition.
    """
    pass
