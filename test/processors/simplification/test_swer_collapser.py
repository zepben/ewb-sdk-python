#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest
from zepben.evolve.processors.simplification.swer_collapser import SwerCollapser

from zepben.evolve import BaseVoltage, TestNetworkBuilder, PhaseCode, TransformerFunctionKind, Terminal


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
    # assert len(list(test_network.objects(AcLineSegment))) == 1

    swerTerminal: Terminal = test_network.get("tx2-t2")
    assert {io.conducting_equipment.mrid for io in swerTerminal.connected_terminals()} == {"ec9", "pec11"}

    assert {io.mrid for io in test_network.get("tx2-t2-lvf").equipment} == {"tx2", "ec9", "pec11"}
    assert {io.mrid for io in test_network.get("tx2-t2-lvf").normal_energizing_feeders} == {"fdr12"}
    assert {io.mrid for io in test_network.get("fdr12").normal_energized_lv_feeders} >= {"tx2-t2-lvf", "lvf13"}
    assert "ec9" not in {io.mrid for io in test_network.get("lvf14").equipment}
    assert "pec11" not in {io.mrid for io in test_network.get("lvf14").equipment}
    assert test_network.get("tx2-e2").base_voltage.nominal_voltage == 250
    assert test_network.get("ec9").base_voltage.nominal_voltage == 250
    assert test_network.get("pec11").base_voltage.nominal_voltage == 250
    assert test_network.get("tx2-e3").base_voltage == bv430

    assert what_it_did.originalToNew.keys() >= {"c4", "tx5", "c6", "j7", "c8", "c10"}
    assert what_it_did.newToOriginal[swerTerminal.connectivity_node.mrid] >= {"c4", "tx5", "c6", "j7", "c8", "c10"}
