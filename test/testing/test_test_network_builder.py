#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections import Counter
from typing import Callable, List

import pytest
from pytest import raises

from zepben.evolve import PhaseCode, PowerTransformerEnd, Terminal, NetworkService, ConductingEquipment, Breaker, Feeder, PowerTransformer, \
    connected_terminals, TestNetworkBuilder, Fuse, LvFeeder, ConnectivityNode, TransformerEndRatedS, TransformerCoolingType


class TestTestNetworkBuilder:

    @pytest.mark.asyncio
    async def test_sample_network_starting_with_source(self):
        #
        # s0 11--c1--21 b2 21 s3
        #
        # s4 11--c5--2
        #
        n = await (TestNetworkBuilder()
                   .from_source(PhaseCode.ABC)  # s0
                   .to_acls(PhaseCode.ABC)  # c1
                   .to_breaker(PhaseCode.ABC)  # b2
                   .to_source(PhaseCode.ABC)  # s3
                   .from_source(PhaseCode.AB)  # s4
                   .to_acls(PhaseCode.AB)  # c5
                   .build())
        print(hex(id(n)))

        self._validate_connections(n, "s0", [["c1-t1"]])
        self._validate_connections(n, "c1", [["s0-t1"], ["b2-t1"]])
        self._validate_connections(n, "b2", [["c1-t2"], ["s3-t1"]])
        self._validate_connections(n, "s3", [["b2-t2"]])
        self._validate_connections(n, "s4", [["c5-t1"]])
        self._validate_connections(n, "c5", [["s4-t1"], []])

    @pytest.mark.asyncio
    async def test_sample_network_starting_with_acls(self):
        #
        # 1--c0--21 b1 21--c2--2
        #         1 b3 21--c4--2
        #
        # 1--c5--21--c6--2
        #
        n = await (TestNetworkBuilder()
                   .from_acls(PhaseCode.ABC)  # c0
                   .to_breaker(PhaseCode.ABC, is_normally_open=True)  # b1
                   .to_acls(PhaseCode.AB)  # c2
                   .branch_from("c0")
                   .to_breaker(PhaseCode.ABC, is_open=True)  # b3
                   .to_acls(PhaseCode.AB)  # c4
                   .from_acls(PhaseCode.AB)  # c5
                   .to_acls(PhaseCode.AB)  # c6
                   .connect("c2", "c4", 2, 2)
                   .build())
        print(hex(id(n)))

        self._validate_connections(n, "c0", [[], ["b1-t1", "b3-t1"]])
        self._validate_connections(n, "b1", [["c0-t2", "b3-t1"], ["c2-t1"]])
        self._validate_connections(n, "c2", [["b1-t2"], ["c4-t2"]])
        self._validate_connections(n, "b3", [["c0-t2", "b1-t1"], ["c4-t1"]])
        self._validate_connections(n, "c4", [["b3-t2"], ["c2-t2"]])
        self._validate_connections(n, "c5", [[], ["c6-t1"]])
        self._validate_connections(n, "c6", [["c5-t2"], []])

    @pytest.mark.asyncio
    async def test_sample_network_starting_with_breaker(self):
        #
        # 1 b0*21--c1--21--c2--21--c4--2
        #
        # 1 b5*21--c6--21 tx7+21--c8--2
        #
        n = await (TestNetworkBuilder()
                   .from_breaker(PhaseCode.ABC)  # b0
                   .to_acls(PhaseCode.ABC)  # c1
                   .to_acls(PhaseCode.ABC)  # c2
                   .add_feeder("b0")  # fdr3
                   .to_acls(PhaseCode.ABC)  # c4
                   .from_breaker(PhaseCode.AB)  # b5
                   .to_acls(PhaseCode.AB)  # c6
                   .to_power_transformer([PhaseCode.AB, PhaseCode.A])  # tx7
                   .to_acls(PhaseCode.A)  # c8
                   .add_feeder("b5", 1)  # fdr9
                   .add_lv_feeder("tx7")  # lvf10
                   .build())
        print(hex(id(n)))

        self._validate_connections(n, "b0", [[], ["c1-t1"]])
        self._validate_connections(n, "c1", [["b0-t2"], ["c2-t1"]])
        self._validate_connections(n, "c2", [["c1-t2"], ["c4-t1"]])
        self._validate_feeder(n, "fdr3", "b0-t2")
        self._validate_connections(n, "c4", [["c2-t2"], []])
        self._validate_connections(n, "b5", [[], ["c6-t1"]])
        self._validate_connections(n, "c6", [["b5-t2"], ["tx7-t1"]])
        self._validate_connections(n, "tx7", [["c6-t2"], ["c8-t1"]])
        self._validate_connections(n, "c8", [["tx7-t2"], []])
        self._validate_feeder(n, "fdr9", "b5-t1")
        self._validate_lv_feeder(n, "lvf10", "tx7-t2")

    @pytest.mark.asyncio
    async def test_sample_network_starting_with_junction(self):
        #
        # 1 j0 21--c1--21 j2 2
        #
        # 1 j3 31--c4--2
        #   2
        #
        n = await (TestNetworkBuilder()
                   .from_junction(PhaseCode.ABC)  # j0
                   .to_acls(PhaseCode.ABC)  # c1
                   .to_junction(PhaseCode.ABC)  # j2
                   .from_junction(PhaseCode.AB, 3)  # j3
                   .to_acls(PhaseCode.AB)  # c4
                   .build())
        print(hex(id(n)))

        self._validate_connections(n, "j0", [[], ["c1-t1"]])
        self._validate_connections(n, "c1", [["j0-t2"], ["j2-t1"]])
        self._validate_connections(n, "j2", [["c1-t2"], []])
        self._validate_connections(n, "j3", [[], [], ["c4-t1"]])
        self._validate_connections(n, "c4", [["j3-t3"], []])

    @pytest.mark.asyncio
    async def test_sample_network_starting_with_power_transformer(self):
        #
        # 1 tx0 21--c1--21 tx2 2
        #
        # 1 tx3 31--c4--2
        #    2
        #
        n = await (TestNetworkBuilder()
                   .from_power_transformer()  # tx0
                   .to_acls(PhaseCode.ABC)  # c1
                   .to_power_transformer([PhaseCode.ABC])  # tx2
                   .from_power_transformer([PhaseCode.AB, PhaseCode.AB, PhaseCode.AN])  # tx3
                   .to_acls(PhaseCode.AN)  # c4
                   .build())
        print(hex(id(n)))

        self._validate_connections(n, "tx0", [[], ["c1-t1"]])
        self._validate_connections(n, "c1", [["tx0-t2"], ["tx2-t1"]])
        self._validate_connections(n, "tx2", [["c1-t2"]])
        self._validate_connections(n, "tx3", [[], [], ["c4-t1"]])
        self._validate_connections(n, "c4", [["tx3-t3"], []])

        self._validate_ends(n, "tx0", [PhaseCode.ABC, PhaseCode.ABC])
        self._validate_ends(n, "tx2", [PhaseCode.ABC])
        self._validate_ends(n, "tx3", [PhaseCode.AB, PhaseCode.AB, PhaseCode.AN])

    @pytest.mark.asyncio
    async def test_can_override_ids(self):
        ns = await (TestNetworkBuilder()
                    .from_source(mrid="my source 1")
                    .to_source(mrid="my source 2")
                    .from_acls(mrid="my acls 1")
                    .to_acls(mrid="my acls 2")
                    .from_breaker(mrid="my breaker 1")
                    .to_breaker(mrid="my breaker 2")
                    .from_junction(mrid="my junction 1")
                    .to_junction(mrid="my junction 2")
                    .to_power_electronics_connection(mrid="my pec 1")
                    .from_power_transformer(mrid="my tx 1")
                    .to_power_transformer(mrid="my tx 2")
                    .to_energy_consumer(mrid="my ec 1")
                    .from_other(Fuse, mrid="my other 1")
                    .to_other(Fuse, mrid="my other 2")
                    .build())

        assert {it.mrid for it in ns.objects(ConductingEquipment)} == {
            "my source 1",
            "my source 2",
            "my acls 1",
            "my acls 2",
            "my breaker 1",
            "my breaker 2",
            "my junction 1",
            "my junction 2",
            "my pec 1",
            "my tx 1",
            "my tx 2",
            "my ec 1",
            "my other 1",
            "my other 2"
        }

    @pytest.mark.asyncio
    async def test_can_start_with_open_points(self):
        #
        # 1 b0 2
        # 1 b1 2
        # 1 b2 2
        # 1 b3 2
        #
        n = await (TestNetworkBuilder()
                   .from_breaker(PhaseCode.A, is_normally_open=True, is_open=False)  # b0
                   .from_breaker(PhaseCode.B, is_normally_open=True, is_open=False)  # b1
                   .from_breaker(PhaseCode.B)  # b2
                   .from_breaker(PhaseCode.B, is_normally_open=True)  # b3
                   .build())
        print(hex(id(n)))

        self._validate_open_states(n, "b0", expected_is_normally_open=True, expected_is_open=False)
        self._validate_open_states(n, "b1", expected_is_normally_open=True, expected_is_open=False)
        self._validate_open_states(n, "b2", expected_is_normally_open=False, expected_is_open=False)
        self._validate_open_states(n, "b3", expected_is_normally_open=True, expected_is_open=True)

    @pytest.mark.asyncio
    async def test_can_branch_from_junction(self):
        #
        #           2
        #           |
        #           c2
        #           |
        #           1
        #           1
        # 2--c1--14 j0 31--c4--21--c5--2
        #           2
        #           1
        #           |
        #           c3
        #           |
        #           2
        #
        n = await (TestNetworkBuilder()
                   .from_junction(PhaseCode.A, 4)  # j0
                   .to_acls(PhaseCode.A)  # c1
                   .branch_from("j0", 1)
                   .to_acls(PhaseCode.A)  # c2
                   .branch_from("j0", 2)
                   .to_acls(PhaseCode.A)  # c3
                   .branch_from("j0", 3)
                   .to_acls(PhaseCode.A)  # c4
                   .to_acls(PhaseCode.A)  # c5
                   .build())
        print(hex(id(n)))

        self._validate_connections(n, "j0", [["c2-t1"], ["c3-t1"], ["c4-t1"], ["c1-t1"]])
        self._validate_connections(n, "c1", [["j0-t4"], []])
        self._validate_connections(n, "c2", [["j0-t1"], []])
        self._validate_connections(n, "c3", [["j0-t2"], []])
        self._validate_connections(n, "c4", [["j0-t3"], ["c5-t1"]])
        self._validate_connections(n, "c5", [["c4-t2"], []])

    def test_must_use_valid_source_phases(self):
        with raises(ValueError, match="EnergySource phases must be a subset of ABCN"):
            TestNetworkBuilder() \
                .from_source(PhaseCode.XYN)

        with raises(ValueError, match="EnergySource phases must be a subset of ABCN"):
            (TestNetworkBuilder()
             .from_source(PhaseCode.ABC)
             .from_source(PhaseCode.XYN))

    @pytest.mark.asyncio
    async def test_can_initialise_ends(self):
        #
        # 1 tx0 21 tx1
        #
        # 1 tx3 3
        #    2
        #
        def init_rated_u(val: int) -> Callable[[PowerTransformerEnd], None]:
            def set_rated_u(end: PowerTransformerEnd):
                end.rated_u = val

            return set_rated_u

        def init_rated_s(val: int) -> Callable[[PowerTransformerEnd], None]:
            def set_rated_s(end: PowerTransformerEnd):
                end.rated_s = val

            return set_rated_s

        def init_s_rating(cooling_type: TransformerCoolingType,  rated_s: int) -> Callable[[PowerTransformerEnd], None]:
            def add_s_rating(end: PowerTransformerEnd):
                end.add_transformer_end_rated_s(TransformerEndRatedS(cooling_type, rated_s))

            return add_s_rating

        def init_b(val: float) -> Callable[[PowerTransformerEnd], None]:
            def set_b(end: PowerTransformerEnd):
                end.b = val

            return set_b

        n = await (TestNetworkBuilder()
                   .from_power_transformer([PhaseCode.ABC, PhaseCode.ABC], [init_rated_u(1), init_rated_u(2)])  # tx0
                   .to_power_transformer([PhaseCode.ABC], [init_s_rating(TransformerCoolingType.UNKNOWN_COOLING_TYPE, 3)])  # tx1
                   .from_power_transformer([PhaseCode.AB, PhaseCode.AB, PhaseCode.AN], [init_b(4.0), init_b(5.0), init_b(6.0)])  # tx2
                   .build())
        print(hex(id(n)))

        assert n.get("tx0-e1", PowerTransformerEnd).rated_u == 1
        assert n.get("tx0-e2", PowerTransformerEnd).rated_u == 2
        assert n.get("tx1-e1", PowerTransformerEnd).rated_s == 3
        assert n.get("tx2-e1", PowerTransformerEnd).b == 4.0
        assert n.get("tx2-e2", PowerTransformerEnd).b == 5.0
        assert n.get("tx2-e3", PowerTransformerEnd).b == 6.0

    @pytest.mark.asyncio
    async def test_sample_network_with_generics(self):
        #
        # o0 11 my-id[o1]
        #
        # 1 o2 21 o3 2
        #
        def replace_o1(mrid: str) -> ConductingEquipment:
            assert mrid == "o1"
            return Fuse(mrid="my-id")

        # noinspection PyTypeChecker
        n = await (TestNetworkBuilder()
                   .from_other(Fuse, num_terminals=1)  # o0
                   .to_other(replace_o1, num_terminals=1)  # my-id[o1]
                   .from_other(Fuse, PhaseCode.AB)  # o2
                   .to_other(Fuse, PhaseCode.AB)  # o3
                   .build())
        print(hex(id(n)))

        self._validate_connections(n, "o0", [["my-id-t1"]])
        self._validate_connections(n, "my-id", [["o0-t1"]])
        self._validate_connections(n, "o2", [[], ["o3-t1"]])
        self._validate_connections(n, "o3", [["o2-t2"], []])

    def test_can_choose_the_connectivity_node_id(self):
        self._validate_connectivity_node_override(lambda b, mrid, cn_mrid: b.to_breaker(mrid=mrid, connectivity_node_mrid=cn_mrid))
        self._validate_connectivity_node_override(lambda b, mrid, cn_mrid: b.to_junction(mrid=mrid, connectivity_node_mrid=cn_mrid))
        self._validate_connectivity_node_override(lambda b, mrid, cn_mrid: b.to_acls(mrid=mrid, connectivity_node_mrid=cn_mrid))
        self._validate_connectivity_node_override(lambda b, mrid, cn_mrid: b.to_power_transformer(mrid=mrid, connectivity_node_mrid=cn_mrid))
        self._validate_connectivity_node_override(lambda b, mrid, cn_mrid: b.to_power_electronics_connection(mrid=mrid, connectivity_node_mrid=cn_mrid))
        self._validate_connectivity_node_override(lambda b, mrid, cn_mrid: b.to_energy_consumer(mrid=mrid, connectivity_node_mrid=cn_mrid))
        self._validate_connectivity_node_override(lambda b, mrid, cn_mrid: b.to_source(mrid=mrid, connectivity_node_mrid=cn_mrid))
        self._validate_connectivity_node_override(lambda b, mrid, cn_mrid: b.to_other(Fuse, mrid=mrid, connectivity_node_mrid=cn_mrid))

    def _validate_connections(self, n: NetworkService, mrid: str, expected_terms: List[List[str]]):
        assert n.get(mrid, ConductingEquipment).num_terminals() == len(expected_terms)
        for i, expected in enumerate(expected_terms):
            self._validate_terminal_connections(n.get(f"{mrid}-t{i + 1}"), expected)

    @staticmethod
    def _validate_terminal_connections(terminal: Terminal, expected_terms: List[str]):
        if expected_terms:
            diff = {it.to_terminal.mrid for it in connected_terminals(terminal)} ^ set(expected_terms)
            if diff:
                assert not diff
            assert not diff
        else:
            assert not connected_terminals(terminal)

    @staticmethod
    def _validate_open_states(n: NetworkService, mrid: str, expected_is_normally_open: bool, expected_is_open: bool):
        assert n.get(mrid, Breaker).is_normally_open() == expected_is_normally_open
        assert n.get(mrid, Breaker).is_open() == expected_is_open

    @staticmethod
    def _validate_feeder(n: NetworkService, mrid: str, head_terminal: str):
        assert n.get(mrid, Feeder).normal_head_terminal == n.get(head_terminal, Terminal)

    @staticmethod
    def _validate_lv_feeder(n: NetworkService, mrid: str, head_terminal: str):
        assert n.get(mrid, LvFeeder).normal_head_terminal == n.get(head_terminal, Terminal)

    @staticmethod
    def _validate_ends(n: NetworkService, mrid: str, expected_ends: List[PhaseCode]):
        tx = n.get(mrid, PowerTransformer)
        assert tx.num_terminals() == len(expected_ends)
        assert tx.num_ends() == len(expected_ends)

        for end, terminal in zip(tx.ends, tx.terminals):
            assert end.terminal == terminal

    @staticmethod
    def _validate_connectivity_node_override(add_with_connectivity_node: Callable[[TestNetworkBuilder, str, str], None]):
        builder = TestNetworkBuilder()
        ns = builder.network

        builder.from_source()  # s0
        # Connect using a specific connectivity node
        add_with_connectivity_node(builder, "my1", "specified-cn")
        builder.from_acls()  # c1
        # Reuse the specific connectivity node, which should connect all 4 items.
        add_with_connectivity_node(builder, "my2", "specified-cn")
        builder.from_acls()  # c2
        builder.from_acls()  # c3
        # Force connect to the specific connectivity node, which should connect the additional 2 items.
        builder.connect("c2", "c3", 2, 1, "specified-cn")
        builder.from_acls()  # c4
        # Force connect using a different connectivity node, which should be overridden due to the `to` terminal being connected.
        builder.connect("c2", "c4", 2, 1, "different-cn")
        builder.from_acls()  # c5
        # Force connect using a different connectivity node, which should be overridden due to the `from` terminal being connected.
        builder.connect("c5", "c4", 2, 1, "different-cn")

        assert Counter([it.mrid for it in ns.get("specified-cn", ConnectivityNode).terminals]) == \
               Counter(["s0-t1", "my1-t1", "c1-t2", "my2-t1", "c2-t2", "c3-t1", "c4-t1", "c5-t2"])

        # Make sure our overridden connectivity node was not created.
        assert ns.get("different-cn", ConnectivityNode, default=None) is None
