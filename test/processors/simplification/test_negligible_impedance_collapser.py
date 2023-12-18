#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest

from zepben.evolve import PerLengthSequenceImpedance, TestNetworkBuilder, AcLineSegment, EnergyConsumer, ConductingEquipment, Terminal, connected_terminals, \
    BusbarSection, connected_equipment, LinearShuntCompensator
from zepben.evolve.processors.simplification.negligible_impedance_collapser import NegligibleImpedanceCollapser


@pytest.mark.timeout(324234)
@pytest.mark.asyncio
async def test_collapses_simple_group():
    plsi = PerLengthSequenceImpedance()
    plsi.r = 0.001
    plsi.x = 0.0012

    test_network = (await TestNetworkBuilder()
                    .from_source()
                    .to_acls(action=lambda c: _acls_setup(c, plsi, 1.0))
                    .to_junction(num_terminals=3)
                    .to_acls(action=lambda c: _acls_setup(c, plsi, 0.5))
                    .to_breaker()
                    .branch_from("j2", 2)
                    .to_acls()
                    .to_power_transformer()
                    .to_other(EnergyConsumer, num_terminals=1)
                    .build())
    test_network.add(plsi)

    what_it_did = await NegligibleImpedanceCollapser().process(test_network)

    assert set([ce.mrid for ce in test_network.objects(ConductingEquipment)]) == {"s0", "c1", "b4", "tx6", "o7"}
    assert set([t.mrid for t in test_network.objects(Terminal)]) == {"s0-t1", "c1-t1", "c1-t2", "b4-t1", "b4-t2", "tx6-t1", "tx6-t2", "o7-t1"}
    assert set([cr.to_terminal.conducting_equipment.mrid for cr in connected_terminals(test_network.get("c1-t2"))]) == {"b4", "tx6"}

    expected_removed_mrids = {"generated_cn_1", "generated_cn_2", "generated_cn_3", "generated_cn_4", "generated_cn_5",
                              "j2-t1", "j2", "j2-t2", "j2-t3", "c3-t1", "c3", "c3-t2", "c5-t1", "c5", "c5-t2"}

    assert len(what_it_did.newToOriginal.keys()) == 1
    node = list(what_it_did.newToOriginal.keys())[0]

    assert what_it_did.newToOriginal[node] == expected_removed_mrids
    assert set(what_it_did.originalToNew.keys()) == expected_removed_mrids
    for value in what_it_did.originalToNew.values():
        assert value == {test_network.get(node)}


@pytest.mark.timeout(324234)
@pytest.mark.asyncio
async def test_collapses_group_at_edge():
    test_network = (await TestNetworkBuilder()
                    .from_power_transformer()
                    .to_junction()
                    .to_other(BusbarSection)
                    .build())

    what_it_did = await NegligibleImpedanceCollapser().process(test_network)

    assert set([ce.mrid for ce in test_network.objects(ConductingEquipment)]) == {"tx0"}
    assert set([t.mrid for t in test_network.objects(Terminal)]) == {"tx0-t1", "tx0-t2"}
    assert connected_equipment(test_network.get("tx0")) == []

    expected_removed_mrids = {"generated_cn_0", "generated_cn_1", "j1-t1", "j1", "j1-t2", "o2-t1", "o2", "o2-t2"}

    assert len(what_it_did.newToOriginal.keys()) == 1
    node = list(what_it_did.newToOriginal.keys())[0]

    assert what_it_did.newToOriginal[node] == expected_removed_mrids
    assert set(what_it_did.originalToNew.keys()) == expected_removed_mrids
    for value in what_it_did.originalToNew.values():
        assert value == {test_network.get(node)}


@pytest.mark.timeout(324234)
@pytest.mark.asyncio
async def test_preserves_lines_connected_to_shunt_compensator():
    plsi = PerLengthSequenceImpedance()
    plsi.r = 0.001
    plsi.x = 0.0012

    test_network = (await TestNetworkBuilder()
                    .from_source()
                    .to_acls(action=lambda c: _acls_setup(c, plsi, 1.0))
                    .to_junction(num_terminals=3)
                    .to_acls(action=lambda c: _acls_setup(c, plsi, 0.5))
                    .to_other(LinearShuntCompensator, num_terminals=1)
                    .branch_from("j2", 2)
                    .to_acls()
                    .to_power_transformer()
                    .to_other(EnergyConsumer, num_terminals=1)
                    .build())

    what_it_did = await NegligibleImpedanceCollapser().process(test_network)

    assert set([ce.mrid for ce in test_network.objects(ConductingEquipment)]) == {"s0", "c1", "c3", "o4", "tx6", "o7"}
    assert set([t.mrid for t in test_network.objects(Terminal)]) == {"s0-t1", "c1-t1", "c1-t2", "c3-t1", "c3-t2", "o4-t1", "tx6-t1", "tx6-t2", "o7-t1"}
    assert set([cr.to_terminal.conducting_equipment.mrid for cr in connected_terminals(test_network.get("c1-t2"))]) == {"c3", "tx6"}

    expected_removed_mrids = {"generated_cn_1", "generated_cn_2", "generated_cn_4", "generated_cn_5", "j2-t1", "j2", "j2-t2", "j2-t3", "c5-t1", "c5", "c5-t2"}

    assert len(what_it_did.newToOriginal.keys()) == 1
    node = list(what_it_did.newToOriginal.keys())[0]

    assert what_it_did.newToOriginal[node] == expected_removed_mrids
    assert set(what_it_did.originalToNew.keys()) == expected_removed_mrids
    for value in what_it_did.originalToNew.values():
        assert value == {test_network.get(node)}


def _acls_setup(acls: AcLineSegment, plsi: PerLengthSequenceImpedance = None, length: float = None):
    if plsi is not None:
        acls.per_length_sequence_impedance = plsi
    if length is not None:
        acls.length = length
