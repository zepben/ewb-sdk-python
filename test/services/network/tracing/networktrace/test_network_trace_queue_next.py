#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import TypeVar, List
from unittest.mock import MagicMock

import pytest

from services.network.tracing.networktrace.util import mock_nts_path, mock_nts, mock_ctx
from zepben.ewb import ComputeData, NetworkTraceStep, ngen, NetworkStateOperators
from zepben.ewb.services.network.tracing.networktrace.network_trace_queue_next import NetworkTraceQueueNext

T = TypeVar('T')


class Queuer:
    def __init__(self):
        self.queued: List[NetworkTraceStep[T]] = []

    def __call__(self, step: NetworkTraceStep[T]) -> bool:
        try:
            self.queued.append(step)
            return True
        except:
            return False


class TestNetworkTraceQueueNext:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.state_operators = MagicMock(NetworkStateOperators)
        self.data_computer = MagicMock(ComputeData)
        self.queuer = Queuer()
        self.branching_queuer = Queuer()
        yield

    def test_queues_next_basic(self):
        queue_next = NetworkTraceQueueNext.Basic(self.state_operators, self.data_computer)

        seed_path = mock_nts_path()
        seed_step = mock_nts(seed_path, 3, 1)
        seed_step.configure_mock(
            num_terminal_steps=3,
            num_equipment_steps=1,
            path = seed_path
        )


        seed_context = mock_ctx()

        next_path_1 = mock_nts_path(traced_internally=False)
        next_path_2 = mock_nts_path(traced_internally=True)

        self.state_operators.next_paths = lambda seed_path: ngen((next_path_1, next_path_2))

        def mock_computer(seed_step, seed_context, path):
            if path is next_path_1:
                return "Foo"
            elif path is next_path_2:
                return "Bar"

        self.data_computer.compute_next = mock_computer

        queue_next.accept(seed_step, seed_context, self.queuer)

        assert len(self.queuer.queued) == 2

        _assert_step_equal(self.queuer.queued[0], next_path_1, "Foo", 4, 2)
        _assert_step_equal(self.queuer.queued[1], next_path_2, "Bar", 4, 1)

    def test_calls_branching_queuer_when_queing_more_then_1_path_on_branching_queue_next(self):
        queue_next = NetworkTraceQueueNext.Branching(self.state_operators, self.data_computer)

        seed_path = mock_nts_path()
        seed_step = mock_nts(seed_path, 3, 1)

        seed_context = mock_ctx()

        next_path_1 = mock_nts_path(traced_internally=False)
        next_path_2 = mock_nts_path(traced_internally=True)

        self.state_operators.next_paths = lambda seed_path: ngen((next_path_1, next_path_2))

        def mock_computer(seed_step, seed_context, path):
            if path is next_path_1:
                return "Foo"
            elif path is next_path_2:
                return "Bar"

        self.data_computer.compute_next = mock_computer

        queue_next.accept(seed_step, seed_context, self.queuer, self.branching_queuer)

        assert len(self.queuer.queued) == 0
        assert len(self.branching_queuer.queued) == 2

        _assert_step_equal(self.branching_queuer.queued[0], next_path_1, "Foo", 4, 2)
        _assert_step_equal(self.branching_queuer.queued[1], next_path_2, "Bar", 4, 1)

    def test_calls_straight_queuer_when_queuing_a_single_path_on_branching_queue_next(self):
        queue_next = NetworkTraceQueueNext.Branching(self.state_operators, self.data_computer)

        seed_path = mock_nts_path()
        seed_step = mock_nts(seed_path, 3, 1)

        seed_context = mock_ctx()

        next_path_1 = mock_nts_path(traced_internally=False)

        self.state_operators.next_paths = lambda seed_path: ngen([next_path_1])

        def mock_computer(seed_step, seed_context, path):
            if path is next_path_1:
                return "Foo"

        self.data_computer.compute_next = mock_computer

        queue_next.accept(seed_step, seed_context, self.queuer, self.branching_queuer)

        assert len(self.queuer.queued) == 1
        assert len(self.branching_queuer.queued) == 0

        _assert_step_equal(self.queuer.queued[0], next_path_1, "Foo", 4, 2)

def _assert_step_equal(step: NetworkTraceStep, path: NetworkTraceStep.Path, data, num_term_step, num_equip_step):
    assert step.path is path
    assert step.data == data
    assert step.num_terminal_steps == num_term_step
    assert step.num_equipment_steps == num_equip_step
