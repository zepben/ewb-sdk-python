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

from zepben.cimbend.tracing.queue import Queue
from zepben.cimbend.tracing.tracing import BaseTraversal, SearchType, create_queue
from zepben.cimbend.tracing.tracker import Tracker
from typing import Callable, Set, List, Awaitable, TypeVar
import copy

__all__ = ["BranchRecursiveTraversal"]
T = TypeVar('T')


class BranchRecursiveTraversal(BaseTraversal[T]):
    def __init__(self,
                 queue_next: Callable[[T, BaseTraversal[T], Set[T]], None],
                 branch_queue: Queue,
                 start_item: T = None,
                 search_type: SearchType = SearchType.DEPTH,
                 tracker: Tracker = Tracker(),
                 parent: BaseTraversal = None,
                 on_branch_start: Callable[[T], None] = None,
                 stop_conditions: List[Callable[[T], Awaitable[bool]]] = None,
                 step_actions: List[Callable[[T, bool], Awaitable[None]]] = None):
        """

        :param queue_next: A callable for each item encountered during the trace, that should queue the next items
                           found on the given traversal's `process_queue`. The first argument will be the current item,
                           the second this traversal, and the third a set of already visited items that can be used as
                           an optimisation when queuing.
        :param start_item: The starting point for this trace.
        :param branch_queue:
        :param search_type:
        :param tracker:
        :param parent: A parent :class:`zepben.cimbend.tracing.Traversal` of this traversal.
        :param on_branch_start:
        :param stop_conditions:
        :param step_actions:
        """
        super().__init__(start_item=start_item, stop_conditions=stop_conditions, step_actions=step_actions)
        self.queue_next = queue_next
        self.parent = parent
        self.branch_queue = branch_queue
        self.on_branch_start = on_branch_start
        self.tracker = tracker
        self.process_queue = create_queue(search_type)

    def __lt__(self, other):
        """
        This Traversal is Less than `other` if the starting item is less than other's starting item.
        This is used to dictate which branch is next to traverse in the branch_queue.
        :param other:
        :return:
        """
        if self.start_item is not None and other.start_item is not None:
            return self.start_item < other.start_item
        elif self.start_item is None and other.start_item is None:
            return False
        elif other.start_item is None:
            return True
        else:
            return False

    def has_visited(self, item: T):
        """
        Check whether item has been visited before. An item is visited if this traversal or any parent has
        visited it.
        :param item: The item to check
        :return: True if the item has been visited once.
        """
        parent = self.parent
        while parent is not None:
            if parent.tracker.has_visited(item):
                return True
            parent = parent.parent

        return self.tracker.has_visited(item)

    def visit(self, item: T):
        """
        Visit an item.
        :param item: Item to visit
        :return: True if we visit the item. False if this traversal or any parent has previously visited this item.
        """
        parent = self.parent
        while parent is not None:
            if parent.tracker.has_visited(item):
                return False
            parent = parent.parent
        return self.tracker.visit(item)

    async def traverse_branches(self):
        """
        Start a new traversal for the next branch in the queue.
        on_branch_start will be called on the start_item for the branch.
        """
        while not self.branch_queue.empty():
            t = self.branch_queue.get()
            if t is not None:
                if self.on_branch_start is not None:
                    self.on_branch_start(t.start_item)
                await t.trace()

    def reset(self):
        self._reset_run_flags()
        self.process_queue.queue.clear()
        self.branch_queue.queue.clear()
        self.tracker.clear()

    def create_branch(self):
        """
        Create a branch for this `Traversal`. Will take copies of queues, actions, conditions, and tracker, and
        pass this `Traversal` as the parent. The new Traversal will be :meth:`reset` prior to being returned.
        :return: A new :class:`BranchRecursiveTraversal` the same as this, but with this Traversal as its parent
        """
        branch = BranchRecursiveTraversal(self.queue_next,
                                          branch_queue=copy.deepcopy(self.branch_queue),
                                          tracker=copy.deepcopy(self.tracker),
                                          parent=self,
                                          on_branch_start=self.on_branch_start,
                                          step_actions=copy.deepcopy(self.step_actions),
                                          stop_conditions=copy.deepcopy(self.stop_conditions))
        branch.process_queue = copy.deepcopy(self.process_queue)
        branch.reset()
        return branch

    async def _run_trace(self, can_stop_on_start_item: bool = True):
        """
        Run's the trace. Stop conditions and step_actions are called with await, so you can utilise asyncio when
        performing a trace if your step actions or conditions are IO intensive. Stop conditions and
        step actions will always be called for each item in the order provided.
        :param can_stop_on_start_item: Whether the trace can stop on the start_item. Actions will still be applied to
                                       the start_item.
        """
        # Unroll first iteration of loop to handle can_stop_on_start_item = True
        if self.start_item is None:
            try:
                self.start_item = self.process_queue.get()
            except IndexError:
                # Our start point may very well be a branch - if so we don't need to process this branch.
                await self.traverse_branches()
                return

        self.tracker.visit(self.start_item)
        # If we can't stop on the start item we don't run any stop conditions. if this causes a problem for you,
        # work around it by running the stop conditions for the start item prior to running the trace.
        stopping = can_stop_on_start_item and await self.matches_stop_condition(self.start_item)
        await self.apply_step_actions(self.start_item, stopping)
        if not stopping:
            self.queue_next(self.start_item, self, self.tracker.visited)

        while not self.process_queue.empty():
            current = self.process_queue.get()
            if self.visit(current):
                stopping = await self.matches_stop_condition(current)
                await self.apply_step_actions(current, stopping)
                if not stopping:
                    self.queue_next(current, self, self.tracker.visited)

        await self.traverse_branches()
