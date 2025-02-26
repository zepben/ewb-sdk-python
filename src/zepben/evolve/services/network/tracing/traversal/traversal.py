#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from collections import deque
from collections.abc import Collection
from typing import List, Callable, TypeVar, Generic, Optional, Dict, Any, overload

from zepben.evolve import require
from zepben.evolve.services.network.tracing.traversal.context_value_computer import ContextValueComputer
from zepben.evolve.services.network.tracing.traversal.queue_condition import QueueCondition, QueueConditionWithContextValue
from zepben.evolve.services.network.tracing.traversal.step_action import StepAction, StepActionWithContextValue
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext
from zepben.evolve.services.network.tracing.traversal.stop_condition import StopCondition, StopConditionWithContextValue

__all__ = ["Traversal"]

from zepben.evolve.services.network.tracing.traversal.traversal_condition import TraversalCondition
from zepben.evolve.services.network.tracing.traversal.traversal_queue import TraversalQueue

T = TypeVar('T')
D = TypeVar('D')



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
    def __init__(self, queue_type: QueueType[T, D], parent: Optional[D] = None):
        self._queue_type = queue_type
        self._parent = parent
        self.queue_next: Callable[[T, StepContext], None] = self._initialize_queue_next()
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

    def _initialize_queue_next(self) -> Callable[[T, StepContext], None]:
        if isinstance(self._queue_type, BasicQueueType):
            return lambda current, context: self.queue_next_non_branching(current, context, self._queue_type.queue_next)
        elif isinstance(self._queue_type, BranchingQueueType):
            return lambda current, context: self.queue_next_branching(current, context, self._queue_type.queue_next)

    def can_action_item(self, item: T, context: 'StepContext') -> bool:
        """
        Determines if the traversal can apply step actions and stop conditions on the specified item.

        `item` The item to check.
        `context` The context of the current traversal step.
        Returns `true` if the item can be acted upon; `false` otherwise.
        """
        return True

    def can_visit_item(self, item: T, context: 'StepContext') -> bool:
        raise NotImplementedError

    def get_derived_this(self) -> D:
        """
        Retrieves the derived instance of this traversal class.

        Returns The derived traversal instance.
        """
        raise NotImplementedError

    def create_new_this(self) -> D:
        """
        Creates a new instance of the traversal for branching purposes.

        Returns A new traversal instance.
        """
        raise NotImplementedError

    def add_condition(self, condition: TraversalCondition[T]) -> D:
        """
        Adds a traversal condition to the traversal.

        `condition` The condition to add.
        Returns this traversal instance.
        """
        if isinstance(condition, QueueCondition):
            self.add_queue_condition(condition)
        elif isinstance(condition, StopCondition):
            self.add_stop_condition(condition)
        return self.get_derived_this()

    def add_stop_condition(self, condition: StopCondition[T]) -> D:
        """
        Adds a stop condition to the traversal. If any stop condition returns `true`, the traversal
        will not call the callback to queue more items from the current item.

        `condition` The stop condition to add.
        Returns this traversal instance.
        """
        self.stop_conditions.append(condition)
        if isinstance(condition, StopConditionWithContextValue):
            self.compute_next_context_funs[condition.key] = condition
        return self.get_derived_this()

    def copy_stop_conditions(self, other: Traversal[T, D]) -> D:
        """
        Copies all the stop conditions from another traversal to this traversal.

        `other` The other traversal object to copy from.
        Returns The current traversal instance.
        """
        for it in other.stop_conditions:
            self.add_stop_condition(it)
        return self.get_derived_this()

    def matches_any_stop_condition(self, item: T, context: StepContext) -> bool:
        # TODO: need to make sure this behaviour is right, kotlin hit me for 6 on this one.
        return any(condition.should_stop(item, context) for condition in self.stop_conditions)

    def add_queue_condition(self, condition: QueueCondition[T]) -> D:
        """
        Adds a queue condition to the traversal. Queue conditions determine whether an item should be queued for traversal.
        All registered queue conditions must return true for an item to be queued.

        `condition` The queue condition to add.
        Returns The current traversal instance.
        """
        self.queue_conditions.append(condition)
        if isinstance(condition, QueueConditionWithContextValue):
            self.compute_next_context_funs[condition.key] = condition
        return self.get_derived_this()


    def copy_queue_conditions(self, other: Traversal[T, D]) -> D:
        """
        Copies all queue conditions from another traversal to this traversal.

        `other` The other traversal from which to copy queue conditions.
         Returns The current traversal instance.
        """
        for it in other.queue_conditions:
            self.add_queue_condition(it)
        return self.get_derived_this()

    def add_step_action(self, action: StepAction[T]) -> D:
        """
        Adds an action to be performed on each item in the traversal, including the starting items.

        `action` The action to perform on each item.
        Returns The current traversal instance.
        """
        self.step_actions.append(action)
        if isinstance(action, StepActionWithContextValue):
            self.compute_next_context_funs[action.key] = action
        return self.get_derived_this()

    def if_not_stopping(self, action: StepAction[T]) -> D:
        """
        Adds an action to be performed on each item that does not match any stop condition.

        `action` The action to perform on each non-stopping item.
        Returns The current traversal instance.
        """
        self.step_actions.append(lambda it, context: action.apply(it, context) if not context.is_stopping else None)
        return self.get_derived_this()


    def if_stopping(self, action: StepAction[T]) -> D:
        """
        Adds an action to be performed on each item that matches a stop condition.

        `action` The action to perform on each stopping item.
        Returns The current traversal instance.
        """
        self.step_actions.append(lambda it, context: action.apply(it, context) if context.is_stopping else None)
        return self.get_derived_this()

    def copy_step_actions(self, other: Traversal[T, D]) -> D:
        """
        Copies all the step actions from the passed in traversal to this traversal.

        `other` The other traversal object to copy from.
        Returns The current traversal instance.
        """
        for it in other.step_actions:
            self.add_step_action(it)
        return self.get_derived_this()

    def apply_step_actions(self, item: T, context: StepContext) -> D:
        for it in self.step_actions:
            it.apply(item, context)
        return self.get_derived_this()

    def add_context_value_computer(self, computer: ContextValueComputer[T]) -> D:
        """
        Adds a standalone context value computer to compute additional [StepContext] values during traversal.

        `computer` The context value computer to add.
        Returns The current traversal instance.
        """
        require(isinstance(computer, TraversalCondition), lambda: "`computer` must not be a TraversalCondition. Use `addCondition` to add conditions that also compute context values")
        self.compute_next_context_funs[computer.key] = computer
        return self.get_derived_this()

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
        return self.get_derived_this()

    def _compute_intial_context(self, next_step: T) -> StepContext:
        new_context_data = dict()
        for key, computer in self.compute_next_context_funs:
            new_context_data[key] = computer.compute_initial_value(next_step)
        return StepContext(True, False, 0, 0, new_context_data)

    def _compute_next_context(self, current_item: T, context: StepContext, next_step: T, is_branch_start: bool) -> StepContext:
        new_context_data = dict()
        for key, computer in self.compute_next_context_funs:
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
        return self.get_derived_this()


    def run(self, start_item: T=None, can_stop_on_start_item: bool=True) -> D:
        """
        Runs the traversal optionally adding [startItem] to the collection of start items.

        `startItem` The item from which to start the traversal. (optional)
        `canStopOnStartItem` Indicates if the traversal should check stop conditions on the starting item.
        Returns The current traversal instance.
        """
        if start_item:
            self.start_items.append(start_item)
            self.run(can_stop_on_start_item)  # TODO: check if this double entry of `run` is actually utilised at all
            return self.get_derived_this()

        else:
            require(not self.running, "Traversal is already running")

            if self.has_run:
                self.reset()

            self.running = True
            self.has_run = True

            if (self._parent is None and isinstance(self._queue_type, BranchingQueueType) and len(self.start_items()) > 1 ):
                self.branch_start_items()
            else:
                self.traverse(can_stop_on_start_item)

            self.traverse_branches(can_stop_on_start_item)

            self.running = False

    def reset(self) -> D:
        """
        Resets the traversal to allow it to be reused.

        Returns The current traversal instance.
        """
        require(not self.running, "Traversal is currently running.")
        self.has_run = False
        self.queue.clear()
        self.branch_queue.clear()

        self.on_reset()

        return self.get_derived_this()

    def on_reset(self):
        """
        Called when the traversal is reset. Derived classes can override this to reset additional state.
        """
        pass

    def branch_start_items(self):
        while len(self.start_items) > 0:
            start_item = self.start_items.popleft() # TODO: equivalent to startItems.removeFirst?
            if self.can_queue_start_item(start_item):
                branch = self.create_new_branch(start_item, self._compute_intial_context(start_item))
                require(self.branch_queue is not None, "INTERNAL ERROR: self.branch_queue should never be null here")
                self.branch_queue.put(branch)

    def traverse(self, can_stop_on_start_item: bool):
        while len(self.start_items) > 0:
            start_item = self.start_items.popleft()

            if self._parent is None:
                if self.can_queue_start_item(start_item):
                    self.contexts[start_item] = self._compute_intial_context(start_item)
                    self.queue.add(start_item)
            else:
                self.queue.add(start_item)

            can_stop = can_stop_on_start_item
            for current in  self.queue.get():
                context = self.get_step_context(current)
                if self.can_visit_item(current, context):
                    context.is_actionable_item = self.can_action_item(current, context)

                    if context.is_actionable_item:
                        context.is_stopping = can_stop and self.matches_any_stop_condition(current, context)
                        self.apply_step_actions(current, context)

                    if not context.is_stopping:
                        self.queue_next(current, context)

                    can_stop = True

    def get_step_context(self, item: T) -> StepContext:
        context = self.contexts.pop(item)
        require(context is not None, "INTERNAL ERROR: Traversal item should always have a context.")

    def create_new_branch(self, start_item: T, context: StepContext) -> D:
        it = self.create_new_this()
        it.copy_queue_conditions(it)
        it.copy_step_actions(it)
        it.copy_stop_conditions(it)
        it.copy_context_value_computers(it)

        it.contexts[start_item] = context
        it.add_start_item(start_item)
        return it

    def item_queuer(self, current_item: T, current_context) -> Callable[[T], bool]:
        def inner(next_item: T) -> bool:
            next_context = self._compute_next_context(current_item, current_context, next_item, False)
            if self.can_queue_item(next_item, next_context, current_item, current_context) and self.queue.add(next_item):
                self.contexts[next_item] = next_context
                return True
            else:
                return False

        return inner

    def queue_next_non_branching(self, current: T, current_context: StepContext, queue_next: QueueNext[T]):
        queue_next.accept(current, current_context, self.item_queuer(current, current_context))

    def queue_next_branching(self, current: T, current_context: StepContext, queue_next: BranchingQueueNext[T]):
        pass

    def traverse_branches(self, can_stop_on_start_item: bool):
        if self.branch_queue is None:
            return

        while self.branch_queue.has_next():
            self.branch_queue.get().run(can_stop_on_start_item)

    def can_queue_item(self, next_item: T, next_context: StepContext, current_item: T, current_context: StepContext) -> bool:
        return all(it.should_queue(next_item, next_context, current_item, current_context) for it in self.queue_conditions)

    def can_queue_start_item(self, start_item: T) -> bool:
        return all(it.should_queue_start_item(start_item) for it in self.queue_conditions)


class QueueNext[T]:
    """
    Functional interface for queuing items in a non-branching traversal.
    """
    def accept(self, item: T, context: 'StepContext', queue_item: Callable[[T], bool]) -> None:
        pass

class BranchingQueueNext[T]:
    """
    Functional interface for queuing items in a branching traversal.
    """
    def accept(self, item: T, context: 'StepContext', queue_item: Callable[[T], bool], queue_branch: Callable[[T], bool]) -> None:
        pass

class QueueType[T, D: 'Traversal[T, D]']():
    """
    Defines the types of queues used in the traversal.
    """
    @property
    def queue(self) -> TraversalQueue[T]:
        pass

    @property
    def branch_queue(self) -> Optional['TraversalQueue[D]']:
        pass

class BasicQueueType[T, D: 'Traversal[T, D]'](QueueType[T, D]):
    """
    Basic queue type that handles non-branching item queuing.

    `queueNext` Logic for queueing the next item in the traversal.
    `queue` The primary queue of items.
    """
    def __init__(self, queue_next: QueueNext[T], queue: 'TraversalQueue[T]'):
        self.queue_next = queue_next
        self._queue = queue
        self._branch_queue = None

    @property
    def queue(self) -> 'TraversalQueue[T]':
        return self._queue

    @property
    def branch_queue(self) -> Optional['TraversalQueue[D]']:
        return self._branch_queue

class BranchingQueueType(QueueType[T, D]):
    """
    Branching queue type, supporting operations that may split into separate branches during traversal.

    `queueNext` Logic for queueing the next item in a branching traversal.
    `queueFactory` Factory function to create the main queue.
    `branchQueueFactory` Factory function to create the branch queue.
    """
    def __init__(self, queue_next: BranchingQueueNext[T], queue_factory: Callable[[], 'TraversalQueue[T]'], branch_queue_factory: Callable[[], 'TraversalQueue[D]']):
        self.queue_next = queue_next
        self.queue_factory = queue_factory
        self.branch_queue_factory = branch_queue_factory

    @property
    def queue(self) -> 'TraversalQueue[T]':
        return self.queue_factory()

    @property
    def branch_queue(self) -> 'TraversalQueue[D]':
        return self.branch_queue_factory()

