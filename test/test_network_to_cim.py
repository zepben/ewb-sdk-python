#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.protobuf.cim.iec61970.base.core.IdentifiedObject_pb2 import IdentifiedObject as PBIdentifiedObject
from zepben.protobuf.cim.iec61968.assetinfo.CableInfo_pb2 import CableInfo as PBCableInfo
from zepben.protobuf.cim.iec61968.assetinfo.OverheadWireInfo_pb2 import OverheadWireInfo as PBOverheadWireInfo
from zepben.protobuf.cim.iec61968.assetinfo.WireInfo_pb2 import WireInfo as PBWireInfo
from zepben.protobuf.cim.iec61968.assetinfo.WireMaterialKind_pb2 import WireMaterialKind as PBWireMaterialKind
from zepben.protobuf.cim.iec61968.assets.AssetInfo_pb2 import AssetInfo as PBAssetInfo
from zepben.protobuf.cim.iec61968.metering.EndDevice_pb2 import EndDevice as PBEndDevice
from zepben.protobuf.cim.iec61968.metering.Meter_pb2 import Meter as PBMeter
from zepben.protobuf.cim.iec61968.metering.UsagePoint_pb2 import UsagePoint as PBUsagePoint
from zepben.protobuf.cim.iec61970.base.core.AcDcTerminal_pb2 import AcDcTerminal as PBAcDcTerminal
from zepben.protobuf.cim.iec61970.base.core.BaseVoltage_pb2 import BaseVoltage as PBBaseVoltage
from zepben.protobuf.cim.iec61970.base.core.ConductingEquipment_pb2 import ConductingEquipment as PBConductingEquipment
from zepben.protobuf.cim.iec61970.base.core.Equipment_pb2 import Equipment as PBEquipment
from zepben.protobuf.cim.iec61970.base.core.Terminal_pb2 import Terminal as PBTerminal
from zepben.protobuf.cim.iec61970.base.wires.AcLineSegment_pb2 import AcLineSegment as PBAcLineSegment
from zepben.protobuf.cim.iec61970.base.wires.Breaker_pb2 import Breaker as PBBreaker
from zepben.protobuf.cim.iec61970.base.wires.Conductor_pb2 import Conductor as PBConductor
from zepben.protobuf.cim.iec61970.base.wires.EnergyConnection_pb2 import EnergyConnection as PBEnergyConnection
from zepben.protobuf.cim.iec61970.base.wires.EnergySource_pb2 import EnergySource as PBEnergySource
from zepben.protobuf.cim.iec61970.base.wires.PerLengthImpedance_pb2 import PerLengthImpedance as PBPerLengthImpedance
from zepben.protobuf.cim.iec61970.base.wires.PerLengthLineParameter_pb2 import \
    PerLengthLineParameter as PBPerLengthLineParameter
from zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance_pb2 import \
    PerLengthSequenceImpedance as PBPerLengthSequenceImpedance
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformer_pb2 import PowerTransformer as PBPowerTransformer
from zepben.protobuf.cim.iec61970.base.wires.ProtectedSwitch_pb2 import ProtectedSwitch as PBProtectedSwitch
from zepben.protobuf.cim.iec61970.base.wires.Switch_pb2 import Switch as PBSwitch

from zepben.evolve.services.network.network import NetworkService

from zepben.evolve.services.network.translator.network_proto2cim import NetworkProtoToCim


class TestNetworkToCim(object):
    def test_add_pb(self):
        """Test addition to the network works for CableInfo PB type."""
       
        # Create network
        network = NetworkProtoToCim(NetworkService())

        # BaseVoltage1
        io_bv1 = PBIdentifiedObject(mRID="bv1", name="bv1")
        bv1 = PBBaseVoltage(io=io_bv1, nominalVoltage=22000)
        network.add_from_pb(bv1)

        # BaseVoltage2
        io_bv2 = PBIdentifiedObject(mRID="bv2", name="bv2")
        bv2 = PBBaseVoltage(io=io_bv2, nominalVoltage=415)
        network.add_from_pb(bv2)

        # Terminal
        io_ad = PBIdentifiedObject(mRID="t", name="t")
        ad = PBAcDcTerminal(io=io_ad, connected=True)
        t = PBTerminal(ad=ad, connectivityNodeMRID="c1")
        eq = PBEquipment(inService=True)
        ce1 = PBConductingEquipment(eq=eq, baseVoltageMRID="bv1", terminalMRIDs=["t"])
        ec = PBEnergyConnection(ce=ce1)
        es = PBEnergySource(ec=ec)
        # AttributeError: 'EnergySource' object has no attribute 'conducting_equipment'
        network.add_from_pb(es)

        # PerLengthSequenceImpedance
        io_lp = PBIdentifiedObject(mRID="plsi1", name="plsi1")
        lp = PBPerLengthLineParameter(io=io_lp)
        pli = PBPerLengthImpedance(lp=lp)
        plsi = PBPerLengthSequenceImpedance(pli=pli)
        # PerLengthLineParameter.mrid = lambda self: self.lo.mRID
        # E   AttributeError: lo
        #network.add_from_pb(plsi)

        # CableInfo
        io_ci = PBIdentifiedObject(mRID="7", name="ci")
        ai = PBAssetInfo(io=io_ci)
        wi = PBWireInfo(ai=ai, ratedCurrent=12, material=PBWireMaterialKind.aaac)
        ci = PBCableInfo(wi=wi)
        network.add_from_pb(ci)

        # AcLineSegment
        ce2 = PBConductingEquipment(baseVoltageMRID="bv1")
        cd = PBConductor(ce=ce2)
        acls = PBAcLineSegment(cd=cd, perLengthSequenceImpedanceMRID="plsi1")
        # PerLengthLineParameter.mrid = lambda self: self.lo.mRID
        # E   AttributeError: lo
        # network.add_from_pb(acls)

        # PowerTransformer
        ce3 = PBConductingEquipment(baseVoltageMRID="bv2")
        pt = PBPowerTransformer(ce=ce3)
        network.add_from_pb(pt)

        # Breaker
        ce4 = PBConductingEquipment(baseVoltageMRID="bv2")
        sw = PBSwitch(ce=ce4)
        psw = PBProtectedSwitch(sw=sw)
        br = PBBreaker(sw=psw)
        network.add_from_pb(br)

        # DOES THIS EXIST?
        # cust = PBCustomer()

        # OverheadWireInfo
        io_owi = PBIdentifiedObject(mRID="8", name="owi")
        ai2 = PBAssetInfo(io=io_owi)
        wi2 = PBWireInfo(ai=ai2)
        owi = PBOverheadWireInfo(wi=wi2)
        network.add_from_pb(owi)

        # UsagePoint
        io_up = PBIdentifiedObject(mRID="up1", name="up")
        up = PBUsagePoint(io=io_up)
        network.add_from_pb(up)

        # Meter
        ed = PBEndDevice(usagePointMRIDs=["up1"])
        me = PBMeter(ed=ed)
        network.add_from_pb(me)

        print(network.service)