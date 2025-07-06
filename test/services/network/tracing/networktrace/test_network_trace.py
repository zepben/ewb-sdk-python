#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys
import unittest
DEFAULT_RECURSION_LIMIT = sys.getrecursionlimit()

from typing import List, Set, Tuple

import pytest

from services.network.tracing.networktrace.test_network_trace_step_path_provider import PathTerminal, _verify_paths
from zepben.evolve import AcLineSegment, Clamp, Terminal, NetworkTraceStep, Cut, ConductingEquipment, TraversalQueue, Junction, ngen, NetworkTraceActionType, \
    Tracing
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
        _verify_paths(ngen([trace.start_items[0].path]), (clamp[1] + clamp[1],))

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

    @pytest.mark.asyncio
    async def test_doesnt_bypass_stop_conditions_with_multiple_branches_in_equipment_traces_loop(self):
        #
        # /--21--c1--21
        # c0          j2 21--c3--2
        # \--12--c4--13
        #
        ns = (TestNetworkBuilder()
              .from_acls()  # c0
              .to_acls()  # c1
              .to_junction(num_terminals=3)  # j2
              .branch_from('j2', 2)
              .to_acls()  # c3
              .branch_from('j2', 3)
              .to_acls()  # c4
              .connect('c4', 'c0', 2, 1)
              ).network

        stepped_on: List[str] = []
        await Tracing.network_trace() \
            .add_stop_condition(lambda step, _: step.path.to_equipment.mrid == 'j2') \
            .add_step_action(lambda step, _: stepped_on.append(step.path.to_equipment.mrid)) \
            .run(ns.get('c0', ConductingEquipment))

        assert stepped_on == ['c0', 'c1', 'j2', 'c4']

    @pytest.mark.asyncio
    async def test_breadth_first_queue_supports_multiple_start_items(self):
        #
        # 1--c1--21--c2--2
        # 2              1
        # j0             j3
        # 1              2
        # 2--c5--12--c4--1
        #
        ns = (TestNetworkBuilder()
              .from_junction()  # j0
              .to_acls()  # c1
              .to_acls()  # c2
              .to_junction()  # j3
              .to_acls()  # c4
              .to_acls()  # c5
              .connect('c5', 'j0', 2, 1)
              ).network

        steps: List[NetworkTraceStep] = []
        await Tracing.network_trace(queue=TraversalQueue.breadth_first()) \
            .add_step_action(lambda step, _: steps.append(step)) \
            .run(ns.get('j0', Junction))

        assert list(map(lambda it: (it.num_equipment_steps, it.path.to_equipment.mrid), steps)) \
               == [(0, 'j0'),
                   (1, 'c5'),
                   (1, 'c1'),
                   (2, 'c4'),
                   (2, 'c2'),
                   (3, 'j3')]

    @pytest.mark.asyncio
    async def test_can_stop_on_start_item_when_running_from_conducting_equipment(self):
        #
        # 1 b0 21--c1--2
        #
        ns = (TestNetworkBuilder()
              .from_breaker()  # b0
              .to_acls()  # c1
              ).network

        steps: List[NetworkTraceStep] = []
        await Tracing.network_trace() \
            .add_step_action(lambda step, _: steps.append(step)) \
            .add_stop_condition(lambda step, _: True) \
            .run(ns.get('b0', ConductingEquipment))

        assert list(map(lambda it: (it.num_equipment_steps, it.path.to_equipment.mrid), steps)) \
               == [(0, 'b0')]

    @pytest.mark.asyncio
    async def test_can_stop_on_start_item_when_running_from_conducting_equipment_branching(self):
        return
        #
        # 1 b0 21--c1--2
        #      1
        #       \--c2--2
        #
        ns = (TestNetworkBuilder()
              .from_breaker()  # b0
              .to_acls()  # c1
              .branch_from('b0')
              .to_acls()  # c2
              ).network

        steps: Set[NetworkTraceStep] = set()
        await Tracing.network_trace_branching() \
            .add_step_action(lambda step, _: steps.add(step)) \
            .add_stop_condition(lambda step, _: True) \
            .run(ns.get('b0', ConductingEquipment))

        assert set(map(lambda it: (it.num_equipment_steps, it.path.to_equipment.mrid), steps)) \
               == {(0, 'b0')}

    if 'TOX_ENV_NAME' not in os.environ:  # Skips the test during tox runs as variable hardware will affect speed
        @pytest.mark.asyncio
        #todo
        @unittest.skip("why did this stack overflow with the extra stack size?")
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

    @pytest.mark.asyncio
    async def test_multiple_start_items_can_stop_on_start_doesnt_prevent_stop_checks_when_visiting_via_loop(self):
        ns = (TestNetworkBuilder()
              .from_acls()  # c0
              .to_acls()  # c1
              .to_acls()  # c2
              .connect_to('c0')
              ).network

        stop_checks: List[str] = []
        steps: List[str] = []

        def stop_condition(item, _):
            stop_checks.append(item.path.to_terminal.mrid)
            return item.path.to_equipment.mrid == 'c1'

        trace = Tracing.network_trace(action_step_type=NetworkTraceActionType.ALL_STEPS) \
            .add_stop_condition(stop_condition) \
            .if_not_stopping(lambda item, _: steps.append(item.path.to_terminal.mrid))
        await trace.run(ns.get('c1', ConductingEquipment), can_stop_on_start_item=False)

        assert stop_checks == ['c2-t1', 'c2-t2', 'c0-t1', 'c0-t2', 'c1-t1']
        assert steps == ['c1-t2', 'c2-t1', 'c2-t2', 'c0-t1', 'c0-t2']

    @pytest.mark.asyncio
    async def test_can_provide_a_path_to_force_the_trace_to_traverse_in_a_given_direction(self):
        #
        # 1--c0--21--c1-*-21--c2--2
        #         1
        #         1--c3--2
        #

        def create_start_path(start: Tuple[str, str]):

            _from_ce = (_from := ns.get(start[0], Terminal)).conducting_equipment
            _to_ce = (_to := ns.get(start[1], Terminal)).conducting_equipment

            def traversed():
                if (_to_ce == _from_ce) and isinstance(_to_ce, AcLineSegment):
                    return _to_ce
                elif isinstance(_to_ce, Clamp) and _to_ce.ac_line_segment == _from_ce:
                    return _to_ce.ac_line_segment
                elif isinstance(_from_ce, Clamp) and _from_ce.ac_line_segment == _to_ce:
                    return _from_ce.ac_line_segment
                return None

            return NetworkTraceStep.Path(_from, _to, traversed())

        async def validate(start: Tuple[str, str], action_step_type: NetworkTraceActionType, expected: List[str]):
            stepped_on: List[NetworkTraceStep] = []

            await (Tracing.network_trace(action_step_type=action_step_type)
                   .add_step_action(lambda item, ctx: stepped_on.append(item))
                   ).run(create_start_path(start))

            assert [it.path.to_terminal.mrid for it in stepped_on] == expected

        ns = (TestNetworkBuilder()
              .from_acls()  # c0
              .to_acls()  # c1
              .with_clamp()  # c1-clamp1
              .to_acls()  # c2
              .branch_from('c1-clamp1')
              .to_acls()  # c3
              ).network

        await validate(('c0-t1', 'c0-t2'), NetworkTraceActionType.ALL_STEPS, ["c0-t2", "c1-t1", "c1-t2", "c2-t1", "c2-t2", "c1-clamp1-t1", "c3-t1", "c3-t2"])
        await validate(('c0-t2', 'c0-t1'), NetworkTraceActionType.ALL_STEPS, ["c0-t1"])
        await validate(('c1-t2', 'c2-t1'), NetworkTraceActionType.ALL_STEPS, ["c2-t1", "c2-t2"])
        await validate(('c1-t1', 'c1-clamp1-t1'), NetworkTraceActionType.ALL_STEPS, ["c1-clamp1-t1", "c3-t1", "c3-t2"])
        await validate(('c1-clamp1-t1', 'c1-t2'), NetworkTraceActionType.ALL_STEPS, ["c1-t2", "c2-t1", "c2-t2"])

        await validate(('c0-t1', 'c0-t2'), NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT, ["c0-t2", "c1-t1", "c2-t1", "c1-clamp1-t1", "c3-t1"])
        await validate(('c0-t2', 'c0-t1'), NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT, ["c0-t1"])
        await validate(('c1-t2', 'c2-t1'), NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT, ["c2-t1"])
        await validate(('c1-t1', 'c1-clamp1-t1'), NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT, ["c1-clamp1-t1", "c3-t1"])
        await validate(('c1-clamp1-t1', 'c1-t2'), NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT, ["c1-t2", "c2-t1"])

        # Can even use bizarre paths, they are just the same as any other external path.
        await validate(('c0-t1', 'c2-t1'), NetworkTraceActionType.ALL_STEPS, ["c2-t1", "c2-t2"])
        await validate(('c0-t1', 'c2-t1'), NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT, ["c2-t1"])
