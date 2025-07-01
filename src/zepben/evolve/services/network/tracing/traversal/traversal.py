#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import inspect
from abc import abstractmethod
from collections import deque
from collections.abc import Callable
from functools import singledispatchmethod
from logging import Logger
from typing import List, TypeVar, Generic, Optional, Dict, Union

from zepben.evolve import require
from zepben.evolve.services.network.tracing.traversal.context_value_computer import ContextValueComputer
from zepben.evolve.services.network.tracing.traversal.debug_logging import DebugLoggingWrapper
from zepben.evolve.services.network.tracing.traversal.queue_condition import QueueCondition, QueueConditionWithContextValue, ShouldQueue
from zepben.evolve.services.network.tracing.traversal.step_action import StepAction, StepActionWithContextValue, StepActionFunc
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext
from zepben.evolve.services.network.tracing.traversal.stop_condition import StopCondition, StopConditionWithContextValue, ShouldStop

__all__ = ["Traversal"]

from zepben.evolve.services.network.tracing.traversal.queue import TraversalQueue

T = TypeVar('T')
U = TypeVar('U')
D = TypeVar('D', bound='Traversal')
QT = TypeVar('QT')
QD = TypeVar('QD')

QueueConditionTypes = Union[ShouldQueue, QueueCondition[T]]
StopConditionTypes = Union[ShouldStop, StopCondition[T]]
ConditionTypes = Union[QueueConditionTypes, StopConditionTypes]
StepActionTypes = Union[StepActionFunc, StepAction]


class Traversal(Generic[T, D]):
    """
    A base traversal class allowing items in a connected graph to be traced.
    It provides the main interface and implementation for traversal logic.
    This class manages conditions, actions, and context values that guide each
    traversal step.

    This class supports a concept of 'branching', whereby when a new branch is
    created a new child traversal instance is created. The child inherits its
    parents conditions, actions and what it has tracked. However, it knows nothing
    about what its siblings have tracked. This allows traversing both ways around
    loops in the graph.

    This class is abstract to allow for type-specific implementations for branching
    traversals and custom start item handling.

    This class is **not thread safe**.

    `T` The type of object to be traversed.
    `D` The specific type of traversal, extending :class:`Traversal`.

    :var name: The name of the traversal. Can be used for logging purposes and will be included in all debug logging.
    :var _queue_type: The type of queue to use for processing this traversal.
    :var _parent: The parent traversal, or None if this is a root level traversal. Primarily used to track branching traversals.
    :var _debug_logger: An optional logger to add information about how the trace is processing items.
    """

    class QueueType(Generic[QT, QD]):
        """
        Defines the types of queues used in the traversal.

        :var queue_next: Logic for queueing the next item in the traversal.
        :var queue: The primary queue of items.
        """

        queue_next: Traversal.QueueNext[QT]
        queue: TraversalQueue[QT]

        @property
        @abstractmethod
        def queue(self) -> TraversalQueue[QT]:
            raise NotImplementedError

        @property
        def branch_queue(self) -> Optional[TraversalQueue[QD]]:
            raise NotImplementedError

    class BasicQueueType(QueueType[QT, QD]):
        """
        Basic queue type that handles non-branching item queuing.

        :param queue_next: Logic for queueing the next item in the traversal.
        :param queue: The primary queue of items.
        """

        def __init__(self, queue_next: Traversal.QueueNext[QT], queue: TraversalQueue[QT]):
            self.queue_next = queue_next
            self._queue = queue
            self._branch_queue = None

        @property
        def queue(self) -> TraversalQueue[QT]:
            """The primary queue of items."""
            return self._queue

        @property
        def branch_queue(self) -> Optional[TraversalQueue[QD]]:
            return self._branch_queue

    class BranchingQueueType(QueueType[QT, QD]):
        """
        Branching queue type, supporting operations that may split into separate
        branches during traversal.

        :param queue_next: Logic for queueing the next item in a branching traversal.
        :param queue_factory: Factory function to create the main queue.
        :param branch_queue_factory: Factory function to create the branch queue.
        """

        def __init__(
            self,
            queue_next: Traversal.BranchingQueueNext[QT],
            queue_factory: Callable[[], TraversalQueue[QT]],
            branch_queue_factory: Callable[[], TraversalQueue[QD]],
        ):
            self.queue_next: Traversal.BranchingQueueNext[QT] = queue_next
            self.queue_factory = queue_factory
            self.branch_queue_factory = branch_queue_factory

        @property
        def queue(self) -> TraversalQueue[QT]:
            return self.queue_factory()

        @property
        def branch_queue(self) -> Optional[TraversalQueue[QD]]:
            return self.branch_queue_factory()

    name: str

    def __init__(self, queue_type, parent: Optional[D] = None, debug_logger: Logger = None):
        self._queue_type = queue_type
        self._parent: D = parent
        self._debug_logger = DebugLoggingWrapper(self.name, debug_logger) if debug_logger else None

        if type(queue_type) == Traversal.BasicQueueType:
            self.queue_next = lambda current, context: self._queue_next_non_branching(current, context, self._queue_type.queue_next)
        elif type(queue_type) == Traversal.BranchingQueueType:
            self.queue_next = lambda current, context: self._queue_next_branching(current, context, self._queue_type.queue_next)

        self.queue: TraversalQueue[T] = queue_type.queue
        self.branch_queue: Optional[TraversalQueue[D]] = queue_type.branch_queue
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
        Determines if the traversal can apply step actions and stop conditions
        on the specified item.

        :param item: The item to check.
        :param context: The context of the current traversal step.
        :returns: ``True`` if the item can be acted upon; ``False`` otherwise.
        """

        return True

    def can_visit_item(self, item: T, context: StepContext) -> bool:
        raise NotImplementedError

    def create_new_this(self) -> D:
        """
        Creates a new instance of the traversal for branching purposes.

            NOTE: Do NOT add the debug logger to this call, as all traces created for
                  branching will already have their actions wrapped, and passing the
                  debug logger through means you get duplicate wrappers that double,
                  triple etc. log the debug messages.

        :returns: A new traversal instance.
        """

        raise NotImplementedError

    @singledispatchmethod
    def add_condition(self, condition: ConditionTypes) -> D:
        """
        Adds a traversal condition to the traversal.

        :param condition: The condition to add.

        :return: this traversal instance.
        """

        if callable(condition):  # Callable[[NetworkTraceStep[T], StepContext], None]
            if len(inspect.getfullargspec(condition).args) == 2:
                return self.add_stop_condition(condition)
            elif len(inspect.getfullargspec(condition).args) == 4:
                return self.add_queue_condition(condition)
            else:
                raise RuntimeError(f'Condition does not match expected: Number of args is not 2(Stop Condition) or 4(QueueCondition)')

        else:
            raise RuntimeError(
                f'Condition [{condition.__class__.__name__}] does not match expected: '
                + "[QueueCondition | DirectionCondition | StopCondition | Callable[_,_] | Callable[_,_,_,_]]"
            )

    @singledispatchmethod
    @add_condition.register(StopCondition)
    def add_stop_condition(self, condition: StopConditionTypes) -> D:
        """
        Adds a stop condition to the traversal. If any stop condition returns
        ``True``, the traversal will not call the callback to queue more items
        from the current item.

        :param condition: The stop condition to add.
        :return: this traversal instance.
        """

        raise RuntimeError(f'Condition [{condition.__class__.__name__}] does not match expected: [StopCondition | StopConditionWithContextValue | Callable]')

    @add_stop_condition.register(Callable)
    def _(self, condition: ShouldStop):
        return self.add_stop_condition(StopCondition(condition))

    @add_stop_condition.register
    def _(self, condition: StopCondition):

        if self._debug_logger is not None:
            self._debug_logger.wrap(condition)

        self.stop_conditions.append(condition)
        if isinstance(condition, StopConditionWithContextValue):
            self.compute_next_context_funs[condition.key] = condition
        return self

    def copy_stop_conditions(self, other: Traversal[T, D]) -> D:
        """
        Copies all the stop conditions from another traversal to this traversal.

        :param other: The other traversal object to copy from.
        :return: The current traversal instance.
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
        Adds a queue condition to the traversal.
        Queue conditions determine whether an item should be queued for traversal.
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

        if self._debug_logger is not None:
            self._debug_logger.wrap(condition)

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

    @singledispatchmethod
    def add_step_action(self, action: StepActionTypes) -> D:
        """
        Adds an action to be performed on each item in the traversal, including the
        starting items.

        :param action: The action to perform on each item.
        :return: The current traversal instance.
        """

        raise RuntimeError(f'StepAction [{action.__class__.__name__}] does not match expected: [StepAction | StepActionWithContextValue | Callable]')

    @add_step_action.register
    def _(self, action: StepAction):
        if self._debug_logger is not None:
            self._debug_logger.wrap(action)

        self.step_actions.append(action)
        if isinstance(action, StepActionWithContextValue):
            self.compute_next_context_funs[action.key] = action
        return self

    @add_step_action.register(Callable)
    def _(self, action: StepActionFunc):
        return self.add_step_action(StepAction(action))

    @singledispatchmethod
    def if_not_stopping(self, action: StepActionTypes) -> D:
        """
        Adds an action to be performed on each item that does not match any stop condition.

        :param action: The action to perform on each non-stopping item.
        :return: The current traversal instance.
        """
        raise RuntimeError(f'StepAction [{action}] does not match expected: [StepAction | StepActionWithContextValue | Callable]')

    @if_not_stopping.register(Callable)
    def _(self, action: StepActionFunc) -> D:
        return self.add_step_action(lambda it, context: action(it, context) if not context.is_stopping else None)

    @if_not_stopping.register
    def _(self, action: StepAction) -> D:
        action.apply = lambda it, context: action._func(it, context) if not context.is_stopping else None
        return self.add_step_action(action)

    @singledispatchmethod
    def if_stopping(self, action: StepActionTypes) -> D:
        """
        Adds an action to be performed on each item that matches a stop condition.

        :param action: The action to perform on each stopping item.
        :return: The current traversal instance.
        """
        raise RuntimeError(f'StepAction [{action}] does not match expected: [StepAction | StepActionWithContextValue | Callable]')

    @if_stopping.register(Callable)
    def _(self, action: StepActionFunc) -> D:
        return self.add_step_action(lambda it, context: action(it, context) if context.is_stopping else None)

    @if_stopping.register
    def _(self, action: StepAction) -> D:
        action.apply = lambda it, context: action._func(it, context) if context.is_stopping else None
        return self.add_step_action(action)

    def copy_step_actions(self, other: Traversal[T, D]) -> D:
        """
        Copies all the step actions from the passed in traversal to this traversal.

        :param other: The other traversal object to copy from.
        :return: The current traversal instance.
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
        Adds a standalone context value computer to compute additional `StepContext`
        values during traversal.

        :param computer: The context value computer to add.
        :return: The current traversal instance.
        """

        # require(not issubclass(computer.__class__, TraversalCondition), lambda: "`computer` must not be a TraversalCondition. Use `addCondition` to add conditions that also compute context values")
        self.compute_next_context_funs[computer.key] = computer
        return self

    def copy_context_value_computer(self, other: Traversal[T, D]) -> D:
        """
        Copies all standalone context value computers from another traversal to this
        traversal.
        That is, it does not copy any `TraversalCondition` registered that also
        implements `ContextValueComputer`

        :param other: The other traversal from which to copy context value computers.
        :return: The current traversal instance.
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

        branch_depth = context.branch_depth + 1 if is_branch_start else context.branch_depth
        return StepContext(False, is_branch_start, context.step_number + 1, branch_depth, new_context_data)

    def add_start_item(self, item: T) -> D:
        """
        Adds a starting item to the traversal.

        :param item: The item to add.
        :return: The current traversal instance.
        """

        self.start_items.append(item)
        return self

    async def run(self, start_item: T = None, can_stop_on_start_item: bool = True) -> D:
        """
        Runs the traversal optionally adding [startItem] to the collection of start items.

        :param start_item: The item from which to start the traversal. (optional)
        :param can_stop_on_start_item: Indicates if the traversal should check stop conditions
            on the starting item.
        :return: The current traversal instance.
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

        :return: The current traversal instance.
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
        Called when the traversal is reset. Derived classes can override this to
        reset additional state.
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
        # fmt: off
        it = (
            self.create_new_this()
            .copy_queue_conditions(self)
            .copy_step_actions(self)
            .copy_stop_conditions(self)
            .copy_context_value_computer(self)
        )
        # fmt: on

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
