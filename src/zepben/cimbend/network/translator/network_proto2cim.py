"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""


from dataclasses import dataclass

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

from zepben.cimbend.common.base_proto2cim import *
from zepben.cimbend.cim.iec61968.assetinfo.wire_info import CableInfo, OverheadWireInfo, WireInfo
from zepben.cimbend.cim.iec61968.assetinfo import WireMaterialKind
from zepben.cimbend.cim.iec61968.assets.asset import Asset, AssetContainer
from zepben.cimbend.cim.iec61968.assets.asset_info import AssetInfo
from zepben.cimbend.cim.iec61968.assets.asset_organisation_role import AssetOwner, AssetOrganisationRole
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

__all__ = ["positionpoint_from_pb", "towndetail_from_pb", "streetaddress_from_pb", "set_perlengthimpedance",
           "set_perlengthlineparameter", "set_acdcterminal", "set_tracedphases", "NetworkProtoToCim"]


# IEC61968 COMMON #
def positionpoint_from_pb(pb: PBPositionPoint) -> PositionPoint:
    return PositionPoint(pb.xPosition, pb.yPosition)


def towndetail_from_pb(pb: PBTownDetail) -> TownDetail:
    return TownDetail(name=pb.name, state_or_province=pb.stateOrProvince)


def streetaddress_from_pb(pb: PBStreetAddress) -> StreetAddress:
    return StreetAddress(pb.postalCode, towndetail_from_pb(pb.townDetail))


# MODEL #
def set_tracedphases(pb: PBTracedPhases, cim: TracedPhases, nominal_phases: PhaseCode):
    for phs in nominal_phases.single_phases:
        cim.set_normal(phase(pb.normalStatus, phs), direction(pb.normalStatus, phs), phs)
        cim.set_current(phase(pb.currentStatus, phs), direction(pb.currentStatus, phs), phs)


# IEC61970 CORE #
def set_acdcterminal(pb: PBAcDcTerminal, cim: AcDcTerminal):
    set_identifiedobject(pb.io, cim)


# IEC61970 WIRES #
def set_perlengthlineparameter(pb: PBPerLengthLineParameter, cim: PerLengthLineParameter):
    set_identifiedobject(pb.io, cim)


def set_perlengthimpedance(pb: PBPerLengthImpedance, cim: PerLengthImpedance):
    set_perlengthlineparameter(pb.lp, cim)


@dataclass
class NetworkProtoToCim(BaseProtoToCim):
    service: NetworkService

    # IEC61968 ASSET INFO #
    def add_cableinfo(self, pb: PBCableInfo):
        cim = CableInfo(pb.mrid())
        self.set_wire_info(pb.wi, cim)
        self.service.add(cim)

    def add_overheadwireinfo(self, pb: PBOverheadWireInfo):
        cim = OverheadWireInfo(pb.mrid())
        self.set_wire_info(pb.wi, cim)
        self.service.add(cim)

    def set_wire_info(self, pb: PBWireInfo, cim: WireInfo):
        self.set_asset_info(pb.ai, cim)
        cim.rated_current = pb.ratedCurrent
        cim.material = WireMaterialKind[PBWireMaterialKind.Name(pb.material)]

    # IEC61968 ASSETS #
    def set_asset(self, pb: PBAsset, cim: Asset):
        set_identifiedobject(pb.io, cim)
        for mrid in pb.organisationRoleMRIDs:
            cim.add_organisation_role(self._get(mrid, OrganisationRole, cim))

    def set_asset_container(self, pb: PBAssetContainer, cim: AssetContainer):
        self.set_asset(pb.at, cim)

    def set_asset_info(self, pb: PBAssetInfo, cim: AssetInfo):
        set_identifiedobject(pb.io, cim)

    def set_asset_organisation_role(self, pb: PBAssetOrganisationRole, cim: AssetOrganisationRole):
        self.set_organisation_role(getattr(pb, 'or'), cim)

    def add_asset_owner(self, pb: PBAssetOwner):
        cim = AssetOwner(pb.mrid())
        self.set_asset_organisation_role(pb.aor, cim)
        self.service.add(cim)

    # IEC61968 COMMON #
    def add_location(self, pb: PBLocation):
        cim = Location(pb.mrid())
        set_identifiedobject(pb.io, cim)
        cim.main_address = streetaddress_from_pb(pb.mainAddress) if pb.HasField('mainAddress') else None
        for point in pb.positionPoints:
            cim.add_point(positionpoint_from_pb(point))
        self.service.add(cim)

    # IEC61968 METERING #
    def set_end_device(self, pb: PBEndDevice, cim: EndDevice):
        self.set_asset_container(pb.ac, cim)
        for mrid in pb.usagePointMRIDs:
            cim.add_usage_point(self._get(mrid, UsagePoint, cim))
        if pb.customerMRID:
            cim.customer_mrid = pb.customerMRID
        cim.service_location = self._ensure_get(pb.serviceLocationMRID, Location, cim)

    def add_meter(self, pb: PBMeter):
        cim = Meter(pb.mrid())
        self.set_end_device(pb.ed, cim)
        self.service.add(cim)

    def add_usagepoint(self, pb: PBUsagePoint):
        cim = UsagePoint(pb.mrid())
        set_identifiedobject(pb.io, cim)
        cim.usage_point_location = self._ensure_get(pb.usagePointLocationMRID, Location, cim)
        for mrid in pb.equipmentMRIDs:
            cim.add_equipment(self._get(mrid, Equipment, cim))
        self.service.add(cim)

    # IEC61968 OPERATIONS #
    def add_operationalrestriction(self, pb: PBOperationalRestriction):
        cim = OperationalRestriction(pb.mrid())
        set_document(pb.doc, cim)
        for mrid in pb.equipmentMRIDs:
            cim.add_equipment(self._get(mrid, Equipment, cim))
        self.service.add(cim)

    # IEC61970 AUXILIARY EQUIPMENT #
    def set_auxiliaryequipment(self, pb: PBAuxiliaryEquipment, cim: AuxiliaryEquipment):
        self.set_equipment(pb.eq, cim)
        cim.terminal = self._ensure_get(pb.terminalMRID, Terminal, cim)

    def add_faultindicator(self, pb: PBFaultIndicator):
        cim = FaultIndicator(pb.mrid())
        self.set_auxiliaryequipment(pb.ae, cim)
        self.service.add(cim)

    # IEC61970 CORE #
    def add_basevoltage(self, pb: PBBaseVoltage):
        cim = BaseVoltage(pb.mrid())
        set_identifiedobject(pb.io, cim)
        self.service.add(cim)

    def set_conductingequipment(self, pb: PBConductingEquipment, cim: ConductingEquipment):
        self.set_equipment(pb.eq, cim)
        cim.base_voltage = self._ensure_get(pb.baseVoltageMRID, BaseVoltage, cim)
        for mrid in pb.terminalMRIDs:
            cim.add_terminal(self._get(mrid, Terminal, cim))

    def add_connectivitynode(self, pb: PBConnectivityNode):
        cim = self.service.add_connectivitynode(pb.mrid())
        set_identifiedobject(pb.io, cim)

    def set_connectivitynodecontainer(self, pb: PBConnectivityNodeContainer, cim: ConnectivityNodeContainer):
        self.set_powersystemresource(pb.psr, cim)

    def set_equipment(self, pb: PBEquipment, cim: Equipment):
        self.set_powersystemresource(pb.psr, cim)
        cim.in_service = pb.inService
        cim.normally_in_service = pb.normallyInService
        for mrid in pb.equipmentContainerMRIDs:
            cim.add_container(self._get(mrid, EquipmentContainer, cim))
        for mrid in pb.usagePointMRIDs:
            cim.add_usage_point(self._get(mrid, UsagePoint, cim))
        for mrid in pb.operationalRestrictionMRIDs:
            cim.add_restriction(self._get(mrid, OperationalRestriction, cim))

    def set_equipmentcontainer(self, pb: PBEquipmentContainer, cim: EquipmentContainer):
        self.set_connectivitynodecontainer(pb.cnc, cim)

        for mrid in pb.equipmentMRIDs:
            cim.add_equipment(self._get(mrid, Equipment, cim))

    def add_feeder(self, pb: PBFeeder):
        term = self._get(pb.normalHeadTerminalMRID, Terminal, pb.name_and_mrid())
        cim = Feeder(term, pb.mrid())
        self.set_equipmentcontainer(pb.ec, cim)
        cim.normal_energizing_substation = self._ensure_get(pb.normalEnergizingSubstationMRID, Substation,
                                                            pb.name_and_mrid())
        self.service.add(cim)

    def add_geographicalregion(self, pb: PBGeographicalRegion):
        cim = GeographicalRegion(pb.mrid())
        set_identifiedobject(pb.io, cim)
        for mrid in pb.subGeographicalRegionMRIDs:
            cim.add_sub_geographical_region(self._get(mrid, SubGeographicalRegion, cim))
        self.service.add(cim)

    def set_powersystemresource(self, pb: PBPowerSystemResource, cim: PowerSystemResource):
        set_identifiedobject(pb.io, cim)
        cim.location = self._ensure_get(pb.locationMRID, Location, cim)
        cim.num_controls = pb.numControls
        cim.num_measurements = pb.numMeasurements

    def add_site(self, pb: PBSite):
        cim = Site(pb.mrid())
        self.set_equipmentcontainer(pb.ec, cim)
        self.service.add(cim)

    def add_subgeographicalregion(self, pb: PBSubGeographicalRegion):
        cim = SubGeographicalRegion(pb.mrid())
        set_identifiedobject(pb.io, cim)
        cim.geographical_region = self._ensure_get(pb.geographicalRegionMRID, GeographicalRegion, cim)
        for mrid in pb.substationMRIDs:
            cim.add_substation(self._get(mrid, Substation, cim))
        self.service.add(cim)

    def add_substation(self, pb: PBSubstation):
        cim = Substation(pb.mrid())
        self.set_equipmentcontainer(pb.ec, cim)
        cim.sub_geographical_region = self._ensure_get(pb.subGeographicalRegionMRID, SubGeographicalRegion, cim)
        for mrid in pb.normalEnergizedFeederMRIDs:
            cim.add_feeder(self._get(mrid, Feeder, cim))

        self.service.add(cim)

    def add_terminal(self, pb: PBTerminal):
        ce = self._get(pb.conductingEquipmentMRID, ConductingEquipment, pb.name_and_mrid())
        cim = Terminal(ce, pb.mrid(), phases=PhaseCode[PBPhaseCode.Name(pb.phases)])
        set_acdcterminal(pb.ad, cim)
        set_tracedphases(pb.tracedPhases, cim.traced_phases, cim.phases)
        self.service.connect_by_mrid(cim, pb.connectivityNodeMRID)
        self.service.add(cim)

    # IEC61970 WIRES #
    def add_aclinesegment(self, pb: PBAcLineSegment):
        cim = AcLineSegment(pb.mrid())
        self.set_conductor(pb.cd, cim)
        cim.per_length_sequence_impedance = self._ensure_get(pb.perLengthSequenceImpedanceMRID,
                                                             PerLengthSequenceImpedance, cim)
        self.service.add(cim)

    def add_breaker(self, pb: PBBreaker):
        cim = Breaker(pb.mrid())
        self.set_protectedswitch(pb.sw, cim)
        self.service.add(cim)

    def set_conductor(self, pb: PBConductor, cim: Conductor):
        self.set_conductingequipment(pb.ce, cim)
        cim.length = pb.length
        cim.asset_info = self._ensure_get(pb.assetInfoMRID, WireInfo, cim)

    def set_connector(self, pb: PBConnector, cim: Connector):
        self.set_conductingequipment(pb.ce, cim)

    def add_disconnector(self, pb: PBDisconnector):
        cim = Disconnector(pb.mrid())
        self.set_switch(pb.sw, cim)
        self.service.add(cim)

    def set_energyconnection(self, pb: PBEnergyConnection, cim: EnergyConnection):
        self.set_conductingequipment(pb.ce, cim)

    def add_energyconsumer(self, pb: PBEnergyConsumer):
        cim = EnergyConsumer(pb.mrid())
        self.set_energyconnection(pb.ec, cim)
        for mrid in pb.energyConsumerPhasesMRIDs:
            cim.add_phase(self._get(mrid, EnergyConsumerPhase, cim))
        cim.customer_count = pb.customerCount
        cim.grounded = pb.grounded
        cim.p = pb.p
        cim.p_fixed = pb.pFixed
        cim.phase_connection = PhaseShuntConnectionKind[PBPhaseShuntConnectionKind.Name(pb.phaseConnection)]
        cim.q = pb.q
        cim.q_fixed = pb.qFixed
        self.service.add(cim)

    def add_energyconsumerphase(self, pb: PBEnergyConsumerPhase):
        ec = self._get(pb.energyConsumerMRID, EnergyConsumer, pb.name_and_mrid())
        cim = EnergyConsumerPhase(ec, pb.mrid(), phase=SinglePhaseKind[PBSinglePhaseKind.Name(pb.phase)])
        self.set_powersystemresource(pb.psr, cim)
        cim.p = pb.p
        cim.p_fixed = pb.pFixed
        cim.q = pb.q
        cim.q_fixed = pb.qFixed
        self.service.add(cim)

    def add_energysource(self, pb: PBEnergySource):
        cim = EnergySource(pb.mrid())
        self.set_energyconnection(pb.ec, cim)
        for mrid in pb.energySourcePhasesMRIDs:
            cim.add_phase(self._get(mrid, EnergySourcePhase, cim))
        cim.active_power = pb.activePower
        cim.reactive_power = pb.reactivePower
        cim.voltage_angle = pb.voltageAngle
        cim.voltage_magnitude = pb.voltageMagnitude
        cim.r = pb.r
        cim.x = pb.x
        cim.p_max = pb.pMax
        cim.p_min = pb.pMin
        cim.r0 = pb.r0
        cim.rn = pb.rn
        cim.x0 = pb.x0
        cim.xn = pb.xn
        self.service.add(cim)

    def add_energysourcephase(self, pb: PBEnergySourcePhase):
        es = self._get(pb.energySourceMRID, EnergySource, pb.name_and_mrid())
        cim = EnergySourcePhase(es, pb.mrid(), phase=SinglePhaseKind[PBSinglePhaseKind.Name(pb.phase)])
        self.set_powersystemresource(pb.psr, cim)
        self.service.add(cim)

    def add_fuse(self, pb: PBFuse):
        cim = Fuse(pb.mrid())
        self.set_switch(pb.sw, cim)
        self.service.add(cim)

    def add_jumper(self, pb: PBJumper):
        cim = Jumper(pb.mrid())
        self.set_switch(pb.sw, cim)
        self.service.add(cim)

    def add_junction(self, pb: PBJunction):
        cim = Junction(pb.mrid())
        self.set_connector(pb.cn, cim)
        self.service.add(cim)

    def add_linearshuntcompensator(self, pb: PBLinearShuntCompensator):
        cim = LinearShuntCompensator(pb.mrid())
        self.set_shuntcompensator(pb.sc, cim)
        cim.b0_per_section = pb.b0PerSection
        cim.b_per_section = pb.bPerSection
        cim.g0_per_section = pb.g0PerSection
        cim.g_per_section = pb.gPerSection
        self.service.add(cim)

    def add_perlengthsequenceimpedance(self, pb: PBPerLengthSequenceImpedance):
        cim = PerLengthSequenceImpedance(pb.mrid())
        set_perlengthimpedance(pb.pli, cim)
        cim.r = pb.r
        cim.x = pb.x
        cim.r0 = pb.r0
        cim.x0 = pb.x0
        cim.bch = pb.bch
        cim.gch = pb.gch
        cim.b0ch = pb.b0Ch
        cim.g0ch = pb.b0Ch
        self.service.add(cim)

    def add_powertransformer(self, pb: PBPowerTransformer):
        cim = PowerTransformer(pb.mrid())
        self.set_conductingequipment(pb.ce, cim)
        for mrid in pb.powerTransformerEndMRIDs:
            cim.add_end(self._get(mrid, PowerTransformerEnd, cim))
        cim.vector_group = VectorGroup[PBVectorGroup.Name(pb.vectorGroup)]
        self.service.add(cim)

    def add_powertransformerend(self, pb: PBPowerTransformerEnd):
        pt = self._get(pb.powerTransformerMRID, PowerTransformer, pb.name_and_mrid())
        cim = PowerTransformerEnd(pt, pb.mrid())
        self.set_transformerend(pb.te, cim)
        cim.rated_s = pb.ratedS
        cim.rated_u = pb.ratedU
        cim.r = pb.r
        cim.r0 = pb.r0
        cim.x = pb.x
        cim.x0 = pb.x0
        cim.connection_kind = WindingConnection[PBWindingConnection.Name(pb.connectionKind)]
        cim.b = pb.b
        cim.b0 = pb.b0
        cim.g = pb.g
        cim.g0 = pb.g0
        cim.phase_angle_clock = pb.phaseAngleClock
        self.service.add(cim)

    def set_protectedswitch(self, pb: PBProtectedSwitch, cim: ProtectedSwitch):
        self.set_switch(pb.sw, cim)

    def add_ratiotapchanger(self, pb: PBRatioTapChanger):
        cim = RatioTapChanger(pb.mrid())
        self.set_tapchanger(pb.tc, cim)
        cim.step_voltage_increment = pb.stepVoltageIncrement
        self.service.add(cim)

    def add_recloser(self, pb: PBRecloser):
        cim = Recloser(pb.mrid())
        self.set_protectedswitch(pb.sw, cim)
        self.service.add(cim)

    def set_regulatingcondeq(self, pb: PBRegulatingCondEq, cim: RegulatingCondEq):
        self.set_energyconnection(pb.ec, cim)
        cim.control_enabled = pb.control_enabled

    def set_shuntcompensator(self, pb: PBShuntCompensator, cim: ShuntCompensator):
        self.set_regulatingcondeq(pb.rce, cim)
        cim.sections = pb.sections
        cim.grounded = pb.grounded
        cim.nom_u = pb.nomU
        cim.phase_connection = PhaseShuntConnectionKind[PBPhaseShuntConnectionKind.Name(pb.phaseConnection)]

    def set_switch(self, pb: PBSwitch, cim: Switch):
        self.set_conductingequipment(pb.ce, cim)
        cim.set_normally_open(pb.normalOpen)
        cim.set_open(pb.open)

    def set_tapchanger(self, pb: PBTapChanger, cim: TapChanger):
        self.set_powersystemresource(pb.psr, cim)
        cim.high_step = pb.highStep
        cim.low_step = pb.lowStep
        cim.step = pb.step
        cim.neutral_step = pb.neutralStep
        cim.neutral_u = pb.neutralU
        cim.normal_step = pb.normalStep
        cim.control_enabled = pb.controlEnabled

    def set_transformerend(self, pb: PBTransformerEnd, cim: TransformerEnd):
        set_identifiedobject(pb.io, cim)
        cim.terminal = self._ensure_get(pb.terminalMRID, Terminal, cim)
        cim.base_voltage = self._ensure_get(pb.baseVoltageMRID, BaseVoltage, cim)
        cim.ratio_tap_changer = self._ensure_get(pb.ratioTapChangerMRID, RatioTapChanger, cim)
        cim.grounded = pb.grounded
        cim.r_ground = pb.rGround
        cim.x_ground = pb.xGround
