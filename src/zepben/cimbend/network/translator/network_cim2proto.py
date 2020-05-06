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

from zepben.cimbend import ConnectivityNode
from zepben.cimbend.common import mrid_or_empty
from zepben.cimbend.common.base_cim2proto import *
from zepben.cimbend.common.decorators import map_type
from zepben.cimbend.cim.iec61968.assetinfo.wire_info import CableInfo, OverheadWireInfo, WireInfo
from zepben.cimbend.cim.iec61968.assets.asset import Asset, AssetContainer
from zepben.cimbend.cim.iec61968.assets.asset_info import AssetInfo
from zepben.cimbend.cim.iec61968.assets.asset_organisation_role import AssetOwner, AssetOrganisationRole
from zepben.cimbend.cim.iec61968.common.location import StreetAddress, TownDetail, PositionPoint, Location
from zepben.cimbend.cim.iec61968.metering import EndDevice, UsagePoint, Meter
from zepben.cimbend.cim.iec61968.operations.operational_restriction import OperationalRestriction
from zepben.cimbend.cim.iec61970.base.auxiliaryequipment.auxiliary_equipment import AuxiliaryEquipment, FaultIndicator
from zepben.cimbend.cim.iec61970.base.core import BaseVoltage
from zepben.cimbend.cim.iec61970.base.core import ConductingEquipment
from zepben.cimbend.cim.iec61970.base.core.connectivity_node_container import ConnectivityNodeContainer
from zepben.cimbend.cim.iec61970.base.core.equipment import Equipment
from zepben.cimbend.cim.iec61970.base.core.equipment_container import EquipmentContainer, Feeder, Site
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
from zepben.cimbend.cim.iec61970.base.wires.power_transformer import PowerTransformer, PowerTransformerEnd, RatioTapChanger, \
    TapChanger, TransformerEnd
from zepben.cimbend.cim.iec61970.base.wires import LinearShuntCompensator, ShuntCompensator
from zepben.cimbend.cim.iec61970.base.wires.switch import Breaker, Disconnector, Fuse, Jumper, ProtectedSwitch, Recloser, \
    Switch
from zepben.cimbend.phases import TracedPhases

__all__ = ["CimTranslationException", "get_cableinfo", "get_overheadwireinfo", "get_wireinfo", "get_asset", "get_assetcontainer", "get_assetinfo",
           "get_assetorganisationrole", "get_assetowner", "get_positionpoint", "get_towndetail", "get_streetaddress",
           "get_location", "get_enddevice", "get_meter", "get_usagepoint", "get_operationalrestriction",
           "get_auxiliaryequipment", "get_faultindicator", "get_acdcterminal", "get_basevoltage",
           "get_conductingequipment", "get_connectivitynode", "get_connectivitynodecontainer", "get_equipment",
           "get_equipmentcontainer", "get_feeder", "get_geographicalregion", "get_powersystemresource", "get_site",
           "get_subgeographicalregion", "get_substation", "get_terminal", "get_perlengthlineparameter",
           "get_perlengthimpedance", "get_aclinesegment", "get_breaker", "get_conductor", "get_connector",
           "get_disconnector", "get_energyconnection", "get_energyconsumer", "get_energyconsumerphase",
           "get_energysource", "get_energysourcephase", "get_fuse", "get_jumper", "get_junction",
           "get_linearshuntcompensator", "get_perlengthsequenceimpedance", "get_powertransformer",
           "get_powertransformerend", "get_protectedswitch", "get_ratiotapchanger", "get_recloser",
           "get_regulatingcondeq", "get_shuntcompensator", "get_switch", "get_tapchanger", "get_transformerend",
           "get_tracedphases"]


def get_or_none(getter, obj) -> object:
    return getter(obj) if obj else None


class CimTranslationException(Exception):
    pass


# IEC61968 ASSET INFO #
def get_cableinfo(cim: CableInfo) -> PBCableInfo:
    return PBCableInfo(wi=get_wireinfo(cim))


def get_overheadwireinfo(cim: OverheadWireInfo) -> PBOverheadWireInfo:
    return PBOverheadWireInfo(wi=get_wireinfo(cim))


def get_wireinfo(cim: WireInfo) -> PBWireInfo:
    return PBWireInfo(ai=get_assetinfo(cim),
                      ratedCurrent=cim.rated_current,
                      material=PBWireMaterialKind.Value(cim.material.short_name))


# IEC61968 ASSETS #
def get_asset(cim: Asset) -> PBAsset:
    """
    OrganisationRoles are sent with Asset
    :param cim:
    :return:
    """
    return PBAsset(io=get_identifiedobject(cim),
                   organisationRoleMRIDs=[str(io.mrid) for io in cim.organisation_roles])


def get_assetcontainer(cim: AssetContainer) -> PBAssetContainer:
    return PBAssetContainer(at=get_asset(cim))


def get_assetinfo(cim: AssetInfo) -> PBAssetInfo:
    return PBAssetInfo(io=get_identifiedobject(cim))


def get_assetorganisationrole(cim: AssetOrganisationRole) -> PBAssetOrganisationRole:
    pb = PBAssetOrganisationRole()
    getattr(pb, "or").CopyFrom(get_organisationrole(cim))
    return pb


def get_assetowner(cim: AssetOwner) -> PBAssetOwner:
    return PBAssetOwner(aor=get_assetorganisationrole(cim))


# IEC61968 COMMON #
def get_positionpoint(cim: PositionPoint) -> PBPositionPoint:
    return PBPositionPoint(xPosition=cim.x_position, yPosition=cim.y_position)


def get_towndetail(cim: TownDetail) -> PBTownDetail:
    return PBTownDetail(name=cim.name, stateOrProvince=cim.state_or_province)


def get_streetaddress(cim: StreetAddress) -> PBStreetAddress:
    return PBStreetAddress(postalCode=cim.postal_code, townDetail=get_or_none(get_towndetail(cim.town_detail)))


def get_location(cim: Location) -> PBLocation:
    return PBLocation(io=get_identifiedobject(cim),
                      mainAddress=get_or_none(get_streetaddress, cim.main_address),
                      positionPoints=[get_positionpoint(point) for _, point in cim.points])


# IEC61968 METERING #
def get_enddevice(cim: EndDevice) -> PBEndDevice:
    return PBEndDevice(ac=get_assetcontainer(cim),
                       usagePointMRIDs=[str(io.mrid) for io in cim.usage_points],
                       customerMRID=cim.customer_mrid,
                       serviceLocationMRID=mrid_or_empty(cim.service_location))


def get_meter(cim: Meter) -> PBMeter:
    return PBMeter(ed=get_enddevice(cim))


def get_usagepoint(cim: UsagePoint) -> PBUsagePoint:
    """
    usagePointLocation is sent with UsagePoint.
    :param cim:
    :return:
    """
    return PBUsagePoint(io=get_identifiedobject(cim),
                        usagePointLocationMRID=mrid_or_empty(cim.usage_point_location),
                        equipmentMRIDs=[str(io.mrid) for io in cim.equipment])


# IEC61968 OPERATIONS #
def get_operationalrestriction(cim: OperationalRestriction) -> PBOperationalRestriction:
    return PBOperationalRestriction(doc=get_document(cim),
                                    equipmentMRIDs=[str(io.mrid) for io in cim.equipment])


# IEC61970 AUXILIARY EQUIPMENT #
def get_auxiliaryequipment(cim: AuxiliaryEquipment) -> PBAuxiliaryEquipment:
    """
    Terminal is sent with AuxiliaryEquipment
    :param cim:
    :return:
    """
    return PBAuxiliaryEquipment(eq=get_equipment(cim),
                                terminalMRID=mrid_or_empty(cim.terminal))


def get_faultindicator(cim: FaultIndicator) -> PBFaultIndicator:
    return PBFaultIndicator(ae=get_auxiliaryequipment(cim))


# IEC61970 CORE #
def get_acdcterminal(cim: AcDcTerminal) -> PBAcDcTerminal:
    return PBAcDcTerminal(io=get_identifiedobject(cim))


def get_basevoltage(cim: BaseVoltage) -> PBBaseVoltage:
    return PBBaseVoltage(io=get_identifiedobject(cim))


def get_conductingequipment(cim: ConductingEquipment) -> PBConductingEquipment:
    """
    BaseVoltage and Terminals are sent with ConductingEquipment
    :param cim:
    :return:
    """
    return PBConductingEquipment(eq=get_equipment(cim),
                                 baseVoltageMRID=mrid_or_empty(cim.base_voltage),
                                 terminalMRIDs=[str(io.mrid) for _, io in cim.terminals])


def get_connectivitynode(cim: ConnectivityNode) -> PBConnectivityNode:
    return PBConnectivityNode(io=get_identifiedobject(cim))


def get_connectivitynodecontainer(cim: ConnectivityNodeContainer) -> PBConnectivityNodeContainer:
    return PBConnectivityNodeContainer(psr=get_powersystemresource(cim))


def get_equipment(cim: Equipment) -> PBEquipment:
    """
    Equipment Containers, usage points, and operational restrictions are sent with Equipment.
    :param cim:
    :return:
    """
    pb = PBEquipment(psr=get_powersystemresource(cim),
                     inService=cim.in_service,
                     normallyInService=cim.normally_in_service,
                     equipmentContainerMRIDs=[str(io.mrid) for io in cim.equipment_containers],
                     usagePointMRIDs=[str(io.mrid) for io in cim.usage_points],
                     operationalRestrictionMRIDs=[str(io.mrid) for io in cim.operational_restrictions])
    return pb


def get_equipmentcontainer(cim: EquipmentContainer) -> PBEquipmentContainer:
    return PBEquipmentContainer(cnc=get_connectivitynodecontainer(cim),
                                equipmentMRIDs=[str(io.mrid) for io in cim.equipment])


def get_feeder(cim: Feeder) -> PBFeeder:
    """
    normalHeadTerminal is sent with Feeder
    :param cim:
    :return:
    """
    return PBFeeder(ec=get_equipmentcontainer(cim),
                    normalHeadTerminalMRID=mrid_or_empty(cim.normal_head_terminal),
                    normalEnergizingSubstationMRID=mrid_or_empty(cim.normal_energizing_substation))


def get_geographicalregion(cim: GeographicalRegion) -> PBGeographicalRegion:
    return PBGeographicalRegion(io=get_identifiedobject(cim),
                                subGeographicalRegionMRIDs=[str(io.mrid) for io in cim.sub_geographical_regions])


def get_powersystemresource(cim: PowerSystemResource) -> PBPowerSystemResource:
    """
    AssetInfo, Location is sent with PowerSystemResource
    :param cim:
    :return:
    """
    return PBPowerSystemResource(io=get_identifiedobject(cim),
                                 assetInfoMRID=mrid_or_empty(cim.asset_info),
                                 locationMRID=mrid_or_empty(cim.location),
                                 numControls=cim.num_controls,
                                 numMeasurements=cim.num_measurements)


def get_site(cim: Site) -> PBSite:
    return PBSite(ec=get_equipmentcontainer(cim))


def get_subgeographicalregion(cim: SubGeographicalRegion) -> PBSubGeographicalRegion:
    """
    GeographicalRegion is sent with SubGeographicalRegion
    :param cim:
    :return:
    """
    return PBSubGeographicalRegion(io=get_identifiedobject(cim),
                                   geographicalRegionMRID=mrid_or_empty(cim.geographical_region),
                                   substationMRIDs=[str(io.mrid) for io in cim.substations])


def get_substation(cim: Substation) -> PBSubstation:
    """
    SubGeographicalRegion is sent with Substation
    :param cim:
    :return:
    """
    return PBSubstation(ec=get_equipmentcontainer(cim),
                        subGeographicalRegionMRID=mrid_or_empty(cim.sub_geographical_region),
                        normalEnergizedFeederMRIDs=[str(io.mrid) for io in cim.feeders])


def get_terminal(cim: Terminal) -> PBTerminal:
    """
    ConnectivityNode's are sent with Terminals
    :param cim:
    :return:
    """
    return PBTerminal(ad=get_acdcterminal(cim),
                      conductingEquipmentMRID=mrid_or_empty(cim.conducting_equipment),
                      connectivityNodeMRID=mrid_or_empty(cim.connectivity_node),
                      tracedPhases=get_tracedphases(cim.traced_phases),
                      phases=PBPhaseCode.Value(cim.phases.short_name))


# IEC61970 WIRES #

def get_aclinesegment(cim: AcLineSegment) -> PBAcLineSegment:
    """
    PerLengthSequenceImpedances are sent with AcLineSegment
    :param cim:
    :return:
    """
    return PBAcLineSegment(cd=get_conductor(cim),
                           perLengthSequenceImpedanceMRID=mrid_or_empty(cim.per_length_sequence_impedance))


def get_breaker(cim: Breaker) -> PBBreaker:
    return PBBreaker(sw=get_protectedswitch(cim))


def get_conductor(cim: Conductor) -> PBConductor:
    return PBConductor(ce=get_conductingequipment(cim),
                       length=cim.length)


def get_connector(cim: Connector) -> PBConnector:
    return PBConnector(ce=get_conductingequipment(cim))


def get_disconnector(cim: Disconnector) -> PBDisconnector:
    return PBDisconnector(sw=get_switch(cim))


def get_energyconnection(cim: EnergyConnection) -> PBEnergyConnection:
    return PBEnergyConnection(ce=get_conductingequipment(cim))


def get_energyconsumer(cim: EnergyConsumer) -> PBEnergyConsumer:
    """
    EnergyConsumerPhases are sent with EnergyConsumer
    :param cim:
    :return:
    """
    return PBEnergyConsumer(ec=get_energyconnection(cim),
                            energyConsumerPhasesMRIDs=[str(io.mrid) for io in cim.phases],
                            customerCount=cim.customer_count,
                            grounded=cim.grounded,
                            p=cim.p,
                            pFixed=cim.p_fixed,
                            phaseConnection=PBPhaseShuntConnectionKind.Enum.Value(cim.phase_connection.short_name),
                            q=cim.q,
                            qFixed=cim.q_fixed)


def get_energyconsumerphase(cim: EnergyConsumerPhase) -> PBEnergyConsumerPhase:
    return PBEnergyConsumerPhase(psr=get_powersystemresource(cim),
                                 energyConsumerMRID=mrid_or_empty(cim.energy_consumer),
                                 phase=PBSinglePhaseKind.Value(cim.phase.short_name),
                                 p=cim.p,
                                 pFixed=cim.p_fixed,
                                 q=cim.q,
                                 qFixed=cim.q_fixed)


def get_energysource(cim: EnergySource) -> PBEnergySource:
    """
    EnergySourcePhases are sent with EnergySource
    :param cim:
    :return:
    """
    return PBEnergySource(ec=get_energyconnection(cim),
                          energySourcePhasesMRIDs=[str(io.mrid) for io in cim.phases],
                          activePower=cim.active_power,
                          reactivePower=cim.reactive_power,
                          voltageAngle=cim.voltage_angle,
                          voltageMagnitude=cim.voltage_magnitude,
                          r=cim.r,
                          x=cim.x,
                          pMax=cim.p_max,
                          pMin=cim.p_min,
                          r0=cim.r0,
                          rn=cim.rn,
                          x0=cim.x0,
                          xn=cim.xn)


def get_energysourcephase(cim: EnergySourcePhase) -> PBEnergySourcePhase:
    return PBEnergySourcePhase(psr=get_powersystemresource(cim),
                               energySourceMRID=mrid_or_empty(cim.energy_source),
                               phase=PBSinglePhaseKind.Value(cim.phase.short_name))


def get_fuse(cim: Fuse) -> PBFuse:
    return PBFuse(sw=get_switch(cim))


def get_jumper(cim: Jumper) -> PBJumper:
    return PBJumper(sw=get_switch(cim))


def get_junction(cim: Junction) -> PBJunction:
    return PBJunction(cn=get_connector(cim))


def get_linearshuntcompensator(cim: LinearShuntCompensator) -> PBLinearShuntCompensator:
    return PBLinearShuntCompensator(sc=get_shuntcompensator(cim),
                                    b0PerSection=cim.b0_per_section,
                                    bPerSection=cim.b_per_section,
                                    g0PerSection=cim.g0_per_section,
                                    gPerSection=cim.g_per_section)


def get_perlengthlineparameter(cim: PerLengthLineParameter) -> PBPerLengthLineParameter:
    return PBPerLengthLineParameter(io=get_identifiedobject(cim))


def get_perlengthimpedance(cim: PerLengthImpedance) -> PBPerLengthImpedance:
    return PBPerLengthImpedance(lp=get_perlengthlineparameter(cim))


def get_perlengthsequenceimpedance(cim: PerLengthSequenceImpedance) -> PBPerLengthSequenceImpedance:
    return PBPerLengthSequenceImpedance(pli=get_perlengthimpedance(cim),
                                        r=cim.r,
                                        x=cim.x,
                                        r0=cim.r0,
                                        x0=cim.x0,
                                        bch=cim.bch,
                                        gch=cim.gch,
                                        b0ch=cim.b0ch,
                                        g0ch=cim.g0ch)


def get_powertransformer(cim: PowerTransformer) -> PBPowerTransformer:
    return PBPowerTransformer(ce=get_conductingequipment(cim),
                              powerTransformerEndMRIDs=[str(io.mrid) for _, io in cim.ends],
                              vectorGroup=PBVectorGroup.Value(cim.vector_group.short_name))


def get_powertransformerend(cim: PowerTransformerEnd) -> PBPowerTransformerEnd:
    """
    PowerTransformer is sent with PowerTransformerEnd because it is required
    by the PowerTransformerEnd.
    :param cim:
    :return:
    """
    return PBPowerTransformerEnd(te=get_transformerend(cim),
                                 powerTransformerMRID=mrid_or_empty(cim.power_transformer),
                                 ratedS=cim.rated_s,
                                 ratedU=cim.rated_u,
                                 r=cim.r,
                                 r0=cim.r0,
                                 x=cim.x,
                                 x0=cim.x0,
                                 connectionKind=PBWindingConnection.Value(cim.connection_kind.short_name),
                                 b=cim.b,
                                 b0=cim.b0,
                                 g=cim.g,
                                 g0=cim.g0,
                                 phaseAngleClock=cim.phase_angle_clock)


def get_protectedswitch(cim: ProtectedSwitch) -> PBProtectedSwitch:
    return PBProtectedSwitch(sw=get_switch(cim))


def get_ratiotapchanger(cim: RatioTapChanger) -> PBRatioTapChanger:
    return PBRatioTapChanger(tc=get_tapchanger(cim),
                             stepVoltageIncrement=cim.step_voltage_increment)


def get_recloser(cim: Recloser) -> PBRecloser:
    return PBRecloser(sw=get_protectedswitch(cim))


def get_regulatingcondeq(cim: RegulatingCondEq) -> PBRegulatingCondEq:
    return PBRegulatingCondEq(ec=get_energyconnection(cim),
                              controlEnabled=cim.control_enabled)


def get_shuntcompensator(cim: ShuntCompensator) -> PBShuntCompensator:
    return PBShuntCompensator(rce=get_regulatingcondeq(cim),
                              sections=cim.sections,
                              grounded=cim.grounded,
                              nomU=cim.nom_u,
                              phaseConnection=PBPhaseShuntConnectionKind.Value(cim.phase_connection))


def get_switch(cim: Switch) -> PBSwitch:
    return PBSwitch(ce=get_conductingequipment(cim),
                    normalOpen=cim.get_normal_state(),
                    open=cim.get_state())


def get_tapchanger(cim: TapChanger) -> PBTapChanger:
    return PBTapChanger(psr=get_powersystemresource(cim),
                        highStep=cim.high_step,
                        lowStep=cim.low_step,
                        step=cim.step,
                        neutralStep=cim.neutral_step,
                        neutralU=cim.neutral_u,
                        normalStep=cim.normal_step,
                        controlEnabled=cim.control_enabled)


def get_transformerend(cim: TransformerEnd) -> PBTransformerEnd:
    """
    RatioTapChanger, BaseVoltage, and Terminal are sent with the TransformerEnd
    :param cim:
    :return:
    """
    return PBTransformerEnd(io=get_identifiedobject(cim),
                            terminalMRID=mrid_or_empty(cim.terminal),
                            baseVoltageMRID=mrid_or_empty(cim.base_voltage),
                            ratioTapChangerMRID=mrid_or_empty(cim.ratio_tap_changer),
                            grounded=cim.grounded,
                            rGround=cim.r_ground,
                            xGround=cim.x_ground)


# MODEL #
def get_tracedphases(cim: TracedPhases) -> PBTracedPhases:
    return PBTracedPhases(normalStatus=cim.normal_status,
                          currentStatus=cim.current_status)


# Extension functions for each CIM type.
CableInfo.to_pb = lambda self: get_cableinfo(self)
OverheadWireInfo.to_pb = lambda self: get_overheadwireinfo(self)
WireInfo.to_pb = lambda self: get_wireinfo(self)
Asset.to_pb = lambda self: get_asset(self)
AssetContainer.to_pb = lambda self: get_assetcontainer(self)
AssetInfo.to_pb = lambda self: get_assetinfo(self)
AssetOrganisationRole.to_pb = lambda self: get_assetorganisationrole(self)
AssetOwner.to_pb = lambda self: get_assetowner(self)
PositionPoint.to_pb = lambda self: get_positionpoint(self)
TownDetail.to_pb = lambda self: get_towndetail(self)
StreetAddress.to_pb = lambda self: get_streetaddress(self)
Location.to_pb = lambda self: get_location(self)
EndDevice.to_pb = lambda self: get_enddevice(self)
Meter.to_pb = lambda self: get_meter(self)
UsagePoint.to_pb = lambda self: get_usagepoint(self)
OperationalRestriction.to_pb = lambda self: get_operationalrestriction(self)
AuxiliaryEquipment.to_pb = lambda self: get_auxiliaryequipment(self)
FaultIndicator.to_pb = lambda self: get_faultindicator(self)
AcDcTerminal.to_pb = lambda self: get_acdcterminal(self)
BaseVoltage.to_pb = lambda self: get_basevoltage(self)
ConductingEquipment.to_pb = lambda self: get_conductingequipment(self)
ConnectivityNode.to_pb = lambda self: get_connectivitynode(self)
ConnectivityNodeContainer.to_pb = lambda self: get_connectivitynodecontainer(self)
Equipment.to_pb = lambda self: get_equipment(self)
EquipmentContainer.to_pb = lambda self: get_equipmentcontainer(self)
Feeder.to_pb = lambda self: get_feeder(self)
GeographicalRegion.to_pb = lambda self: get_geographicalregion(self)
PowerSystemResource.to_pb = lambda self: get_powersystemresource(self)
Site.to_pb = lambda self: get_site(self)
SubGeographicalRegion.to_pb = lambda self: get_subgeographicalregion(self)
Substation.to_pb = lambda self: get_substation(self)
Terminal.to_pb = lambda self: get_terminal(self)
PerLengthLineParameter.to_pb = lambda self: get_perlengthlineparameter(self)
PerLengthImpedance.to_pb = lambda self: get_perlengthimpedance(self)
AcLineSegment.to_pb = lambda self: get_aclinesegment(self)
Breaker.to_pb = lambda self: get_breaker(self)
Conductor.to_pb = lambda self: get_conductor(self)
Connector.to_pb = lambda self: get_connector(self)
Disconnector.to_pb = lambda self: get_disconnector(self)
EnergyConnection.to_pb = lambda self: get_energyconnection(self)
EnergyConsumer.to_pb = lambda self: get_energyconsumer(self)
EnergyConsumerPhase.to_pb = lambda self: get_energyconsumerphase(self)
EnergySource.to_pb = lambda self: get_energysource(self)
EnergySourcePhase.to_pb = lambda self: get_energysourcephase(self)
Fuse.to_pb = lambda self: get_fuse(self)
Jumper.to_pb = lambda self: get_jumper(self)
Junction.to_pb = lambda self: get_junction(self)
LinearShuntCompensator.to_pb = lambda self: get_linearshuntcompensator(self)
PerLengthSequenceImpedance.to_pb = lambda self: get_perlengthsequenceimpedance(self)
PowerTransformer.to_pb = lambda self: get_powertransformer(self)
PowerTransformerEnd.to_pb = lambda self: get_powertransformerend(self)
ProtectedSwitch.to_pb = lambda self: get_protectedswitch(self)
RatioTapChanger.to_pb = lambda self: get_ratiotapchanger(self)
Recloser.to_pb = lambda self: get_recloser(self)
RegulatingCondEq.to_pb = lambda self: get_regulatingcondeq(self)
ShuntCompensator.to_pb = lambda self: get_shuntcompensator(self)
Switch.to_pb = lambda self: get_switch(self)
TapChanger.to_pb = lambda self: get_tapchanger(self)
TransformerEnd.to_pb = lambda self: get_transformerend(self)
TracedPhases.to_pb = lambda self: get_tracedphases(self)
