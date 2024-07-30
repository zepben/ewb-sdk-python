#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional

import pytest

from services.network.tracing.feeder.direction_logger import log_directions
from zepben.evolve import TestNetworkBuilder, PhaseCode, NetworkService, Terminal, ConductingEquipment, FeederDirection, RemoveDirection

DOWNSTREAM = FeederDirection.DOWNSTREAM
UPSTREAM = FeederDirection.UPSTREAM
NONE = FeederDirection.NONE
BOTH = FeederDirection.BOTH


class TestRemoveDirection:

    def setup_method(self):
        self.nb = TestNetworkBuilder() \
            .from_junction(PhaseCode.A, 1) \
            .to_acls(PhaseCode.A) \
            .to_acls(PhaseCode.A) \
            .to_junction(PhaseCode.A, 1)

    @pytest.mark.asyncio
    async def test_removes_all_directions_present_by_default_down(self):
        self.nb.add_feeder("j0")
        n = await self._build_and_log(self.nb)

        self._validate_directions(n, DOWNSTREAM, UPSTREAM, DOWNSTREAM, UPSTREAM, DOWNSTREAM, UPSTREAM)

        await RemoveDirection().run_terminal(self._get_t(n, "c1", 2))

        await log_directions(n["j0"])
        self._validate_directions(n, DOWNSTREAM, UPSTREAM, NONE, NONE, NONE, NONE)

    @pytest.mark.asyncio
    async def test_removes_all_directions_present_by_default_up(self):
        self.nb.add_feeder("j0")
        n = await self._build_and_log(self.nb)

        self._validate_directions(n, DOWNSTREAM, UPSTREAM, DOWNSTREAM, UPSTREAM, DOWNSTREAM, UPSTREAM)

        await RemoveDirection().run_terminal(self._get_t(n, "c2", 1))

        await log_directions(n["j0"])
        self._validate_directions(n, NONE, NONE, NONE, NONE, DOWNSTREAM, UPSTREAM)

    @pytest.mark.asyncio
    async def test_removes_all_directions_present_by_default_both(self):
        self.nb \
            .add_feeder("j0") \
            .add_feeder("j3")
        n = await self._build_and_log(self.nb)

        self._validate_directions(n, BOTH, BOTH, BOTH, BOTH, BOTH, BOTH)

        await RemoveDirection().run_terminal(self._get_t(n, "c1", 2))

        await log_directions(n["j0"])
        self._validate_directions(n, BOTH, BOTH, NONE, NONE, NONE, NONE)

    @pytest.mark.asyncio
    async def test_can_remove_only_selected_directions_down(self):
        self.nb \
            .add_feeder("j0") \
            .add_feeder("j3")
        n = await self._build_and_log(self.nb)

        self._validate_directions(n, BOTH, BOTH, BOTH, BOTH, BOTH, BOTH)

        await RemoveDirection().run_terminal(self._get_t(n, "j0", 1), DOWNSTREAM)

        await log_directions(n["j0"])
        self._validate_directions(n, UPSTREAM, DOWNSTREAM, UPSTREAM, DOWNSTREAM, UPSTREAM, DOWNSTREAM)

    @pytest.mark.asyncio
    async def test_can_remove_only_selected_directions_up(self):
        self.nb \
            .add_feeder("j0") \
            .add_feeder("j3")
        n = await self._build_and_log(self.nb)

        self._validate_directions(n, BOTH, BOTH, BOTH, BOTH, BOTH, BOTH)

        await RemoveDirection().run_terminal(self._get_t(n, "j0", 1), UPSTREAM)

        await log_directions(n["j0"])
        self._validate_directions(n, DOWNSTREAM, UPSTREAM, DOWNSTREAM, UPSTREAM, DOWNSTREAM, UPSTREAM)

    @pytest.mark.asyncio
    async def test_respects_multi_feeds_up(self):
        #
        # j0 --c1-- --c2-- j3
        #          |
        #          c4
        #          |
        #           --c5--
        #
        self.nb \
            .branch_from("c1") \
            .to_acls(PhaseCode.A) \
            .to_acls(PhaseCode.A) \
            .add_feeder("j0") \
            .add_feeder("j3")
        n = await self._build_and_log(self.nb)

        self._validate_directions(n, BOTH, BOTH, BOTH, BOTH, BOTH, BOTH)
        self._validate_terminal_directions(self._get_t(n, "c4", 1), UPSTREAM)
        self._validate_terminal_directions(self._get_t(n, "c4", 2), DOWNSTREAM)
        self._validate_terminal_directions(self._get_t(n, "c5", 1), UPSTREAM)
        self._validate_terminal_directions(self._get_t(n, "c5", 2), DOWNSTREAM)

        await RemoveDirection().run_terminal(self._get_t(n, "c5", 1))
        await log_directions(n["j0"])

        self._validate_directions(n, BOTH, BOTH, BOTH, BOTH, BOTH, BOTH)
        self._validate_terminal_directions(self._get_t(n, "c4", 1), NONE)
        self._validate_terminal_directions(self._get_t(n, "c4", 2), NONE)
        self._validate_terminal_directions(self._get_t(n, "c5", 1), NONE)
        self._validate_terminal_directions(self._get_t(n, "c5", 2), DOWNSTREAM)

    @pytest.mark.asyncio
    async def test_respects_multi_feeds_down(self):
        #
        # j0 --c1-- --c2-- j3
        #          |
        #          c4
        #          |
        #           --c5--
        #
        self.nb \
            .branch_from("c1") \
            .to_acls(PhaseCode.A) \
            .to_acls(PhaseCode.A) \
            .add_feeder("j0") \
            .add_feeder("j3")
        n = await self._build_and_log(self.nb)

        self._validate_directions(n, BOTH, BOTH, BOTH, BOTH, BOTH, BOTH)
        self._validate_terminal_directions(self._get_t(n, "c4", 1), UPSTREAM)
        self._validate_terminal_directions(self._get_t(n, "c4", 2), DOWNSTREAM)
        self._validate_terminal_directions(self._get_t(n, "c5", 1), UPSTREAM)
        self._validate_terminal_directions(self._get_t(n, "c5", 2), DOWNSTREAM)

        await RemoveDirection().run_terminal(self._get_t(n, "j0", 1), DOWNSTREAM)
        await log_directions(n["j0"])

        self._validate_directions(n, UPSTREAM, DOWNSTREAM, UPSTREAM, DOWNSTREAM, UPSTREAM, DOWNSTREAM)
        self._validate_terminal_directions(self._get_t(n, "c4", 1), UPSTREAM)
        self._validate_terminal_directions(self._get_t(n, "c4", 2), DOWNSTREAM)
        self._validate_terminal_directions(self._get_t(n, "c5", 1), UPSTREAM)
        self._validate_terminal_directions(self._get_t(n, "c5", 2), DOWNSTREAM)

    @pytest.mark.asyncio
    async def test_respects_multi_feeds_both(self):
        #
        # j0 --c1-- --c2-- j3
        #          |
        #          c4
        #          |
        #           --c5--
        #
        # j6 --c7--
        #
        self.nb \
            .branch_from("c1") \
            .to_acls(PhaseCode.A) \
            .to_acls(PhaseCode.A) \
            .from_junction(PhaseCode.A, 1) \
            .to_acls(PhaseCode.A) \
            .add_feeder("j0") \
            .add_feeder("j3") \
            .add_feeder("j6")
        n = await self._build_and_log(self.nb, "j0", "j6")

        self._validate_directions(n, BOTH, BOTH, BOTH, BOTH, BOTH, BOTH)
        self._validate_terminal_directions(self._get_t(n, "c4", 1), UPSTREAM)
        self._validate_terminal_directions(self._get_t(n, "c4", 2), DOWNSTREAM)
        self._validate_terminal_directions(self._get_t(n, "c5", 1), UPSTREAM)
        self._validate_terminal_directions(self._get_t(n, "c5", 2), DOWNSTREAM)
        self._validate_terminal_directions(self._get_t(n, "j6", 1), DOWNSTREAM)
        self._validate_terminal_directions(self._get_t(n, "c7", 1), UPSTREAM)
        self._validate_terminal_directions(self._get_t(n, "c7", 2), DOWNSTREAM)

        await RemoveDirection().run_terminal(self._get_t(n, "j0", 1), BOTH)
        await log_directions(n["j0"], n["j6"])

        self._validate_directions(n, NONE, NONE, NONE, NONE, NONE, NONE)
        self._validate_terminal_directions(self._get_t(n, "c4", 1), NONE)
        self._validate_terminal_directions(self._get_t(n, "c4", 2), NONE)
        self._validate_terminal_directions(self._get_t(n, "c5", 1), NONE)
        self._validate_terminal_directions(self._get_t(n, "c5", 2), NONE)
        self._validate_terminal_directions(self._get_t(n, "j6", 1), DOWNSTREAM)
        self._validate_terminal_directions(self._get_t(n, "c7", 1), UPSTREAM)
        self._validate_terminal_directions(self._get_t(n, "c7", 2), DOWNSTREAM)

    @pytest.mark.asyncio
    async def test_respects_multi_feeds_junction(self):
        #
        # j0 12--c1--21 j2 31--c3--21 j4
        #               2
        #               1
        #               |
        #               c5
        #               |
        #               2
        #               1
        #               j6
        #
        tnb = TestNetworkBuilder() \
            .from_junction(PhaseCode.A, 1) \
            .to_acls(PhaseCode.A) \
            .to_junction(PhaseCode.A, 3) \
            .to_acls(PhaseCode.A) \
            .to_junction(PhaseCode.A, 1) \
            .from_acls(PhaseCode.A) \
            .connect("j2", "c5", 2, 1) \
            .to_junction(PhaseCode.A, 1) \
            .add_feeder("j0") \
            .add_feeder("j4") \
            .add_feeder("j6")
        n = await self._build_and_log(tnb)

        self._validate_terminal_directions(self._get_t(n, "j0", 1), BOTH)
        self._validate_terminal_directions(self._get_t(n, "j2", 1), BOTH)
        self._validate_terminal_directions(self._get_t(n, "j2", 2), BOTH)
        self._validate_terminal_directions(self._get_t(n, "j2", 3), BOTH)
        self._validate_terminal_directions(self._get_t(n, "j4", 1), BOTH)
        self._validate_terminal_directions(self._get_t(n, "j6", 1), BOTH)

        await RemoveDirection().run_terminal(self._get_t(n, "j0", 1), DOWNSTREAM)
        await log_directions(n["j0"])

        self._validate_terminal_directions(self._get_t(n, "j0", 1), UPSTREAM)
        self._validate_terminal_directions(self._get_t(n, "j2", 1), DOWNSTREAM)
        self._validate_terminal_directions(self._get_t(n, "j2", 2), BOTH)
        self._validate_terminal_directions(self._get_t(n, "j2", 3), BOTH)
        self._validate_terminal_directions(self._get_t(n, "j4", 1), BOTH)
        self._validate_terminal_directions(self._get_t(n, "j6", 1), BOTH)

    @pytest.mark.asyncio
    async def test_can_remove_from_entire_network(self):
        #
        # j0 --c1-- --c2-- j3
        #
        # j4 --c5--
        #
        self.nb \
            .from_junction(PhaseCode.B) \
            .to_acls(PhaseCode.B) \
            .add_feeder("j0") \
            .add_feeder("j4", 2)
        n = await self._build_and_log(self.nb, "j0", "j4")

        self._validate_directions(n, DOWNSTREAM, UPSTREAM, DOWNSTREAM, UPSTREAM, DOWNSTREAM, UPSTREAM)
        self._validate_terminal_directions(self._get_t(n, "j4", 1), NONE)
        self._validate_terminal_directions(self._get_t(n, "j4", 2), DOWNSTREAM)
        self._validate_terminal_directions(self._get_t(n, "c5", 1), UPSTREAM)
        self._validate_terminal_directions(self._get_t(n, "c5", 2), DOWNSTREAM)

        RemoveDirection().run(n)
        await log_directions(n["j0"], n["j4"])

        self._validate_directions(n, NONE, NONE, NONE, NONE, NONE, NONE)
        self._validate_terminal_directions(self._get_t(n, "j4", 1), NONE)
        self._validate_terminal_directions(self._get_t(n, "j4", 2), NONE)
        self._validate_terminal_directions(self._get_t(n, "c5", 1), NONE)
        self._validate_terminal_directions(self._get_t(n, "c5", 2), NONE)

    @staticmethod
    def _get_t(ns: NetworkService, ce: str, t: int) -> Terminal:
        return ns.get(ce, ConductingEquipment).get_terminal_by_sn(t)

    def _validate_directions(
        self,
        ns: NetworkService,
        j1: FeederDirection,
        c1t1: FeederDirection,
        c1t2: FeederDirection,
        c2t1: FeederDirection,
        c2t2: FeederDirection,
        c3: FeederDirection
    ):
        self._validate_terminal_directions(self._get_t(ns, "j0", 1), j1)
        self._validate_terminal_directions(self._get_t(ns, "c1", 1), c1t1)
        self._validate_terminal_directions(self._get_t(ns, "c1", 2), c1t2)
        self._validate_terminal_directions(self._get_t(ns, "c2", 1), c2t1)
        self._validate_terminal_directions(self._get_t(ns, "c2", 2), c2t2)
        self._validate_terminal_directions(self._get_t(ns, "j3", 1), c3)

    @staticmethod
    async def _build_and_log(tnb: TestNetworkBuilder, *log_from: str) -> NetworkService:
        ns = await tnb.build()

        if not log_from:
            await log_directions(ns["j0"])
        else:
            await log_directions(*map(lambda it: ns[it], log_from))

        return ns

    @staticmethod
    def _validate_terminal_directions(
        terminal: Terminal,
        expected_normal_direction: FeederDirection,
        expected_current_direction: Optional[FeederDirection] = None
    ):
        assert terminal.normal_feeder_direction == expected_normal_direction
        assert terminal.current_feeder_direction == (expected_current_direction or expected_normal_direction)
