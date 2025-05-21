#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Tuple
from unittest.mock import MagicMock

from zepben.evolve import FeederDirection, NetworkTraceStep, Terminal, Junction, NetworkStateOperators
from zepben.evolve.services.network.tracing.networktrace.conditions.direction_condition import DirectionCondition


class TestDirectionCondition:
    def test_should_queue(self):
        traced_internally = True
        _terminal_should_queue((FeederDirection.NONE, FeederDirection.NONE, traced_internally), True)
        _terminal_should_queue((FeederDirection.NONE, FeederDirection.UPSTREAM, traced_internally), False)
        _terminal_should_queue((FeederDirection.NONE, FeederDirection.DOWNSTREAM, traced_internally), False)
        _terminal_should_queue((FeederDirection.NONE, FeederDirection.BOTH, traced_internally), False)
        _terminal_should_queue((FeederDirection.NONE, FeederDirection.CONNECTOR, traced_internally), False)

        _terminal_should_queue((FeederDirection.UPSTREAM, FeederDirection.NONE, traced_internally), False)
        _terminal_should_queue((FeederDirection.UPSTREAM, FeederDirection.UPSTREAM, traced_internally), True)
        _terminal_should_queue((FeederDirection.UPSTREAM, FeederDirection.DOWNSTREAM, traced_internally), False)
        _terminal_should_queue((FeederDirection.UPSTREAM, FeederDirection.BOTH, traced_internally), True)
        _terminal_should_queue((FeederDirection.UPSTREAM, FeederDirection.CONNECTOR, traced_internally), True)

        _terminal_should_queue((FeederDirection.DOWNSTREAM, FeederDirection.NONE, traced_internally), False)
        _terminal_should_queue((FeederDirection.DOWNSTREAM, FeederDirection.UPSTREAM, traced_internally), False)
        _terminal_should_queue((FeederDirection.DOWNSTREAM, FeederDirection.DOWNSTREAM, traced_internally), True)
        _terminal_should_queue((FeederDirection.DOWNSTREAM, FeederDirection.BOTH, traced_internally), True)
        _terminal_should_queue((FeederDirection.DOWNSTREAM, FeederDirection.CONNECTOR, traced_internally), True)

        _terminal_should_queue((FeederDirection.BOTH, FeederDirection.NONE, traced_internally), False)
        _terminal_should_queue((FeederDirection.BOTH, FeederDirection.UPSTREAM, traced_internally), False)
        _terminal_should_queue((FeederDirection.BOTH, FeederDirection.DOWNSTREAM, traced_internally), False)
        _terminal_should_queue((FeederDirection.BOTH, FeederDirection.BOTH, traced_internally), True)
        _terminal_should_queue((FeederDirection.BOTH, FeederDirection.CONNECTOR, traced_internally), True)

        traced_internally = False
        _terminal_should_queue((FeederDirection.NONE, FeederDirection.UPSTREAM, traced_internally), False)
        _terminal_should_queue((FeederDirection.NONE, FeederDirection.DOWNSTREAM, traced_internally), False)
        _terminal_should_queue((FeederDirection.NONE, FeederDirection.BOTH, traced_internally), False)
        _terminal_should_queue((FeederDirection.NONE, FeederDirection.NONE, traced_internally), True)
        _terminal_should_queue((FeederDirection.NONE, FeederDirection.CONNECTOR, traced_internally), False)

        _terminal_should_queue((FeederDirection.UPSTREAM, FeederDirection.NONE, traced_internally), False)
        _terminal_should_queue((FeederDirection.UPSTREAM, FeederDirection.UPSTREAM, traced_internally), False)
        _terminal_should_queue((FeederDirection.UPSTREAM, FeederDirection.DOWNSTREAM, traced_internally), True)
        _terminal_should_queue((FeederDirection.UPSTREAM, FeederDirection.BOTH, traced_internally), True)
        _terminal_should_queue((FeederDirection.UPSTREAM, FeederDirection.CONNECTOR, traced_internally), True)

        _terminal_should_queue((FeederDirection.DOWNSTREAM, FeederDirection.NONE, traced_internally), False)
        _terminal_should_queue((FeederDirection.DOWNSTREAM, FeederDirection.UPSTREAM, traced_internally), True)
        _terminal_should_queue((FeederDirection.DOWNSTREAM, FeederDirection.DOWNSTREAM, traced_internally), False)
        _terminal_should_queue((FeederDirection.DOWNSTREAM, FeederDirection.BOTH, traced_internally), True)
        _terminal_should_queue((FeederDirection.DOWNSTREAM, FeederDirection.CONNECTOR, traced_internally), True)

        _terminal_should_queue((FeederDirection.BOTH, FeederDirection.UPSTREAM, traced_internally), False)
        _terminal_should_queue((FeederDirection.BOTH, FeederDirection.DOWNSTREAM, traced_internally), False)
        _terminal_should_queue((FeederDirection.BOTH, FeederDirection.BOTH, traced_internally), True)
        _terminal_should_queue((FeederDirection.BOTH, FeederDirection.NONE, traced_internally), False)
        _terminal_should_queue((FeederDirection.BOTH, FeederDirection.CONNECTOR, traced_internally), True)

    def test_should_queue_start_item(self):
        _start_terminal_should_queue((FeederDirection.NONE, FeederDirection.NONE), True)
        _start_terminal_should_queue((FeederDirection.NONE, FeederDirection.UPSTREAM), False)
        _start_terminal_should_queue((FeederDirection.NONE, FeederDirection.DOWNSTREAM), False)
        _start_terminal_should_queue((FeederDirection.NONE, FeederDirection.BOTH), False)
        _start_terminal_should_queue((FeederDirection.NONE, FeederDirection.CONNECTOR), False)

        _start_terminal_should_queue((FeederDirection.UPSTREAM, FeederDirection.NONE), False)
        _start_terminal_should_queue((FeederDirection.UPSTREAM, FeederDirection.UPSTREAM), True)
        _start_terminal_should_queue((FeederDirection.UPSTREAM, FeederDirection.DOWNSTREAM), False)
        _start_terminal_should_queue((FeederDirection.UPSTREAM, FeederDirection.BOTH), True)
        _start_terminal_should_queue((FeederDirection.UPSTREAM, FeederDirection.CONNECTOR), True)

        _start_terminal_should_queue((FeederDirection.DOWNSTREAM, FeederDirection.NONE), False)
        _start_terminal_should_queue((FeederDirection.DOWNSTREAM, FeederDirection.UPSTREAM), False)
        _start_terminal_should_queue((FeederDirection.DOWNSTREAM, FeederDirection.DOWNSTREAM), True)
        _start_terminal_should_queue((FeederDirection.DOWNSTREAM, FeederDirection.BOTH), True)
        _start_terminal_should_queue((FeederDirection.DOWNSTREAM, FeederDirection.CONNECTOR), True)

        _start_terminal_should_queue((FeederDirection.BOTH, FeederDirection.NONE), False)
        _start_terminal_should_queue((FeederDirection.BOTH, FeederDirection.UPSTREAM), False)
        _start_terminal_should_queue((FeederDirection.BOTH, FeederDirection.DOWNSTREAM), False)
        _start_terminal_should_queue((FeederDirection.BOTH, FeederDirection.BOTH), True)
        _start_terminal_should_queue((FeederDirection.BOTH, FeederDirection.CONNECTOR), True)

def _terminal_should_queue(condition: Tuple[FeederDirection, FeederDirection, bool], expected):
    direction, to_direction, traced_internally = condition

    next_path = MagicMock(spec=NetworkTraceStep.Path)()
    next_path.traced_internally = traced_internally
    next_path.to_terminal = Terminal()
    next_path.to_equipment = Junction()
    next_path.did_traverse_ac_line_segment = False

    next_item = NetworkTraceStep(next_path, 0, 0, None)

    state_operators = NetworkStateOperators
    state_operators.get_direction = lambda t: to_direction

    result = DirectionCondition(direction, state_operators).should_queue(next_item, None, None, None)
    assert result == expected

def _start_terminal_should_queue(condition: Tuple[FeederDirection, FeederDirection], expected):
    direction, to_direction = condition

    next_path = MagicMock(spec=NetworkTraceStep.Path)()
    next_path.to_terminal = Terminal()
    next_path.to_equipment = Junction()
    next_path.did_traverse_ac_line_segment = False

    next_item = NetworkTraceStep(next_path, 0, 0, None)

    state_operators = NetworkStateOperators
    state_operators.get_direction = lambda t: to_direction

    result = DirectionCondition(direction, state_operators).should_queue_start_item(next_item)
    assert result == expected
