#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List, Callable, Awaitable

import pytest

from zepben.evolve import BasicTraversal, breadth_first, Traversal


def _queue_next(i: int, t: BasicTraversal[int]):
    for n in [i - 2, i - 1, i + 1, i + 2]:
        if n > 0:
            t.process_queue.put(n)


def _geq(n: int) -> Callable[[int], Awaitable[bool]]:
    async def compare(i: int):
        return i >= n

    return compare


def _append_to(a: List) -> Callable[[int, bool], Awaitable[None]]:
    async def append(i: int, _: bool):
        a.append(i)

    return append


@pytest.mark.asyncio
async def test_breadth_first():
    expected_order = [1, 2, 3, 4, 5, 6, 7]
    visit_order = []

    # noinspection PyArgumentList
    t = BasicTraversal(queue_next=_queue_next, process_queue=breadth_first(), stop_conditions=[_geq(6)],
                       step_actions=[_append_to(visit_order)])

    await _validate_run(t, True, visit_order, expected_order)


@pytest.mark.asyncio
async def test_depth_first():
    expected_order = [1, 3, 5, 7, 6, 4, 2]
    visit_order = []

    # noinspection PyArgumentList
    t = BasicTraversal(queue_next=_queue_next, stop_conditions=[_geq(6)], step_actions=[_append_to(visit_order)])

    await _validate_run(t, True, visit_order, expected_order)


# noinspection PyArgumentList
@pytest.mark.asyncio
async def test_can_control_stopping_on_first_asset():
    await _validate_stopping_on_first_asset(BasicTraversal(queue_next=_queue_next, process_queue=breadth_first()), [1, 2, 3])
    await _validate_stopping_on_first_asset(BasicTraversal(queue_next=_queue_next), [1, 3, 2])


@pytest.mark.asyncio
async def test_passes_stopping_to_step():
    def queue_next_greater(i: int, t: BasicTraversal[int]):
        t.process_queue.put(i + 1)
        t.process_queue.put(i + 2)

    visited = set()
    stopping_on = set()

    async def update_sets(i: int, stopping: bool):
        visited.add(i)
        if stopping:
            stopping_on.add(i)

    # noinspection PyArgumentList
    t = BasicTraversal(queue_next=queue_next_greater, stop_conditions=[_geq(3)],
                       step_actions=[update_sets])

    await t.run(1, True)
    assert visited == {1, 2, 3, 4}
    assert stopping_on == {3, 4}


@pytest.mark.asyncio
async def test_runs_all_stop_checks():
    stop_calls = [0, 0, 0]

    async def queue_nothing(_: int, _2: bool):
        pass

    def set_and_stop(stop_calls_i: int):
        async def stop_condition(i: int):
            stop_calls[stop_calls_i] = i
            return True

        return stop_condition

    # noinspection PyArgumentList
    await BasicTraversal(queue_next=queue_nothing, stop_conditions=[set_and_stop(i) for i in range(3)]).run(1, True)

    assert stop_calls == [1, 1, 1]


@pytest.mark.asyncio
async def test_runs_all_step_actions():
    step_calls = [0, 0, 0]

    async def queue_nothing(_: int, _2: bool):
        pass

    def set_step_call(stop_calls_i: int):
        async def step_action(i: int, _: bool):
            step_calls[stop_calls_i] = i

        return step_action

    # noinspection PyArgumentList
    await BasicTraversal(queue_next=queue_nothing, step_actions=[set_step_call(i) for i in range(3)]).run(1, True)

    assert step_calls == [1, 1, 1]


@pytest.mark.asyncio
async def test_stop_checking_actions_are_triggered_correctly():
    # We do not bother with the queue next as we will just prime the queue with what we want to test.
    async def queue_nothing(_: int, _2: bool):
        pass

    stepped_on = set()
    not_stopping_on = set()
    stopping_on = set()

    # noinspection PyArgumentList
    t = BasicTraversal(queue_next=queue_nothing)

    async def stop_on(item: int) -> bool:
        return item >= 3

    async def on_step(item: int, _: bool):
        stepped_on.add(item)

    async def on_not_stopping(item: int):
        not_stopping_on.add(item)

    async def on_stopping(item: int):
        stopping_on.add(item)

    t.add_stop_condition(stop_on)
    t.add_step_action(on_step)
    t.if_not_stopping(on_not_stopping)
    t.if_stopping(on_stopping)

    t.process_queue.extend([1, 2, 3, 4])

    await t.run()

    assert stepped_on == {1, 2, 3, 4}
    assert not_stopping_on == {1, 2}
    assert stopping_on == {3, 4}


# noinspection PyArgumentList
def test_default_fields_are_not_shared():
    async def queue_nothing(_: int, _2: bool):
        pass

    t1 = BasicTraversal(queue_next=queue_nothing)
    t2 = BasicTraversal(queue_next=queue_nothing)

    # By default, class variables are shared with instances. This makes fields with mutable types tricky to work with.
    # dataclassy.dataclass turns each default field value into a factory, eliminating this gotcha.
    assert t1.process_queue is not t2.process_queue
    assert t1.tracker is not t2.tracker


async def _validate_stopping_on_first_asset(t: BasicTraversal[int], expected_order: List[int]):
    visit_order = []

    async def append_to_visit_order(i: int, _: bool):
        visit_order.append(i)

    t.add_stop_condition(_geq(0))
    t.add_stop_condition(_geq(6))
    t.add_step_action(append_to_visit_order)

    await _validate_run(t, False, visit_order, expected_order)

    t.reset()
    visit_order.clear()

    await _validate_run(t, True, visit_order, [1])


async def _validate_run(t: Traversal[int], can_stop_on_start: bool, visit_order: List[int], expected_order: List[int]):
    await t.run(1, can_stop_on_start)
    assert visit_order == expected_order
    for n in expected_order:
        assert t.tracker.has_visited(n), f"traversal did not visit {n}, according to its tracker."
