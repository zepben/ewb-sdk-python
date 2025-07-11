#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections import deque
from logging import Logger
from typing import Callable, TypeVar, Tuple, Any, Optional

import pytest

from zepben.ewb import StepContext, Traversal, TraversalQueue, ContextValueComputer, StepActionWithContextValue, StepAction

T = TypeVar('T')
D = TypeVar('D')


class TraversalTest(Traversal[T, D]):
    name = 'TestTraversal'

    def __init__(
        self,
        queue_type,
        parent: Optional["TraversalTest[T, D]"],
        can_visit_item: Callable[[T, StepContext], bool],
        can_action_item: Callable[[T, StepContext], bool],
        on_reset: Callable[[], Any],
        debug_logger: Logger = None,
    ):
        super().__init__(queue_type, parent, debug_logger=debug_logger)
        self._can_visit_item_impl = can_visit_item
        self._can_action_item_impl = can_action_item
        self._on_reset_impl = on_reset

    def can_visit_item(self, item: T, context: StepContext) -> bool:
        return self._can_visit_item_impl(item, context)

    def can_action_item(self, item: T, context: StepContext) -> bool:
        return self._can_action_item_impl(item, context)

    def on_reset(self):
        return self._on_reset_impl()

    def create_new_this(self) -> "TraversalTest[T, D]":
        return TraversalTest(self._queue_type, self, self._can_visit_item_impl, self._can_action_item_impl, self._on_reset_impl)


def _create_traversal(
    can_visit_item: Callable[[int, StepContext], bool] = lambda x, y: True,
    can_action_item: Callable[[int, StepContext], bool] = lambda x, y: True,
    on_reset: Callable[[], Any] = lambda: None,
    queue: TraversalQueue[int] = TraversalQueue.depth_first(),
) -> TraversalTest[int, D]:
    def queue_next(item, _, queue_item):
        if item < 0:
            queue_item(item - 1)
        else:
            queue_item(item + 1)

    queue_type = Traversal.BasicQueueType[int, TraversalTest[int, D]](queue_next=Traversal.QueueNext(queue_next), queue=queue)

    return TraversalTest(queue_type, None, can_visit_item, can_action_item, on_reset)


def _create_branching_traversal() -> TraversalTest[int, D]:
    def queue_next(item, _, queue_item, queue_branch):
        if item == 0:
            queue_branch(-10)
            queue_branch(10)
        elif item < 0:
            queue_item(item + 1)
        else:
            queue_item(item - 1)

    queue_type = Traversal.BranchingQueueType[int, TraversalTest[int, D]](
        queue_next=Traversal.BranchingQueueNext(queue_next),
        queue_factory=lambda: TraversalQueue.depth_first(),
        branch_queue_factory=lambda: TraversalQueue.depth_first(),
    )

    return TraversalTest(queue_type, None,
                         can_visit_item=lambda x, y: True,
                         can_action_item=lambda x, y: True,
                         on_reset=lambda: None)


class TestTraversal:

    def setup_method(self, test_method) -> None:
        self.last_num = None
        return test_method

    @pytest.mark.asyncio
    async def test_add_condition_with_stop_condition(self):
        def step_action(item, _):
            self.last_num = item

        await (
            _create_traversal()
            .add_condition(lambda item, _: item == 2)
            .add_step_action(step_action)
            .run(1)
        )

        assert self.last_num == 2

    @pytest.mark.asyncio
    async def test_add_condition_with_queue_condition(self):
        def step_action(item, _):
            self.last_num = item

        await (
            _create_traversal()
            .add_condition(lambda item, x, y, z: item < 3)
            .add_step_action(step_action)
            .run(1)
        )

        assert self.last_num == 2

    @pytest.mark.asyncio
    async def test_stop_conditions(self):
        steps = []

        await (
            _create_traversal()
            .add_stop_condition(lambda item, _: item == 3)
            .add_step_action(lambda item, ctx: steps.append((item, ctx)))
            .run(1)
        )

        def check_item_ctx(step: Tuple[int, StepContext], item_val: int, ctx_stopping=False):
            return step[0] == item_val and step[1].is_stopping == ctx_stopping

        assert check_item_ctx(steps[0], 1)
        assert check_item_ctx(steps[1], 2)
        assert check_item_ctx(steps[2], 3, True)

    @pytest.mark.asyncio
    async def test_stops_when_matching_any_stop_condition(self):
        def step_action(item, _):
            self.last_num = item

        await (
            _create_traversal()
            .add_stop_condition(lambda item, _: item == 3)
            .add_stop_condition(lambda item, _: item % 2 == 0)
            .add_step_action(step_action)
            .run(1)
        )

        assert self.last_num == 2

    @pytest.mark.asyncio
    async def test_can_stop_on_start_item_true(self):
        def step_action(item, _):
            self.last_num = item

        await (
            _create_traversal()
            .add_stop_condition(lambda item, _: item == 1)
            .add_stop_condition(lambda item, _: item == 2)
            .add_step_action(step_action)
            .run(1, can_stop_on_start_item=True)
        )

        assert self.last_num == 1

    @pytest.mark.asyncio
    async def test_can_stop_on_start_item_false(self):
        def step_action(item, _):
            self.last_num = item

        await (
            _create_traversal()
            .add_stop_condition(lambda item, _: item == 1)
            .add_stop_condition(lambda item, _: item == 2)
            .add_step_action(step_action)
            .run(1, can_stop_on_start_item=False)
        )

        assert self.last_num == 2

    @pytest.mark.asyncio
    async def test_checks_queue_condition(self):
        def step_action(item, _):
            self.last_num = item

        await (
            _create_traversal()
            .add_queue_condition(lambda next_item, x, y, z: next_item < 3)
            .add_step_action(step_action)
            .run(1)
        )

        assert self.last_num == 2

    @pytest.mark.asyncio
    async def test_queues_when_matching_all_queue_condition(self):
        def step_action(item, _):
            self.last_num = item

        await (
            _create_traversal()
            .add_queue_condition(lambda next_item, x, y, z: next_item < 3)
            .add_queue_condition(lambda next_item, x, y, z: next_item > 3)
            .add_step_action(step_action)
            .run(1)
        )

        assert self.last_num == 1

    @pytest.mark.asyncio
    async def test_calls_all_registered_step_actions(self):
        called1 = []
        called2 = []

        await (
            _create_traversal()
            .add_stop_condition(lambda item, _: item == 2)
            .add_step_action(lambda x, y: called1.append(True))
            .add_step_action(lambda x, y: called2.append(True))
            .run(1)
        )

        assert len(called1) == 2
        assert len(called2) == 2

    @pytest.mark.asyncio
    async def test_if_not_stopping_helper_only_calls_when_not_stopping(self):
        steps = []
        await (
            _create_traversal()
            .add_stop_condition(lambda item, _: item == 3)
            .if_not_stopping(lambda item, _: steps.append(item))
            .run(1)
        )

        assert steps == [1, 2]

    @pytest.mark.asyncio
    async def test_if_not_stopping_helper_accepts_step_actions(self):
        steps = []
        await (
            _create_traversal()
            .add_stop_condition(lambda item, _: item == 3)
            .if_not_stopping(StepAction(lambda item, _: steps.append(item)))
            .run(1)
        )

        assert steps == [1, 2]

    @pytest.mark.asyncio
    async def test_if_stopping_helper_only_calls_when_stopping(self):
        steps = []
        await (
            _create_traversal()
            .add_stop_condition(lambda item, _: item == 3)
            .if_stopping(lambda item, _: steps.append(item))
            .run(1)
        )

        assert steps == [3]

    @pytest.mark.asyncio
    async def test_if_stopping_helper_accepts_step_actions(self):
        steps = []
        await (
            _create_traversal()
            .add_stop_condition(lambda item, _: item == 3)
            .if_stopping(StepAction(lambda item, _: steps.append(item)))
            .run(1)
        )

        assert steps == [3]

    @pytest.mark.asyncio
    async def test_if_not_stopping_helper_accepts_step_action_with_context_value_and_context_is_computed(self):
        data_capture: dict[int, str] = {}
        contex_data_capture = list()

        class TestSAWCV(StepActionWithContextValue[int]):
            """We append to `context_data_capture` on every step to ensure that the context is computed on every step."""

            def compute_next_value(self, next_item: int, current_item: int, current_value):
                contex_data_capture.append(True)
                return f'{current_value} : (next_item={next_item}, current_item={current_item})'

            def compute_initial_value(self, item: int):
                contex_data_capture.append(True)
                return f'{item}'

        def step_action(item, ctx: StepContext):
            data_capture[item] = ctx.get_value('test')

        await (
            _create_traversal()
            .add_stop_condition(lambda item, _: item == 3)
            .if_not_stopping(TestSAWCV(_func=step_action, key='test'))
            .run(1)
        )

        assert len(data_capture) == 2
        assert data_capture[1] == '1'
        assert data_capture[2] == '1 : (next_item=2, current_item=1)'

        # If this fails, either the number of steps changed, or context wasn't computed every step
        assert len(contex_data_capture) == 3

    @pytest.mark.asyncio
    async def test_if_stopping_helper_accepts_step_action_with_context_value_and_context_is_computed(self):
        data_capture: dict[int, str] = {}
        contex_data_capture = list()

        class TestSAWCV(StepActionWithContextValue[int]):
            """We append to `context_data_capture` on every step to ensure that the context is computed on every step."""

            def compute_next_value(self, next_item: int, current_item: int, current_value):
                contex_data_capture.append(True)
                return f'{current_value} : (next_item={next_item}, current_item={current_item})'

            def compute_initial_value(self, item: int):
                contex_data_capture.append(True)
                return f'{item}'

        def step_action(item, ctx: StepContext):
            data_capture[item] = ctx.get_value('test')

        await (
            _create_traversal()
            .add_stop_condition(lambda item, _: item == 3)
            .if_stopping(TestSAWCV(_func=step_action, key='test'))
            .run(1)
        )

        assert len(data_capture) == 1
        assert data_capture[3] == '1 : (next_item=2, current_item=1) : (next_item=3, current_item=2)'

        # If this fails, either the number of steps changed, or context wasn't computed every step
        assert len(contex_data_capture) == 3

    @pytest.mark.asyncio
    async def test_context_value_computer_adds_value_to_context(self):
        data_capture: dict[int, str] = {}

        def step_action(item, ctx: StepContext):
            data_capture[item] = ctx.get_value('test')

        class TestCVC(ContextValueComputer[int]):
            def compute_next_value(self, next_item: int, current_item: int, current_value):
                return f'{current_value} : (next_item={next_item}, current_item={current_item})'

            def compute_initial_value(self, item: int):
                return f'{item}'

        await (
            _create_traversal()
            .add_context_value_computer(TestCVC('test'))
            .add_step_action(step_action)
            .add_stop_condition(lambda item, _: item == 2)
            .run(1)
        )

        assert data_capture[1] == '1'
        assert data_capture[2] == '1 : (next_item=2, current_item=1)'

    @pytest.mark.asyncio
    async def test_start_items(self):
        steps: dict[int, StepContext] = {}

        def step_action(item, ctx: StepContext):
            steps[item] = ctx

        traversal = (
            _create_traversal()
            .add_start_item(1)
            .add_start_item(-1)
            .add_stop_condition(lambda item, _: abs(item) == 2)
            .add_step_action(step_action)
        )

        assert traversal.start_items == deque([1, -1])
        await traversal.run()

        for key, expected in ((1, True), (-1, True), (2, False), (-2, False)):
            assert steps[key].is_start_item == expected

    @pytest.mark.asyncio
    async def test_only_visits_items_that_can_be_visited(self):
        steps = []

        await (
            _create_traversal(can_visit_item=lambda item, _: item < 0)
            .add_stop_condition(lambda item, _: item == -2)
            .add_step_action(lambda item, _: steps.append(item))
            .add_start_item(1)
            .add_start_item(-1)
            .run()
        )

        assert steps == [-1, -2]

    @pytest.mark.asyncio
    async def test_only_actions_items_that_can_be_actioned(self):
        steps = []

        await (
            _create_traversal(can_action_item=lambda item, _: item % 2 == 1)
            .add_stop_condition(lambda item, _: item == 3)
            .add_step_action(lambda item, _: steps.append(item))
            .run(1)
        )

        assert steps == [1, 3]

    @pytest.mark.asyncio
    async def test_can_be_rerun(self):
        steps: dict[int, int] = {}

        def step_action(item, _):
            steps[item] = steps.get(item, 0) + 1

        reset_called = []
        traversal = (
            _create_traversal(on_reset=lambda: reset_called.append(True))
            .add_stop_condition(lambda item, _: item == 2)
            .add_step_action(step_action)
        )

        await traversal.run(1)
        await traversal.run(2)

        assert steps[1] == 1
        assert steps[2] == 2
        assert all(reset_called)

    @pytest.mark.asyncio
    async def test_supports_branching_traversals(self):
        steps: dict[int, StepContext] = {}

        def step_action(item, ctx):
            steps[item] = ctx

        trace = (
            _create_branching_traversal()
            .add_queue_condition(lambda item, ctx, x, y: (ctx.branch_depth <= 1) and (item != 0))
            .add_step_action(step_action)
        )
        await trace.run(0, can_stop_on_start_item=False)

        assert not steps[0].is_branch_start_item
        assert steps[0].is_start_item
        assert steps[0].branch_depth == 0

        assert steps[10].is_branch_start_item
        assert steps[10].branch_depth == 1

        assert not steps[1].is_branch_start_item
        assert not steps[1].is_start_item
        assert steps[1].branch_depth == 1

        assert steps[-10].is_branch_start_item
        assert steps[-10].branch_depth == 1

        assert not steps[-1].is_branch_start_item
        assert not steps[-1].is_start_item
        assert steps[-1].branch_depth == 1

    @pytest.mark.asyncio
    async def test_can_stop_on_start_item_is_not_assessed_on_branch_start_items(self):
        stop_condition_triggered = []

        def stop_condition(item: int, context):
            if abs(item) == 10:
                stop_condition_triggered.append(True)
                return stop_condition_triggered

        await (
            _create_branching_traversal()
            .add_stop_condition(stop_condition)
            .add_queue_condition(lambda x, ctx, y, z: ctx.branch_depth < 2)
            .add_start_item(1)
            .add_start_item(-1)
        ).run(can_stop_on_start_item=False)

        assert all(stop_condition_triggered)

    @pytest.mark.asyncio
    async def test_start_items_are_queued_before_traversal_starts_so_queue_type_is_honoured_for_start_items(self):
        steps = []
        await (
            _create_traversal(queue=TraversalQueue.breadth_first())
            .add_stop_condition(lambda item, x: item >= 2 or item <= -2)
            .add_step_action(lambda item, x: steps.append(item))
            .add_start_item(-1)
            .add_start_item(1)
        ).run()

        assert steps == [-1, 1, -2, 2]

    @pytest.mark.asyncio
    async def test_multiple_start_items_respect_can_stop_on_start(self):
        steps = []
        traversal = (
            _create_traversal(queue=TraversalQueue.breadth_first())
            .add_stop_condition(lambda item, x: True)
            .add_step_action(lambda item, x: steps.append(item))
            .add_start_item(1)
            .add_start_item(11)
        )
        await traversal.run(can_stop_on_start_item=False)

        assert steps == [1, 11, 2, 12]
