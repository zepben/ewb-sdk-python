#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.ewb import TraversalQueue, WeightedPriorityQueue
from zepben.ewb.services.network.tracing.traversal.queue import LIFODeque, FIFODeque


class TestQueue:
    def test_lifo_queue(self):
        queue = TraversalQueue.depth_first()

        for i in range(10):
            queue.append(i)
        assert queue.queue == LIFODeque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        assert len(queue) == 10

        assert queue.pop() == 9

    def test_fifo_queue(self):
        queue = TraversalQueue.breadth_first()

        for i in range(10):
            queue.append(i)
        assert queue.queue == FIFODeque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        assert len(queue) == 10

        assert queue.pop() == 0

    def test_lifo_weighted_priority_queue(self):
        weight = 0

        queue = WeightedPriorityQueue(
            lambda: TraversalQueue.depth_first(),
            lambda t: weight
        )
        for i in range(4):
            queue.append(i)

        assert queue.pop() == 3
        assert queue.pop() == 2

        weight = 1

        for i in range(4):
            queue.append(i)

        assert queue.pop() == 3
        assert queue.pop() == 2
        assert queue.pop() == 1
        assert queue.pop() == 0
        assert queue.pop() == 1
        assert queue.pop() == 0

    def test_fifo_weighted_priority_queue(self):
        weight = 0

        queue = WeightedPriorityQueue(
            lambda: TraversalQueue.breadth_first(),
            lambda t: weight
        )
        for i in range(4):
            queue.append(i)

        assert queue.pop() == 0
        assert queue.pop() == 1

        weight = 1

        for i in range(4):
            queue.append(i)

        assert queue.pop() == 0
        assert queue.pop() == 1
        assert queue.pop() == 2
        assert queue.pop() == 3
        assert queue.pop() == 2
        assert queue.pop() == 3
