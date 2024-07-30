#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List, Optional
from unittest.mock import patch

import pytest

from services.network.tracing.phases.util import validate_phases_from_term_or_equip
from zepben.evolve import TestNetworkBuilder, PhaseCode, SinglePhaseKind, PhaseInferrer, Terminal, NetworkService

A = SinglePhaseKind.A
B = SinglePhaseKind.B
C = SinglePhaseKind.C
N = SinglePhaseKind.N
NONE = SinglePhaseKind.NONE


class TestPhaseInferrer:
    """
    Test the `PhaseInferrer`
    """

    @pytest.mark.asyncio
    async def test_ab_to_bc_to_xy_to_abc(self, caplog):
        """
        # nominal
        # AB -> BC -> XY -> ABC
        # traced
        # AB -> B? -> B? -> ?B?
        #
        # infer nominal
        # AB -> BC -> BC -> ABC
        """
        network = await (TestNetworkBuilder()
                         .from_source(PhaseCode.AB)
                         .to_acls(PhaseCode.BC)
                         .to_acls(PhaseCode.XY)
                         .to_acls(PhaseCode.ABC)
                         .build())

        validate_phases_from_term_or_equip(network, "c1", [B, NONE])
        validate_phases_from_term_or_equip(network, "c2", [B, NONE])
        validate_phases_from_term_or_equip(network, "c3", [NONE, B, NONE])

        await PhaseInferrer().run(network)

        validate_phases_from_term_or_equip(network, "c1", PhaseCode.BC)
        validate_phases_from_term_or_equip(network, "c2", PhaseCode.BC)
        validate_phases_from_term_or_equip(network, "c3", PhaseCode.ABC)

        self._validate_log(caplog, correct=["c1", "c3"])

    @pytest.mark.asyncio
    async def test_abn_to_bcn_to_xyn_to_abcn(self, caplog):
        """
        # nominal
        # ABN -> BCN -> XYN -> ABCN
        # traced
        # ABN -> B?N -> B?N -> ?B?N
        #
        # infer nominal
        # ABN -> BCN -> BCN -> ABCN
        """
        network = await (TestNetworkBuilder()
                         .from_source(PhaseCode.ABN)
                         .to_acls(PhaseCode.BCN)
                         .to_acls(PhaseCode.XYN)
                         .to_acls(PhaseCode.ABCN)
                         .build())

        validate_phases_from_term_or_equip(network, "c1", [B, NONE, N])
        validate_phases_from_term_or_equip(network, "c2", [B, NONE, N])
        validate_phases_from_term_or_equip(network, "c3", [NONE, B, NONE, N])

        await PhaseInferrer().run(network)

        validate_phases_from_term_or_equip(network, "c1", PhaseCode.BCN)
        validate_phases_from_term_or_equip(network, "c2", PhaseCode.BCN)
        validate_phases_from_term_or_equip(network, "c3", PhaseCode.ABCN)

        self._validate_log(caplog, correct=["c1", "c3"])

    @pytest.mark.asyncio
    async def test_bc_to_ac_to_xy_to_abc(self, caplog):
        """
        # nominal
        # BC -> AC -> XY -> ABC
        # traced
        # BC -> ?C -> ?C -> ??C
        #
        # infer nominal
        # BC -> AC -> AC -> ABC
        """
        network = await(TestNetworkBuilder()
                        .from_source(PhaseCode.BC)
                        .to_acls(PhaseCode.AC)
                        .to_acls(PhaseCode.XY)
                        .to_acls(PhaseCode.ABC)
                        .build())

        validate_phases_from_term_or_equip(network, "c1", [NONE, C])
        validate_phases_from_term_or_equip(network, "c2", [NONE, C])
        validate_phases_from_term_or_equip(network, "c3", [NONE, NONE, C])

        await PhaseInferrer().run(network)

        validate_phases_from_term_or_equip(network, "c1", PhaseCode.AC)
        validate_phases_from_term_or_equip(network, "c2", PhaseCode.AC)
        validate_phases_from_term_or_equip(network, "c3", PhaseCode.ABC)

        self._validate_log(caplog, correct=["c1", "c3"])

    @pytest.mark.asyncio
    async def test_abc_to_xyn_to_xy_to_bc(self, caplog):
        """
        # nominal
        # ABC -> XYN -> XY -> BC
        # traced
        # ABC -> BC? -> BC -> BC
        #
        # infer nominal
        # ABC -> BCN -> BC -> BC
        """
        network = await(TestNetworkBuilder()
                        .from_source(PhaseCode.ABC)
                        .to_acls(PhaseCode.XYN)
                        .to_acls(PhaseCode.XY)
                        .to_acls(PhaseCode.BC)
                        .build())

        validate_phases_from_term_or_equip(network, "c1", [B, C, NONE])
        validate_phases_from_term_or_equip(network, "c2", PhaseCode.BC)
        validate_phases_from_term_or_equip(network, "c3", PhaseCode.BC)

        await PhaseInferrer().run(network)

        validate_phases_from_term_or_equip(network, "c1", PhaseCode.BCN)
        validate_phases_from_term_or_equip(network, "c2", PhaseCode.BC)
        validate_phases_from_term_or_equip(network, "c3", PhaseCode.BC)

        self._validate_log(caplog, correct=["c1"])

    @pytest.mark.asyncio
    async def test_abc_to_xy_to_xyn_to_bc(self, caplog):
        """
        # nominal
        # ABC -> XY -> XYN -> BC
        # traced
        # ABC -> BC -> BC? -> BC
        #
        # infer nominal
        # ABC -> BC -> BCN -> BC
        """
        network = await(TestNetworkBuilder()
                        .from_source(PhaseCode.ABC)
                        .to_acls(PhaseCode.XY)
                        .to_acls(PhaseCode.XYN)
                        .to_acls(PhaseCode.BC)
                        .build())

        validate_phases_from_term_or_equip(network, "c1", PhaseCode.BC)
        validate_phases_from_term_or_equip(network, "c2", [B, C, NONE])
        validate_phases_from_term_or_equip(network, "c3", PhaseCode.BC)

        await PhaseInferrer().run(network)

        validate_phases_from_term_or_equip(network, "c1", PhaseCode.BC)
        validate_phases_from_term_or_equip(network, "c2", PhaseCode.BCN)
        validate_phases_from_term_or_equip(network, "c3", PhaseCode.BC)

        self._validate_log(caplog, correct=["c2"])

    @pytest.mark.asyncio
    async def test_abc_to_n_to_abcn(self, caplog):
        """
        # nominal
        # ABC -> ABC -> N -> ABCN
        # traced
        # ABC -> ABC -> ? -> ????
        #
        # infer nominal
        # ABC -> ABC -> N -> ABCN
        """
        network = await(TestNetworkBuilder()
                        .from_source(PhaseCode.ABC)
                        .to_acls(PhaseCode.ABC)
                        .to_acls(PhaseCode.N)
                        .to_acls(PhaseCode.ABCN)
                        .build())

        validate_phases_from_term_or_equip(network, "c1", PhaseCode.ABC)
        validate_phases_from_term_or_equip(network, "c2", PhaseCode.NONE)
        validate_phases_from_term_or_equip(network, "c3", PhaseCode.NONE)

        await PhaseInferrer().run(network)

        validate_phases_from_term_or_equip(network, "c1", PhaseCode.ABC)
        validate_phases_from_term_or_equip(network, "c2", PhaseCode.N)
        validate_phases_from_term_or_equip(network, "c3", PhaseCode.ABCN)

        self._validate_log(caplog, correct=["c2", "c3"])

    @pytest.mark.asyncio
    async def test_abc_to_b_to_xyn(self, caplog):
        """
        # nominal
        # ABC -> ABC -> B -> XYN
        # traced
        # ABC -> ABC -> B -> B??
        #
        # infer nominal
        # ABC -> ABC -> B -> B?N
        # infer xy
        # ABC -> ABC -> B -> BCN
        """
        network = await(TestNetworkBuilder()
                        .from_source(PhaseCode.ABC)
                        .to_acls(PhaseCode.ABC)
                        .to_acls(PhaseCode.B)
                        .to_acls(PhaseCode.XYN)
                        .build())

        validate_phases_from_term_or_equip(network, "c1", PhaseCode.ABC)
        validate_phases_from_term_or_equip(network, "c2", PhaseCode.B)
        validate_phases_from_term_or_equip(network, "c3", [B, NONE, NONE])

        await PhaseInferrer().run(network)

        validate_phases_from_term_or_equip(network, "c1", PhaseCode.ABC)
        validate_phases_from_term_or_equip(network, "c2", PhaseCode.B)
        validate_phases_from_term_or_equip(network, "c3", PhaseCode.BCN)

        self._validate_log(caplog, suspect=["c3"])

    @pytest.mark.asyncio
    async def test_abc_to_c_to_xyn(self, caplog):
        """
        # nominal
        # ABC -> ABC -> C -> XYN
        # traced
        # ABC -> ABC -> C -> C??
        #
        # infer nominal
        # ABC -> ABC -> C -> C?N
        # infer xy
        # ABC -> ABC -> C -> C?N
        """
        network = await(TestNetworkBuilder()
                        .from_source(PhaseCode.ABC)
                        .to_acls(PhaseCode.ABC)
                        .to_acls(PhaseCode.C)
                        .to_acls(PhaseCode.XYN)
                        .build())

        validate_phases_from_term_or_equip(network, "c1", PhaseCode.ABC)
        validate_phases_from_term_or_equip(network, "c2", PhaseCode.C)
        validate_phases_from_term_or_equip(network, "c3", [C, NONE, NONE])

        await PhaseInferrer().run(network)

        validate_phases_from_term_or_equip(network, "c1", PhaseCode.ABC)
        validate_phases_from_term_or_equip(network, "c2", PhaseCode.C)
        validate_phases_from_term_or_equip(network, "c3", [C, NONE, N])

        self._validate_log(caplog, suspect=["c3"])

    @pytest.mark.asyncio
    async def test_abc_to_a_to_xn(self, caplog):
        """
        # nominal
        # ABC -> ABC -> A -> XN
        # traced
        # ABC -> ABC -> A -> A?
        #
        # infer nominal
        # ABC -> ABC -> A -> AN
        """
        network = await(TestNetworkBuilder()
                        .from_source(PhaseCode.ABC)
                        .to_acls(PhaseCode.ABC)
                        .to_acls(PhaseCode.A)
                        .to_acls(PhaseCode.XN)
                        .build())

        validate_phases_from_term_or_equip(network, "c1", PhaseCode.ABC)
        validate_phases_from_term_or_equip(network, "c2", PhaseCode.A)
        validate_phases_from_term_or_equip(network, "c3", [A, NONE])

        await PhaseInferrer().run(network)

        validate_phases_from_term_or_equip(network, "c1", PhaseCode.ABC)
        validate_phases_from_term_or_equip(network, "c2", PhaseCode.A)
        validate_phases_from_term_or_equip(network, "c3", PhaseCode.AN)

        self._validate_log(caplog, correct=["c3"])

    @pytest.mark.asyncio
    async def test_dual_feed_an_to_abcn(self, caplog):
        """
        # nominal
        # AN <-> ABCN <-> AN
        # traced
        # AN <-> A??N <-> AN
        #
        # infer nominal
        # AN <-> ABCN <-> AN
        """
        network = await(TestNetworkBuilder()
                        .from_source(PhaseCode.AN)
                        .to_acls(PhaseCode.ABCN)
                        .to_source(PhaseCode.AN)
                        .build())

        validate_phases_from_term_or_equip(network, "s0", PhaseCode.AN)
        validate_phases_from_term_or_equip(network, "c1", [A, NONE, NONE, N])
        validate_phases_from_term_or_equip(network, "s2", PhaseCode.AN)

        await PhaseInferrer().run(network)

        validate_phases_from_term_or_equip(network, "s0", PhaseCode.AN)
        validate_phases_from_term_or_equip(network, "c1", PhaseCode.ABCN)
        validate_phases_from_term_or_equip(network, "s2", PhaseCode.AN)

        self._validate_log(caplog, correct=["c1"])

    @pytest.mark.asyncio
    async def test_abcn_to_n_to_ab_to_xy(self, caplog):
        """
        # nominal
        # ABCN -> ABCN -> N -> AB -> XY
        # traced
        # ABCN -> ABCN -> N -> ?? -> ??
        #
        # infer nominal
        # ABCN -> ABCN -> N -> AB -> AB
        """
        network = await(TestNetworkBuilder()
                        .from_source(PhaseCode.ABCN)
                        .to_acls(PhaseCode.ABCN)
                        .to_acls(PhaseCode.N)
                        .to_acls(PhaseCode.AB)
                        .to_acls(PhaseCode.XY)
                        .build())

        validate_phases_from_term_or_equip(network, "c1", PhaseCode.ABCN)
        validate_phases_from_term_or_equip(network, "c2", PhaseCode.N)
        validate_phases_from_term_or_equip(network, "c3", PhaseCode.NONE)
        validate_phases_from_term_or_equip(network, "c4", PhaseCode.NONE)

        await PhaseInferrer().run(network)

        validate_phases_from_term_or_equip(network, "c1", PhaseCode.ABCN)
        validate_phases_from_term_or_equip(network, "c2", PhaseCode.N)
        validate_phases_from_term_or_equip(network, "c3", PhaseCode.AB)
        validate_phases_from_term_or_equip(network, "c4", PhaseCode.AB)

        self._validate_log(caplog, correct=["c3"])

    @pytest.mark.asyncio
    async def test_with_open_switch(self, caplog):
        """
        # nominal
        # ABC -> ABC -> ABC OPEN SWICH -> ABC
        # traced
        # ABC -> ABC -> ABC/??? -> ???
        #
        # infer nominal
        # ABC -> ABC -> ABC/??? -> ???
        """
        network = await(TestNetworkBuilder()
                        .from_source(PhaseCode.ABC)
                        .to_acls(PhaseCode.ABC)
                        .to_breaker(PhaseCode.ABC, is_normally_open=True)
                        .to_acls(PhaseCode.ABC)
                        .build())

        validate_phases_from_term_or_equip(network, "c1", PhaseCode.ABC)
        validate_phases_from_term_or_equip(network, "b2", PhaseCode.ABC, PhaseCode.NONE)
        validate_phases_from_term_or_equip(network, "c3", PhaseCode.NONE)

        await PhaseInferrer().run(network)

        validate_phases_from_term_or_equip(network, "c1", PhaseCode.ABC)
        validate_phases_from_term_or_equip(network, "b2", PhaseCode.ABC, PhaseCode.NONE)
        validate_phases_from_term_or_equip(network, "c3", PhaseCode.NONE)

        self._validate_log(caplog)

    @pytest.mark.asyncio
    async def test_validate_directions_with_dropped_direction_loop(self, caplog):
        """
        # s0 * 1----2 * 1----2 * 1----2 * 1----2 * 1----2 * 1----2 *
        #        c1       c2       c3       c4   2   c5   1   c9
        # ABC    ABC      XY       ABC      ABC  |   ABC  |   ABC
        #                                     c8 |     c6 |
        #                                     ABC|     ABC|
        #                                        1        2
        #                                        * 2----1 *
        #                                            c7
        #                                            XY
        """
        network = await(TestNetworkBuilder()
                        .from_source(PhaseCode.ABC)  # s0
                        .to_acls(PhaseCode.ABC)  # c1
                        .to_acls(PhaseCode.XY)  # c2
                        .to_acls(PhaseCode.ABC)  # c3
                        .to_acls(PhaseCode.ABC)  # c4
                        .to_acls(PhaseCode.ABC)  # c5
                        .to_acls(PhaseCode.ABC)  # c6
                        .to_acls(PhaseCode.XY)  # c7
                        .to_acls(PhaseCode.ABC)  # c8
                        .connect("c8", "c4", 2, 2)
                        .branch_from("c5")
                        .to_acls(PhaseCode.ABC)  # c9
                        .add_feeder("s0")
                        .build())

        terminals = [network.get("c6-t2", Terminal)] + [t for t in network.objects(Terminal) if t.mrid != "c6-t2"]
        with patch.object(NetworkService, 'objects', wraps=lambda _: terminals):
            await PhaseInferrer().run(network)

        validate_phases_from_term_or_equip(network, "c2", PhaseCode.AC, PhaseCode.AC)
        validate_phases_from_term_or_equip(network, "c3", PhaseCode.ABC, PhaseCode.ABC)
        validate_phases_from_term_or_equip(network, "c4", PhaseCode.ABC, PhaseCode.ABC)
        validate_phases_from_term_or_equip(network, "c5", PhaseCode.ABC, PhaseCode.ABC)
        validate_phases_from_term_or_equip(network, "c6", PhaseCode.ABC, PhaseCode.ABC)
        validate_phases_from_term_or_equip(network, "c7", PhaseCode.AC, PhaseCode.AC)
        validate_phases_from_term_or_equip(network, "c8", PhaseCode.ABC, PhaseCode.ABC)
        validate_phases_from_term_or_equip(network, "c9", PhaseCode.ABC, PhaseCode.ABC)

        self._validate_log(caplog, correct=["c6"])

    def _validate_log(self, caplog, correct: Optional[List[str]] = None, suspect: Optional[List[str]] = None):
        correct = correct or []
        suspect = suspect or []

        assert len(caplog.records) == (len(correct) + len(suspect)), "logged the correct number of things"

        for mrid in correct:
            assert self._correct_message(mrid) in caplog.text, f"logged correct for {mrid}"

        for mrid in suspect:
            assert self._suspect_message(mrid) in caplog.text, f"logged suspect for {mrid}"

    @staticmethod
    def _correct_message(mrid: str) -> str:
        return f"*** Action Required *** Inferred missing phase for '' [{mrid}] which should be correct. The phase was inferred due to a disconnected " \
               f"nominal phase because of an upstream error in the source data. Phasing information for the upstream equipment should be fixed in the " \
               f"source system."

    @staticmethod
    def _suspect_message(mrid: str) -> str:
        return f"*** Action Required *** Inferred missing phases for '' [{mrid}] which may not be correct. The phases were inferred due to a disconnected " \
               f"nominal phase because of an upstream error in the source data. Phasing information for the upstream equipment should be fixed in the " \
               f"source system."
