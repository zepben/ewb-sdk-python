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
from zepben.protobuf.cim.iec61968.assets.AssetContainer_pb2 import AssetContainer as PBAssetContainer
from zepben.protobuf.cim.iec61968.assets.AssetInfo_pb2 import AssetInfo as PBAssetInfo
from zepben.protobuf.cim.iec61968.assets.AssetOrganisationRole_pb2 import \
    AssetOrganisationRole as PBAssetOrganisationRole
from zepben.protobuf.cim.iec61968.assets.AssetOwner_pb2 import AssetOwner as PBAssetOwner
from zepben.protobuf.cim.iec61968.assets.Asset_pb2 import Asset as PBAsset
from zepben.protobuf.cim.iec61968.assets.Pole_pb2 import Pole as  PBPole
from zepben.protobuf.cim.iec61968.assets.Streetlight_pb2 import Streetlight as PBStreetlight
from zepben.protobuf.cim.iec61968.assets.StreetlightLampKind_pb2 import StreetlightLampKind as PBStreetlightLampKind
from zepben.protobuf.cim.iec61968.assets.Structure_pb2 import Structure as PBStructure
from zepben.protobuf.cim.iec61968.common.Location_pb2 import Location as PBLocation
from zepben.protobuf.cim.iec61968.common.PositionPoint_pb2 import PositionPoint as PBPositionPoint
from zepben.protobuf.cim.iec61968.common.StreetAddress_pb2 import StreetAddress as PBStreetAddress
from zepben.protobuf.cim.iec61968.common.TownDetail_pb2 import TownDetail as PBTownDetail
from zepben.protobuf.cim.iec61968.metering.EndDevice_pb2 import EndDevice as PBEndDevice
from zepben.protobuf.cim.iec61968.metering.Meter_pb2 import Meter as PBMeter
from zepben.protobuf.cim.iec61968.metering.UsagePoint_pb2 import UsagePoint as PBUsagePoint
from zepben.protobuf.cim.iec61968.operations.OperationalRestriction_pb2 import \
    OperationalRestriction as PBOperationalRestriction
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.AuxiliaryEquipment_pb2 import \
    AuxiliaryEquipment as PBAuxiliaryEquipment
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.FaultIndicator_pb2 import FaultIndicator as PBFaultIndicator
from zepben.protobuf.cim.iec61970.base.core.AcDcTerminal_pb2 import AcDcTerminal as PBAcDcTerminal
from zepben.protobuf.cim.iec61970.base.core.BaseVoltage_pb2 import BaseVoltage as PBBaseVoltage
from zepben.protobuf.cim.iec61970.base.core.ConductingEquipment_pb2 import ConductingEquipment as PBConductingEquipment
from zepben.protobuf.cim.iec61970.base.core.ConnectivityNodeContainer_pb2 import \
    ConnectivityNodeContainer as PBConnectivityNodeContainer
from zepben.protobuf.cim.iec61970.base.core.ConnectivityNode_pb2 import ConnectivityNode as PBConnectivityNode
from zepben.protobuf.cim.iec61970.base.core.EquipmentContainer_pb2 import EquipmentContainer as PBEquipmentContainer
from zepben.protobuf.cim.iec61970.base.core.Equipment_pb2 import Equipment as PBEquipment
from zepben.protobuf.cim.iec61970.base.core.Feeder_pb2 import Feeder as PBFeeder
from zepben.protobuf.cim.iec61970.base.core.GeographicalRegion_pb2 import GeographicalRegion as PBGeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.PhaseCode_pb2 import PhaseCode as PBPhaseCode
from zepben.protobuf.cim.iec61970.base.core.PowerSystemResource_pb2 import PowerSystemResource as PBPowerSystemResource
from zepben.protobuf.cim.iec61970.base.core.Site_pb2 import Site as PBSite
from zepben.protobuf.cim.iec61970.base.core.SubGeographicalRegion_pb2 import \
    SubGeographicalRegion as PBSubGeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.Substation_pb2 import Substation as PBSubstation
from zepben.protobuf.cim.iec61970.base.core.Terminal_pb2 import Terminal as PBTerminal
from zepben.protobuf.cim.iec61970.base.wires.AcLineSegment_pb2 import AcLineSegment as PBAcLineSegment
from zepben.protobuf.cim.iec61970.base.wires.Breaker_pb2 import Breaker as PBBreaker
from zepben.protobuf.cim.iec61970.base.wires.Conductor_pb2 import Conductor as PBConductor
from zepben.protobuf.cim.iec61970.base.wires.Connector_pb2 import Connector as PBConnector
from zepben.protobuf.cim.iec61970.base.wires.Disconnector_pb2 import Disconnector as PBDisconnector
from zepben.protobuf.cim.iec61970.base.wires.EnergyConnection_pb2 import EnergyConnection as PBEnergyConnection
from zepben.protobuf.cim.iec61970.base.wires.EnergyConsumerPhase_pb2 import EnergyConsumerPhase as PBEnergyConsumerPhase
from zepben.protobuf.cim.iec61970.base.wires.EnergyConsumer_pb2 import EnergyConsumer as PBEnergyConsumer
from zepben.protobuf.cim.iec61970.base.wires.EnergySourcePhase_pb2 import EnergySourcePhase as PBEnergySourcePhase
from zepben.protobuf.cim.iec61970.base.wires.EnergySource_pb2 import EnergySource as PBEnergySource
from zepben.protobuf.cim.iec61970.base.wires.Fuse_pb2 import Fuse as PBFuse
from zepben.protobuf.cim.iec61970.base.wires.Jumper_pb2 import Jumper as PBJumper
from zepben.protobuf.cim.iec61970.base.wires.Junction_pb2 import Junction as PBJunction
from zepben.protobuf.cim.iec61970.base.wires.LinearShuntCompensator_pb2 import \
    LinearShuntCompensator as PBLinearShuntCompensator
from zepben.protobuf.cim.iec61970.base.wires.PerLengthImpedance_pb2 import PerLengthImpedance as PBPerLengthImpedance
from zepben.protobuf.cim.iec61970.base.wires.PerLengthLineParameter_pb2 import \
    PerLengthLineParameter as PBPerLengthLineParameter
from zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance_pb2 import \
    PerLengthSequenceImpedance as PBPerLengthSequenceImpedance
from zepben.protobuf.cim.iec61970.base.wires.PhaseShuntConnectionKind_pb2 import \
    PhaseShuntConnectionKind as PBPhaseShuntConnectionKind
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformerEnd_pb2 import PowerTransformerEnd as PBPowerTransformerEnd
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformer_pb2 import PowerTransformer as PBPowerTransformer
from zepben.protobuf.cim.iec61970.base.wires.ProtectedSwitch_pb2 import ProtectedSwitch as PBProtectedSwitch
from zepben.protobuf.cim.iec61970.base.wires.RatioTapChanger_pb2 import RatioTapChanger as PBRatioTapChanger
from zepben.protobuf.cim.iec61970.base.wires.Recloser_pb2 import Recloser as PBRecloser
from zepben.protobuf.cim.iec61970.base.wires.RegulatingCondEq_pb2 import RegulatingCondEq as PBRegulatingCondEq
from zepben.protobuf.cim.iec61970.base.wires.ShuntCompensator_pb2 import ShuntCompensator as PBShuntCompensator
from zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind_pb2 import SinglePhaseKind as PBSinglePhaseKind
from zepben.protobuf.cim.iec61970.base.wires.Switch_pb2 import Switch as PBSwitch
from zepben.protobuf.cim.iec61970.base.wires.TapChanger_pb2 import TapChanger as PBTapChanger
from zepben.protobuf.cim.iec61970.base.wires.TransformerEnd_pb2 import TransformerEnd as PBTransformerEnd
from zepben.protobuf.cim.iec61970.base.wires.VectorGroup_pb2 import VectorGroup as PBVectorGroup
from zepben.protobuf.cim.iec61970.base.wires.WindingConnection_pb2 import WindingConnection as PBWindingConnection
from zepben.protobuf.network.model.TracedPhases_pb2 import TracedPhases as PBTracedPhases

from zepben.cimbend.common.translator.base_proto2cim import *
from zepben.cimbend.cim.iec61968.assetinfo.wire_info import CableInfo, OverheadWireInfo, WireInfo
from zepben.cimbend.cim.iec61968.assetinfo import WireMaterialKind
from zepben.cimbend.cim.iec61968.assets.asset import Asset, AssetContainer
from zepben.cimbend.cim.iec61968.assets.asset_info import AssetInfo
from zepben.cimbend.cim.iec61968.assets.asset_organisation_role import AssetOwner, AssetOrganisationRole
from zepben.cimbend.cim.iec61968.assets.pole import Pole
from zepben.cimbend.cim.iec61968.assets.streetlight import Streetlight, StreetlightLampKind
from zepben.cimbend.cim.iec61968.assets.structure import Structure
from zepben.cimbend.cim.iec61968.common.location import StreetAddress, TownDetail, PositionPoint, Location
from zepben.cimbend.cim.iec61968.common.organisation_role import OrganisationRole
from zepben.cimbend.cim.iec61968.metering import EndDevice, UsagePoint, Meter
from zepben.cimbend.cim.iec61968.operations.operational_restriction import OperationalRestriction
from zepben.cimbend.cim.iec61970.base.auxiliaryequipment.auxiliary_equipment import AuxiliaryEquipment, FaultIndicator
from zepben.cimbend.cim.iec61970.base.core import BaseVoltage
from zepben.cimbend.cim.iec61970.base.core import ConductingEquipment
from zepben.cimbend.cim.iec61970.base.core.connectivity_node_container import ConnectivityNodeContainer
from zepben.cimbend.cim.iec61970.base.core.equipment import Equipment
from zepben.cimbend.cim.iec61970.base.core.equipment_container import EquipmentContainer, Feeder, Site
from zepben.cimbend.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.cimbend.cim.iec61970.base.core import PowerSystemResource
from zepben.cimbend.cim.iec61970.base.core.regions import GeographicalRegion, SubGeographicalRegion
from zepben.cimbend.cim.iec61970.base.core import Substation
from zepben.cimbend.cim.iec61970.base.core.terminal import Terminal, AcDcTerminal
from zepben.cimbend.cim.iec61970.base.wires import Conductor, AcLineSegment
from zepben.cimbend.cim.iec61970.base.wires import Junction, Connector
from zepben.cimbend.cim.iec61970.base.wires import EnergyConnection, RegulatingCondEq
from zepben.cimbend.cim.iec61970.base.wires import EnergyConsumer, EnergyConsumerPhase
from zepben.cimbend.cim.iec61970.base.wires import EnergySource
from zepben.cimbend.cim.iec61970.base.wires import EnergySourcePhase
from zepben.cimbend.cim.iec61970.base.wires import PerLengthSequenceImpedance, PerLengthLineParameter, \
    PerLengthImpedance
from zepben.cimbend.cim.iec61970.base.wires import PhaseShuntConnectionKind
from zepben.cimbend.cim.iec61970.base.wires.power_transformer import PowerTransformer, PowerTransformerEnd, RatioTapChanger, \
    TapChanger, TransformerEnd
from zepben.cimbend.cim.iec61970.base.wires import LinearShuntCompensator, ShuntCompensator
from zepben.cimbend.cim.iec61970.base.wires import SinglePhaseKind
from zepben.cimbend.cim.iec61970.base.wires.switch import Breaker, Disconnector, Fuse, Jumper, ProtectedSwitch, Recloser, \
    Switch
from zepben.cimbend.cim.iec61970.base.wires import VectorGroup
from zepben.cimbend.cim.iec61970.base.wires import WindingConnection
from zepben.cimbend.network.network import NetworkService
from zepben.cimbend.phases import TracedPhases, direction, phase

from zepben.cimbend.network.translator.network_proto2cim import NetworkProtoToCim


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