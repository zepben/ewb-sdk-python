#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from abc import abstractmethod
from typing import List, Callable, Awaitable, TypeVar, Generic

from dataclassy import dataclass

from zepben.evolve import Tracker, BasicTracker
from zepben.evolve.exceptions import TracingException

__all__ = ["Traversal"]
T = TypeVar('T')


@dataclass(slots=True)
class Traversal(Generic[T]):
    """
    Base class that provides some common functionality for traversals. This includes things like registering callbacks
    to be called at every step in the traversal as well as registering stop conditions that traversals can check for when
    to stop following a path.

    This class is asyncio compatible. Stop condition and step action callbacks are called with await.

    A stop condition is a callback function that must return a boolean indicating whether the Traversal should stop
    processing the current branch. Tracing will only stop when either:
        - All branches have been exhausted, or
        - A stop condition has returned true on every possible branch.
    Stop conditions will be called prior to applying any callbacks, but the stop will only occur after all actions
    have been applied.

    Step actions are functions to be called on each item visited in the trace. These are called after the stop conditions are evaluated, and each action is
    passed the current item, as well as the `stopping` state (True if the trace is stopping after the current item, False otherwise). Thus, the signature of
    each step action must be:
    :func: action(it: T, is_stopping: bool) -> None

    This base class does not actually provide any way to traverse the items. It needs to be implemented in
    subclasses. See `BasicTraversal` for an example.
    """

    start_item: T = None
    """The starting item for this `Traversal`"""

    stop_conditions: List[Callable[[T], Awaitable[bool]]] = []
    """A list of callback functions, to be called in order with the current item."""

    step_actions: List[Callable[[T, bool], Awaitable[None]]] = []
    """A list of callback functions, to be called on each item."""

    tracker: Tracker = BasicTracker()
    """A `zepben.evolve.traversals.tracker.Tracker` for tracking which items have been seen. If not provided a `Tracker` will be created for this trace."""

    _has_run: bool = False
    """Whether this traversal has run """

    _running: bool = False
    """Whether this traversal is currently running"""

    async def matches_any_stop_condition(self, item: T) -> bool:
        """
        Checks all the stop conditions for the passed in item and returns true if any match.
        This calls all registered stop conditions even if one has already returned true to make sure everything is
        notified about this item.
        Each stop condition will be awaited and thus must be an async function.

        `item` The item to pass to the stop conditions.
        Returns True if any of the stop conditions return True.
        """
        stop = False
        for cond in self.stop_conditions:
            # Use non-short-circuiting | to ensure each condition is awaited.
            stop = stop | await cond(item)
        return stop

    def add_stop_condition(self, cond: Callable[[T], Awaitable[bool]]) -> Traversal[T]:
        """
        Add a callback to check whether the current item in the traversal is a stop point.
        If any of the registered stop conditions return true, the traversal will not call the callback to queue more items.
        Note that a match on a stop condition doesn't necessarily stop the traversal, it just stops traversal of the current branch.

        `cond` A function that if returns true will cause the traversal to stop traversing the branch.
        Returns this traversal instance.
        """
        self.stop_conditions.append(cond)
        return self

    def add_step_action(self, action: Callable[[T, bool], Awaitable[None]]) -> Traversal[T]:
        """
        Add a callback which is called for every item in the traversal (including the starting item).

        `action` Action to be called on each item in the traversal, passing if the trace will stop on this step.
        Returns this traversal instance.
        """
        self.step_actions.append(action)
        return self

    def copy_stop_conditions(self, other: Traversal[T]):
        """Copy the stop conditions from `other` to this `Traversal`."""
        self.stop_conditions.extend(other.stop_conditions)

    def copy_step_actions(self, other: Traversal[T]):
        """Copy the step actions from `other` to this `Traversal`."""
        self.step_actions.extend(other.step_actions)

    def clear_stop_conditions(self):
        """Clear all stop conditions."""
        self.stop_conditions.clear()

    def clear_step_actions(self):
        """Clear all step actions"""
        self.step_actions.clear()

    async def apply_step_actions(self, item: T, is_stopping: bool):
        """
        Calls all the step actions with the passed in item.
        Each action will be awaited.
        `item` The item to pass to the step actions.
        `is_stopping` Indicates if the trace will stop on this step.
        """
        for action in self.step_actions:
            await action(item, is_stopping)

    def _reset_run_flag(self):
        if self._running:
            raise TracingException("Can't reset when Traversal is currently executing.")
        self._has_run = False

    @abstractmethod
    def reset(self):
        """
        Reset this traversal. Should take care to reset all fields and queues so that the traversal can be reused.
        """
        raise NotImplementedError()

    async def run(self, start_item: T = None, can_stop_on_start_item: bool = True):
        """
        Perform a trace across the network from `start_item`, applying actions to each piece of equipment encountered
        until all branches of the network are exhausted, or a stop condition succeeds and we cannot continue any further.
        When a stop condition is reached, we will stop tracing that branch of the network and continue with other branches.
        `start_item` The starting point. Must implement :func:`ConductingEquipment::get_connectivity`
                           which allows tracing over the terminals in a network.
        `can_stop_on_start_item` If it's possible for stop conditions to apply to the start_item.
        """
        if self._running:
            raise TracingException("Traversal is already running.")

        if self._has_run:
            raise TracingException("Traversal must be reset before reuse.")

        self._running = True
        self._has_run = True
        self.start_item = start_item if start_item is not None else self.start_item
        await self._run_trace(can_stop_on_start_item)
        self._running = False

    @abstractmethod
    async def _run_trace(self, can_stop_on_start_item: bool = True):
        """
        Extend and implement your tracing algorithm here.
        `start_item` The starting object to commence tracing. Must implement :func:`ConductingEquipment.get_connectivity`
        `can_stop_on_start_item` Whether to
        """
        raise NotImplementedError()
