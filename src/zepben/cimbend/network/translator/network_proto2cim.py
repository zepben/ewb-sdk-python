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
from zepben.protobuf.cim.iec61968.assets.AssetContainer_pb2 import AssetContainer as PBAssetContainer
from zepben.protobuf.cim.iec61968.assets.AssetInfo_pb2 import AssetInfo as PBAssetInfo
from zepben.protobuf.cim.iec61968.assets.AssetOrganisationRole_pb2 import \
    AssetOrganisationRole as PBAssetOrganisationRole
from zepben.protobuf.cim.iec61968.assets.AssetOwner_pb2 import AssetOwner as PBAssetOwner
from zepben.protobuf.cim.iec61968.assets.Asset_pb2 import Asset as PBAsset
from zepben.protobuf.cim.iec61968.assets.Pole_pb2 import Pole as PBPole
from zepben.protobuf.cim.iec61968.assets.Streetlight_pb2 import Streetlight as PBStreetlight
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
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformerEnd_pb2 import PowerTransformerEnd as PBPowerTransformerEnd
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformer_pb2 import PowerTransformer as PBPowerTransformer
from zepben.protobuf.cim.iec61970.base.wires.ProtectedSwitch_pb2 import ProtectedSwitch as PBProtectedSwitch
from zepben.protobuf.cim.iec61970.base.wires.RatioTapChanger_pb2 import RatioTapChanger as PBRatioTapChanger
from zepben.protobuf.cim.iec61970.base.wires.Recloser_pb2 import Recloser as PBRecloser
from zepben.protobuf.cim.iec61970.base.wires.RegulatingCondEq_pb2 import RegulatingCondEq as PBRegulatingCondEq
from zepben.protobuf.cim.iec61970.base.wires.ShuntCompensator_pb2 import ShuntCompensator as PBShuntCompensator
from zepben.protobuf.cim.iec61970.base.wires.Switch_pb2 import Switch as PBSwitch
from zepben.protobuf.cim.iec61970.base.wires.TapChanger_pb2 import TapChanger as PBTapChanger
from zepben.protobuf.cim.iec61970.base.wires.TransformerEnd_pb2 import TransformerEnd as PBTransformerEnd
from zepben.protobuf.network.model.TracedPhases_pb2 import TracedPhases as PBTracedPhases

from zepben.cimbend.common.base_proto2cim import *
from zepben.cimbend.cim.iec61968.assetinfo.wire_info import CableInfo, OverheadWireInfo, WireInfo
from zepben.cimbend.cim.iec61968.assetinfo import WireMaterialKind
from zepben.cimbend.cim.iec61968.assets.asset import Asset, AssetContainer
from zepben.cimbend.cim.iec61968.assets.asset_info import AssetInfo
from zepben.cimbend.cim.iec61968.assets.asset_organisation_role import AssetOwner, AssetOrganisationRole
from zepben.cimbend.cim.iec61968.assets.pole import Pole
from zepben.cimbend.cim.iec61968.assets.streetlight import Streetlight, StreetlightLampKind
from zepben.cimbend.cim.iec61968.assets.structure import Structure
from zepben.cimbend.cim.iec61968.common.location import StreetAddress, TownDetail, PositionPoint, Location
from zepben.cimbend.cim.iec61968.metering import EndDevice, UsagePoint, Meter
from zepben.cimbend.cim.iec61968.operations.operational_restriction import OperationalRestriction
from zepben.cimbend.cim.iec61970.base.auxiliaryequipment.auxiliary_equipment import AuxiliaryEquipment, FaultIndicator
from zepben.cimbend.cim.iec61970.base.core import BaseVoltage
from zepben.cimbend.cim.iec61970.base.core import ConductingEquipment
from zepben.cimbend.cim.iec61970.base.core.connectivity_node_container import ConnectivityNodeContainer
from zepben.cimbend.cim.iec61970.base.core.equipment import Equipment
from zepben.cimbend.cim.iec61970.base.core.equipment_container import EquipmentContainer, Feeder, Site
from zepben.cimbend.cim.iec61970.base.core.phase_code import PhaseCode, phasecode_by_id
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
from zepben.cimbend.cim.iec61970.base.wires.power_transformer import PowerTransformer, PowerTransformerEnd, \
    RatioTapChanger, \
    TapChanger, TransformerEnd
from zepben.cimbend.cim.iec61970.base.wires import LinearShuntCompensator, ShuntCompensator
from zepben.cimbend.cim.iec61970.base.wires.single_phase_kind import phasekind_by_id
from zepben.cimbend.cim.iec61970.base.wires.switch import Breaker, Disconnector, Fuse, Jumper, ProtectedSwitch, \
    Recloser, \
    Switch
from zepben.cimbend.cim.iec61970.base.wires import VectorGroup
from zepben.cimbend.cim.iec61970.base.wires import WindingConnection
from zepben.cimbend.network.network import NetworkService
from zepben.cimbend.phases import TracedPhases, direction, phase

from zepben.cimbend.common import resolver

__all__ = ["positionpoint_from_pb", "towndetail_from_pb", "streetaddress_from_pb", "set_perlengthimpedance",
           "set_perlengthlineparameter", "set_acdcterminal", "set_tracedphases", "NetworkProtoToCim"]


### IEC61968 ASSET INFO
def cableinfo_to_cim(pb: PBCableInfo, network_service: NetworkService):
    cim = CableInfo(pb.mrid())
    wireinfo_to_cim(pb.wi, cim, network_service)


def overheadwireinfo_to_cim(pb: PBOverheadWireInfo, network_service: NetworkService):
    cim = OverheadWireInfo(pb.mrid())
    wireinfo_to_cim(pb.wi, cim, network_service)


def wireinfo_to_cim(pb: PBWireInfo, cim: WireInfo, network_service: NetworkService):
    cim.rated_current = pb.ratedCurrent
    cim.material = WireMaterialKind(pb.material)
    assetinfo_to_cim(pb.ai, cim, network_service)


PBCableInfo.to_cim = cableinfo_to_cim
PBOverheadWireInfo.to_cim = overheadwireinfo_to_cim
PBWireInfo.to_cim = wireinfo_to_cim


### IEC61968 ASSETS
def asset_to_cim(pb: PBAsset, cim: Asset, network_service: NetworkService):
    network_service.resolve_or_defer_reference(resolver.at_location(cim), pb.locationMRID)
    for mrid in pb.organisationRoleMRIDs:
        network_service.resolve_or_defer_reference(resolver.organisation_roles(cim), mrid)
    set_identifiedobject(pb.io, cim, network_service)


def assetcontainer_to_cim(pb: PBAssetContainer, cim: AssetContainer, network_service: NetworkService):
    asset_to_cim(pb.at, cim, network_service)


def assetinfo_to_cim(pb: PBAssetInfo, cim: AssetInfo, network_service: NetworkService):
    set_identifiedobject(pb.io, cim, network_service)


def assetorganisationrole_to_cim(pb: PBAssetOrganisationRole, cim: AssetOrganisationRole,
                                 network_service: NetworkService):
    organisationrole_to_cim(getattr(pb, 'or'), cim, network_service)


def assetowner_to_cim(pb: PBAssetOwner, network_service: NetworkService):
    cim = AssetOwner(pb.mrid())
    assetorganisationrole_to_cim(pb.aor, cim, network_service)


def pole_to_cim(pb: PBPole, network_service: NetworkService):
    cim = Pole(pb.mrid())
    for mrid in pb.streetlightMRIDs:
        network_service.resolve_or_defer_reference(resolver.streetlights(cim), mrid)
    structure_to_cim(pb.st, cim, network_service)


def streetlight_to_cim(pb: PBStreetlight, network_service: NetworkService):
    cim = Streetlight(pb.mrid())
    network_service.resolve_or_defer_reference(resolver.pole(cim), pb.poleMRID)
    cim.light_rating = pb.lightRating
    cim.lamp_kind = StreetlightLampKind(pb.lampKind)
    asset_to_cim(pb.at, cim, network_service)


def structure_to_cim(pb: PBStructure, cim: Structure, network_service: NetworkService):
    assetcontainer_to_cim(pb.ac, cim, network_service)


PBAsset.to_cim = asset_to_cim
PBAssetContainer.to_cim = assetcontainer_to_cim
PBAssetInfo.to_cim = assetinfo_to_cim
PBAssetOrganisationRole.to_cim = assetorganisationrole_to_cim
PBAssetOwner.to_cim = assetowner_to_cim
PBPole.to_cim = pole_to_cim
PBStreetlight.to_cim = streetlight_to_cim
PBStructure.to_cim = structure_to_cim


### IEC61968 COMMON

def location_to_cim(pb: PBLocation, network_service: NetworkService) -> Location:
    cim = Location(pb.mrid())
    cim.main_address = streetaddress_from_pb(pb.mainAddress) if pb.HasField('mainAddress') else None
    for point in pb.positionPoints:
        cim.add_point(positionpoint_from_pb(point))
    set_identifiedobject(pb.io, cim, network_service)


def positionpoint_to_cim(pb: PBPositionPoint) -> PositionPoint:
    return PositionPoint(pb.xPosition, pb.yPosition)


def towndetail_to_cim(pb: PBTownDetail) -> TownDetail:
    return TownDetail(name=pb.name, state_or_province=pb.stateOrProvince)


def streetaddress_to_cim(pb: PBStreetAddress) -> StreetAddress:
    return StreetAddress(pb.postalCode, towndetail_from_pb(pb.townDetail))


PBLocation.to_cim = location_to_cim
PBPositionPoint.to_cim = positionpoint_to_cim
PBTownDetail.to_cim = towndetail_to_cim
PBStreetAddress.to_cim = streetaddress_to_cim


### IEC61968 METERING

def enddevice_to_cim(pb: PBEndDevice, cim: EndDevice, network_service: NetworkService):
    for mrid in pb.usagePointMRIDs:
        network_service.resolve_or_defer_reference(resolver.ed_usage_points(cim), mrid)
    if pb.customerMRID:
        cim.customer_mrid = pb.customerMRID
        network_service.resolve_or_defer_reference(resolver.service_location(cim), pb.serviceLocationMRID)
    assetcontainer_to_cim(pb.ac, cim, network_service)


def meter_to_cim(pb: PBMeter, network_service: NetworkService):
    cim = Meter(pb.mrid())
    enddevice_to_cim(pb.ed, cim, network_service)


def usagepoint_to_cim(pb: PBUsagePoint, network_service: NetworkService):
    cim = UsagePoint(pb.mrid())
    network_service.resolve_or_defer_reference(resolver.usage_point_location(cim), pb.usagePointLocationMRID)
    for mrid in pb.equipmentMRIDs:
        network_service.resolve_or_defer_reference(resolver.up_equipment(cim), mrid)
    set_identifiedobject(pb.io, cim, network_service)


PBEndDevice.to_cim = enddevice_to_cim
PBMeter.to_cim = meter_to_cim
PBUsagePoint.to_cim = usagepoint_to_cim


### IEC61968 OPERATIONS
def operationalrestriction_to_cim(pb: PBOperationalRestriction, network_service: NetworkService):
    cim = OperationalRestriction(pb.mrid())
    for mrid in pb.equipmentMRIDs:
        network_service.resolve_or_defer_reference(resolver.or_equipment(cim), mrid)
    set_document(pb.doc, cim, network_service)


PBOperationalRestriction.to_cim = operationalrestriction_to_cim


### IEC61970 AUXILIARY EQUIPMENT
def auxiliaryequipment_to_cim(pb: PBAuxiliaryEquipment, cim: AuxiliaryEquipment, network_service: NetworkService):
    network_service.resolve_or_defer_reference(resolver.ae_terminal(cim), pb.terminalMRID)
    equipment_to_cim(pb.eq, cim, network_service)


def faultindicator_to_cim(pb: PBFaultIndicator, network_service: NetworkService):
    cim = FaultIndicator(pb.mrid())
    auxiliaryequipment_to_cim(pb.ae, cim, network_service)


PBAuxiliaryEquipment.to_cim = auxiliaryequipment_to_cim
PBFaultIndicator.to_cim = faultindicator_to_cim


### IEC61970 CORE
def acdcterminal_to_cim(pb: PBAcDcTerminal, cim: AcDcTerminal, network_service: NetworkService):
    set_identifiedobject(pb.io, cim, network_service)


def basevoltage_to_cim(pb: PBBaseVoltage, network_service: NetworkService):
    cim = BaseVoltage(pb.mrid())
    set_identifiedobject(pb.io, cim, network_service)


def conductingequipment_to_cim(pb: PBConductingEquipment, cim: ConductingEquipment, network_service: NetworkService):
    network_service.resolve_or_defer_reference(resolver.ce_base_voltage(cim), pb.baseVoltageMRID)
    for mrid in pb.terminalMRIDs:
        network_service.resolve_or_defer_reference(resolver.ce_terminals(cim), mrid)
    equipment_to_cim(pb.eq, cim, network_service)


def connectivitynode_to_cim(pb: PBConnectivityNode, network_service: NetworkService):
    cim = network_service.add_connectivitynode(pb.mrid())
    for mrid in pb.terminalMRIDs:
        network_service.resolve_or_defer_reference(resolver.cn_terminals(cim), mrid)
    set_identifiedobject(pb.io, cim, network_service)


def connectivitynodecontainer_to_cim(pb: PBConnectivityNodeContainer, cim: ConnectivityNodeContainer,
                                     network_service: NetworkService):
    powersystemresource_to_cim(pb.psr, cim, network_service)


def equipment_to_cim(pb: PBEquipment, cim: Equipment, network_service: NetworkService):
    cim.in_service = pb.inService
    cim.normally_in_service = pb.normallyInService
    for mrid in pb.equipmentContainerMRIDs:
        network_service.resolve_or_defer_reference(resolver.containers(cim), mrid)
    for mrid in pb.usagePointMRIDs:
        network_service.resolve_or_defer_reference(resolver.eq_usage_points(cim), mrid)
    for mrid in pb.operationalRestrictionMRIDs:
        network_service.resolve_or_defer_reference(resolver.operational_restrictions(cim), mrid)
    for mrid in pb.currentFeederMRIDs:
        network_service.resolve_or_defer_reference(resolver.current_feeders(cim), mrid)
    powersystemresource_to_cim(pb.psr, cim, network_service)


def equipmentcontainer_to_cim(pb: PBEquipmentContainer, cim: EquipmentContainer, network_service: NetworkService):
    for mrid in pb.equipmentMRIDs:
        network_service.resolve_or_defer_reference(resolver.ec_equipment(cim), mrid)
    connectivitynodecontainer_to_cim(pb.cnc, cim, network_service)


def feeder_to_cim(pb: PBFeeder, network_service: NetworkService):
    cim = Feeder(mrid=pb.mrid())
    network_service.resolve_or_defer_reference(resolver.normal_head_terminal(cim), pb.normalHeadTerminalMRID)
    network_service.resolve_or_defer_reference(resolver.normal_energizing_substation(cim),
                                               pb.normalEnergizingSubstationMRID)
    equipmentcontainer_to_cim(pb.ec, cim, network_service)


def geographicalregion_to_cim(pb: PBGeographicalRegion, network_service: NetworkService):
    cim = GeographicalRegion(pb.mrid())
    for mrid in pb.subGeographicalRegionMRIDs:
        network_service.resolve_or_defer_reference(resolver.sub_geographical_regions(cim), mrid)
    set_identifiedobject(pb.io, cim, network_service)


def powersystemresource_to_cim(pb: PBPowerSystemResource, cim: PowerSystemResource, network_service: NetworkService):
    network_service.resolve_or_defer_reference(resolver.psr_location(cim), pb.locationMRID)
    set_identifiedobject(pb.io, cim, network_service)


def site_to_cim(pb: PBSite, network_service: NetworkService):
    cim = Site(pb.mrid())
    equipmentcontainer_to_cim(pb.ec, cim, network_service)


def subgeographicalregion_to_cim(pb: PBSubGeographicalRegion, network_service: NetworkService):
    cim = SubGeographicalRegion(pb.mrid())
    network_service.resolve_or_defer_reference(resolver.geographical_region(cim), pb.geographicalRegionMRID)
    for mrid in pb.substationMRIDs:
        network_service.resolve_or_defer_reference(resolver.substations(cim), mrid)
    set_identifiedobject(pb.io, cim, network_service)


def substation_to_cim(pb: PBSubstation, network_service: NetworkService):
    cim = Substation(pb.mrid())
    network_service.resolve_or_defer_reference(resolver.sub_geographical_region(cim), pb.subGeographicalRegionMRID)
    for mrid in pb.normalEnergizedFeederMRIDs:
        network_service.resolve_or_defer_reference(resolver.normal_energizing_feeders(cim), mrid)
    equipmentcontainer_to_cim(pb.ec, cim, network_service)


def terminal_to_cim(pb: PBTerminal, network_service: NetworkService):
    cim = Terminal(mrid=pb.mrid(), phases=phasecode_by_id(pb.phases))
    network_service.resolve_or_defer_reference(resolver.conducting_equipment(cim), pb.conductingEquipmentMRID)
    set_tracedphases(pb.tracedPhases, cim.traced_phases, cim.phases)
    network_service.resolve_or_defer_reference(resolver.connectivity_node(cim), pb.connectivityNodeMRID)
    acdcterminal_to_cim(pb.ad, cim, network_service)


PBAcDcTerminal.to_cim = acdcterminal_to_cim
PBBaseVoltage.to_cim = basevoltage_to_cim
PBConductingEquipment.to_cim = conductingequipment_to_cim
PBConnectivityNode.to_cim = connectivitynode_to_cim
PBConnectivityNodeContainer.to_cim = connectivitynodecontainer_to_cim
PBEquipment.to_cim = equipment_to_cim
PBEquipmentContainer.to_cim = equipmentcontainer_to_cim
PBFeeder.to_cim = feeder_to_cim
PBGeographicalRegion.to_cim = geographicalregion_to_cim
PBPowerSystemResource.to_cim = powersystemresource_to_cim
PBSite.to_cim = site_to_cim
PBSubGeographicalRegion.to_cim = subgeographicalregion_to_cim
PBSubstation.to_cim = substation_to_cim
PBTerminal.to_cim = terminal_to_cim


### IEC61970 WIRES
def aclinesegment_to_cim(pb: PBAcLineSegment, network_service: NetworkService):
    cim = AcLineSegment(pb.mrid())
    network_service.resolve_or_defer_reference(resolver.per_length_sequence_impedance(cim),
                                               pb.perLengthSequenceImpedanceMRID)
    conductor_to_cim(pb.cd, cim, network_service)


def breaker_to_cim(pb: PBBreaker, network_service: NetworkService):
    cim = Breaker(pb.mrid())
    protectedswitch_to_cim(pb.sw, cim, network_service)


def conductor_to_cim(pb: PBConductor, cim: Conductor, network_service: NetworkService):
    cim.length = pb.length
    network_service.resolve_or_defer_reference(resolver.asset_info(cim), pb.asset_info_mrid())
    conductingequipment_to_cim(pb.ce, cim, network_service)


def connector_to_cim(pb: PBConnector, cim: Connector, network_service: NetworkService):
    conductingequipment_to_cim(pb.ce, cim, network_service)


def disconnector_to_cim(pb: PBDisconnector, network_service: NetworkService):
    cim = Disconnector(pb.mrid())
    switch_to_cim(pb.sw, cim, network_service)


def energyconnection_to_cim(pb: PBEnergyConnection, cim: EnergyConnection, network_service: NetworkService):
    conductingequipment_to_cim(pb.ce, cim, network_service)


def energyconsumer_to_cim(pb: PBEnergyConsumer, network_service: NetworkService):
    cim = EnergyConsumer(pb.mrid())
    for mrid in pb.energyConsumerPhasesMRIDs:
        network_service.resolve_or_defer_reference(resolver.ec_phases(cim), mrid)
    cim.customer_count = pb.customerCount
    cim.grounded = pb.grounded
    cim.p = pb.p
    cim.p_fixed = pb.pFixed
    cim.phase_connection = PhaseShuntConnectionKind(pb.phaseConnection)
    cim.q = pb.q
    cim.q_fixed = pb.qFixed
    energyconnection_to_cim(pb.ec, cim, network_service)


def energyconsumerphase_to_cim(pb: PBEnergyConsumerPhase, network_service: NetworkService):
    cim = EnergyConsumerPhase(mrid=pb.mrid(), phase=phasekind_by_id(pb.phase))
    network_service.resolve_or_defer_reference(resolver.energy_consumer(cim), pb.energyConsumerMRID)
    cim.p = pb.p
    cim.p_fixed = pb.pFixed
    cim.q = pb.q
    cim.q_fixed = pb.qFixed
    powersystemresource_to_cim(pb.psr, cim, network_service)


def energysource_to_cim(pb: PBEnergySource, network_service: NetworkService):
    cim = EnergySource(pb.mrid())
    for mrid in pb.energySourcePhasesMRIDs:
        network_service.resolve_or_defer_reference(resolver.es_phases(cim), mrid)
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
    energyconnection_to_cim(pb.ec, cim, network_service)


def energysourcephase_to_cim(pb: PBEnergySourcePhase, network_service: NetworkService):
    cim = EnergySourcePhase(mrid=pb.mrid(), phase=phasekind_by_id(pb.phase))
    network_service.resolve_or_defer_reference(resolver.energy_source(cim), pb.energySourceMRID)
    powersystemresource_to_cim(pb.psr, cim, network_service)


def fuse_to_cim(pb: PBFuse, network_service: NetworkService):
    cim = Fuse(pb.mrid())
    switch_to_cim(pb.sw, cim, network_service)


def jumper_to_cim(pb: PBJumper, network_service: NetworkService):
    cim = Jumper(pb.mrid())
    switch_to_cim(pb.sw, cim, network_service)


def junction_to_cim(pb: PBJunction, network_service: NetworkService):
    cim = Junction(pb.mrid())
    connector_to_cim(pb.cn, cim, network_service)


def linearshuntcompensator_to_cim(pb: PBLinearShuntCompensator, network_service: NetworkService):
    cim = LinearShuntCompensator(pb.mrid())
    cim.b0_per_section = pb.b0PerSection
    cim.b_per_section = pb.bPerSection
    cim.g0_per_section = pb.g0PerSection
    cim.g_per_section = pb.gPerSection
    shuntcompensator_to_cim(pb.sc, cim, network_service)


def tracedphases_to_cim(pb: PBTracedPhases, cim: TracedPhases, nominal_phases: PhaseCode):
    pass
    # for phs in nominal_phases.single_phases:
    #     cim.set_normal(phase(pb.normalStatus, phs), direction(pb.normalStatus, phs), phs)
    #     cim.set_current(phase(pb.currentStatus, phs), direction(pb.currentStatus, phs), phs)


def perlengthlineparameter_to_cim(pb: PBPerLengthLineParameter, cim: PerLengthLineParameter,
                                  network_service: NetworkService):
    set_identifiedobject(pb.io, cim, network_service)


def perlengthimpedance_to_cim(pb: PBPerLengthImpedance, cim: PerLengthImpedance, network_service: NetworkService):
    perlengthlineparameter_to_cim(pb.lp, cim, network_service)


def perlengthsequenceimpedance_to_cim(pb: PBPerLengthSequenceImpedance, network_service: NetworkService):
    cim = PerLengthSequenceImpedance(pb.mrid())
    cim.r = pb.r
    cim.x = pb.x
    cim.r0 = pb.r0
    cim.x0 = pb.x0
    cim.bch = pb.bch
    cim.gch = pb.gch
    cim.b0ch = pb.b0ch
    cim.g0ch = pb.b0ch
    perlengthimpedance_to_cim(pb.pli, cim, network_service)


def powertransformer_to_cim(pb: PBPowerTransformer, network_service: NetworkService):
    cim = PowerTransformer(pb.mrid())
    for mrid in pb.powerTransformerEndMRIDs:
        network_service.resolve_or_defer_reference(resolver.ends(cim), mrid)
    cim.vector_group = VectorGroup(pb.vectorGroup)
    conductingequipment_to_cim(pb.ce, cim, network_service)


def powertransformerend_to_cim(pb: PBPowerTransformerEnd, network_service: NetworkService):
    cim = PowerTransformerEnd(mrid=pb.mrid())
    network_service.resolve_or_defer_reference(resolver.power_transformer(cim), pb.powerTransformerMRID)
    cim.rated_s = pb.ratedS
    cim.rated_u = pb.ratedU
    cim.r = pb.r
    cim.r0 = pb.r0
    cim.x = pb.x
    cim.x0 = pb.x0
    cim.connection_kind = WindingConnection(pb.connectionKind)
    cim.b = pb.b
    cim.b0 = pb.b0
    cim.g = pb.g
    cim.g0 = pb.g0
    cim.phase_angle_clock = pb.phaseAngleClock
    transformerend_to_cim(pb.te, cim, network_service)


def protectedswitch_to_cim(pb: PBProtectedSwitch, cim: ProtectedSwitch, network_service: NetworkService):
    switch_to_cim(pb.sw, cim, network_service)


def ratiotapchanger_to_cim(pb: PBRatioTapChanger, network_service: NetworkService):
    cim = RatioTapChanger(pb.mrid())
    cim.step_voltage_increment = pb.stepVoltageIncrement
    tapchanger_to_cim(pb.tc, cim, network_service)


def recloser_to_cim(pb: PBRecloser, network_service: NetworkService):
    cim = Recloser(pb.mrid())
    protectedswitch_to_cim(pb.sw, cim, network_service)


def regulatingcondeq_to_cim(pb: PBRegulatingCondEq, cim: RegulatingCondEq, network_service: NetworkService):
    cim.control_enabled = pb.control_enabled
    energyconnection_to_cim(pb.ec, cim, network_service)


def shuntcompensator_to_cim(pb: PBShuntCompensator, cim: ShuntCompensator, network_service: NetworkService):
    cim.sections = pb.sections
    cim.grounded = pb.grounded
    cim.nom_u = pb.nomU
    cim.phase_connection = PhaseShuntConnectionKind(pb.phaseConnection)
    regulatingcondeq_to_cim(pb.rce, cim, network_service)


def switch_to_cim(pb: PBSwitch, cim: Switch, network_service: NetworkService):
    cim.set_normally_open(pb.normalOpen)
    cim.set_open(pb.open)
    conductingequipment_to_cim(pb.ce, cim, network_service)


def tapchanger_to_cim(pb: PBTapChanger, cim: TapChanger, network_service: NetworkService):
    cim.high_step = pb.highStep
    cim.low_step = pb.lowStep
    cim.step = pb.step
    cim.neutral_step = pb.neutralStep
    cim.neutral_u = pb.neutralU
    cim.normal_step = pb.normalStep
    cim.control_enabled = pb.controlEnabled
    powersystemresource_to_cim(pb.psr, cim, network_service)


def transformerend_to_cim(pb: PBTransformerEnd, cim: TransformerEnd, network_service: NetworkService):
    network_service.resolve_or_defer_reference(resolver.te_terminal(cim), pb.terminalMRID)
    network_service.resolve_or_defer_reference(resolver.te_base_voltage(cim), pb.baseVoltageMRID)
    network_service.resolve_or_defer_reference(resolver.ratio_tap_changer(cim), pb.ratioTapChangerMRID)
    cim.grounded = pb.grounded
    cim.r_ground = pb.rGround
    cim.x_ground = pb.xGround
    set_identifiedobject(pb.io, cim, network_service)


PBAcLineSegment.to_cim = aclinesegment_to_cim
PBBreaker.to_cim = breaker_to_cim
PBConductor.to_cim = conductor_to_cim
PBConnector.to_cim = connector_to_cim
PBDisconnector.to_cim = disconnector_to_cim
PBEnergyConnection.to_cim = energyconnection_to_cim
PBEnergyConsumer.to_cim = energyconsumer_to_cim
PBEnergyConsumerPhase.to_cim = energyconsumerphase_to_cim
PBEnergySource.to_cim = energysource_to_cim
PBEnergySourcePhase.to_cim = energysourcephase_to_cim
PBFuse.to_cim = fuse_to_cim
PBJumper.to_cim = jumper_to_cim
PBJunction.to_cim = junction_to_cim
PBLinearShuntCompensator.to_cim = linearshuntcompensator_to_cim
PBPerLengthSequenceImpedance.to_cim = perlengthsequenceimpedance_to_cim
PBPerLengthLineParameter.to_cim = perlengthlineparameter_to_cim
PBPerLengthImpedance = perlengthimpedance_to_cim
PBPowerTransformer.to_cim = powertransformer_to_cim
PBPowerTransformerEnd.to_cim = powertransformerend_to_cim
PBProtectedSwitch.to_cim = protectedswitch_to_cim
PBRatioTapChanger.to_cim = ratiotapchanger_to_cim
PBRecloser.to_cim = recloser_to_cim
PBRegulatingCondEq.to_cim = regulatingcondeq_to_cim
PBShuntCompensator.to_cim = shuntcompensator_to_cim
PBSwitch.to_cim = switch_to_cim
PBTapChanger.to_cim = tapchanger_to_cim
PBTransformerEnd.to_cim = transformerend_to_cim


### Extensions
def add_from_pb(network_service: NetworkService, pb):
    """Must only be called by objects for which .to_cim() takes themselves and the network service."""
    pb.to_cim(network_service)


NetworkService.add_from_pb = add_from_pb


### Make a class similar to the Kotlin one

@dataclass
class NetworkProtoToCim(BaseProtoToCim):
    service: NetworkService

    def add_from_pb(self, pb):
        """Must only be called by objects for which .to_cim() takes themselves and the network."""
        pb.to_cim(self.service)


# IEC61968 COMMON #
positionpoint_from_pb = positionpoint_to_cim

towndetail_from_pb = towndetail_to_cim

streetaddress_from_pb = streetaddress_to_cim

# MODEL #
set_tracedphases = tracedphases_to_cim

set_perlengthimpedance = perlengthimpedance_to_cim

set_perlengthlineparameter = perlengthlineparameter_to_cim

set_acdcterminal = acdcterminal_to_cim
