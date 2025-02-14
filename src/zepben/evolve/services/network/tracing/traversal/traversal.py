#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from collections import deque
from typing import List, Callable, TypeVar, Generic, Optional, Dict, Any

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
        return True

    def can_visit_item(self, item: T, context: 'StepContext') -> bool:
        raise NotImplementedError

    def get_derived_this(self) -> D:
        raise NotImplementedError

    def create_new_this(self) -> D:
        raise NotImplementedError

    def add_condition(self, condition: TraversalCondition[T]) -> D:
        if isinstance(condition, QueueCondition):
            self.add_queue_condition(condition)
        elif isinstance(condition, StopCondition):
            self.add_stop_condition(condition)
        return self.get_derived_this()

    def add_stop_condition(self, condition: StopCondition[T]) -> D:
        self.stop_conditions.append(condition)
        if isinstance(condition, StopConditionWithContextValue):
            self.compute_next_context_funs[condition.key] = condition
        return self.get_derived_this()

    def copy_stop_conditions(self, other: Traversal[T, D]) -> D:
        for it in other.stop_conditions:
            self.add_stop_condition(it)
        return self.get_derived_this()

    def matches_any_stop_condition(self, item: T, context: StepContext) -> bool:
        # TODO: need to make sure this behaviour is right, kotlin hit me for 6 on this one.
        return any(condition.should_stop(item, context) for condition in self.stop_conditions)

    def add_queue_condition(self, condition: QueueCondition[T]) -> D:
        self.queue_conditions.append(condition)
        if isinstance(condition, QueueConditionWithContextValue):
            self.compute_next_context_funs[condition.key] = condition
        return self.get_derived_this()


    def copy_queue_conditions(self, other: Traversal[T, D]) -> D:
        for it in other.queue_conditions:
            self.add_queue_condition(it)
        return self.get_derived_this()

    def add_step_action(self, action: StepAction[T]) -> D:
        self.step_actions.append(action)
        if isinstance(action, StepActionWithContextValue):
            self.compute_next_context_funs[action.key] = action
        return self.get_derived_this()

    def if_not_stopping(self, action: StepAction[T]) -> D:
        # TODO: not sure on this one either
        self.step_actions.append(lambda it, context: action.apply(it, context) if not context.is_stopping else None)
        return self.get_derived_this()


    def if_stopping(self, action: StepAction[T]) -> D:
        # TODO: not sure on this one either
        self.step_actions.append(lambda it, context: action.apply(it, context) if context.is_stopping else None)
        return self.get_derived_this()

    def copy_step_actions(self, other: Traversal[T, D]) -> D:
        for it in other.step_actions:
            self.add_step_action(it)
        return self.get_derived_this()

    def apply_step_actions(self, item: T, context: StepContext) -> D:
        for it in self.step_actions:
            it.apply(item, context)
        return self.get_derived_this()

    def add_context_value_computer(self, computer: ContextValueComputer[T]) -> D:
        require(isinstance(computer, TraversalCondition), lambda: "`computer` must not be a TraversalCondition. Use `addCondition` to add conditions that also compute context values")
        self.compute_next_context_funs[computer.key] = computer
        return self.get_derived_this()


class QueueNext[T]:
    def accept(self, item: T, context: 'StepContext', queue_item: Callable[[T], bool]) -> None:
        pass

class BranchingQueueNext[T]:
    def accept(self, item: T, context: 'StepContext', queue_item: Callable[[T], bool], queue_branch: Callable[[T], bool]) -> None:
        pass

class QueueType[T, D: 'Traversal[T, D]']():
    @property
    def queue(self) -> TraversalQueue[T]:
        pass

    @property
    def branch_queue(self) -> Optional['TraversalQueue[D]']:
        pass

class BasicQueueType[T, D: 'Traversal[T, D]'](QueueType[T, D]):
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

