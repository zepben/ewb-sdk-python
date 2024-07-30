#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

import pytest

from zepben.evolve import BranchRecursiveTraversal, breadth_first


class TestBranchRecursiveTraversal:

    _visit_order: List[int]
    _stop_count: int
    _traversal: BranchRecursiveTraversal[int]

    @pytest.fixture(autouse=True)
    def before_each(self):
        self._visit_order = []
        self._stop_count = 0

        async def _append_to_visit_order(item: int, _: bool):
            self._visit_order.append(item)

        async def _increment_stop_count(_: int) -> bool:
            self._stop_count += 1
            return False

        # noinspection PyArgumentList
        self._traversal = BranchRecursiveTraversal(
            queue_next=_queue_next,
            branch_queue=breadth_first(),
            step_actions=[_append_to_visit_order],
            stop_conditions=[_increment_stop_count]
        )

    @pytest.mark.asyncio
    async def test_simple(self):
        await self._traversal.run(0)

        assert self._visit_order == [0, 1, 2, 3, 3, 2, 1]
        assert self._stop_count == len(self._visit_order)

    @pytest.mark.asyncio
    async def test_can_control_stopping_on_first_asset(self):
        async def eq_0(i: int):
            return i == 0

        await self._traversal.add_stop_condition(eq_0).run(0, False)

        assert self._visit_order == [0, 1, 2, 3, 3, 2, 1]


def _queue_next(item: int, traversal: BranchRecursiveTraversal[int]):
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
