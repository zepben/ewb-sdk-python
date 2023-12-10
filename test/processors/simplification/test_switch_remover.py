#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from asyncio import get_event_loop

import pytest

from zepben.evolve import TestNetworkBuilder, Switch, AcLineSegment, PerLengthSequenceImpedance, ConductingEquipment, PhaseCode, BaseVoltage, \
    TransformerFunctionKind, PowerTransformerEnd, FeederDirection, Terminal, NetworkService, connected_equipment, SinglePhaseKind, Junction, currently_open
from zepben.evolve.processors.simplification.negligible_impedance_collapser import NegligibleImpedanceCollapser
from zepben.evolve.processors.simplification.swer_collapser import SwerCollapser
from zepben.evolve.processors.simplification.switch_remover import SwitchRemover


@pytest.mark.timeout(323434)
@pytest.mark.asyncio
async def test_uno():
    test_network = (await TestNetworkBuilder()
                    .from_acls()
                    .to_breaker()
                    .to_acls()
                    .build())
    what_it_did = await SwitchRemover().process(test_network)
    assert len(list(test_network.objects(Switch))) == 0


@pytest.mark.timeout(324234)
@pytest.mark.asyncio
async def test_other():
    plsi = PerLengthSequenceImpedance(mrid="test-plsi", r=4.0, x=3.3)

    def myAction(ce: ConductingEquipment) -> None:
        setattr(ce, "per_length_sequence_impedance", plsi)
        setattr(ce, "length", 14.7)

    test_network = (await TestNetworkBuilder().from_acls()
                    .to_breaker()
                    .to_acls()
                    .to_acls()
                    .to_breaker()
                    .to_acls(mrid="test1", action=myAction)
                    .build())
    what_it_did = await NegligibleImpedanceCollapser().process(test_network)
    assert len(list(test_network.objects(AcLineSegment))) == 1


@pytest.mark.timeout(324234)
@pytest.mark.asyncio
async def test_real_test_name():
    plsi = PerLengthSequenceImpedance(mrid="test-plsi", r=4.0, x=3.3)

    def myAction(ce: ConductingEquipment) -> None:
        setattr(ce, "per_length_sequence_impedance", plsi)
        setattr(ce, "length", 14.7)

    test_network = (await TestNetworkBuilder()
                    .from_breaker()  # b0
                    .to_power_transformer()  # tx1
                    .to_acls()  # c2
                    .to_power_transformer([PhaseCode.AB, PhaseCode.A],
                                          end_actions=[lambda end: end, lambda end: _make_swer_end(end)],
                                          action=lambda pt: setattr(pt, "function", TransformerFunctionKind.isolationTransformer))  # tx3
                    .to_acls(PhaseCode.A)  # c4
                    .to_acls(PhaseCode.A)  # c5
                    .to_power_transformer([PhaseCode.A, PhaseCode.AN])  # tx6
                    .to_acls(PhaseCode.AN, action=_make_lv)  # c7
                    .add_feeder("b0")  # fdr8
                    .build())
    what_it_did = await SwerCollapser().process(test_network)
    assert len(list(test_network.objects(AcLineSegment))) == 1


@pytest.mark.asyncio
async def test_removes_completely_open_switches():
    test_network = (await TestNetworkBuilder()
                    .from_acls()
                    .to_breaker(is_normally_open=True)
                    .to_acls()
                    .build())

    what_it_did = await SwitchRemover().process(test_network)
    assert list(test_network.objects(Switch)) == []
    assert connected_equipment(test_network.get("c0")) == []
    assert connected_equipment(test_network.get("c2")) == []
    assert what_it_did.originalToNew == {"b1": set(), "b1-t1": set(), "b1-t2": set()}
    assert what_it_did.newToOriginal == {}


@pytest.mark.asyncio
async def test_removes_partially_open_switches():
    test_network = (await TestNetworkBuilder()
                    .from_acls()
                    .to_breaker(action=lambda br: br.set_normally_open(True, SinglePhaseKind.A))
                    .to_acls()
                    .build())

    what_it_did = await SwitchRemover().process(test_network)

    assert list(test_network.objects(Switch)) == []
    assert connected_equipment(test_network.get("c0")) == []
    assert connected_equipment(test_network.get("c2")) == []
    assert what_it_did.originalToNew == {"b1": set(), "b1-t1": set(), "b1-t2": set()}
    assert what_it_did.newToOriginal == {}


@pytest.mark.timeout(3234234)
@pytest.mark.asyncio
async def test_replaces_closed_switch_with_junctions():
    test_network = (await TestNetworkBuilder()
                    .from_acls()
                    .to_breaker(is_normally_open=False)
                    .to_acls()
                    .build())

    what_it_did = await SwitchRemover().process(test_network)

    junction = list(what_it_did.originalToNew["b1"])[0]

    assert list(test_network.objects(Switch)) == []
    assert list(test_network.objects(Junction)) == [junction]
    assert junction in [result.to_terminal.conducting_equipment for result in connected_equipment(test_network.get("c0"))]
    assert junction in [result.to_terminal.conducting_equipment for result in connected_equipment(test_network.get("c2"))]
    assert what_it_did.originalToNew == {"b1": {junction},
                                         "b1-t1": {junction.get_terminal_by_sn(1)},
                                         "b1-t2": {junction.get_terminal_by_sn(2)}}
    assert what_it_did.newToOriginal == {junction: {"b1"},
                                         junction.get_terminal_by_sn(1): {"b1-t1"},
                                         junction.get_terminal_by_sn(2): {"b1-t2"}}


@pytest.mark.asyncio
async def test_uses_provided_network_state():
    test_network = (await TestNetworkBuilder()
                    .from_acls()
                    .to_breaker(is_normally_open=False, is_open=True)
                    .to_acls()
                    .build())

    what_it_did = await SwitchRemover(currently_open).process(test_network)

    assert list(test_network.objects(Switch)) == []
    assert connected_equipment(test_network.get("c0")) == []
    assert connected_equipment(test_network.get("c2")) == []
    assert what_it_did.originalToNew == {"b1": set(), "b1-t1": set(), "b1-t2": set()}
    assert what_it_did.newToOriginal == {}


def _make_lv(ce: ConductingEquipment):
    bv = BaseVoltage()
    bv.nominal_voltage = 415
    ce.base_voltage = bv


def _make_swer_end(pte: PowerTransformerEnd):
    bv = BaseVoltage()
    bv.nominal_voltage = 12700
    pte.base_voltage = bv
    pte.terminal.normal_feeder_direction = FeederDirection.DOWNSTREAM
