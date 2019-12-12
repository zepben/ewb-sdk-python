from zepben.model.tracing.queue import Queue
from zepben.model.tracing.tracing import BaseTraversal, SearchType, create_queue
from zepben.model.tracing.tracker import Tracker
from typing import Callable, Set, List, Awaitable, TypeVar
import copy

T = TypeVar('T')


class BranchRecursiveTraversal(BaseTraversal[T]):
    def __init__(self,
                 queue_next: Callable[[T, BaseTraversal[T], Set[T]], List[T]],
                 branch_queue: Queue,
                 start_item: T = None,
                 search_type: SearchType = SearchType.DEPTH,
                 tracker: Tracker = Tracker(),
                 parent: BaseTraversal = None,
                 on_branch_start: Callable[[T], None] = None,
                 stop_conditions: List[Callable[[T], Awaitable[bool]]] = None,
                 step_actions: List[Callable[[T, bool], Awaitable[None]]] = None):
        """

        :param queue_next:
        :param start_item: The starting point for this trace.
        :param branch_queue:
        :param search_type:
        :param tracker:
        :param parent: A parent :class:`zepben.model.tracing.Traversal` of this traversal.
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

    def traverse_branches(self):
        """
        Start a new traversal for the next branch in the queue.
        on_branch_start will be called on the start_item for the branch.
        """
        while not self.branch_queue.empty():
            t = self.branch_queue.get()
            if t is not None:
                if self.on_branch_start is not None:
                    self.on_branch_start(t.start_item)
                t.trace()

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
        self.tracker.visit(self.start_item)
        # If we can't stop on the start item we don't run any stop conditions. if this causes a problem for you,
        # work around it by running the stop conditions for the start item prior to running the trace.
        stopping = can_stop_on_start_item and await self.matches_stop_condition(self.start_item)
        await self.apply_step_actions(self.start_item, stopping)
        if not stopping:
            for x in self.queue_next(self.start_item, self, self.tracker.visited):
                self.process_queue.put(x)

        while not self.process_queue.empty():
            current = self.process_queue.get()
            if self.visit(current):
                # this won't call matches_stop_condition if can_stop == False :/
                stopping = await self.matches_stop_condition(current)
                await self.apply_step_actions(current, stopping)
                if not stopping:
                    for x in self.queue_next(current, self.tracker.visited):
                        self.process_queue.put(x)

        self.traverse_branches()
