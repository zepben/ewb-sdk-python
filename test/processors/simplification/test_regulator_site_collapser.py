#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

import pytest
from zepben.evolve.processors.simplification.reshape import Reshape

from zepben.evolve import AcLineSegment, CableInfo, OverheadWireInfo, NetworkService, PerLengthSequenceImpedance, BaseVoltage, FeederDirection, \
    ConductingEquipment, Terminal, PowerTransformer, TransformerFunctionKind, Location, PowerTransformerEnd, TransformerCoolingType, Switch, Breaker, \
    set_direction, TapChangerControl, RatioTapChanger, PhaseCode, connected_equipment, IdentifiedObject
from zepben.evolve.processors.simplification.regulator_site_collapser import RegulatorSiteCollapser


class TestRegulatorSiteCollapser:
    network: NetworkService = NetworkService()
    bv22k = BaseVoltage()
    bv22k.nominal_voltage = 22000

    @pytest.mark.timeout(324234)
    @pytest.mark.asyncio
    async def test_populate(self):
        await self.populateRegulatorsNetwork()
        reshape = await RegulatorSiteCollapser().process(self.network)
        x = 3

        assert len(list(self.network.objects(AcLineSegment))) == 36
        assert len(list(self.network.objects(PowerTransformer))) == 11
        # assert len(list(self.network.objects(Switch))) == 0 # will double check later, might be an artifact of not adding switches to the service in the jvm test

        self.assertAllInNetwork("c11", "c12", "r11-collapsed")
        self.assertNoneInNetwork("r11", "c13", "c14", "c15", "c16", "s11")
        self.verifyEquipmentConnectivity("r11-collapsed", ["c11", "c12"])
        self.verifyEnds("r11-collapsed", "c11", "c12", 0.1, 0.2)
        self.verifyReshape(reshape, ["r11", "c13", "c14", "c15", "c15", "s11"], "r11-collapsed")


        self.assertAllInNetwork("c21", "c22", "r21-collapsed")
        self.assertNoneInNetwork("r21", "r22", "r23", "c23", "c24", "c25", "c26", "c27", "c28", "c29", "c210", "c211", "c212", "c213", "c214", "s21")
        self.verifyEquipmentConnectivity("r21-collapsed", ["c21", "c22"])
        self.verifyEnds("r21-collapsed", "c21", "c22", 0.1, 0.2)
        self.verifyReshape(
            reshape,
            ["r21", "r22", "r23", "c23", "c24", "c25", "c26", "c27", "c28", "c29", "c210", "c211", "c212", "c213", "c214", "s21"],
            "r21-collapsed"
        )

        self.assertAllInNetwork("c31", "c32", "c311", "r31-collapsed", "r32-collapsed-node")
        self.assertNoneInNetwork("r31", "r32", "c33", "c34", "c35", "c36", "c37", "c38", "c39", "c310", "s31", "s32")
        self.verifyEquipmentConnectivity("r31-collapsed", ["c31", "c32"])
        self.verifyEquipmentConnectivity("c32", ["r31-collapsed", "c311"])
        self.verifyEnds("r31-collapsed", "c31", "c32", 0.1, 0.2)
        self.verifyReshape(reshape, ["r31", "c33", "c34", "c35", "c36", "s31"], "r31-collapsed")
        self.verifyReshape(reshape, ["r32", "c37", "c38", "c39", "c310", "s32"], "r32-collapsed-node")

        self.assertAllInNetwork("c41", "c42", "c47", "c48", "r41-collapsed")
        self.assertNoneInNetwork("r41", "c43", "c44", "c45", "c46", "s41")
        self.verifyEquipmentConnectivity("r41-collapsed", ["c41", "c48"])
        self.verifyEnds("r41-collapsed", "c41", "c48", 0.1, 0.2)
        self.verifyReshape(
            reshape,
            ["r41", "c43", "c44", "c45", "c46", "s41"],
            "r41-collapsed"
        )

        self.assertAllInNetwork("c51", "c52", "r51")
        self.verifyEquipmentConnectivity("r51", ["c51", "c52"])
        assert "r51" not in reshape.originalToNew

        self.assertAllInNetwork("c61", "c62", "c63", "c64", "r61")
        self.verifyEquipmentConnectivity("r61", ["c61", "c62", "c63"])
        assert "r61" not in reshape.originalToNew

        self.assertAllInNetwork("c71", "c72", "c73", "c74", "c75", "c76", "c77", "c78", "c79", "c710", "c711", "c712", "c713", "c714", "c715", "r71")
        self.verifyEquipmentConnectivity("r71", ["c73", "c74"])
        self.verifyEquipmentConnectivity("r72", ["c77", "c78"])
        self.verifyEquipmentConnectivity("r73", ["c79", "c710"])
        assert "r71" not in reshape.originalToNew
        assert "r72" not in reshape.originalToNew
        assert "r73" not in reshape.originalToNew

        self.assertAllInNetwork("c81", "c82", "r81")
        self.verifyEquipmentConnectivity("r81", ["c81", "c82"])
        assert "r81" not in reshape.originalToNew

        self.assertAllInNetwork("c91", "c92", "r93-collapsed")
        self.assertNoneInNetwork("r92", "r93", "r93", "c93", "c94", "c95", "c96", "c97", "c98", "c99", "c910", "c911", "c912", "c913", "c914", "s91")
        self.verifyEquipmentConnectivity("r93-collapsed", ["c91", "c92"])
        self.verifyEnds("r93-collapsed", "c91", "c92", 0.1, 0.2)
        self.verifyReshape(
            reshape,
            ["r91", "r92", "r93", "c93", "c94", "c95", "c96", "c97", "c98", "c99", "c910", "c911", "c912", "c913", "c914", "s91"],
            "r93-collapsed"
        )

        rtc = self.network.get("r93-collapsed").get_end_by_num(1).ratio_tap_changer
        assert rtc.mrid == "rtc"
        assert rtc.tap_changer_control.mrid == "tcc"


    def verifyReshape(self, reshape: Reshape, originalMRIDs: List[str], newMRID: str):
        newObject: IdentifiedObject = self.network.get(newMRID)
        for mRID in originalMRIDs:
            newObjects = reshape.originalToNew[mRID]
            assert newObject in newObjects
        assert set(reshape.newToOriginal[newObject.mrid]) >= set(originalMRIDs)

    def verifyEnds(self, regulatorMRID: str, t1ConnectedMRID: str, t2ConnectedMRID: str, rPrimary: float, rSecondary: float):
        reg: PowerTransformer = self.network.get(regulatorMRID)
        assert reg.num_ends() == 2
        end1, end2 = reg.ends
        assert [ct.conducting_equipment.mrid for ct in end1.terminal.connected_terminals()] == [t1ConnectedMRID]
        assert [ct.conducting_equipment.mrid for ct in end2.terminal.connected_terminals()] == [t2ConnectedMRID]
        assert end1.r == rPrimary
        assert end2.r == rSecondary

    def verifyEquipmentConnectivity(self,
                                    equipmentMRID: str,
                                    connectedMRIDs: List[str],
                                    directions: List[FeederDirection] = None,
                                    phases: List[PhaseCode] = None):
        if directions is None:
            directions = [FeederDirection.UPSTREAM, FeederDirection.DOWNSTREAM]
        if phases is None:
            phases = [PhaseCode.ABC, PhaseCode.ABC]

        reg: ConductingEquipment = self.network.get(equipmentMRID)

        assert [rc.to_equip.mrid for rc in connected_equipment(reg)] == connectedMRIDs
        assert [t.normal_feeder_direction for t in reg.terminals] == directions
        assert [t.phases for t in reg.terminals] == phases

    def assertAllInNetwork(self, *mRIDS: str):
        for mRID in mRIDS:
            assert mRID in self.network

    def assertNoneInNetwork(self, *mRIDS: str):
        for mRID in mRIDS:
            assert mRID not in self.network

    async def populateRegulatorsNetwork(self):
        c11 = self.createAcls("c11", False, 2.0, 2.0, 2000, 1.0, 1.0)
        c12 = self.createAcls("c12", False, 2.0, 2.0, 2000, 1.0, 1.0)
        c13 = self.createAcls("c13", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c14 = self.createAcls("c14", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c15 = self.createAcls("c15", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c16 = self.createAcls("c16", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        reg11 = self.createRegulator("r11", 0.1, 0.2)
        s11 = self.createSwitch("s11", True)

        self.network.connect_terminals(list(c11.terminals)[1], list(c13.terminals)[0])
        self.network.connect_terminals(list(c11.terminals)[1], list(c15.terminals)[0])
        self.network.connect_terminals(list(c13.terminals)[1], list(reg11.terminals)[0])
        self.network.connect_terminals(list(c15.terminals)[1], list(s11.terminals)[0])
        self.network.connect_terminals(list(reg11.terminals)[1], list(c14.terminals)[0])
        self.network.connect_terminals(list(s11.terminals)[1], list(c16.terminals)[0])
        self.network.connect_terminals(list(c14.terminals)[1], list(c12.terminals)[0])
        self.network.connect_terminals(list(c16.terminals)[1], list(c12.terminals)[0])
        await set_direction().run_terminal(list(c11.terminals)[1])

        c21 = self.createAcls("c21", False, 2.0, 2.0, 2000, 1.0, 1.0)
        c22 = self.createAcls("c22", False, 2.0, 2.0, 2000, 1.0, 1.0)
        c23 = self.createAcls("c23", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c24 = self.createAcls("c24", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c25 = self.createAcls("c25", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c26 = self.createAcls("c26", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c27 = self.createAcls("c27", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c28 = self.createAcls("c28", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c29 = self.createAcls("c29", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c210 = self.createAcls("c210", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c211 = self.createAcls("c211", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c212 = self.createAcls("c212", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c213 = self.createAcls("c213", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c214 = self.createAcls("c214", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        reg21 = self.createRegulator("r21", 0.1, 0.2)
        reg22 = self.createRegulator("r22", 0.1, 0.2)
        reg23 = self.createRegulator("r23", 0.1, 0.2)
        s21 = self.createSwitch("s21", True)

        self.network.connect_terminals(list(c21.terminals)[1], list(c23.terminals)[0])
        self.network.connect_terminals(list(c21.terminals)[1], list(c211.terminals)[0])
        self.network.connect_terminals(list(c211.terminals)[1], list(c212.terminals)[0])
        self.network.connect_terminals(list(c212.terminals)[1], list(c25.terminals)[0])
        self.network.connect_terminals(list(c211.terminals)[1], list(c27.terminals)[0])
        self.network.connect_terminals(list(c212.terminals)[1], list(c29.terminals)[0])
        self.network.connect_terminals(list(c23.terminals)[1], list(reg21.terminals)[0])
        self.network.connect_terminals(list(c27.terminals)[1], list(reg22.terminals)[0])
        self.network.connect_terminals(list(c29.terminals)[1], list(reg23.terminals)[0])
        self.network.connect_terminals(list(c25.terminals)[1], list(s21.terminals)[0])
        self.network.connect_terminals(list(reg21.terminals)[1], list(c24.terminals)[0])
        self.network.connect_terminals(list(reg22.terminals)[1], list(c28.terminals)[0])
        self.network.connect_terminals(list(reg23.terminals)[1], list(c210.terminals)[0])
        self.network.connect_terminals(list(s21.terminals)[1], list(c26.terminals)[0])
        self.network.connect_terminals(list(c24.terminals)[1], list(c22.terminals)[0])
        self.network.connect_terminals(list(c213.terminals)[1], list(c22.terminals)[0])
        self.network.connect_terminals(list(c28.terminals)[1], list(c213.terminals)[0])
        self.network.connect_terminals(list(c214.terminals)[1], list(c213.terminals)[0])
        self.network.connect_terminals(list(c210.terminals)[1], list(c214.terminals)[0])
        self.network.connect_terminals(list(c26.terminals)[1], list(c214.terminals)[0])
        await set_direction().run_terminal(list(c21.terminals)[1])

        c31 = self.createAcls("c31", False, 2.0, 2.0, 2000, 1.0, 1.0)
        c32 = self.createAcls("c32", False, 2.0, 2.0, 2000, 1.0, 1.0)
        c33 = self.createAcls("c33", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c34 = self.createAcls("c34", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c35 = self.createAcls("c35", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c36 = self.createAcls("c36", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        reg31 = self.createRegulator("r31", 0.1, 0.2)
        s31 = self.createSwitch("s31", True)
        c37 = self.createAcls("c37", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c38 = self.createAcls("c38", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c39 = self.createAcls("c39", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c310 = self.createAcls("c310", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c311 = self.createAcls("c311", False, 2.0, 2.0, 2000, 1.0, 1.0)
        reg32 = self.createRegulator("r32", 0.1, 0.2)
        s32 = self.createSwitch("s32", True)

        self.network.connect_terminals(list(c31.terminals)[1], list(c33.terminals)[0])
        self.network.connect_terminals(list(c31.terminals)[1], list(c35.terminals)[0])
        self.network.connect_terminals(list(c33.terminals)[1], list(reg31.terminals)[0])
        self.network.connect_terminals(list(c35.terminals)[1], list(s31.terminals)[0])
        self.network.connect_terminals(list(reg31.terminals)[1], list(c34.terminals)[0])
        self.network.connect_terminals(list(s31.terminals)[1], list(c36.terminals)[0])
        self.network.connect_terminals(list(c34.terminals)[1], list(c32.terminals)[0])
        self.network.connect_terminals(list(c36.terminals)[1], list(c32.terminals)[0])
        self.network.connect_terminals(list(c32.terminals)[1], list(c37.terminals)[0])
        self.network.connect_terminals(list(c32.terminals)[1], list(c39.terminals)[0])
        self.network.connect_terminals(list(c37.terminals)[1], list(reg32.terminals)[0])
        self.network.connect_terminals(list(c39.terminals)[1], list(s32.terminals)[0])
        self.network.connect_terminals(list(reg32.terminals)[1], list(c38.terminals)[0])
        self.network.connect_terminals(list(s32.terminals)[1], list(c310.terminals)[0])
        self.network.connect_terminals(list(c38.terminals)[1], list(c311.terminals)[0])
        self.network.connect_terminals(list(c310.terminals)[1], list(c311.terminals)[0])
        await set_direction().run_terminal(list(c31.terminals)[1])

        c41 = self.createAcls("c41", False, 2.0, 2.0, 2000, 1.0, 1.0)
        c42 = self.createAcls("c42", False, 2.0, 2.0, 2000, 1.0, 1.0)
        c43 = self.createAcls("c43", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c44 = self.createAcls("c44", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c45 = self.createAcls("c45", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c46 = self.createAcls("c46", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c47 = self.createAcls("c47", False, 2.0, 2.0, 2000, 1.0, 1.0)
        c48 = self.createAcls("c48", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        reg41 = self.createRegulator("r41", 0.1, 0.2)
        s41 = self.createSwitch("s41", True)

        self.network.connect_terminals(list(c41.terminals)[1], list(c43.terminals)[0])
        self.network.connect_terminals(list(c41.terminals)[1], list(c45.terminals)[0])
        self.network.connect_terminals(list(c43.terminals)[1], list(reg41.terminals)[0])
        self.network.connect_terminals(list(c45.terminals)[1], list(s41.terminals)[0])
        self.network.connect_terminals(list(reg41.terminals)[1], list(c44.terminals)[0])
        self.network.connect_terminals(list(s41.terminals)[1], list(c46.terminals)[0])
        self.network.connect_terminals(list(c44.terminals)[1], list(c48.terminals)[0])
        self.network.connect_terminals(list(c46.terminals)[1], list(c48.terminals)[0])
        self.network.connect_terminals(list(c48.terminals)[1], list(c42.terminals)[0])
        self.network.connect_terminals(list(c48.terminals)[1], list(c47.terminals)[0])
        await set_direction().run_terminal(list(c41.terminals)[1])

        c51 = self.createAcls("c51", False, 2.0, 2.0, 2000, 1.0, 1.0)
        c52 = self.createAcls("c52", False, 2.0, 2.0, 2000, 1.0, 1.0)
        reg51 = self.createRegulator("r51", 0.1, 0.2)

        self.network.connect_terminals(list(c51.terminals)[1], list(reg51.terminals)[0])
        self.network.connect_terminals(list(reg51.terminals)[1], list(c52.terminals)[0])
        await set_direction().run_terminal(list(c51.terminals)[1])

        c61 = self.createAcls("c61", False, 2.0, 2.0, 2000, 1.0, 1.0)
        c62 = self.createAcls("c62", False, 2.0, 2.0, 2000, 1.0, 1.0)
        c63 = self.createAcls("c63", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c64 = self.createAcls("c64", False, 2.0, 2.0, 2000, 1.0, 1.0)
        reg61 = self.createRegulator("r61", 0.1, 0.2)

        self.network.connect_terminals(list(c61.terminals)[1], list(reg61.terminals)[0])
        self.network.connect_terminals(list(reg61.terminals)[1], list(c62.terminals)[0])
        self.network.connect_terminals(list(reg61.terminals)[1], list(c63.terminals)[0])
        self.network.connect_terminals(list(c63.terminals)[1], list(c64.terminals)[0])
        await set_direction().run_terminal(list(c61.terminals)[1])

        c71 = self.createAcls("c71", False, 2.0, 2.0, 2000, 1.0, 1.0)
        c72 = self.createAcls("c72", False, 2.0, 2.0, 2000, 1.0, 1.0)
        c73 = self.createAcls("c73", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c74 = self.createAcls("c74", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c75 = self.createAcls("c75", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c76 = self.createAcls("c76", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c77 = self.createAcls("c77", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c78 = self.createAcls("c78", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c79 = self.createAcls("c79", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c710 = self.createAcls("c710", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c711 = self.createAcls("c711", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c712 = self.createAcls("c712", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c713 = self.createAcls("c713", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c714 = self.createAcls("c714", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c715 = self.createAcls("c715", False, 2.0, 2.0, 2000, 1.0, 1.0)
        reg71 = self.createRegulator("r71", 0.1, 0.2)
        reg72 = self.createRegulator("r72", 0.1, 0.2)
        reg73 = self.createRegulator("r73", 0.1, 0.2)
        s71 = self.createSwitch("s71", True)

        self.network.connect_terminals(list(c71.terminals)[1], list(c73.terminals)[0])
        self.network.connect_terminals(list(c71.terminals)[1], list(c711.terminals)[0])
        self.network.connect_terminals(list(c711.terminals)[1], list(c712.terminals)[0])
        self.network.connect_terminals(list(c712.terminals)[1], list(c75.terminals)[0])
        self.network.connect_terminals(list(c711.terminals)[1], list(c77.terminals)[0])
        self.network.connect_terminals(list(c712.terminals)[1], list(c79.terminals)[0])
        self.network.connect_terminals(list(c73.terminals)[1], list(reg71.terminals)[0])
        self.network.connect_terminals(list(c77.terminals)[1], list(reg72.terminals)[0])
        self.network.connect_terminals(list(c79.terminals)[1], list(reg73.terminals)[0])
        self.network.connect_terminals(list(c75.terminals)[1], list(s71.terminals)[0])
        self.network.connect_terminals(list(reg71.terminals)[1], list(c74.terminals)[0])
        self.network.connect_terminals(list(reg72.terminals)[1], list(c78.terminals)[0])
        self.network.connect_terminals(list(reg73.terminals)[1], list(c710.terminals)[0])
        self.network.connect_terminals(list(s71.terminals)[1], list(c76.terminals)[0])
        self.network.connect_terminals(list(c74.terminals)[1], list(c72.terminals)[0])
        self.network.connect_terminals(list(c713.terminals)[1], list(c72.terminals)[0])
        self.network.connect_terminals(list(c713.terminals)[1], list(c715.terminals)[0])
        self.network.connect_terminals(list(c78.terminals)[1], list(c713.terminals)[0])
        self.network.connect_terminals(list(c714.terminals)[1], list(c713.terminals)[0])
        self.network.connect_terminals(list(c710.terminals)[1], list(c714.terminals)[0])
        self.network.connect_terminals(list(c76.terminals)[1], list(c714.terminals)[0])
        await set_direction().run_terminal(list(c71.terminals)[1])

        c81 = self.createAcls("c81", False, 2.0, 2.0, 2000, 1.0, 1.0)
        c82 = self.createAcls("c82", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        reg81 = self.createRegulator("r81", 0.1, 0.2)

        self.network.connect_terminals(list(c81.terminals)[1], list(reg81.terminals)[0])
        self.network.connect_terminals(list(reg81.terminals)[1], list(c82.terminals)[0])
        await set_direction().run_terminal(list(c81.terminals)[1])

        c91 = self.createAcls("c91", False, 2.0, 2.0, 2000, 1.0, 1.0)
        c92 = self.createAcls("c92", False, 2.0, 2.0, 2000, 1.0, 1.0)
        c93 = self.createAcls("c93", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c94 = self.createAcls("c94", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c95 = self.createAcls("c95", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c96 = self.createAcls("c96", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c97 = self.createAcls("c97", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c98 = self.createAcls("c98", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c99 = self.createAcls("c99", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c910 = self.createAcls("c910", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c911 = self.createAcls("c911", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c912 = self.createAcls("c912", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c913 = self.createAcls("c913", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        c914 = self.createAcls("c914", False, 2.0, 2.0, 2000, 1.0, 1.0, 1.0)
        reg91 = self.createRegulator("r91", 0.1, 0.2)
        reg92 = self.createRegulator("r92", 0.1, 0.2)
        reg93 = self.createRegulator("r93", 0.1, 0.2)
        s91 = self.createSwitch("s91", True)
        tcc = TapChangerControl(mrid="tcc")
        self.network.add(tcc)
        rtc = RatioTapChanger(mrid="rtc")
        rtc.tap_changer_control = tcc
        self.network.add(rtc)
        reg93.get_end_by_num(1).ratio_tap_changer = rtc

        self.network.connect_terminals(list(c91.terminals)[1], list(c93.terminals)[0])
        self.network.connect_terminals(list(c91.terminals)[1], list(c911.terminals)[0])
        self.network.connect_terminals(list(c911.terminals)[1], list(c912.terminals)[0])
        self.network.connect_terminals(list(c912.terminals)[1], list(c95.terminals)[0])
        self.network.connect_terminals(list(c911.terminals)[1], list(c97.terminals)[0])
        self.network.connect_terminals(list(c912.terminals)[1], list(c99.terminals)[0])
        self.network.connect_terminals(list(c93.terminals)[1], list(reg91.terminals)[0])
        self.network.connect_terminals(list(c97.terminals)[1], list(reg92.terminals)[0])
        self.network.connect_terminals(list(c99.terminals)[1], list(reg93.terminals)[0])
        self.network.connect_terminals(list(c95.terminals)[1], list(s91.terminals)[0])
        self.network.connect_terminals(list(reg91.terminals)[1], list(c94.terminals)[0])
        self.network.connect_terminals(list(reg92.terminals)[1], list(c98.terminals)[0])
        self.network.connect_terminals(list(reg93.terminals)[1], list(c910.terminals)[0])
        self.network.connect_terminals(list(s91.terminals)[1], list(c96.terminals)[0])
        self.network.connect_terminals(list(c94.terminals)[1], list(c92.terminals)[0])
        self.network.connect_terminals(list(c913.terminals)[1], list(c92.terminals)[0])
        self.network.connect_terminals(list(c98.terminals)[1], list(c913.terminals)[0])
        self.network.connect_terminals(list(c914.terminals)[1], list(c913.terminals)[0])
        self.network.connect_terminals(list(c910.terminals)[1], list(c914.terminals)[0])
        self.network.connect_terminals(list(c96.terminals)[1], list(c914.terminals)[0])
        await set_direction().run_terminal(list(c91.terminals)[1])

    def createSwitch(self, mRID: str, isOpen: bool) -> Switch:
        breaker = Breaker(mrid=mRID)
        breaker.base_voltage = self.bv22k
        location = Location(mrid=f'{mRID}-loc')
        self.network.add(location)
        breaker.location = location
        breaker.set_normally_open(isOpen)
        breaker.set_open(isOpen)
        self.addTerminalForEquipment(breaker, FeederDirection.UPSTREAM)
        self.addTerminalForEquipment(breaker, FeederDirection.DOWNSTREAM)
        self.network.add(breaker)  # originally not added to the network?
        return breaker

    def createRegulator(self, mRID: str, rPrimary: float, rSecondary: float) -> PowerTransformer:
        regulator = PowerTransformer(mrid=mRID)
        regulator.base_voltage = self.bv22k
        regulator.function = TransformerFunctionKind.voltageRegulator
        location = Location(mrid=f'{mRID}-loc')
        regulator.location = location
        self.network.add(location)
        upTerminal = self.addTerminalForEquipment(regulator, FeederDirection.UPSTREAM)
        downTerminal = self.addTerminalForEquipment(regulator, FeederDirection.DOWNSTREAM)
        upEnd = PowerTransformerEnd(mrid=f'{mRID}-e1')
        upEnd.base_voltage = self.bv22k
        upEnd.add_rating(TransformerCoolingType.UNKNOWN_COOLING_TYPE, 1000)
        upEnd.terminal = upTerminal
        upEnd.r = rPrimary
        regulator.add_end(upEnd)
        self.network.add(upEnd)

        downEnd = PowerTransformerEnd(mrid=f'{mRID}-e2')
        downEnd.base_voltage = self.bv22k
        downEnd.add_rating(TransformerCoolingType.UNKNOWN_COOLING_TYPE, 1000)
        downEnd.terminal = downTerminal
        downEnd.r = rSecondary
        regulator.add_end(downEnd)
        self.network.add(downEnd)

        self.network.add(regulator)
        return regulator

    def createAcls(self,
                   mRID: str,
                   isUnderground: bool,
                   resistance: float,
                   reactance: float,
                   rating: int,
                   zeroSequenceResistance: float,
                   zeroSequenceReactance: float,
                   length: float = 100.0) -> AcLineSegment:
        lineInfo = CableInfo(mrid=f'{mRID}-wi') if isUnderground else OverheadWireInfo(mrid=f'{mRID}-wi')
        lineInfo.rated_current = rating
        self.network.add(lineInfo)

        plsi = PerLengthSequenceImpedance(mrid=f'{mRID}-plsi')
        plsi.r = resistance
        plsi.x = reactance
        plsi.r0 = zeroSequenceResistance
        plsi.x0 = zeroSequenceReactance
        self.network.add(plsi)

        acls = AcLineSegment(mrid=mRID)
        acls.base_voltage = self.bv22k
        acls.length = length
        acls.asset_info = lineInfo
        acls.per_length_sequence_impedance = plsi

        self.addTerminalForEquipment(acls, FeederDirection.UPSTREAM)
        self.addTerminalForEquipment(acls, FeederDirection.DOWNSTREAM)
        self.network.add(acls)
        return acls

    def addTerminalForEquipment(self, ce: ConductingEquipment, direction: FeederDirection) -> Terminal:
        t = Terminal(mrid=f'{ce.mrid}-t{ce.num_terminals() + 1}')
        t.normal_feeder_direction = direction
        ce.add_terminal(t)
        self.network.add(t)
        return t
