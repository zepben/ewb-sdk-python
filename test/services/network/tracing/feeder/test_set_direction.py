#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest

from services.network.test_data.phase_swap_loop_network import create_phase_swap_loop_network
from services.network.tracing.feeder.direction_logger import log_directions
from zepben.evolve import FeederDirection, TestNetworkBuilder, SetDirection, PhaseCode, NetworkService, Feeder, Terminal, ConductingEquipment, Substation

UPSTREAM = FeederDirection.UPSTREAM
DOWNSTREAM = FeederDirection.DOWNSTREAM
BOTH = FeederDirection.BOTH
NONE = FeederDirection.NONE


class TestSetDirection:

    @pytest.mark.asyncio
    async def test_set_direction(self):
        n = create_phase_swap_loop_network()

        await self._do_set_direction_trace(n)

        self._check_expected_direction(self._get_t(n, "ac_line_segment0", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "ac_line_segment0", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "ac_line_segment1", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "ac_line_segment4", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "node4", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "node4", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "node4", 3), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "node8", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "node5", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "node5", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "node5", 3), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "node9", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "node6", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "node6", 2), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "ac_line_segment2", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "ac_line_segment3", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "ac_line_segment9", 2), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "node2", 1), UPSTREAM)

    @pytest.mark.asyncio
    async def test_stops_at_open_points(self):
        #
        # 1--c0--21 b1 21--c2--2
        #         1 b3 21--c4--2
        #
        n = TestNetworkBuilder() \
            .from_acls() \
            .to_breaker(is_normally_open=True, is_open=False) \
            .to_acls() \
            .branch_from("c0") \
            .to_breaker(is_open=True) \
            .to_acls() \
            .network

        await SetDirection().run_terminal(self._get_t(n, "c0", 2))
        await log_directions(n["c0"])

        self._check_expected_direction(self._get_t(n, "c0", 1), NONE)
        self._check_expected_direction(self._get_t(n, "c0", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "b1", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "b1", 2), NONE, DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "c2", 1), NONE, UPSTREAM)
        self._check_expected_direction(self._get_t(n, "c2", 2), NONE, DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "b3", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "b3", 2), DOWNSTREAM, NONE)
        self._check_expected_direction(self._get_t(n, "c4", 1), UPSTREAM, NONE)
        self._check_expected_direction(self._get_t(n, "c4", 2), DOWNSTREAM, NONE)

    @pytest.mark.asyncio
    async def test_does_not_trace_through_feeder_heads(self):
        #
        # 1--c0--21 j1*21--c2--21*j3 21--c4--2
        #
        # * = feeder start
        #
        n = await TestNetworkBuilder() \
            .from_acls() \
            .to_junction() \
            .to_acls() \
            .to_junction() \
            .to_acls() \
            .add_feeder("j1", 2) \
            .add_feeder("j3", 1) \
            .build()

        await log_directions(n["c0"])

        self._check_expected_direction(self._get_t(n, "c0", 1), NONE)
        self._check_expected_direction(self._get_t(n, "c0", 2), NONE)
        self._check_expected_direction(self._get_t(n, "j1", 1), NONE)
        self._check_expected_direction(self._get_t(n, "j1", 2), BOTH)
        self._check_expected_direction(self._get_t(n, "c2", 1), BOTH)
        self._check_expected_direction(self._get_t(n, "c2", 2), BOTH)
        self._check_expected_direction(self._get_t(n, "j3", 1), BOTH)
        self._check_expected_direction(self._get_t(n, "j3", 2), NONE)
        self._check_expected_direction(self._get_t(n, "c4", 1), NONE)
        self._check_expected_direction(self._get_t(n, "c4", 2), NONE)

    @pytest.mark.asyncio
    async def test_doesnt_trace_from_open_feeder_heads(self):
        #
        # 1 b0 21--c1--21--c2--21 b3 2
        #
        n = (TestNetworkBuilder()
             .from_breaker()  # b0
             .to_acls()  # c1
             .to_acls()  # c2
             .to_breaker(is_normally_open=True)  # b3
             .add_feeder("b0", 2)
             .add_feeder("b3", 1)
             .network)

        await SetDirection().run(n)
        await log_directions(n["b0"])

        self._check_expected_direction(self._get_t(n, "b0", 1), NONE)
        self._check_expected_direction(self._get_t(n, "b0", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "c1", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "c1", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "c2", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "c2", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "b3", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "b3", 2), NONE)

    @pytest.mark.asyncio
    async def test_traces_through_non_substation_power_transformers(self):
        #
        # 1 b0*21--c1--21-tx2-21--c3--2
        #
        # * = feeder start
        #
        n = await TestNetworkBuilder() \
            .from_breaker() \
            .to_acls() \
            .to_power_transformer() \
            .to_acls() \
            .add_feeder("b0", 2) \
            .build()

        await log_directions(n["b0"])

        self._check_expected_direction(self._get_t(n, "b0", 1), NONE)
        self._check_expected_direction(self._get_t(n, "b0", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "c1", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "c1", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "tx2", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "tx2", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "c3", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "c3", 2), DOWNSTREAM)

    @pytest.mark.asyncio
    async def test_stops_at_zone_transformers_incase_feeder_heads_are_missing(self):
        #
        # 1 b0*21--c1--21 tx2 21--c3--2
        #
        # * = feeder start
        #
        n = await TestNetworkBuilder() \
            .from_breaker() \
            .to_acls() \
            .to_power_transformer(action=lambda tx: tx.add_container(Substation())) \
            .to_acls() \
            .add_feeder("b0", 2) \
            .build()

        await log_directions(n["b0"])

        self._check_expected_direction(self._get_t(n, "b0", 1), NONE)
        self._check_expected_direction(self._get_t(n, "b0", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "c1", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "c1", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "tx2", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "tx2", 2), NONE)
        self._check_expected_direction(self._get_t(n, "c3", 1), NONE)
        self._check_expected_direction(self._get_t(n, "c3", 2), NONE)

    @pytest.mark.asyncio
    async def test_set_direction_in_closed_loop(self):
        #
        # s0 11----21 j2 21----21 j4 21----21 j6 21----21 j8 2
        #       c1       1  c3          c5  2       c7
        #                |__________________|
        #                         c9
        #
        n = TestNetworkBuilder() \
            .from_source(PhaseCode.A) \
            .to_acls(PhaseCode.A) \
            .to_junction(PhaseCode.A) \
            .to_acls(PhaseCode.A) \
            .to_junction(PhaseCode.A) \
            .to_acls(PhaseCode.A) \
            .to_junction(PhaseCode.A) \
            .to_acls(PhaseCode.A) \
            .to_junction(PhaseCode.A, 1) \
            .branch_from("j2") \
            .to_acls(PhaseCode.A) \
            .connect("c9", "j6", 2, 1) \
            .add_feeder("s0") \
            .network  # Do not call build as we do not want to trace the directions yet.

        await self._do_set_direction_trace(n)

        self._check_expected_direction(self._get_t(n, "s0", 1), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "c1", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "c1", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "j2", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "j2", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "c3", 1), BOTH)
        self._check_expected_direction(self._get_t(n, "c3", 2), BOTH)
        self._check_expected_direction(self._get_t(n, "j4", 1), BOTH)
        self._check_expected_direction(self._get_t(n, "j4", 2), BOTH)
        self._check_expected_direction(self._get_t(n, "c5", 1), BOTH)
        self._check_expected_direction(self._get_t(n, "c5", 2), BOTH)
        self._check_expected_direction(self._get_t(n, "j6", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "j6", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "c7", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "c7", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "j8", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "c9", 1), BOTH)
        self._check_expected_direction(self._get_t(n, "c9", 2), BOTH)

    @pytest.mark.asyncio
    async def test_dual_path_loop_top(self):
        #
        # NOTE: This test is for checking the both setting around the loop when a completed loop via c9 and j4 is
        #       performed before the backwards path through j11.
        #

        #
        #               /-c10-21 j11 21-c12-\
        #               |                   |
        #               1                   2
        #               2                   2
        # j0 11--c1--21 j2                  j6 31--c7--21 j8
        #               32-------c9--------11
        #               1                   2
        #               |                   |
        #               \-c3--21 j4 21---c5-/
        #
        n = TestNetworkBuilder() \
            .from_junction(num_terminals=1) \
            .to_acls() \
            .to_junction(num_terminals=3) \
            .to_acls() \
            .to_junction() \
            .to_acls() \
            .to_junction(num_terminals=3) \
            .to_acls() \
            .to_junction(num_terminals=1) \
            .from_acls() \
            .from_acls() \
            .to_junction() \
            .to_acls() \
            .connect("c9", "j6", 1, 1) \
            .connect("c9", "j2", 2, 3) \
            .connect("c10", "j2", 1, 2) \
            .connect("c12", "j6", 2, 2) \
            .network

        await SetDirection().run_terminal(self._get_t(n, "j0", 1))
        await log_directions(n["j0"])

        # To avoid reprocessing all BOTH loops in larger networks we do not process anything with a direction already set. This means this test will apply
        # a standard UP/DOWN path through j2-t2 through to j6-t2 and then a BOTH loop around the c9/j4 loop which will stop the reverse UP/DOWN path
        # ever being processed from j6-t2 via j2-t3.

        self._check_expected_direction(self._get_t(n, "j0", 1), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "c1", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "c1", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "j2", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "j2", 2), DOWNSTREAM)  # Would have been BOTH if the intermediate loop was reprocessed.
        self._check_expected_direction(self._get_t(n, "j2", 3), BOTH)
        self._check_expected_direction(self._get_t(n, "c3", 1), BOTH)
        self._check_expected_direction(self._get_t(n, "c3", 2), BOTH)
        self._check_expected_direction(self._get_t(n, "j4", 1), BOTH)
        self._check_expected_direction(self._get_t(n, "j4", 2), BOTH)
        self._check_expected_direction(self._get_t(n, "c5", 1), BOTH)
        self._check_expected_direction(self._get_t(n, "c5", 2), BOTH)
        self._check_expected_direction(self._get_t(n, "j6", 1), DOWNSTREAM)  # Would have been BOTH if the intermediate loop was reprocessed.
        self._check_expected_direction(self._get_t(n, "j6", 2), UPSTREAM)  # Would have been BOTH if the intermediate loop was reprocessed.
        self._check_expected_direction(self._get_t(n, "j6", 3), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "c7", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "c7", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "j8", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "c9", 1), BOTH)
        self._check_expected_direction(self._get_t(n, "c9", 2), BOTH)
        self._check_expected_direction(self._get_t(n, "c10", 1), UPSTREAM)  # Would have been BOTH if the intermediate loop was reprocessed.
        self._check_expected_direction(self._get_t(n, "c10", 2), DOWNSTREAM)  # Would have been BOTH if the intermediate loop was reprocessed.
        self._check_expected_direction(self._get_t(n, "j11", 1), UPSTREAM)  # Would have been BOTH if the intermediate loop was reprocessed.
        self._check_expected_direction(self._get_t(n, "j11", 2), DOWNSTREAM)  # Would have been BOTH if the intermediate loop was reprocessed.
        self._check_expected_direction(self._get_t(n, "c12", 1), UPSTREAM)  # Would have been BOTH if the intermediate loop was reprocessed.
        self._check_expected_direction(self._get_t(n, "c12", 2), DOWNSTREAM)  # Would have been BOTH if the intermediate loop was reprocessed.

    @pytest.mark.asyncio
    async def test_dual_path_loop_bottom(self):
        #
        # NOTE: This test is for checking the both setting around the loop when a completed loop via c9 and j11 is
        #       performed after the backwards path through j4.
        #

        #
        #               /-c3--21 j4 21---c5-\
        #               |                   |
        #               1                   2
        #               3                   1
        # j0 11--c1--21 j2                  j6 31--c7--21 j8
        #               22-------c9--------12
        #               1                   2
        #               |                   |
        #               \-c10-21 j11 21-c12-/
        #
        n = TestNetworkBuilder() \
            .from_junction(num_terminals=1) \
            .to_acls() \
            .to_junction(num_terminals=3) \
            .to_acls() \
            .to_junction() \
            .to_acls() \
            .to_junction(num_terminals=3) \
            .to_acls() \
            .to_junction(num_terminals=1) \
            .from_acls() \
            .from_acls() \
            .to_junction() \
            .to_acls() \
            .connect("c9", "j6", 1, 2) \
            .connect("c9", "j2", 2, 2) \
            .connect("c10", "j2", 1, 2) \
            .connect("c12", "j6", 2, 2) \
            .network

        await SetDirection().run_terminal(self._get_t(n, "j0", 1))
        await log_directions(n["j0"])

        # To avoid reprocessing all BOTH loops in larger networks we do not process anything with a direction already set. This means this test will apply
        # a UP/DOWN path through j2-t2 directly into a BOTH loop around the c9/j11 loop which will stop the reverse UP/DOWN path
        # ever being processed from j6-t2 via j2-t3.

        self._check_expected_direction(self._get_t(n, "j0", 1), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "c1", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "c1", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "j2", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "j2", 2), DOWNSTREAM)  # Would have been BOTH if the intermediate loop was reprocessed.
        self._check_expected_direction(self._get_t(n, "j2", 3), BOTH)
        self._check_expected_direction(self._get_t(n, "c3", 1), BOTH)
        self._check_expected_direction(self._get_t(n, "c3", 2), BOTH)
        self._check_expected_direction(self._get_t(n, "j4", 1), BOTH)
        self._check_expected_direction(self._get_t(n, "j4", 2), BOTH)
        self._check_expected_direction(self._get_t(n, "c5", 1), BOTH)
        self._check_expected_direction(self._get_t(n, "c5", 2), BOTH)
        self._check_expected_direction(self._get_t(n, "j6", 1), BOTH)
        self._check_expected_direction(self._get_t(n, "j6", 2), BOTH)
        self._check_expected_direction(self._get_t(n, "j6", 3), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "c7", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "c7", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "j8", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "c9", 1), BOTH)
        self._check_expected_direction(self._get_t(n, "c9", 2), BOTH)
        self._check_expected_direction(self._get_t(n, "c10", 1), BOTH)
        self._check_expected_direction(self._get_t(n, "c10", 2), BOTH)
        self._check_expected_direction(self._get_t(n, "j11", 1), BOTH)
        self._check_expected_direction(self._get_t(n, "j11", 2), BOTH)
        self._check_expected_direction(self._get_t(n, "c12", 1), BOTH)
        self._check_expected_direction(self._get_t(n, "c12", 2), BOTH)

    @pytest.mark.asyncio
    async def test_ignores_phase_pathing(self):
        #
        # j0 11--c1--21--c2--2
        #
        n = TestNetworkBuilder() \
            .from_junction(num_terminals=1, nominal_phases=PhaseCode.AB) \
            .to_acls(nominal_phases=PhaseCode.B) \
            .to_acls(nominal_phases=PhaseCode.A) \
            .network

        await SetDirection().run_terminal(self._get_t(n, "j0", 1))
        await log_directions(n["j0"])

        self._check_expected_direction(self._get_t(n, "j0", 1), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "c1", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "c1", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "c2", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "c2", 2), DOWNSTREAM)

    @pytest.mark.asyncio
    async def test_works_without_phase(self):
        #
        # j0 11--c1--21--c2--2
        #
        n = TestNetworkBuilder() \
            .from_junction(num_terminals=1, nominal_phases=PhaseCode.NONE) \
            .to_acls(nominal_phases=PhaseCode.NONE) \
            .to_breaker(PhaseCode.NONE, is_normally_open=True) \
            .to_acls(nominal_phases=PhaseCode.NONE) \
            .network

        await SetDirection().run_terminal(self._get_t(n, "j0", 1))
        await log_directions(n["j0"])

        self._check_expected_direction(self._get_t(n, "j0", 1), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "c1", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "c1", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "b2", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "b2", 2), NONE)
        self._check_expected_direction(self._get_t(n, "c3", 1), NONE)
        self._check_expected_direction(self._get_t(n, "c3", 2), NONE)

    @pytest.mark.asyncio
    async def test_upstream_terminal_to_feeder_head_not_set(self):
        # feeder_heads:     feeder
        #                   v
        # network:          b0 -- c1 -- j2
        n = await TestNetworkBuilder() \
            .from_breaker() \
            .to_acls() \
            .to_junction() \
            .add_feeder(head_mrid="b0") \
            .build()

        self._check_expected_direction(self._get_t(n, "b0", 1), NONE)
        self._check_expected_direction(self._get_t(n, "b0", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "c1", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "c1", 2), DOWNSTREAM)
        self._check_expected_direction(self._get_t(n, "j2", 1), UPSTREAM)
        self._check_expected_direction(self._get_t(n, "j2", 2), DOWNSTREAM)

    @pytest.mark.asyncio
    async def test_set_direction_doesnt_flow_through_feeder_heads(self):
        # feeder_heads:     feeder1     feeder2
        #                   v           v
        # network:          b0 -- c1 -- b2
        n = await TestNetworkBuilder() \
            .from_breaker() \
            .to_acls() \
            .to_breaker() \
            .add_feeder(head_mrid="b0", sequence_number=2) \
            .add_feeder(head_mrid="b2", sequence_number=1) \
            .build()

        self._check_expected_direction(self._get_t(n, "b0", 1), NONE)
        self._check_expected_direction(self._get_t(n, "b0", 2), BOTH)
        self._check_expected_direction(self._get_t(n, "c1", 1), BOTH)
        self._check_expected_direction(self._get_t(n, "c1", 2), BOTH)
        self._check_expected_direction(self._get_t(n, "b2", 1), BOTH)
        self._check_expected_direction(self._get_t(n, "b2", 2), NONE)

    @staticmethod
    async def _do_set_direction_trace(n: NetworkService):
        await SetDirection().run(n)
        for it in n.objects(Feeder):
            await log_directions(it.normal_head_terminal.conducting_equipment)

    @staticmethod
    def _get_t(network: NetworkService, mrid: str, sequence_number: int) -> Terminal:
        return network.get(mrid, ConductingEquipment).get_terminal_by_sn(sequence_number)

    @staticmethod
    def _check_expected_direction(t: Terminal, expected_normal: FeederDirection, expected_current: FeederDirection = None):
        assert t.normal_feeder_direction == expected_normal
        assert t.current_feeder_direction == expected_current or expected_normal
