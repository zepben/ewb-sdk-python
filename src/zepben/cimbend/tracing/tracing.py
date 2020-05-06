"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""


from abc import ABC, abstractmethod
from zepben.cimbend.tracing.queue import FifoQueue, LifoQueue, PriorityQueue
from zepben.cimbend.tracing.exceptions import TracingException
from zepben.cimbend.tracing.tracker import Tracker
from typing import List, Callable, Awaitable, TypeVar, Generic, Set, Iterable
from enum import Enum

__all__ = ["SearchType", "create_queue", "BaseTraversal", "Traversal"]
T = TypeVar('T')


class SearchType(Enum):
    BREADTH = 1
    DEPTH = 2
    PRIORITY = 3


def create_queue(search_type):
    if search_type == SearchType.DEPTH:
        return LifoQueue()
    elif search_type == SearchType.BREADTH:
        return FifoQueue()
    elif search_type == SearchType.PRIORITY:
        return PriorityQueue()


class BaseTraversal(Generic[T], ABC):
    """
    This class is asyncio compatible. Stop condition and step action callbacks are called with await.

    A stop condition is a callback function that must return a boolean indicating whether the Tracer should stop
    processing the current branch. Tracing will only stop when either:
        - All branches have been exhausted, or
        - A stop condition has returned true on every possible branch.
    Stop conditions will be called prior to applying any callbacks, but the stop will only occur after all actions
    have been applied.

    Step actions are functions to be called on each item visited in the trace. These are called after the stop
    conditions are evaluated, and each action is passed the current :class:`zepben.cimbend.tracing.ConnectivityResult` as well as
    the `stopping` state (True if the trace is stopping after the current `ConnectivityResult, False otherwise).
    Thus, the signature of each step action must be:
    :func: action(cr: :class:`zepben.cimbend.tracing.ConnectivityResult`, is_stopping: bool) -> None
    """
    def __init__(self,
                 start_item: T,
                 stop_conditions: List[Callable[[T], Awaitable[bool]]] = None,
                 step_actions: List[Callable[[T, bool], Awaitable[None]]] = None):
        """

        :param start_item: The starting point for this trace.
        :param stop_conditions: A list of callback functions, to be called in order with the current item.
        :param step_actions: A list of callback functions, to be called on each item.
        """
        self.stop_conditions = stop_conditions if stop_conditions is not None else []
        self.step_actions = step_actions if step_actions else []
        self._start_item = start_item
        self._has_run = False
        self._running = False

    @property
    def start_item(self):
        return self._start_item

    @start_item.setter
    def start_item(self, item):
        self._start_item = item

    async def matches_stop_condition(self, item: T):
        """
        Checks all the stop conditions for the passed in item and returns true if any match.
        This calls all registered stop conditions even if one has already returned true to make sure everything is
        notified about this item.
        Each stop condition will be awaited and thus must be an async function.

        :param item: The item to pass to the stop conditions.
        :return: True if any of the stop conditions return True.
        """
        stop = False
        for cond in self.stop_conditions:
            stop = stop or await cond(item)
        return stop

    def add_stop_condition(self, cond: Callable[[T], Awaitable[bool]]):
        self.stop_conditions.append(cond)

    def add_step_action(self, action: Callable[[T, bool], Awaitable[None]]):
        self.step_actions.append(action)

    def clear_stop_conditions(self):
        self.stop_conditions.clear()

    def remove_stop_condition(self, stop_cnd):
        """
        Remove a previously added stop condition. Will remove the first instance of stop_cnd.
        :param stop_cnd: The stop condition callback
        :raises: ValueError if stop condition wasn't present
        """
        self.stop_conditions.remove(stop_cnd)

    async def apply_step_actions(self, item: T, is_stopping: bool):
        """
        Calls all the step actions with the passed in item.
        Each action will be awaited.
        :param item: The item to pass to the step actions.
        :param is_stopping: Indicates if the trace will stop on this step.
        """
        for action in self.step_actions:
            await action(item, is_stopping)

    def _reset_run_flags(self):
        if self._running:
            raise TracingException("Can't reset when Traversal is currently executing.")
        self._has_run = False

    @abstractmethod
    def reset(self):
        """
        Reset this traversal. Should take care to reset all fields and queues so that the traversal can be reused.
        """
        raise NotImplementedError()

    async def trace(self, start_item: T = None, can_stop_on_start_item: bool = True):
        """
        Perform a trace across the network from `start_item`, applying actions to each piece of equipment encountered
        until all branches of the network are exhausted, or a stop condition succeeds and we cannot continue any further.
        When a stop condition is reached, we will stop tracing that branch of the network and continue with other branches.
        :param start_item: The starting point. Must implement :func:`zepben.cimbend.ConductingEquipment::get_connectivity`
                           which allows tracing over the terminals in a network.
        :param can_stop_on_start_item: If it's possible for stop conditions to apply to the start_item.
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
        :param start_item: The starting object to commence tracing. Must implement :func:`zepben.cimbend.ConductingEquipment.get_connectivity`
        :param can_stop_on_start_item: Whether to
        """
        raise NotImplementedError()


class Traversal(BaseTraversal):
    """
    A basic traversal implementation that can be used to traverse any type of item.

    The traversal gets the next items to be traversed to by calling a user provided callback (next_), with the current
    item of the traversal. This function should return a list of ConnectivityResult's, that will get added to the
    process_queue for processing.

    Different :class:`SearchType`'s types can be used to provide different trace types via the `process_queue`.
    The default `Depth` will utilise a `LifoQueue` to provide a depth-first search of the network, while a `Breadth`
    will use a FIFO `Queue` breadth-first search. More complex searches can be achieved with `Priority`, which
    will use a PriorityQueue under the hood.

    The traversal also requires a :class:`zepben.cimbend.tracing.tracker.Tracker` to be supplied. This gives flexibility
    to track items in unique ways, more than just "has this item been visited" e.g. visiting more than once,
    visiting under different conditions etc.
    """
    def __init__(self,
                 queue_next: Callable[[T, Set[T]], Iterable[T]],
                 start_item: T = None,
                 search_type: SearchType = SearchType.DEPTH,
                 tracker: Tracker = None,
                 stop_conditions: List[Callable[[T], Awaitable[bool]]] = None,
                 step_actions: List[Callable[[T, bool], Awaitable[None]]] = None):
        """
        :param queue_next: A function that will return a list of `T` to add to the queue. The function must take the
                           item to queue and optionally a set of already visited items.
        :param start_item: The starting point for this trace.
        :param search_type: Dictates the type of search to be performed on the network graph. Breadth-first, Depth-first,
                            and Priority based searches are possible.
        :param tracker: A :class:`zepben.cimbend.tracing.Tracker` for tracking which items have been seen. If not provided
                        a `Tracker` will be created for this trace.
        :param stop_conditions: A list of callback functions, to be called in order with the current item.
        :param step_actions: A list of callback functions, to be called on each item.
        """
        super().__init__(start_item=start_item, stop_conditions=stop_conditions, step_actions=step_actions)
        self.queue_next = queue_next
        self.tracker = tracker if tracker is not None else Tracker()
        self.process_queue = create_queue(search_type)

    async def _run_trace(self, can_stop_on_start_item: bool = True):
        """
        Run's the trace. Stop conditions and step_actions are called with await, so you can utilise asyncio when
        performing a trace if your step actions or conditions are IO intensive. Stop conditions and
        step actions will always be called for each item in the order provided.
        :param can_stop_on_start_item: Whether the trace can stop on the start_item. Actions will still be applied to
                                       the start_item.
        """
        if self.start_item is None:
            try:
                self.start_item = self.process_queue.get()
            except IndexError:
                raise TracingException("Starting item wasn't specified and the process queue is empty. Cannot start the trace.")

        self.tracker.visit(self.start_item)
        # If we can't stop on the start item we don't run any stop conditions. if this causes a problem for you,
        # work around it by running the stop conditions for the start item prior to running the trace.
        stopping = can_stop_on_start_item and await self.matches_stop_condition(self.start_item)
        await self.apply_step_actions(self.start_item, stopping)
        if not stopping:
            for x in self.queue_next(self.start_item, self.tracker.visited):
                self.process_queue.put(x)

        while not self.process_queue.empty():
            current = self.process_queue.get()
            if self.tracker.visit(current):
                # this won't call matches_stop_condition if can_stop == False :/
                stopping = await self.matches_stop_condition(current)
                await self.apply_step_actions(current, stopping)
                if not stopping:
                    for x in self.queue_next(current, self.tracker.visited):
                        self.process_queue.put(x)

    def reset(self):
        self._reset_run_flags()
        self.process_queue.queue.clear()
        self.tracker.clear()


def _depth_trace(start_item, stop_on_start_item=True, stop_fn=None, equip_fn=None, term_fn=None):
    equips_to_trace = []
    traced = set()
    for t in start_item.terminals:
        traced.add(t.mrid)
    if stop_on_start_item:
        yield start_item
    equips_to_trace.append(start_item)
    while equips_to_trace:
        try:
            equip = equips_to_trace.pop()
        except IndexError:  # No more equipment
            break
        # Explore all connectivity nodes for this equipments terminals,
        # and set upstream on each terminal.
        for terminal in equip.terminals:
            conn_node = terminal.connectivity_node
            for term in conn_node:
                # keep this
                if term.mrid in traced:
                    continue
                if term != terminal:
                    if not term.conducting_equipment.connected():
                        continue
                    equips_to_trace.append(term.conducting_equipment)
                    yield term.conducting_equipment
                # Don't trace over a terminal twice to stop us from reversing direction
                traced.add(term.mrid)
