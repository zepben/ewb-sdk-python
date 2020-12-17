#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from zepben.evolve import BranchRecursiveTraversal, Traversal, FifoQueue, LifoQueue
from typing import List, Optional, Set


async def validate_run(t: Traversal, visit_order: List[int], expected_order: List[int], can_stop_on_start=True, check_visited=True):
    # clean slate each run
    t.reset()
    visit_order.clear()
    await t.trace(can_stop_on_start_item=can_stop_on_start)
    for i, x in enumerate(expected_order):
        assert visit_order[i] == x
        if check_visited:
            assert t.tracker.has_visited(x)


async def _validate_can_stop(t: Traversal, visit_order: List[int], expected_order: List[int], stop_count=None, check_visited=True):
    await validate_run(t, visit_order=visit_order, expected_order=expected_order, can_stop_on_start=False, check_visited=check_visited)
    if stop_count is not None:
        assert stop_count == len(visit_order)
    await validate_run(t, visit_order=visit_order, expected_order=[expected_order[0]], can_stop_on_start=True, check_visited=check_visited)
    if stop_count is not None:
        assert stop_count == len(visit_order) - 1


def queue_next(item: int, exclude=None):
    return filter(lambda x: x > 0 and x not in exclude, [item - 2, item - 1, item + 1, item + 2])


class TestTracing(object):

    @pytest.mark.asyncio
    async def test_breadth_first(self):
        expected_order = [1, 2, 3, 4, 5, 6, 7]
        visit_order = []

        async def cond(i):
            return i >= 6

        async def action(i, s):
            visit_order.append(i)

        t = Traversal(queue_next=queue_next, start_item=1, process_queue=FifoQueue(), stop_conditions=[cond], step_actions=[action])

        await validate_run(t, can_stop_on_start=True, visit_order=visit_order, expected_order=expected_order)

    @pytest.mark.asyncio
    async def test_depth_first(self):
        expected_order = [1, 3, 5, 7, 6, 4, 2]
        visit_order = []

        async def cond(i):
            return i >= 6

        async def action(i, s):
            visit_order.append(i)

        t = Traversal(queue_next=queue_next, start_item=1, process_queue=LifoQueue(), stop_conditions=[cond], step_actions=[action])

        await validate_run(t, can_stop_on_start=True, visit_order=visit_order, expected_order=expected_order)

    @pytest.mark.asyncio
    async def test_can_stop_on_start_item(self):
        async def cond1(i):
            return i >= 0

        async def cond2(i):
            return i >= 6

        visit_order = []

        async def action(i, s):
            visit_order.append(i)

        t = Traversal(queue_next=queue_next, start_item=1, process_queue=FifoQueue(), stop_conditions=[cond1, cond2], step_actions=[action])
        await _validate_can_stop(t, visit_order=visit_order, expected_order=[1, 2, 3])
        t = Traversal(queue_next=queue_next, start_item=1, process_queue=LifoQueue(), stop_conditions=[cond1, cond2], step_actions=[action])
        await _validate_can_stop(t, visit_order=visit_order, expected_order=[1, 3, 2])

    @pytest.mark.asyncio
    async def test_stopping_to_step(self):
        visited = set()
        stopping_on = set()

        async def cond(i):
            return i >= 3

        async def action(i, s):
            visited.add(i)
            if s:
                stopping_on.add(i)

        t = Traversal(queue_next=lambda i, exc: [i + 1, i + 2], start_item=1, process_queue=LifoQueue(), stop_conditions=[cond], step_actions=[action])

        await t.trace(can_stop_on_start_item=True)
        for x in range(1, 4):
            assert x in visited
        for x in range(3, 4):
            assert x in stopping_on


def queue_next_br(item: int, traversal: BranchRecursiveTraversal, exclude: Optional[Set[int]] = None):
    if item == 0:
        branch = traversal.create_branch()
        branch.start_item = 1
        traversal.branch_queue.put(branch)
        branch = traversal.create_branch()
        branch.start_item = 3
        traversal.branch_queue.put(branch)
    elif item == 1 or item == 3:
        if traversal.tracker.has_visited(2):
            traversal.process_queue.put(0)
        else:
            traversal.process_queue.put(2)
    elif item == 2:
        if traversal.tracker.has_visited(1):
            traversal.process_queue.put(3)
        elif traversal.tracker.has_visited(3):
            traversal.process_queue.put(1)


class TestBranchRecursiveTraversal(object):

    @pytest.mark.asyncio
    async def test_simple(self):
        visited = list()

        async def action(i, s):
            visited.append(i)

        self.stop_count = 0

        async def cond(i):
            self.stop_count += 1
            return False

        t = BranchRecursiveTraversal(start_item=0, queue_next=queue_next_br, process_queue=LifoQueue(), branch_queue=FifoQueue(), step_actions=[action],
                                     stop_conditions=[cond])
        await validate_run(t, visited, [0, 1, 2, 3, 3, 2, 1], check_visited=False)
        assert self.stop_count == len(visited)

    @pytest.mark.asyncio
    async def test_stop_first_asset(self):
        visited = list()

        async def action(i, s):
            visited.append(i)

        self.stop_count = 0

        async def cond1(i):
            self.stop_count += 1
            return False

        async def cond2(i):
            return i == 0

        t = BranchRecursiveTraversal(start_item=0, queue_next=queue_next_br, process_queue=LifoQueue(), branch_queue=FifoQueue(), step_actions=[action],
                                     stop_conditions=[cond1, cond2])
        await _validate_can_stop(t, visited, [0, 1, 2, 3, 3, 2, 1], check_visited=False)
