#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest

from zepben.evolve import ConnectivityResult, BasicTraversal, connected_equipment, TestNetworkBuilder, connectivity_trace, connectivity_breadth_trace, \
    current_connectivity_trace, normal_connectivity_trace, AcLineSegment, Terminal, BusbarSection, NetworkService, create_connectivity_traversal, ignore_open


class TestConnectivityTrace:
    network = (
        TestNetworkBuilder()
        .from_junction()
        .to_breaker(is_normally_open=True, is_open=True)
        .to_breaker(is_normally_open=True, is_open=False)
        .to_junction()
        .to_breaker(is_normally_open=False, is_open=True)
        .to_breaker(is_normally_open=True, is_open=True)
        .to_junction()
        .network
    )
    """
    j0--b1--b2--j3--b4--b5--j6
        bo  no      co  bo

    bo = both open
    no = normally open
    co = currently open
    """

    @pytest.mark.asyncio
    async def test_connectivity_trace_ignores_open_state(self):
        await self._validate_run(connectivity_trace(), "b2", "b1", "j0", "b4", "b5", "j6")
        await self._validate_run(connectivity_breadth_trace(), "b2", "b1", "j0", "b4", "b5", "j6")

    @pytest.mark.asyncio
    async def test_normal_connected_equipment_trace_uses_open_state(self):
        await self._validate_run(normal_connectivity_trace(), "b2", "b4", "b5")

    @pytest.mark.asyncio
    async def test_current_connectivity_trace_uses_open_state(self):
        await self._validate_run(current_connectivity_trace(), "b2", "b1", "b4")

    @pytest.mark.asyncio
    async def test_doesnt_back_trace_busbars(self):
        #
        # ---- | ---- ----
        #  c1 bb1 c2   c3
        #
        c1 = AcLineSegment(mrid="c1", terminals=[Terminal()])
        c2 = AcLineSegment(mrid="c2", terminals=[Terminal(), Terminal()])
        c3 = AcLineSegment(mrid="c3", terminals=[Terminal()])
        bb1 = BusbarSection(mrid="bb1", terminals=[Terminal()])

        bb_network = NetworkService()
        bb_network.connect_terminals(bb1.get_terminal_by_sn(1), c1.get_terminal_by_sn(1))
        bb_network.connect_terminals(bb1.get_terminal_by_sn(1), c2.get_terminal_by_sn(1))
        bb_network.connect_terminals(c2.get_terminal_by_sn(2), c3.get_terminal_by_sn(1))

        t = connectivity_trace()
        t.process_queue.put(ConnectivityResult(c1.get_terminal_by_sn(1), bb1.get_terminal_by_sn(1), []))

        visited = set()

        async def step_action(cr: ConnectivityResult, _: bool):
            visited.add(cr.to_equip.mrid)

        await t.add_step_action(step_action).run()
        assert visited == {bb1.mrid, c2.mrid, c3.mrid}

    @pytest.mark.asyncio
    async def test_can_stop_on_busbars(self):
        #
        # ---- | ---- ----
        #  c1 bb1 c2   c3
        #
        c1 = AcLineSegment(mrid="c1", terminals=[Terminal()])
        c2 = AcLineSegment(mrid="c2", terminals=[Terminal(), Terminal()])
        c3 = AcLineSegment(mrid="c3", terminals=[Terminal()])
        bb1 = BusbarSection(mrid="bb1", terminals=[Terminal()])

        bb_network = NetworkService()
        bb_network.connect_terminals(bb1.get_terminal_by_sn(1), c1.get_terminal_by_sn(1))
        bb_network.connect_terminals(bb1.get_terminal_by_sn(1), c2.get_terminal_by_sn(1))
        bb_network.connect_terminals(c2.get_terminal_by_sn(2), c3.get_terminal_by_sn(1))

        t = connectivity_trace()
        t.process_queue.put(ConnectivityResult(c3.get_terminal_by_sn(1), c2.get_terminal_by_sn(2), []))

        visited = set()

        async def step_action(cr: ConnectivityResult, _: bool):
            visited.add(cr.to_equip.mrid)

        async def should_stop(cr: ConnectivityResult):
            return isinstance(cr.to_equip, BusbarSection)

        await t.add_step_action(step_action).add_stop_condition(should_stop).run()
        assert visited == {c2.mrid, bb1.mrid}

    @pytest.mark.asyncio
    async def test_can_traverse_connected_busbars(self):
        #
        #     |c1
        #     *
        #     |c2             |c3
        #  --bb1--*--bb2--*--bb3--
        #     |c4             |c5
        #
        c1 = AcLineSegment(mrid="c1", terminals=[Terminal()])
        c2 = AcLineSegment(mrid="c2", terminals=[Terminal(), Terminal()])
        c3 = AcLineSegment(mrid="c3", terminals=[Terminal()])
        c4 = AcLineSegment(mrid="c4", terminals=[Terminal()])
        c5 = AcLineSegment(mrid="c5", terminals=[Terminal()])
        bb1 = BusbarSection(mrid="bb1", terminals=[Terminal()])
        bb2 = BusbarSection(mrid="bb2", terminals=[Terminal()])
        bb3 = BusbarSection(mrid="bb3", terminals=[Terminal()])

        bb_network = NetworkService()
        bb_network.connect_terminals(c1.get_terminal_by_sn(1), c2.get_terminal_by_sn(1))
        bb_network.connect_terminals(bb1.get_terminal_by_sn(1), c2.get_terminal_by_sn(2))
        bb_network.connect_terminals(bb1.get_terminal_by_sn(1), c3.get_terminal_by_sn(1))
        bb_network.connect_terminals(bb1.get_terminal_by_sn(1), bb2.get_terminal_by_sn(1))
        bb_network.connect_terminals(bb2.get_terminal_by_sn(1), bb3.get_terminal_by_sn(1))
        bb_network.connect_terminals(bb3.get_terminal_by_sn(1), c4.get_terminal_by_sn(1))
        bb_network.connect_terminals(bb3.get_terminal_by_sn(1), c5.get_terminal_by_sn(1))

        t = connectivity_trace()
        t.process_queue.put(ConnectivityResult(c1.get_terminal_by_sn(1), c2.get_terminal_by_sn(1), []))

        visited = set()

        async def step_action(cr: ConnectivityResult, _: bool):
            visited.add(cr.to_equip.mrid)

        await t.add_step_action(step_action).run()
        assert visited == {bb1.mrid, bb2.mrid, bb3.mrid, c2.mrid, c3.mrid, c4.mrid, c5.mrid}

    def test_create_connectivity_traversal_does_not_reuse_default_queue(self):
        a = create_connectivity_traversal(ignore_open)
        b = create_connectivity_traversal(ignore_open)

        assert a.process_queue is not b.process_queue

    async def _validate_run(self, t: BasicTraversal[ConnectivityResult], *expected: str):
        visited = set()

        for conn in connected_equipment(self.network["j3"]):
            t.process_queue.put(conn)

        async def step_action(cr: ConnectivityResult, _: bool):
            visited.add(cr.to_equip.mrid)

        await t.add_step_action(step_action).run()
        assert visited == set(expected)
