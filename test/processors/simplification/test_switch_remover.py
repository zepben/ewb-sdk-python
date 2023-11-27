#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from asyncio import get_event_loop

import pytest

from zepben.evolve import TestNetworkBuilder, Switch, AcLineSegment, PerLengthSequenceImpedance, ConductingEquipment, PhaseCode, BaseVoltage, \
    TransformerFunctionKind, PowerTransformerEnd, FeederDirection
from zepben.evolve.processors.simplification.negligible_impedance_collapser import NegligibleImpedanceCollapser
from zepben.evolve.processors.simplification.swer_collapser import SwerCollapser
from zepben.evolve.processors.simplification.switch_remover import SwitchRemover


@pytest.mark.timeout(323434)
def test_uno():
    test_network = get_event_loop().run_until_complete(TestNetworkBuilder()
                                                       .from_acls()
                                                       .to_breaker()
                                                       .to_acls()
                                                       .build())
    what_it_did = SwitchRemover().process(test_network)
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


@pytest.mark.timeout(324234)
@pytest.mark.asyncio
async def test_attempt_to_copy_kotlin_test_network():
    bv430 = BaseVoltage()
    bv430.nominal_voltage = 430

    bv12700 = BaseVoltage()
    bv12700.nominal_voltage = 12700

    bv22000 = BaseVoltage()
    bv22000.nominal_voltage = 22000

    test_network = (await TestNetworkBuilder()
                    .from_breaker(action=lambda br: setattr(br, "base_voltage", bv22000))
                    .to_acls(action=lambda acls: setattr(acls, "base_voltage", bv22000))
                    .to_power_transformer(nominal_phases=[PhaseCode.AB, PhaseCode.A, PhaseCode.AN],  # tx2
                                          end_actions=[lambda end: setattr(end, "base_voltage", bv22000),
                                                       lambda end: setattr(end, "base_voltage", bv12700),
                                                       lambda end: setattr(end, "base_voltage", bv430)],
                                          action=lambda pte: setattr(pte, "function", TransformerFunctionKind.isolationTransformer))
                    .to_acls(PhaseCode.AN, action=lambda acls: setattr(acls, "base_voltage", bv430))
                    .branch_from("tx2", 2)
                    .to_acls(PhaseCode.A, action=lambda end: setattr(end, "base_voltage", bv12700))
                    .to_power_transformer(nominal_phases=[PhaseCode.A, PhaseCode.AN],  # tx5
                                          end_actions=[lambda end: setattr(end, "base_voltage", bv12700),
                                                       lambda end: setattr(end, "base_voltage", bv430)],
                                          action=lambda pte: setattr(pte, "function", TransformerFunctionKind.distributionTransformer))
                    .to_acls(PhaseCode.AN)
                    .to_junction(PhaseCode.AN, num_terminals=3)
                    .to_acls(PhaseCode.AN)
                    .to_energy_consumer(PhaseCode.AN)
                    .branch_from("j7", 2)
                    .to_acls(PhaseCode.AN)
                    .to_power_electronics_connection(PhaseCode.AN)
                    .add_feeder("b0", 2)
                    .add_lv_feeder("tx2", 3)
                    .add_lv_feeder("tx5", 2)
                    .build())

    test_network.add(bv430)
    test_network.add(bv12700)
    test_network.add(bv22000)

    what_it_did = await SwerCollapser().process(test_network)
    #assert len(list(test_network.objects(AcLineSegment))) == 1

    swerTerminal = test_network.get("tx2-t2")
    assert {io.conducting_equipment.mrid for io in swerTerminal.connected_terminals()} == {"ec9", "pec11"}

    assert {io.mrid for io in test_network.get("tx2-t2-lvf").equipment} == {"tx2", "ec9", "pec11"}

def _make_lv(ce: ConductingEquipment):
    bv = BaseVoltage()
    bv.nominal_voltage = 415
    ce.base_voltage = bv


def _make_swer_end(pte: PowerTransformerEnd):
    bv = BaseVoltage()
    bv.nominal_voltage = 12700
    pte.base_voltage = bv
    pte.terminal.normal_feeder_direction = FeederDirection.DOWNSTREAM
