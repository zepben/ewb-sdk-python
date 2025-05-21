#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import sys

import pytest

from services.network.tracing.networktrace.test_network_trace_step_path_provider import PathTerminal, _verify_paths
from zepben.evolve import AcLineSegment, Clamp, Terminal, NetworkTraceStep, Cut
from zepben.evolve.services.network.tracing.networktrace.tracing import Tracing
from zepben.evolve.testing.test_network_builder import TestNetworkBuilder

Terminal.__add__ = PathTerminal.__add__
Terminal.__sub__ = PathTerminal.__sub__


class TestNetworkTrace:

    @pytest.mark.asyncio
    async def test_add_start_clamp_terminal_as_traversed_segment_path(self):
        trace = Tracing.network_trace()
        segment = AcLineSegment()
        clamp = Clamp().add_terminal(Terminal())
        segment.add_clamp(clamp)

        trace.add_start_item(clamp[1])
        assert trace.start_items[0].path == clamp[1] - clamp[1]

    @pytest.mark.asyncio
    def test_adds_start_whole_clamp_as_not_traversed_segment_path(self):
        trace = Tracing.network_trace()
        segment = AcLineSegment()
        clamp = Clamp().add_terminal(Terminal())
        segment.add_clamp(clamp)

        trace.add_start_item(clamp)
        _verify_paths((trace.start_items[0].path, ), (clamp[1] + clamp[1], ))

    @pytest.mark.asyncio
    def test_adds_start_AcLineSegment_terminals_cut_terminals_and_clamp_terminals_as_traversed_segment(self):
        trace = Tracing.network_trace()
        segment = AcLineSegment() \
            .add_terminal(Terminal()) \
            .add_terminal(Terminal())

        clamp1 = Clamp() \
            .add_terminal(Terminal())
        segment.add_clamp(clamp1)

        clamp2 = Clamp() \
            .add_terminal(Terminal())
        segment.add_clamp(clamp2)

        cut1 = Cut() \
            .add_terminal(Terminal()) \
            .add_terminal(Terminal())
        segment.add_cut(cut1)

        cut2 = Cut() \
            .add_terminal(Terminal()) \
            .add_terminal(Terminal())
        segment.add_cut(cut2)

        trace.add_start_item(segment)

        _verify_paths((it.path for it in trace.start_items), (
            segment[1] - segment[1],
            segment[2] - segment[2],
            clamp1[1] - clamp1[1],
            clamp2[1] - clamp2[1],
            cut1[1] - cut1[1],
            cut1[2] - cut1[2],
            cut2[1] - cut2[1],
            cut2[2] - cut2[2]))

    @pytest.mark.skip()
    @pytest.mark.asyncio
    async def test_can_run_large_branching_traces(self):
        try:
            sys.setrecursionlimit(100000)  # need to bump this for this test, we're going 1000+ recursive calls deep

            builder = TestNetworkBuilder()
            network = builder.network

            builder.from_junction(num_terminals=1) \
                   .to_acls()

            for i in range(1000):
                builder.to_junction(mrid=f'junc-{i}', num_terminals=3) \
                       .to_acls(mrid=f'acls-{i}-top') \
                       .from_acls(mrid=f'acls-{i}-bottom') \
                       .connect(f'junc-{i}', f'acls-{i}-bottom', 2, 1)

            await Tracing.network_trace_branching().run(network['j0'].get_terminal_by_sn(1))

        except Exception as e:
            sys.setrecursionlimit(1000)  # back to default
            raise e
