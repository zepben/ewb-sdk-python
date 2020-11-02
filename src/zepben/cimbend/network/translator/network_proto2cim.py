#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.cimbend import UnitSymbol
from zepben.protobuf.cim.iec61968.assetinfo.CableInfo_pb2 import CableInfo as PBCableInfo
from zepben.protobuf.cim.iec61968.assetinfo.OverheadWireInfo_pb2 import OverheadWireInfo as PBOverheadWireInfo
from zepben.protobuf.cim.iec61968.assetinfo.WireInfo_pb2 import WireInfo as PBWireInfo
from zepben.protobuf.cim.iec61968.assets.AssetContainer_pb2 import AssetContainer as PBAssetContainer
from zepben.protobuf.cim.iec61968.assets.AssetInfo_pb2 import AssetInfo as PBAssetInfo
from zepben.protobuf.cim.iec61968.assets.AssetOrganisationRole_pb2 import AssetOrganisationRole as PBAssetOrganisationRole
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
from zepben.protobuf.cim.iec61968.operations.OperationalRestriction_pb2 import OperationalRestriction as PBOperationalRestriction
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.AuxiliaryEquipment_pb2 import AuxiliaryEquipment as PBAuxiliaryEquipment
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.FaultIndicator_pb2 import FaultIndicator as PBFaultIndicator
from zepben.protobuf.cim.iec61970.base.core.AcDcTerminal_pb2 import AcDcTerminal as PBAcDcTerminal
from zepben.protobuf.cim.iec61970.base.core.BaseVoltage_pb2 import BaseVoltage as PBBaseVoltage
from zepben.protobuf.cim.iec61970.base.core.ConductingEquipment_pb2 import ConductingEquipment as PBConductingEquipment
from zepben.protobuf.cim.iec61970.base.core.ConnectivityNodeContainer_pb2 import ConnectivityNodeContainer as PBConnectivityNodeContainer
from zepben.protobuf.cim.iec61970.base.core.ConnectivityNode_pb2 import ConnectivityNode as PBConnectivityNode
from zepben.protobuf.cim.iec61970.base.core.EquipmentContainer_pb2 import EquipmentContainer as PBEquipmentContainer
from zepben.protobuf.cim.iec61970.base.core.Equipment_pb2 import Equipment as PBEquipment
from zepben.protobuf.cim.iec61970.base.core.Feeder_pb2 import Feeder as PBFeeder
from zepben.protobuf.cim.iec61970.base.core.GeographicalRegion_pb2 import GeographicalRegion as PBGeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.PowerSystemResource_pb2 import PowerSystemResource as PBPowerSystemResource
from zepben.protobuf.cim.iec61970.base.core.Site_pb2 import Site as PBSite
from zepben.protobuf.cim.iec61970.base.core.SubGeographicalRegion_pb2 import SubGeographicalRegion as PBSubGeographicalRegion
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
from zepben.protobuf.cim.iec61970.base.wires.Line_pb2 import Line as PBLine
from zepben.protobuf.cim.iec61970.base.wires.LinearShuntCompensator_pb2 import LinearShuntCompensator as PBLinearShuntCompensator
from zepben.protobuf.cim.iec61970.base.wires.PerLengthImpedance_pb2 import PerLengthImpedance as PBPerLengthImpedance
from zepben.protobuf.cim.iec61970.base.wires.PerLengthLineParameter_pb2 import PerLengthLineParameter as PBPerLengthLineParameter
from zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance_pb2 import PerLengthSequenceImpedance as PBPerLengthSequenceImpedance
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
from zepben.protobuf.cim.iec61970.base.meas.Control_pb2 import Control as PBControl
from zepben.protobuf.cim.iec61970.base.meas.IoPoint_pb2 import IoPoint as PBIoPoint
from zepben.protobuf.cim.iec61970.base.meas.Measurement_pb2 import Measurement as PBMeasurement
from zepben.protobuf.cim.iec61970.base.meas.Accumulator_pb2 import Accumulator as PBAccumulator
from zepben.protobuf.cim.iec61970.base.meas.Analog_pb2 import Analog as PBAnalog
from zepben.protobuf.cim.iec61970.base.meas.Discrete_pb2 import Discrete as PBDiscrete
from zepben.protobuf.cim.iec61970.base.scada.RemoteControl_pb2 import RemoteControl as PBRemoteControl
from zepben.protobuf.cim.iec61970.base.scada.RemotePoint_pb2 import RemotePoint as PBRemotePoint
from zepben.protobuf.cim.iec61970.base.scada.RemoteSource_pb2 import RemoteSource as PBRemoteSource
from zepben.protobuf.cim.iec61970.infiec61970.feeder.Circuit_pb2 import Circuit as PBCircuit
from zepben.protobuf.cim.iec61970.infiec61970.feeder.Loop_pb2 import Loop as PBLoop
from zepben.cimbend.cim.iec61970.base.meas.iopoint import IoPoint
from zepben.cimbend.cim.iec61970.base.meas.control import Control
from zepben.cimbend.cim.iec61970.base.meas.measurement import Measurement, Accumulator, Analog, Discrete
from zepben.cimbend.cim.iec61970.base.scada.remote_control import RemoteControl
from zepben.cimbend.cim.iec61970.base.scada.remote_point import RemotePoint
from zepben.cimbend.cim.iec61970.base.scada.remote_source import RemoteSource

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
from zepben.cimbend.cim.iec61970.base.wires import Conductor, AcLineSegment, Junction, Connector, EnergyConnection, RegulatingCondEq, EnergyConsumer, \
    EnergyConsumerPhase, EnergySource, EnergySourcePhase, PerLengthSequenceImpedance, PerLengthLineParameter, PerLengthImpedance, PhaseShuntConnectionKind, \
    PowerTransformer, PowerTransformerEnd, RatioTapChanger, TapChanger, TransformerEnd, Line, LinearShuntCompensator, ShuntCompensator, Breaker, Disconnector, Fuse, \
    Jumper, ProtectedSwitch, Recloser, Switch, VectorGroup, WindingConnection, phasekind_by_id
from zepben.cimbend.cim.iec61970.infiec61970.feeder import Loop, Circuit
from zepben.cimbend.common.translator.base_proto2cim import BaseProtoToCim
from zepben.cimbend.network.network import NetworkService

from zepben.cimbend.common import resolver

__all__ = ["cableinfo_to_cim", "overheadwireinfo_to_cim", "wireinfo_to_cim", "asset_to_cim", "assetcontainer_to_cim", "assetinfo_to_cim",
           "assetorganisationrole_to_cim", "assetowner_to_cim", "pole_to_cim", "streetlight_to_cim", "structure_to_cim", "location_to_cim",
           "positionpoint_to_cim", "streetaddress_to_cim", "towndetail_to_cim", "enddevice_to_cim", "meter_to_cim", "usagepoint_to_cim",
           "operationalrestriction_to_cim", "auxiliaryequipment_to_cim", "faultindicator_to_cim", "acdcterminal_to_cim", "basevoltage_to_cim",
           "conductingequipment_to_cim", "connectivitynode_to_cim", "connectivitynodecontainer_to_cim", "equipment_to_cim", "equipmentcontainer_to_cim",
           "feeder_to_cim", "geographicalregion_to_cim", "powersystemresource_to_cim", "site_to_cim", "subgeographicalregion_to_cim", "substation_to_cim",
           "terminal_to_cim", "accumulator_to_cim", "analog_to_cim", "control_to_cim", "discrete_to_cim", "iopoint_to_cim", "measurement_to_cim",
           "remotecontrol_to_cim", "remotepoint_to_cim", "remotesource_to_cim", "aclinesegment_to_cim", "breaker_to_cim", "conductor_to_cim",
           "connector_to_cim", "disconnector_to_cim", "energyconnection_to_cim", "energyconsumer_to_cim", "energyconsumerphase_to_cim", "energysource_to_cim",
           "energysourcephase_to_cim", "fuse_to_cim", "jumper_to_cim", "junction_to_cim", "line_to_cim", "linearshuntcompensator_to_cim",
           "perlengthlineparameter_to_cim", "perlengthimpedance_to_cim", "perlengthsequenceimpedance_to_cim", "powertransformer_to_cim",
           "powertransformerend_to_cim", "protectedswitch_to_cim", "ratiotapchanger_to_cim", "recloser_to_cim", "regulatingcondeq_to_cim",
           "shuntcompensator_to_cim", "switch_to_cim", "tapchanger_to_cim", "transformerend_to_cim", "PBPerLengthImpedance", "circuit_to_cim", "loop_to_cim",
           "add_from_pb", "NetworkProtoToCim"]


### IEC61968 ASSET INFO
def cableinfo_to_cim(pb: PBCableInfo, network_service: NetworkService):
    cim = CableInfo(mrid=pb.mrid())
    wireinfo_to_cim(pb.wi, cim, network_service)
    network_service.add(cim)


def overheadwireinfo_to_cim(pb: PBOverheadWireInfo, network_service: NetworkService):
    cim = OverheadWireInfo(mrid=pb.mrid())
    wireinfo_to_cim(pb.wi, cim, network_service)
    network_service.add(cim)


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
    identifiedobject_to_cim(pb.io, cim, network_service)


def assetcontainer_to_cim(pb: PBAssetContainer, cim: AssetContainer, network_service: NetworkService):
    asset_to_cim(pb.at, cim, network_service)


def assetinfo_to_cim(pb: PBAssetInfo, cim: AssetInfo, network_service: NetworkService):
    identifiedobject_to_cim(pb.io, cim, network_service)


def assetorganisationrole_to_cim(pb: PBAssetOrganisationRole, cim: AssetOrganisationRole,
                                 network_service: NetworkService):
    organisationrole_to_cim(getattr(pb, 'or'), cim, network_service)


def assetowner_to_cim(pb: PBAssetOwner, network_service: NetworkService):
    cim = AssetOwner(mrid=pb.mrid())
    assetorganisationrole_to_cim(pb.aor, cim, network_service)
    network_service.add(cim)


def pole_to_cim(pb: PBPole, network_service: NetworkService):
    cim = Pole(mrid=pb.mrid(), classification=pb.classification)
    for mrid in pb.streetlightMRIDs:
        network_service.resolve_or_defer_reference(resolver.streetlights(cim), mrid)
    structure_to_cim(pb.st, cim, network_service)
    network_service.add(cim)


def streetlight_to_cim(pb: PBStreetlight, network_service: NetworkService):
    cim = Streetlight(mrid=pb.mrid(), light_rating=pb.lightRating, lamp_kind=StreetlightLampKind(pb.lampKind))
    network_service.resolve_or_defer_reference(resolver.pole(cim), pb.poleMRID)
    asset_to_cim(pb.at, cim, network_service)
    network_service.add(cim)


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
    cim = Location(mrid=pb.mrid(), main_address=streetaddress_to_cim(pb.mainAddress) if pb.HasField('mainAddress') else None)
    for point in pb.positionPoints:
        cim.add_point(positionpoint_to_cim(point))
    identifiedobject_to_cim(pb.io, cim, network_service)
    network_service.add(cim)


def positionpoint_to_cim(pb: PBPositionPoint) -> PositionPoint:
    return PositionPoint(pb.xPosition, pb.yPosition)



def streetaddress_to_cim(pb: PBStreetAddress) -> StreetAddress:
    return StreetAddress(postal_code=pb.postalCode, town_detail=towndetail_to_cim(pb.townDetail) if pb.HasField('townDetail') else None)


def towndetail_to_cim(pb: PBTownDetail) -> TownDetail:
    return TownDetail(name=pb.name, state_or_province=pb.stateOrProvince)


PBLocation.to_cim = location_to_cim
PBPositionPoint.to_cim = positionpoint_to_cim
PBTownDetail.to_cim = towndetail_to_cim
PBStreetAddress.to_cim = streetaddress_to_cim


### IEC61968 METERING

def enddevice_to_cim(pb: PBEndDevice, cim: EndDevice, network_service: NetworkService):
    for mrid in pb.usagePointMRIDs:
        network_service.resolve_or_defer_reference(resolver.ed_usage_points(cim), mrid)
    cim.customer_mrid = pb.customerMRID if pb.customerMRID else None
    network_service.resolve_or_defer_reference(resolver.service_location(cim), pb.serviceLocationMRID)
    assetcontainer_to_cim(pb.ac, cim, network_service)


def meter_to_cim(pb: PBMeter, network_service: NetworkService):
    cim = Meter(mrid=pb.mrid())
    enddevice_to_cim(pb.ed, cim, network_service)
    network_service.add(cim)


def usagepoint_to_cim(pb: PBUsagePoint, network_service: NetworkService):
    cim = UsagePoint(mrid=pb.mrid())
    network_service.resolve_or_defer_reference(resolver.usage_point_location(cim), pb.usagePointLocationMRID)
    for mrid in pb.equipmentMRIDs:
        network_service.resolve_or_defer_reference(resolver.up_equipment(cim), mrid)
    for mrid in pb.endDeviceMRIDs:
        network_service.resolve_or_defer_reference(resolver.end_devices(cim), mrid)
    identifiedobject_to_cim(pb.io, cim, network_service)
    network_service.add(cim)


PBEndDevice.to_cim = enddevice_to_cim
PBMeter.to_cim = meter_to_cim
PBUsagePoint.to_cim = usagepoint_to_cim


### IEC61968 OPERATIONS
def operationalrestriction_to_cim(pb: PBOperationalRestriction, network_service: NetworkService):
    cim = OperationalRestriction(mrid=pb.mrid())
    for mrid in pb.equipmentMRIDs:
        network_service.resolve_or_defer_reference(resolver.or_equipment(cim), mrid)
    document_to_cim(pb.doc, cim, network_service)
    network_service.add(cim)


PBOperationalRestriction.to_cim = operationalrestriction_to_cim


### IEC61970 AUXILIARY EQUIPMENT
def auxiliaryequipment_to_cim(pb: PBAuxiliaryEquipment, cim: AuxiliaryEquipment, network_service: NetworkService):
    network_service.resolve_or_defer_reference(resolver.ae_terminal(cim), pb.terminalMRID)
    equipment_to_cim(pb.eq, cim, network_service)


def faultindicator_to_cim(pb: PBFaultIndicator, network_service: NetworkService):
    cim = FaultIndicator(mrid=pb.mrid())
    auxiliaryequipment_to_cim(pb.ae, cim, network_service)
    network_service.add(cim)


PBAuxiliaryEquipment.to_cim = auxiliaryequipment_to_cim
PBFaultIndicator.to_cim = faultindicator_to_cim


### IEC61970 CORE
def acdcterminal_to_cim(pb: PBAcDcTerminal, cim: AcDcTerminal, network_service: NetworkService):
    identifiedobject_to_cim(pb.io, cim, network_service)


def basevoltage_to_cim(pb: PBBaseVoltage, network_service: NetworkService):
    cim = BaseVoltage(mrid=pb.mrid())
    identifiedobject_to_cim(pb.io, cim, network_service)
    network_service.add(cim)


def conductingequipment_to_cim(pb: PBConductingEquipment, cim: ConductingEquipment, network_service: NetworkService):
    network_service.resolve_or_defer_reference(resolver.ce_base_voltage(cim), pb.baseVoltageMRID)
    for mrid in pb.terminalMRIDs:
        network_service.resolve_or_defer_reference(resolver.ce_terminals(cim), mrid)
    equipment_to_cim(pb.eq, cim, network_service)


def connectivitynode_to_cim(pb: PBConnectivityNode, network_service: NetworkService):
    cim = network_service.add_connectivitynode(mrid=pb.mrid())
    for mrid in pb.terminalMRIDs:
        network_service.resolve_or_defer_reference(resolver.cn_terminals(cim), mrid)
    identifiedobject_to_cim(pb.io, cim, network_service)


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
    network_service.resolve_or_defer_reference(resolver.normal_energizing_substation(cim), pb.normalEnergizingSubstationMRID)
    for mrid in pb.currentEquipmentMRIDs:
        network_service.resolve_or_defer_reference(resolver.current_equipment(cim), mrid)
    equipmentcontainer_to_cim(pb.ec, cim, network_service)
    network_service.add(cim)


def geographicalregion_to_cim(pb: PBGeographicalRegion, network_service: NetworkService):
    cim = GeographicalRegion(mrid=pb.mrid())
    for mrid in pb.subGeographicalRegionMRIDs:
        network_service.resolve_or_defer_reference(resolver.sub_geographical_regions(cim), mrid)
    identifiedobject_to_cim(pb.io, cim, network_service)
    network_service.add(cim)


def powersystemresource_to_cim(pb: PBPowerSystemResource, cim: PowerSystemResource, network_service: NetworkService):
    network_service.resolve_or_defer_reference(resolver.psr_location(cim), pb.locationMRID)
    identifiedobject_to_cim(pb.io, cim, network_service)


def site_to_cim(pb: PBSite, network_service: NetworkService):
    cim = Site(mrid=pb.mrid())
    equipmentcontainer_to_cim(pb.ec, cim, network_service)
    network_service.add(cim)


def subgeographicalregion_to_cim(pb: PBSubGeographicalRegion, network_service: NetworkService):
    cim = SubGeographicalRegion(mrid=pb.mrid())
    network_service.resolve_or_defer_reference(resolver.geographical_region(cim), pb.geographicalRegionMRID)
    for mrid in pb.substationMRIDs:
        network_service.resolve_or_defer_reference(resolver.substations(cim), mrid)
    identifiedobject_to_cim(pb.io, cim, network_service)
    network_service.add(cim)


def substation_to_cim(pb: PBSubstation, network_service: NetworkService):
    cim = Substation(mrid=pb.mrid())
    network_service.resolve_or_defer_reference(resolver.sub_geographical_region(cim), pb.subGeographicalRegionMRID)
    for mrid in pb.normalEnergizedFeederMRIDs:
        network_service.resolve_or_defer_reference(resolver.normal_energizing_feeders(cim), mrid)
    for mrid in pb.loopMRIDs:
        network_service.resolve_or_defer_reference(resolver.loops(cim), mrid)
    for mrid in pb.normalEnergizedLoopMRIDs:
        network_service.resolve_or_defer_reference(resolver.normal_energized_loops(cim), mrid)
    for mrid in pb.circuitMRIDs:
        network_service.resolve_or_defer_reference(resolver.circuits(cim), mrid)
    equipmentcontainer_to_cim(pb.ec, cim, network_service)
    network_service.add(cim)


def terminal_to_cim(pb: PBTerminal, network_service: NetworkService):
    cim = Terminal(mrid=pb.mrid(), phases=phasecode_by_id(pb.phases), sequence_number=pb.sequenceNumber)
    network_service.resolve_or_defer_reference(resolver.conducting_equipment(cim), pb.conductingEquipmentMRID)
    cim.traced_phases._normal_status = pb.tracedPhases.normalStatus
    cim.traced_phases._current_status = pb.tracedPhases.currentStatus
    network_service.resolve_or_defer_reference(resolver.connectivity_node(cim), pb.connectivityNodeMRID)
    acdcterminal_to_cim(pb.ad, cim, network_service)
    network_service.add(cim)


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


### IEC61970 MEAS ###
def accumulator_to_cim(pb: PBAccumulator, service: NetworkService):
    cim = Accumulator(mrid=pb.mrid())
    measurement_to_cim(pb.measurement, cim, service)
    service.add_measurement(cim)


def analog_to_cim(pb: PBAnalog, service: NetworkService):
    cim = Analog(mrid=pb.mrid(), positive_flow_in=pb.positiveFlowIn)
    measurement_to_cim(pb.measurement, cim, service)
    service.add_measurement(cim)


def control_to_cim(pb: PBControl, service: NetworkService):
    cim = Control(mrid=pb.mrid())
    service.resolve_or_defer_reference(resolver.remote_control(cim), pb.remoteControlMRID)
    iopoint_to_cim(pb.ip, cim, service)
    service.add(cim)


def discrete_to_cim(pb: PBDiscrete, service: NetworkService):
    cim = Discrete(mrid=pb.mrid())
    measurement_to_cim(pb.measurement, cim, service)
    service.add_measurement(cim)


def iopoint_to_cim(pb: PBIoPoint, cim: IoPoint, service: NetworkService):
    identifiedobject_to_cim(pb.io, cim, service)


def measurement_to_cim(pb: PBMeasurement, cim: Measurement, service: NetworkService):
    cim.power_system_resource_mrid = pb.powerSystemResourceMRID
    cim.terminal_mrid = pb.terminalMRID
    cim.phases = PhaseCode(pb.phases)
    cim.unitSymbol = UnitSymbol(pb.unitSymbol)
    service.resolve_or_defer_reference(resolver.remote_source(cim), pb.remoteSourceMRID)
    identifiedobject_to_cim(pb.io, cim)


PBAccumulator.to_cim = accumulator_to_cim
PBAnalog.to_cim = analog_to_cim
PBControl.to_cim = control_to_cim
PBDiscrete.to_cim = discrete_to_cim
PBIoPoint.to_cim = iopoint_to_cim
PBMeasurement.to_cim = measurement_to_cim


# IEC61970 SCADA #
def remotecontrol_to_cim(pb: PBRemoteControl, service: NetworkService):
    cim = RemoteControl(mrid=pb.mrid())
    service.resolve_or_defer_reference(resolver.control(cim), pb.controlMRID)
    remotepoint_to_cim(pb.rp, cim)
    service.add(cim)


def remotepoint_to_cim(pb: PBRemotePoint, cim: RemotePoint, service: NetworkService):
    identifiedobject_to_cim(pb.io, cim, service)


def remotesource_to_cim(pb: PBRemoteSource, service: NetworkService):
    cim = RemoteSource(mrid=pb.mrid())
    service.resolve_or_defer_reference(resolver.measurement(cim), pb.measurementMRID)
    remotepoint_to_cim(pb.rp, cim)
    service.add(cim)


### IEC61970 WIRES
def aclinesegment_to_cim(pb: PBAcLineSegment, network_service: NetworkService):
    cim = AcLineSegment(mrid=pb.mrid())
    network_service.resolve_or_defer_reference(resolver.per_length_sequence_impedance(cim), pb.perLengthSequenceImpedanceMRID)
    conductor_to_cim(pb.cd, cim, network_service)
    network_service.add(cim)


def breaker_to_cim(pb: PBBreaker, network_service: NetworkService):
    cim = Breaker(mrid=pb.mrid())
    protectedswitch_to_cim(pb.sw, cim, network_service)
    network_service.add(cim)


def conductor_to_cim(pb: PBConductor, cim: Conductor, network_service: NetworkService):
    cim.length = pb.length
    network_service.resolve_or_defer_reference(resolver.asset_info(cim), pb.asset_info_mrid())
    conductingequipment_to_cim(pb.ce, cim, network_service)


def connector_to_cim(pb: PBConnector, cim: Connector, network_service: NetworkService):
    conductingequipment_to_cim(pb.ce, cim, network_service)


def disconnector_to_cim(pb: PBDisconnector, network_service: NetworkService):
    cim = Disconnector(mrid=pb.mrid())
    switch_to_cim(pb.sw, cim, network_service)
    network_service.add(cim)


def energyconnection_to_cim(pb: PBEnergyConnection, cim: EnergyConnection, network_service: NetworkService):
    conductingequipment_to_cim(pb.ce, cim, network_service)


def energyconsumer_to_cim(pb: PBEnergyConsumer, network_service: NetworkService):
    cim = EnergyConsumer(mrid=pb.mrid(), customer_count=pb.customerCount, grounded=pb.grounded, p=pb.p, p_fixed=pb.pFixed, q=pb.q, q_fixed=pb.qFixed,
                         phase_connection=PhaseShuntConnectionKind(pb.phaseConnection))
    for mrid in pb.energyConsumerPhasesMRIDs:
        network_service.resolve_or_defer_reference(resolver.ec_phases(cim), mrid)
    energyconnection_to_cim(pb.ec, cim, network_service)
    network_service.add(cim)


def energyconsumerphase_to_cim(pb: PBEnergyConsumerPhase, network_service: NetworkService):
    cim = EnergyConsumerPhase(mrid=pb.mrid(), phase=phasekind_by_id(pb.phase), p=pb.p, p_fixed=pb.pFixed, q=pb.q, q_fixed=pb.qFixed)
    network_service.resolve_or_defer_reference(resolver.energy_consumer(cim), pb.energyConsumerMRID)
    powersystemresource_to_cim(pb.psr, cim, network_service)
    network_service.add(cim)


def energysource_to_cim(pb: PBEnergySource, network_service: NetworkService):
    cim = EnergySource(mrid=pb.mrid(), active_power=pb.activePower, reactive_power=pb.reactivePower, voltage_angle = pb.voltageAngle,
                       voltage_magnitude=pb.voltageMagnitude, r=pb.r, x=pb.x, p_max=pb.pMax, p_min=pb.pMin, r0=pb.r0, rn=pb.rn, x0=pb.x0, xn=pb.xn)
    for mrid in pb.energySourcePhasesMRIDs:
        network_service.resolve_or_defer_reference(resolver.es_phases(cim), mrid)
    energyconnection_to_cim(pb.ec, cim, network_service)
    network_service.add(cim)


def energysourcephase_to_cim(pb: PBEnergySourcePhase, network_service: NetworkService):
    cim = EnergySourcePhase(mrid=pb.mrid(), phase=phasekind_by_id(pb.phase))
    network_service.resolve_or_defer_reference(resolver.energy_source(cim), pb.energySourceMRID)
    powersystemresource_to_cim(pb.psr, cim, network_service)
    network_service.add(cim)


def fuse_to_cim(pb: PBFuse, network_service: NetworkService):
    cim = Fuse(mrid=pb.mrid())
    switch_to_cim(pb.sw, cim, network_service)
    network_service.add(cim)


def jumper_to_cim(pb: PBJumper, network_service: NetworkService):
    cim = Jumper(mrid=pb.mrid())
    switch_to_cim(pb.sw, cim, network_service)
    network_service.add(cim)


def junction_to_cim(pb: PBJunction, network_service: NetworkService):
    cim = Junction(mrid=pb.mrid())
    connector_to_cim(pb.cn, cim, network_service)
    network_service.add(cim)


def line_to_cim(pb: PBLine, cim: Line, network_service: NetworkService):
    equipmentcontainer_to_cim(pb.ec, cim, network_service)


def linearshuntcompensator_to_cim(pb: PBLinearShuntCompensator, network_service: NetworkService):
    cim = LinearShuntCompensator(mrid=pb.mrid(), b0_per_section=pb.b0PerSection, b_per_section=pb.bPerSection, g0_per_section=pb.g0PerSection,
                                 g_per_section=pb.gPerSection)
    shuntcompensator_to_cim(pb.sc, cim, network_service)
    network_service.add(cim)


def perlengthlineparameter_to_cim(pb: PBPerLengthLineParameter, cim: PerLengthLineParameter,
                                  network_service: NetworkService):
    identifiedobject_to_cim(pb.io, cim, network_service)


def perlengthimpedance_to_cim(pb: PBPerLengthImpedance, cim: PerLengthImpedance, network_service: NetworkService):
    perlengthlineparameter_to_cim(pb.lp, cim, network_service)


def perlengthsequenceimpedance_to_cim(pb: PBPerLengthSequenceImpedance, network_service: NetworkService):
    cim = PerLengthSequenceImpedance(mrid=pb.mrid(), r=pb.r, x=pb.x, r0=pb.r0, x0=pb.x0, bch=pb.bch, gch=pb.gch, b0ch=pb.b0ch, g0ch=pb.g0ch)
    perlengthimpedance_to_cim(pb.pli, cim, network_service)
    network_service.add(cim)


def powertransformer_to_cim(pb: PBPowerTransformer, network_service: NetworkService):
    cim = PowerTransformer(mrid=pb.mrid(), vector_group=VectorGroup(pb.vectorGroup))
    for mrid in pb.powerTransformerEndMRIDs:
        network_service.resolve_or_defer_reference(resolver.ends(cim), mrid)
    conductingequipment_to_cim(pb.ce, cim, network_service)
    network_service.add(cim)


def powertransformerend_to_cim(pb: PBPowerTransformerEnd, network_service: NetworkService):
    cim = PowerTransformerEnd(mrid=pb.mrid(), rated_s=pb.ratedS, rated_u=pb.ratedU, r=pb.r, r0=pb.r0, x=pb.x, x0=pb.x0, b=pb.b, b0=pb.b0, g=pb.g, g0=pb.g0,
                              connection_kind=WindingConnection(pb.connectionKind), phase_angle_clock=pb.phaseAngleClock)
    network_service.resolve_or_defer_reference(resolver.power_transformer(cim), pb.powerTransformerMRID)
    transformerend_to_cim(pb.te, cim, network_service)
    network_service.add(cim)


def protectedswitch_to_cim(pb: PBProtectedSwitch, cim: ProtectedSwitch, network_service: NetworkService):
    switch_to_cim(pb.sw, cim, network_service)


def ratiotapchanger_to_cim(pb: PBRatioTapChanger, network_service: NetworkService):
    cim = RatioTapChanger(mrid=pb.mrid(), step_voltage_increment=pb.stepVoltageIncrement)
    tapchanger_to_cim(pb.tc, cim, network_service)
    network_service.add(cim)


def recloser_to_cim(pb: PBRecloser, network_service: NetworkService):
    cim = Recloser(mrid=pb.mrid())
    protectedswitch_to_cim(pb.sw, cim, network_service)
    network_service.add(cim)


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
    cim.end_number = pb.endNumber
    cim.grounded = pb.grounded
    cim.r_ground = pb.rGround
    cim.x_ground = pb.xGround
    identifiedobject_to_cim(pb.io, cim, network_service)


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
PBLine.to_cim = line_to_cim
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


def circuit_to_cim(pb: PBCircuit, network_service: NetworkService):
    cim = Circuit(mrid=pb.mrid())
    for mrid in pb.endTerminalMRIDs:
        network_service.resolve_or_defer_reference(resolver.end_terminal(cim), mrid)
    for mrid in pb.endSubstationMRIDs:
        network_service.resolve_or_defer_reference(resolver.end_substation(cim), mrid)
    line_to_cim(pb.l, cim, network_service)
    network_service.add(cim)


def loop_to_cim(pb: PBLoop, network_service: NetworkService):
    cim = Loop(mrid=pb.mrid())
    for mrid in pb.circuitMRIDs:
        network_service.resolve_or_defer_reference(resolver.loop_circuits(cim), mrid)
    for mrid in pb.substationMRIDs:
        network_service.resolve_or_defer_reference(resolver.loop_substations(cim), mrid)
    for mrid in pb.normalEnergizingSubstationMRIDs:
        network_service.resolve_or_defer_reference(resolver.loop_energizing_substations(cim), mrid)
    identifiedobject_to_cim(pb.io, cim, network_service)
    network_service.add(cim)


PBCircuit.to_cim = circuit_to_cim
PBLoop.to_cim = loop_to_cim


# Extensions
def add_from_pb(network_service: NetworkService, pb):
    """Must only be called by objects for which .to_cim() takes themselves and the network service."""
    pb.to_cim(network_service)


NetworkService.add_from_pb = add_from_pb


# Convenience class for adding to the service
class NetworkProtoToCim(BaseProtoToCim):
    service: NetworkService

    def add_from_pb(self, pb):
        """Must only be called by objects for which .to_cim() takes themselves and the network."""
        pb.to_cim(self.service)
