#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from abc import abstractmethod
from collections import deque
from collections.abc import Callable
from functools import singledispatchmethod
from typing import List, TypeVar, Generic, Optional, Dict, Union

from zepben.evolve import require
from zepben.evolve.services.network.tracing.traversal.context_value_computer import ContextValueComputer
from zepben.evolve.services.network.tracing.traversal.queue_condition import QueueCondition, QueueConditionWithContextValue, ShouldQueue
from zepben.evolve.services.network.tracing.traversal.step_action import StepAction, StepActionWithContextValue, StepActionFunc
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext
from zepben.evolve.services.network.tracing.traversal.stop_condition import StopCondition, StopConditionWithContextValue, ShouldStop

__all__ = ["Traversal"]

from zepben.evolve.services.network.tracing.traversal.queue import TraversalQueue

T = TypeVar('T')
U = TypeVar('U')
D = TypeVar('D', bound='Traversal')

QueueConditionTypes = Union[ShouldQueue, QueueCondition[T]]
StopConditionTypes = Union[ShouldStop, StopCondition[T]]
ConditionTypes = Union[QueueConditionTypes, StopConditionTypes]


class Traversal(Generic[T, D]):
    """
    A base traversal class allowing items in a connected graph to be traced.
    It provides the main interface and implementation for traversal logic.
    This class manages conditions, actions, and context values that guide each traversal step.

    This class supports a concept of 'branching', whereby when a new branch is created a new child traversal instance is created. The child
    inherits its parents conditions, actions and what it has tracked. However, it knows nothing about what its siblings have tracked. This
    allows traversing both ways around loops in the graph.

    This class is abstract to allow for type-specific implementations for branching traversals and custom start item handling.

    This class is **not thread safe**.

    `T` The type of object to be traversed.
    `D` The specific type of traversal, extending [Traversal].
    """

    class QueueType(Generic[T, D]):
        """
        Defines the types of queues used in the traversal.
        """
        queue_next: Traversal.QueueNext[T]

        @property
        def queue(self) -> TraversalQueue[T]:
            raise NotImplementedError

        @property
        def branch_queue(self) -> Optional[TraversalQueue[D]]:
            raise NotImplementedError


    class BasicQueueType(QueueType[T, D], Generic[T, D]):
        """
        Basic queue type that handles non-branching item queuing.

        `queueNext` Logic for queueing the next item in the traversal.
        `queue` The primary queue of items.
        """
        def __init__(self, queue_next: Traversal.QueueNext[T], queue: TraversalQueue[T]):
            self.queue_next = queue_next
            self._queue = queue
            self._branch_queue = None

        @property
        def queue(self) -> TraversalQueue[T]:
            return self._queue

        @property
        def branch_queue(self) -> Optional[TraversalQueue[D]]:
            return self._branch_queue


    class BranchingQueueType(QueueType[T, D], Generic[T, D]):
        """
        Branching queue type, supporting operations that may split into separate branches during traversal.

        `queueNext` Logic for queueing the next item in a branching traversal.
        `queueFactory` Factory function to create the main queue.
        `branchQueueFactory` Factory function to create the branch queue.
        """
        def __init__(self,
                     queue_next: Traversal.BranchingQueueNext[T],
                     queue_factory: Callable[[], TraversalQueue[T]],
                     branch_queue_factory: Callable[[], TraversalQueue[D]]):
            self.queue_next: Traversal.BranchingQueueNext[T] = queue_next
            self.queue_factory = queue_factory
            self.branch_queue_factory = branch_queue_factory

        @property
        def queue(self) -> TraversalQueue[T]:
            return self.queue_factory()

        @property
        def branch_queue(self) -> Optional[TraversalQueue[D]]:
            return self.branch_queue_factory()

    _queue_type: Union[BasicQueueType, BranchingQueueType]

    def __init__(self, queue_type, parent: Optional[D] = None):
        self._queue_type = queue_type
        self._parent: D = parent

        if type(self._queue_type) == Traversal.BasicQueueType:
            self.queue_next = lambda current, context: self._queue_next_non_branching(current, context, self._queue_type.queue_next)
        elif type(self._queue_type) == Traversal.BranchingQueueType:
            self.queue_next = lambda  current, context: self._queue_next_branching(current, context, self._queue_type.queue_next)

        self.queue: TraversalQueue[T] = self._queue_type.queue
        self.branch_queue: Optional[TraversalQueue[D]] = self._queue_type.branch_queue
        self.start_items: deque[T] = deque()

        self.running: bool = False

        self.has_run: bool = False
        self.stop_conditions: List[StopCondition[T]] = []
        self.queue_conditions: List[QueueCondition[T]] = []
        self.step_actions: List[StepAction[T]] = []
        self.compute_next_context_funs: Dict[str, ContextValueComputer[T]] = {}
        self.contexts: Dict[T, StepContext] = {}

    def queue_next(self, current_item: T, context: StepContext):
        raise NotImplementedError

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        if self._parent is None:
            self._parent = value
        raise Exception

    def can_action_item(self, item: T, context: StepContext) -> bool:
        """
        Determines if the traversal can apply step actions and stop conditions on the specified item.

        `item` The item to check.
        `context` The context of the current traversal step.
        Returns `true` if the item can be acted upon; `false` otherwise.
        """
        return True

    def can_visit_item(self, item: T, context: StepContext) -> bool:
        raise NotImplementedError

    def create_new_this(self) -> D:
        """
        Creates a new instance of the traversal for branching purposes.

        Returns A new traversal instance.
        """
        raise NotImplementedError

    @singledispatchmethod
    def add_condition(self, condition: ConditionTypes) -> D:
        """
        Adds a traversal condition to the traversal.

        :param condition: The condition to add.

        :return: this traversal instance.
        """
        if callable(condition): # Callable[[NetworkTraceStep[T], StepContext], None]
            if condition.__code__.co_argcount == 2:
                return self.add_stop_condition(condition)
            elif condition.__code__.co_argcount == 4:
                return self.add_queue_condition(condition)
            else:
                raise RuntimeError(f'Condition does not match expected: Number of args is not 2(Stop Condition) or 4(QueueCondition)')

        else:
            raise RuntimeError(f'Condition [{condition.__class__.__name__}] does not match expected: ' +
        "[QueueCondition | DirectionCondition | StopCondition | Callable[_,_] | Callable[_,_,_,_]]")

    @singledispatchmethod
    @add_condition.register(StopCondition)
    def add_stop_condition(self, condition: StopConditionTypes) -> D:
        """
        Adds a stop condition to the traversal. If any stop condition returns `true`, the traversal
        will not call the callback to queue more items from the current item.

        `condition` The stop condition to add.
        Returns this traversal instance.
        """
        raise RuntimeError(f'Condition [{condition.__class__.__name__}] does not match expected: [StopCondition | StopConditionWithContextValue | Callable]')

    @add_stop_condition.register(Callable)
    def _(self, condition: ShouldStop):
        return self.add_stop_condition(StopCondition(condition))

    @add_stop_condition.register
    def _(self, condition: StopCondition):
        self.stop_conditions.append(condition)
        if isinstance(condition, StopConditionWithContextValue):
            self.compute_next_context_funs[condition.key] = condition
        return self

    def copy_stop_conditions(self, other: Traversal[T, D]) -> D:
        """
        Copies all the stop conditions from another traversal to this traversal.

        `other` The other traversal object to copy from.
        Returns The current traversal instance.
        """
        for it in other.stop_conditions:
            self.add_stop_condition(it)
        return self

    def matches_any_stop_condition(self, item: T, context: StepContext) -> bool:
        for condition in self.stop_conditions:
            if condition.should_stop(item, context):
                return True
        return False

    @add_condition.register(QueueCondition)
    @singledispatchmethod
    def add_queue_condition(self, condition: QueueConditionTypes) -> D:
        """
        Adds a queue condition to the traversal. Queue conditions determine whether an item should be queued for traversal.
        All registered queue conditions must return true for an item to be queued.

        :param condition: The queue condition to add.
        :returns: The current traversal instance.
        """
        raise RuntimeError(f'Condition [{condition.__class__.__name__}] does not match expected: [QueueCondition | QueueConditionWithContextValue | Callable]')

    @add_queue_condition.register(Callable)
    def _(self, condition: ShouldQueue):
        return self.add_queue_condition(QueueCondition(condition))

    @add_queue_condition.register
    def _(self, condition: QueueCondition):
        self.queue_conditions.append(condition)
        if isinstance(condition, QueueConditionWithContextValue):
            self.compute_next_context_funs[condition.key] = condition
        return self

    def copy_queue_conditions(self, other: Traversal[T, D]) -> D:
        """
        Copies all queue conditions from another traversal to this traversal.

        :param other: The other traversal from which to copy queue conditions.
        :returns: The current traversal instance.
        """
        for it in other.queue_conditions:
            self.add_queue_condition(it)
        return self

    def add_step_action(self, action: Union[StepActionFunc, StepAction[T]]) -> D:
        """
        Adds an action to be performed on each item in the traversal, including the starting items.

        `action` The action to perform on each item.
        Returns The current traversal instance.
        """
        if isinstance(action, StepAction):
            self.step_actions.append(action)
            if isinstance(action, StepActionWithContextValue):
                self.compute_next_context_funs[action.key] = action
            return self

        elif callable(action):
            return self.add_step_action(StepAction(action))

        raise RuntimeError(f'Condition [{action.__class__.__name__}] does not match expected: [StepAction | StepActionWithContextValue | Callable]')

    def if_not_stopping(self, action: Callable[[T, StepContext], None]) -> D:
        """
        Adds an action to be performed on each item that does not match any stop condition.

        `action` The action to perform on each non-stopping item.
        Returns The current traversal instance.
        """
        self.step_actions.append(StepAction(lambda it, context: action(it, context) if not context.is_stopping else None))
        return self


    def if_stopping(self, action: Callable[[T, StepContext], None]) -> D:
        """
        Adds an action to be performed on each item that matches a stop condition.

        `action` The action to perform on each stopping item.
        Returns The current traversal instance.
        """
        self.step_actions.append(StepAction(lambda it, context: action(it, context) if context.is_stopping else None))
        return self

    def copy_step_actions(self, other: Traversal[T, D]) -> D:
        """
        Copies all the step actions from the passed in traversal to this traversal.

        `other` The other traversal object to copy from.
        Returns The current traversal instance.
        """
        for it in other.step_actions:
            self.add_step_action(it)
        return self

    async def apply_step_actions(self, item: T, context: StepContext) -> D:
        for it in self.step_actions:
            try:
                await it.apply(item, context)
            except TypeError:
                pass
        return self

    def add_context_value_computer(self, computer: ContextValueComputer[T]) -> D:
        """
        Adds a standalone context value computer to compute additional [StepContext] values during traversal.

        `computer` The context value computer to add.
        Returns The current traversal instance.
        """
        #require(not issubclass(computer.__class__, TraversalCondition), lambda: "`computer` must not be a TraversalCondition. Use `addCondition` to add conditions that also compute context values")
        self.compute_next_context_funs[computer.key] = computer
        return self

    def copy_context_value_computer(self, other: Traversal[T, D]) -> D:
        """
        Copies all standalone context value computers from another traversal to this traversal.
        That is, it does not copy any [TraversalCondition] registered that also implements [ContextValueComputer]

        `other` The other traversal from which to copy context value computers.
        Returns The current traversal instance.
        """
        for it in other.compute_next_context_funs.values():
            if it.is_standalone_computer():
                self.add_context_value_computer(it)
        return self

    def _compute_intial_context(self, next_step: T) -> StepContext:
        new_context_data = dict()
        for key, computer in self.compute_next_context_funs.items():
            new_context_data[key] = computer.compute_initial_value(next_step)
        return StepContext(True, False, values=new_context_data)

    def _compute_next_context(self, current_item: T, context: StepContext, next_step: T, is_branch_start: bool) -> StepContext:
        new_context_data = dict()
        for key, computer in self.compute_next_context_funs.items():
            new_context_data[key] = computer.compute_next_value(next_step, current_item, context.get_value(key))

        branch_depth = context.branch_depth +1 if is_branch_start else context.branch_depth
        return StepContext(False, is_branch_start, context.step_number + 1, branch_depth, new_context_data)

    def add_start_item(self, item: T) -> D:
        """
        Adds a starting item to the traversal.

        `item` The item to add.
        Returns The current traversal instance.
        """
        self.start_items.append(item)
        return self


    async def run(self, start_item: T=None, can_stop_on_start_item: bool=True) -> D:
        """
        Runs the traversal optionally adding [startItem] to the collection of start items.

        `startItem` The item from which to start the traversal. (optional)
        `canStopOnStartItem` Indicates if the traversal should check stop conditions on the starting item.
        Returns The current traversal instance.
        """
        if start_item is not None:
            self.start_items.append(start_item)

        require(not self.running, lambda: "Traversal is already running")

        if self.has_run:
            self.reset()

        self.running = True
        self.has_run = True

        if self._parent is None and isinstance(self._queue_type, Traversal.BranchingQueueType) and len(self.start_items) > 1:
            self._branch_start_items()
            # Because we don't traverse anything at the top level parent, we need to pass can_stop_at_start item
            # to the child branch only in this case because they are actually start items.
            await self._traverse_branches(can_stop_on_start_item)
        else:
            await self._traverse(can_stop_on_start_item)
            # Child branches should never stop at start items because a branch start item is not a whole trace start item.
            await self._traverse_branches(True)

        self.running = False
        return self

    def reset(self) -> D:
        """
        Resets the traversal to allow it to be reused.

        Returns The current traversal instance.
        """
        require(not self.running, lambda: "Traversal is currently running.")
        self.has_run = False
        self.queue.clear()
        if self.branch_queue is not None:
            self.branch_queue.clear()

        self.on_reset()

        return self

    @abstractmethod
    def on_reset(self):
        """
        Called when the traversal is reset. Derived classes can override this to reset additional state.
        """
        raise NotImplementedError()

    def _branch_start_items(self):
        while len(self.start_items) > 0:
            start_item = self.start_items.popleft()
            if self._can_queue_start_item(start_item):
                branch = self._create_new_branch(start_item, self._compute_intial_context(start_item))
                if self.branch_queue is None:
                    raise Exception("INTERNAL ERROR: self.branch_queue should never be null here")

                self.branch_queue.append(branch)

    async def _traverse(self, can_stop_on_start_item: bool):
        while len(self.start_items) > 0:
            start_item = self.start_items.popleft()

            # If the traversal is not a branch we need to compute an initial context and check if it
            # should even be queued to trace. If the traversal is a branch, the branch creators should
            # have only created the branch if the item was eligible to be queued and added the item
            # context as part of the branch creation.
            if self._parent is None:
                if self._can_queue_start_item(start_item):
                    self.contexts[start_item] = self._compute_intial_context(start_item)
                    self.queue.append(start_item)
            else:
                self.queue.append(start_item)

        while self.queue.has_next():
            current = self.queue.pop()
            context = self._get_step_context(current)
            can_stop = can_stop_on_start_item or (not context.is_start_item)
            if self.can_visit_item(current, context):
                context.is_stopping = can_stop and self.matches_any_stop_condition(current, context)

                context.is_actionable_item = self.can_action_item(current, context)

                if context.is_actionable_item:
                    await self.apply_step_actions(current, context)

                if not context.is_stopping:
                    self.queue_next(current, context)


    def _get_step_context(self, item: T) -> StepContext:
        try:
            context = self.contexts.pop(item)
            return context
        except KeyError:
            raise KeyError("INTERNAL ERROR: Traversal item should always have a context.")

    def _create_new_branch(self, start_item: T, context: StepContext) -> D:
        it = (
            self.create_new_this()
            .copy_queue_conditions(self)
            .copy_step_actions(self)
            .copy_stop_conditions(self)
            .copy_context_value_computer(self)
        )

        it.contexts[start_item] = context
        Traversal.add_start_item(it, start_item)
        return it

    def _item_queuer(self, current_item: T, current_context) -> Callable[[T], bool]:
        def inner(next_item: T) -> bool:
            next_context = self._compute_next_context(current_item, current_context, next_item, is_branch_start=False)
            if self._can_queue_item(next_item, next_context, current_item, current_context) and self.queue.append(next_item):
                self.contexts[next_item] = next_context
                return True
            else:
                return False

        return inner

    def _queue_next_non_branching(self, current: T, current_context: StepContext, queue_next: QueueNext[T]):
        return queue_next.accept(current, current_context, self._item_queuer(current, current_context))

    def _queue_next_branching(self, current: T, current_context: StepContext, queue_next: BranchingQueueNext[T]):
        def queue_branch(next_item: T):
            next_context = self._compute_next_context(current, current_context, next_item, is_branch_start=True)
            if self._can_queue_item(next_item, next_context, current, current_context):
                branch = self._create_new_branch(next_item, next_context)
                self.branch_queue.append(branch)
                return True
            else:
                return False

        return queue_next.accept(current, current_context, self._item_queuer(current, current_context), queue_branch)

    async def _traverse_branches(self, can_stop_on_start_item: bool):
        if self.branch_queue is None:
            return

        while len(self.branch_queue) > 0:
            next_branch = self.branch_queue.pop()
            if next_branch:
                await next_branch.run(can_stop_on_start_item=can_stop_on_start_item)

    def _can_queue_item(self, next_item: T, next_context: StepContext, current_item: T, current_context: StepContext) -> bool:
        for it in self.queue_conditions:
            if not it.should_queue(next_item, next_context, current_item, current_context):
                return False
        return True

    def _can_queue_start_item(self, start_item: T) -> bool:
        for it in self.queue_conditions:
            if not it.should_queue_start_item(start_item):
                return False
        return True


    class QueueNext(Generic[T]):
        def __init__(self, func):
            self._func = func

        def accept(self, item: T, context: StepContext, queue_item: Callable[[T], bool]) -> bool:
            return self._func(item, context, queue_item)

    class BranchingQueueNext(Generic[T]):
        def __init__(self, func):
            self._func = func

        def accept(self, item: T, context: StepContext, queue_item: Callable[[T], bool], queue_branch: Callable[[T], bool]) -> bool:
            return self._func(item, context, queue_item, queue_branch)
