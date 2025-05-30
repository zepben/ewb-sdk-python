#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Tuple
from unittest.mock import MagicMock

import pytest

from zepben.evolve import NetworkStateOperators, FeederDirection, NetworkTraceStep, Terminal, Junction
from services.network.test_data.cuts_and_clamps_network import CutsAndClampsNetwork
from zepben.evolve.services.network.tracing.networktrace.conditions.direction_condition import DirectionCondition


class TestDirectionCondition:

    def test_should_queue_for_non_cut_or_clamp_path(self):
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

    def test_should_queue_start_item_for_non_cut_or_clamp(self):
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

    @pytest.mark.asyncio
    async def test_cuts_queue_when_direction_set_from_segment_end(self):
        network = await CutsAndClampsNetwork.multi_cut_and_clamp_network() \
                  .add_feeder('b0', 2) \
                  .build()

        c1 = network['c1']
        cut1 = network['c1-cut1']
        c4 = network['c4']
        c5 = network['c5']

        _should_queue((FeederDirection.DOWNSTREAM, NetworkTraceStep.Path(cut1[1], cut1[2])), True)
        _should_queue((FeederDirection.DOWNSTREAM, NetworkTraceStep.Path(cut1[1], cut1[1])), True)
        _should_queue((FeederDirection.DOWNSTREAM, NetworkTraceStep.Path(cut1[2], cut1[2])), True)
        _should_queue((FeederDirection.DOWNSTREAM, NetworkTraceStep.Path(c1[1], cut1[1])), True)

        _should_queue((FeederDirection.DOWNSTREAM, NetworkTraceStep.Path(cut1[1], cut1[1])), True)
        _should_queue((FeederDirection.DOWNSTREAM, NetworkTraceStep.Path(cut1[2], cut1[2])), True)
        _should_queue((FeederDirection.DOWNSTREAM, NetworkTraceStep.Path(cut1[2], cut1[1])), True)
        _should_queue((FeederDirection.DOWNSTREAM, NetworkTraceStep.Path(c4[1], cut1[1])), True)
        _should_queue((FeederDirection.DOWNSTREAM, NetworkTraceStep.Path(c5[1], cut1[2])), True)

    @pytest.mark.asyncio
    async def test_cuts_queue_when_direction_set_from_clamp(self):
        network = await CutsAndClampsNetwork.multi_cut_and_clamp_network() \
            .add_feeder('c3', 1) \
            .build()

        c1 = network['c1']
        clamp1 = network['c1-clamp1']
        cut1 = network['c1-cut1']
        c4 = network['c4']
        c5 = network['c5']

        _should_queue((FeederDirection.DOWNSTREAM, NetworkTraceStep.Path(cut1[1], cut1[1])), True)
        _should_queue((FeederDirection.DOWNSTREAM, NetworkTraceStep.Path(cut1[2], cut1[2])), True)
        _should_queue((FeederDirection.DOWNSTREAM, NetworkTraceStep.Path(cut1[1], cut1[2])), True)
        _should_queue((FeederDirection.DOWNSTREAM, NetworkTraceStep.Path(clamp1[1], cut1[1], c1)), True)

        _should_queue((FeederDirection.UPSTREAM, NetworkTraceStep.Path(cut1[1], cut1[1])), True)
        _should_queue((FeederDirection.UPSTREAM, NetworkTraceStep.Path(cut1[2], cut1[2])), False)
        _should_queue((FeederDirection.UPSTREAM, NetworkTraceStep.Path(cut1[2], cut1[1])), True)
        _should_queue((FeederDirection.UPSTREAM, NetworkTraceStep.Path(c5[1], cut1[2])), True)
        _should_queue((FeederDirection.UPSTREAM, NetworkTraceStep.Path(c4[1], cut1[1])), True)

    @pytest.mark.asyncio
    async def test_cuts_queue_when_direction_set_from_cut(self):
        network = await CutsAndClampsNetwork.multi_cut_and_clamp_network() \
            .add_feeder('c4', 1) \
            .build()

        cut1 = network['c1-cut1']
        c4 = network['c4']
        c5 = network['c5']

        _should_queue((FeederDirection.DOWNSTREAM, NetworkTraceStep.Path(cut1[1], cut1[1])), True)
        _should_queue((FeederDirection.DOWNSTREAM, NetworkTraceStep.Path(cut1[2], cut1[2])), True)
        _should_queue((FeederDirection.DOWNSTREAM, NetworkTraceStep.Path(cut1[1], cut1[2])), True)
        _should_queue((FeederDirection.DOWNSTREAM, NetworkTraceStep.Path(c4[1], cut1[1])), True)

        _should_queue((FeederDirection.UPSTREAM, NetworkTraceStep.Path(cut1[1], cut1[1])), True)
        _should_queue((FeederDirection.UPSTREAM, NetworkTraceStep.Path(cut1[2], cut1[2])), False)
        _should_queue((FeederDirection.UPSTREAM, NetworkTraceStep.Path(cut1[2], cut1[1])), True)
        _should_queue((FeederDirection.UPSTREAM, NetworkTraceStep.Path(c5[1], cut1[2])), True)

    def test_does_not_support_connector_conditions(self):
        with pytest.raises(ValueError):
            DirectionCondition(FeederDirection.CONNECTOR, NetworkStateOperators.NORMAL)

def _terminal_should_queue(condition: Tuple[FeederDirection, FeederDirection, bool], expected):
    direction, to_direction, traced_internally = condition

    next_path = MagicMock(spec=NetworkTraceStep.Path)()
    next_path.traced_internally = traced_internally
    next_path.to_terminal = Terminal()
    next_path.to_equipment = Junction()
    next_path.did_traverse_ac_line_segment = False

    next_item = NetworkTraceStep(next_path, 0, 0, None)

    state_operators = MagicMock(NetworkStateOperators.NORMAL)
    state_operators.get_direction = lambda t: to_direction

    result = DirectionCondition(direction, state_operators).should_queue(next_item, None, None, None)
    assert result == expected

def _start_terminal_should_queue(condition: Tuple[FeederDirection, FeederDirection], expected):
    direction, to_direction = condition

    next_path = MagicMock(spec=NetworkTraceStep.Path)
    next_path.configure_mock(
        to_terminal=Terminal(),
        to_equipment=Junction()
    )
    next_path.to_terminal = Terminal()
    next_path.to_equipment = Junction()
    next_path.did_traverse_ac_line_segment = False

    next_item = NetworkTraceStep(next_path, 0, 0, None)

    state_operators = MagicMock(NetworkStateOperators.NORMAL)
    state_operators.get_direction = lambda t: to_direction

    result = DirectionCondition(direction, state_operators).should_queue_start_item(next_item)
    assert result == expected

def _should_queue(condition: Tuple[FeederDirection, NetworkTraceStep.Path], expected: bool):
    direction, path = condition
    next_step = MagicMock(spec=NetworkTraceStep)
    next_step.configure_mock(
        path=path
    )
    should_queue = DirectionCondition(direction, NetworkStateOperators.NORMAL).should_queue(next_step, None, None, None)
    print(f'direction: {direction}')
    print(f'path:  internal: {path.traced_internally}\n  from: {path.from_terminal}\n  to:  {path.to_terminal}\n')
    assert should_queue == expected
