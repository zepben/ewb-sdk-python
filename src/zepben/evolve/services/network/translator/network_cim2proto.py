#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve.services.common.translator.base_cim2proto import identifiedobject_to_pb, organisationrole_to_pb, document_to_pb
from zepben.evolve.services.common.translator.util import mrid_or_empty
from zepben.evolve.model.cim.iec61968.assets.structure import *
from zepben.evolve.model.cim.iec61968.assets.asset import *
from zepben.evolve.model.cim.iec61968.assets.pole import *
from zepben.evolve.model.cim.iec61968.assets.asset_organisation_role import *
from zepben.evolve.model.cim.iec61968.assets.asset_info import *
from zepben.evolve.model.cim.iec61968.assets.streetlight import *
from zepben.evolve.model.cim.iec61968.operations.operational_restriction import *
from zepben.evolve.model.cim.iec61968.assetinfo.wire_info import *
from zepben.evolve.model.cim.iec61968.assetinfo.power_transformer_info import *
from zepben.evolve.model.cim.iec61968.metering.metering import *
from zepben.evolve.model.cim.iec61968.common.location import *
from zepben.evolve.model.cim.iec61970.base.meas.control import *
from zepben.evolve.model.cim.iec61970.base.meas.measurement import *
from zepben.evolve.model.cim.iec61970.base.meas.iopoint import *
from zepben.evolve.model.cim.iec61970.base.scada.remote_point import *
from zepben.evolve.model.cim.iec61970.base.scada.remote_source import *
from zepben.evolve.model.cim.iec61970.base.scada.remote_control import *
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.auxiliary_equipment import *
from zepben.evolve.model.cim.iec61970.base.wires.generation.production.power_electronics_unit import *
from zepben.evolve.model.cim.iec61970.base.wires.line import *
from zepben.evolve.model.cim.iec61970.base.wires.energy_consumer import *
from zepben.evolve.model.cim.iec61970.base.wires.aclinesegment import *
from zepben.evolve.model.cim.iec61970.base.wires.per_length import *
from zepben.evolve.model.cim.iec61970.base.wires.shunt_compensator import *
from zepben.evolve.model.cim.iec61970.base.wires.power_electronics_connection import *
from zepben.evolve.model.cim.iec61970.base.wires.power_transformer import *
from zepben.evolve.model.cim.iec61970.base.wires.energy_source_phase import *
from zepben.evolve.model.cim.iec61970.base.wires.connectors import *
from zepben.evolve.model.cim.iec61970.base.wires.switch import *
from zepben.evolve.model.cim.iec61970.base.wires.energy_source import *
from zepben.evolve.model.cim.iec61970.base.wires.energy_connection import *
from zepben.evolve.model.cim.iec61970.base.core.substation import *
from zepben.evolve.model.cim.iec61970.base.core.terminal import *
from zepben.evolve.model.cim.iec61970.base.core.equipment import *
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import *
from zepben.evolve.model.cim.iec61970.base.core.base_voltage import *
from zepben.evolve.model.cim.iec61970.base.core.power_system_resource import *
from zepben.evolve.model.cim.iec61970.base.core.connectivity_node_container import *
from zepben.evolve.model.cim.iec61970.base.core.regions import *
from zepben.evolve.model.cim.iec61970.base.core.equipment_container import *
from zepben.evolve.model.cim.iec61970.base.core.connectivity_node import *
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.circuit import *
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.loop import *
from zepben.evolve.model.phases import *

from zepben.protobuf.cim.iec61968.assetinfo.CableInfo_pb2 import CableInfo as PBCableInfo
from zepben.protobuf.cim.iec61968.assetinfo.OverheadWireInfo_pb2 import OverheadWireInfo as PBOverheadWireInfo
from zepben.protobuf.cim.iec61968.assetinfo.WireInfo_pb2 import WireInfo as PBWireInfo
from zepben.protobuf.cim.iec61968.assetinfo.PowerTransformerInfo_pb2 import PowerTransformerInfo as PBPowerTransformerInfo
from zepben.protobuf.cim.iec61968.assetinfo.WireMaterialKind_pb2 import WireMaterialKind as PBWireMaterialKind
from zepben.protobuf.cim.iec61968.assets.AssetContainer_pb2 import AssetContainer as PBAssetContainer
from zepben.protobuf.cim.iec61968.assets.AssetInfo_pb2 import AssetInfo as PBAssetInfo
from zepben.protobuf.cim.iec61968.assets.AssetOrganisationRole_pb2 import AssetOrganisationRole as PBAssetOrganisationRole
from zepben.protobuf.cim.iec61968.assets.AssetOwner_pb2 import AssetOwner as PBAssetOwner
from zepben.protobuf.cim.iec61968.assets.Asset_pb2 import Asset as PBAsset
from zepben.protobuf.cim.iec61968.assets.Pole_pb2 import Pole as  PBPole
from zepben.protobuf.cim.iec61968.assets.StreetlightLampKind_pb2 import StreetlightLampKind as PBStreetlightLampKind
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
from zepben.protobuf.cim.iec61970.base.core.PhaseCode_pb2 import PhaseCode as PBPhaseCode
from zepben.protobuf.cim.iec61970.base.core.PowerSystemResource_pb2 import PowerSystemResource as PBPowerSystemResource
from zepben.protobuf.cim.iec61970.base.core.Site_pb2 import Site as PBSite
from zepben.protobuf.cim.iec61970.base.core.SubGeographicalRegion_pb2 import SubGeographicalRegion as PBSubGeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.Substation_pb2 import Substation as PBSubstation
from zepben.protobuf.cim.iec61970.base.core.Terminal_pb2 import Terminal as PBTerminal
from zepben.protobuf.cim.iec61970.base.domain.UnitSymbol_pb2 import UnitSymbol as PBUnitSymbol
from zepben.protobuf.cim.iec61970.base.meas.Accumulator_pb2 import Accumulator as PBAccumulator
from zepben.protobuf.cim.iec61970.base.meas.Analog_pb2 import Analog as PBAnalog
from zepben.protobuf.cim.iec61970.base.meas.Control_pb2 import Control as PBControl
from zepben.protobuf.cim.iec61970.base.meas.Discrete_pb2 import Discrete as PBDiscrete
from zepben.protobuf.cim.iec61970.base.meas.IoPoint_pb2 import IoPoint as PBIoPoint
from zepben.protobuf.cim.iec61970.base.meas.Measurement_pb2 import Measurement as PBMeasurement
from zepben.protobuf.cim.iec61970.base.scada.RemoteControl_pb2 import RemoteControl as PBRemoteControl
from zepben.protobuf.cim.iec61970.base.scada.RemoteSource_pb2 import RemoteSource as PBRemoteSource
from zepben.protobuf.cim.iec61970.base.scada.RemotePoint_pb2 import RemotePoint as PBRemotePoint
from zepben.protobuf.cim.iec61970.base.wires.generation.production.BatteryStateKind_pb2 import BatteryStateKind as PBBatteryStateKind
from zepben.protobuf.cim.iec61970.base.wires.generation.production.BatteryUnit_pb2 import BatteryUnit as PBBatteryUnit
from zepben.protobuf.cim.iec61970.base.wires.generation.production.PhotoVoltaicUnit_pb2 import PhotoVoltaicUnit as PBPhotoVoltaicUnit
from zepben.protobuf.cim.iec61970.base.wires.generation.production.PowerElectronicsUnit_pb2 import PowerElectronicsUnit as PBPowerElectronicsUnit
from zepben.protobuf.cim.iec61970.base.wires.generation.production.PowerElectronicsWindUnit_pb2 import PowerElectronicsWindUnit as PBPowerElectronicsWindUnit
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
from zepben.protobuf.cim.iec61970.base.wires.BusbarSection_pb2 import BusbarSection as PBBusbarSection
from zepben.protobuf.cim.iec61970.base.wires.Line_pb2 import Line as PBLine
from zepben.protobuf.cim.iec61970.base.wires.LinearShuntCompensator_pb2 import LinearShuntCompensator as PBLinearShuntCompensator
from zepben.protobuf.cim.iec61970.base.wires.LoadBreakSwitch_pb2 import LoadBreakSwitch as PBLoadBreakSwitch
from zepben.protobuf.cim.iec61970.base.wires.PerLengthImpedance_pb2 import PerLengthImpedance as PBPerLengthImpedance
from zepben.protobuf.cim.iec61970.base.wires.PerLengthLineParameter_pb2 import PerLengthLineParameter as PBPerLengthLineParameter
from zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance_pb2 import PerLengthSequenceImpedance as PBPerLengthSequenceImpedance
from zepben.protobuf.cim.iec61970.base.wires.PhaseShuntConnectionKind_pb2 import PhaseShuntConnectionKind as PBPhaseShuntConnectionKind
from zepben.protobuf.cim.iec61970.base.wires.PowerElectronicsConnection_pb2 import PowerElectronicsConnection as PBPowerElectronicsConnection
from zepben.protobuf.cim.iec61970.base.wires.PowerElectronicsConnectionPhase_pb2 import PowerElectronicsConnectionPhase as PBPowerElectronicsConnectionPhase
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
from zepben.protobuf.cim.iec61970.infiec61970.feeder.Loop_pb2 import Loop as PBLoop
from zepben.protobuf.cim.iec61970.infiec61970.feeder.Circuit_pb2 import Circuit as PBCircuit
from zepben.protobuf.network.model.TracedPhases_pb2 import TracedPhases as PBTracedPhases

__all__ = ["CimTranslationException", "cableinfo_to_pb", "overheadwireinfo_to_pb", "wireinfo_to_pb", "power_transformer_info_to_pb", "asset_to_pb",
           "assetcontainer_to_pb", "assetinfo_to_pb",
           "assetorganisationrole_to_pb", "assetowner_to_pb", "pole_to_pb", "streetlight_to_pb", "structure_to_pb",
           "positionpoint_to_pb", "towndetail_to_pb", "streetaddress_to_pb",
           "location_to_pb", "enddevice_to_pb", "meter_to_pb", "usagepoint_to_pb", "operationalrestriction_to_pb",
           "auxiliaryequipment_to_pb", "faultindicator_to_pb", "acdcterminal_to_pb", "basevoltage_to_pb",
           "conductingequipment_to_pb", "connectivitynode_to_pb", "connectivitynodecontainer_to_pb", "equipment_to_pb",
           "equipmentcontainer_to_pb", "feeder_to_pb", "geographicalregion_to_pb", "powersystemresource_to_pb", "site_to_pb",
           "subgeographicalregion_to_pb", "substation_to_pb", "terminal_to_pb", "perlengthlineparameter_to_pb",
           "perlengthimpedance_to_pb", "powerelectronicsunit_to_pb", "batteryunit_to_pb", "photovoltaicunit_to_pb", "powerelectronicswindunit_to_pb",
           "aclinesegment_to_pb", "breaker_to_pb", "conductor_to_pb", "connector_to_pb",
           "disconnector_to_pb", "energyconnection_to_pb", "energyconsumer_to_pb", "energyconsumerphase_to_pb",
           "energysource_to_pb", "energysourcephase_to_pb", "fuse_to_pb", "jumper_to_pb", "junction_to_pb", "loadbreakswitch_to_pb",
           "linearshuntcompensator_to_pb", "perlengthsequenceimpedance_to_pb", "powerelectronicsconnection_to_pb", "powerelectronicsconnectionphase_to_pb",
           "powertransformer_to_pb", "powertransformerend_to_pb", "protectedswitch_to_pb", "ratiotapchanger_to_pb", "recloser_to_pb",
           "regulatingcondeq_to_pb", "shuntcompensator_to_pb", "switch_to_pb", "tapchanger_to_pb", "transformerend_to_pb",
           "tracedphases_to_pb"]


def get_or_none(getter, obj) -> object:
    return getter(obj) if obj else None


class CimTranslationException(Exception):
    pass


# IEC61968 ASSET INFO #
def cableinfo_to_pb(cim: CableInfo) -> PBCableInfo:
    return PBCableInfo(wi=wireinfo_to_pb(cim))


def overheadwireinfo_to_pb(cim: OverheadWireInfo) -> PBOverheadWireInfo:
    return PBOverheadWireInfo(wi=wireinfo_to_pb(cim))


def wireinfo_to_pb(cim: WireInfo) -> PBWireInfo:
    return PBWireInfo(ai=assetinfo_to_pb(cim),
                      ratedCurrent=cim.rated_current,
                      material=PBWireMaterialKind.Value(cim.material.short_name))


def power_transformer_info_to_pb(cim: PowerTransformerInfo) -> PBPowerTransformerInfo:
    return PBPowerTransformerInfo(ai=assetinfo_to_pb(cim))


# IEC61968 ASSETS #
def asset_to_pb(cim: Asset) -> PBAsset:
    return PBAsset(io=identifiedobject_to_pb(cim),
                   locationMRID=cim.location.mrid if cim.location else None,
                   organisationRoleMRIDs=[str(io.mrid) for io in cim.organisation_roles])


def assetcontainer_to_pb(cim: AssetContainer) -> PBAssetContainer:
    return PBAssetContainer(at=asset_to_pb(cim))


def assetinfo_to_pb(cim: AssetInfo) -> PBAssetInfo:
    return PBAssetInfo(io=identifiedobject_to_pb(cim))


def assetorganisationrole_to_pb(cim: AssetOrganisationRole) -> PBAssetOrganisationRole:
    pb = PBAssetOrganisationRole()
    getattr(pb, "or").CopyFrom(organisationrole_to_pb(cim))
    return pb


def assetowner_to_pb(cim: AssetOwner) -> PBAssetOwner:
    return PBAssetOwner(aor=assetorganisationrole_to_pb(cim))


def pole_to_pb(cim: Pole) -> PBPole:
    return PBPole(st=structure_to_pb(cim), streetlightMRIDs=[str(io.mrid) for io in cim.streetlights], classification=cim.classification)


def streetlight_to_pb(cim: Streetlight) -> PBStreetlight:
    return PBStreetlight(at=asset_to_pb(cim),
                         poleMRID=str(cim.pole.mrid),
                         lightRating=cim.light_rating,
                         lampKind=PBStreetlightLampKind.Value(cim.lamp_kind.short_name))


def structure_to_pb(cim: Structure) -> PBStructure:
    return PBStructure(ac=assetcontainer_to_pb(cim))


# IEC61968 COMMON #
def location_to_pb(cim: Location) -> PBLocation:
    return PBLocation(io=identifiedobject_to_pb(cim),
                      mainAddress=get_or_none(streetaddress_to_pb, cim.main_address),
                      positionPoints=[positionpoint_to_pb(point) for point in cim.points])


def positionpoint_to_pb(cim: PositionPoint) -> PBPositionPoint:
    return PBPositionPoint(xPosition=cim.x_position, yPosition=cim.y_position)


def streetaddress_to_pb(cim: StreetAddress) -> PBStreetAddress:
    return PBStreetAddress(postalCode=cim.postal_code, townDetail=get_or_none(towndetail_to_pb, cim.town_detail))


def towndetail_to_pb(cim: TownDetail) -> PBTownDetail:
    return PBTownDetail(name=cim.name, stateOrProvince=cim.state_or_province)


# IEC61968 METERING #
def enddevice_to_pb(cim: EndDevice) -> PBEndDevice:
    return PBEndDevice(ac=assetcontainer_to_pb(cim),
                       usagePointMRIDs=[str(io.mrid) for io in cim.usage_points],
                       customerMRID=cim.customer_mrid,
                       serviceLocationMRID=mrid_or_empty(cim.service_location))


def meter_to_pb(cim: Meter) -> PBMeter:
    return PBMeter(ed=enddevice_to_pb(cim))


def usagepoint_to_pb(cim: UsagePoint) -> PBUsagePoint:
    return PBUsagePoint(io=identifiedobject_to_pb(cim),
                        usagePointLocationMRID=mrid_or_empty(cim.usage_point_location),
                        equipmentMRIDs=[str(io.mrid) for io in cim.equipment],
                        endDeviceMRIDs=[str(io.mrid) for io in cim.end_devices])


# IEC61968 OPERATIONS #
def operationalrestriction_to_pb(cim: OperationalRestriction) -> PBOperationalRestriction:
    return PBOperationalRestriction(doc=document_to_pb(cim))


# IEC61970 AUXILIARY EQUIPMENT #
def auxiliaryequipment_to_pb(cim: AuxiliaryEquipment) -> PBAuxiliaryEquipment:
    return PBAuxiliaryEquipment(eq=equipment_to_pb(cim),
                                terminalMRID=mrid_or_empty(cim.terminal))


def faultindicator_to_pb(cim: FaultIndicator) -> PBFaultIndicator:
    return PBFaultIndicator(ae=auxiliaryequipment_to_pb(cim))


# IEC61970 CORE #
def acdcterminal_to_pb(cim: AcDcTerminal) -> PBAcDcTerminal:
    return PBAcDcTerminal(io=identifiedobject_to_pb(cim))


def basevoltage_to_pb(cim: BaseVoltage) -> PBBaseVoltage:
    return PBBaseVoltage(io=identifiedobject_to_pb(cim),
                         nominalVoltage=cim.nominal_voltage)


def conductingequipment_to_pb(cim: ConductingEquipment) -> PBConductingEquipment:
    return PBConductingEquipment(eq=equipment_to_pb(cim),
                                 baseVoltageMRID=mrid_or_empty(cim.base_voltage),
                                 terminalMRIDs=[str(io.mrid) for io in cim.terminals])


def connectivitynode_to_pb(cim: ConnectivityNode) -> PBConnectivityNode:
    return PBConnectivityNode(io=identifiedobject_to_pb(cim))


def connectivitynodecontainer_to_pb(cim: ConnectivityNodeContainer) -> PBConnectivityNodeContainer:
    return PBConnectivityNodeContainer(psr=powersystemresource_to_pb(cim))


def equipment_to_pb(cim: Equipment) -> PBEquipment:
    pb = PBEquipment(psr=powersystemresource_to_pb(cim),
                     inService=cim.in_service,
                     normallyInService=cim.normally_in_service,
                     equipmentContainerMRIDs=[str(io.mrid) for io in cim.equipment_containers],
                     usagePointMRIDs=[str(io.mrid) for io in cim.usage_points],
                     operationalRestrictionMRIDs=[str(io.mrid) for io in cim.operational_restrictions],
                     currentFeederMRIDs=[str(io.mrid) for io in cim.current_feeders])
    return pb


def equipmentcontainer_to_pb(cim: EquipmentContainer) -> PBEquipmentContainer:
    return PBEquipmentContainer(cnc=connectivitynodecontainer_to_pb(cim))


def feeder_to_pb(cim: Feeder) -> PBFeeder:
    return PBFeeder(ec=equipmentcontainer_to_pb(cim),
                    normalHeadTerminalMRID=mrid_or_empty(cim.normal_head_terminal),
                    normalEnergizingSubstationMRID=mrid_or_empty(cim.normal_energizing_substation))


def geographicalregion_to_pb(cim: GeographicalRegion) -> PBGeographicalRegion:
    return PBGeographicalRegion(io=identifiedobject_to_pb(cim),
                                subGeographicalRegionMRIDs=[str(io.mrid) for io in cim.sub_geographical_regions])


def powersystemresource_to_pb(cim: PowerSystemResource) -> PBPowerSystemResource:
    return PBPowerSystemResource(io=identifiedobject_to_pb(cim),
                                 assetInfoMRID=mrid_or_empty(cim.asset_info),
                                 locationMRID=mrid_or_empty(cim.location))


def site_to_pb(cim: Site) -> PBSite:
    return PBSite(ec=equipmentcontainer_to_pb(cim))


def subgeographicalregion_to_pb(cim: SubGeographicalRegion) -> PBSubGeographicalRegion:
    return PBSubGeographicalRegion(io=identifiedobject_to_pb(cim),
                                   geographicalRegionMRID=mrid_or_empty(cim.geographical_region),
                                   substationMRIDs=[str(io.mrid) for io in cim.substations])


def substation_to_pb(cim: Substation) -> PBSubstation:
    return PBSubstation(ec=equipmentcontainer_to_pb(cim),
                        subGeographicalRegionMRID=mrid_or_empty(cim.sub_geographical_region),
                        normalEnergizedFeederMRIDs=[str(io.mrid) for io in cim.feeders],
                        loopMRIDs=[str(io.mrid) for io in cim.loops],
                        normalEnergizedLoopMRIDs=[str(io.mrid) for io in cim.energized_loops],
                        circuitMRIDs=[str(io.mrid) for io in cim.circuits])


def terminal_to_pb(cim: Terminal) -> PBTerminal:
    return PBTerminal(ad=acdcterminal_to_pb(cim),
                      conductingEquipmentMRID=mrid_or_empty(cim.conducting_equipment),
                      connectivityNodeMRID=mrid_or_empty(cim.connectivity_node),
                      tracedPhases=get_or_none(tracedphases_to_pb, cim.traced_phases),
                      phases=PBPhaseCode.Value(cim.phases.short_name),
                      sequenceNumber=cim.sequence_number)


# IEC61970 WIRES #
def powerelectronicsunit_to_pb(cim: PowerElectronicsUnit) -> PBPowerElectronicsUnit:
    return PBPowerElectronicsUnit(eq=equipment_to_pb(cim),
                                  maxP=cim.max_p,
                                  minP=cim.min_p,
                                  powerElectronicsConnectionMRID=mrid_or_empty(cim.power_electronics_connection))


def batteryunit_to_pb(cim: BatteryUnit) -> PBBatteryUnit:
    return PBBatteryUnit(peu=powerelectronicsunit_to_pb(cim),
                         ratedE=cim.rated_e,
                         storedE=cim.stored_e,
                         batteryState=PBBatteryStateKind.Value(cim.battery_state.short_name))


def photovoltaicunit_to_pb(cim: PhotoVoltaicUnit) -> PBPhotoVoltaicUnit:
    return PBPhotoVoltaicUnit(peu=powerelectronicsunit_to_pb(cim))


def powerelectronicswindunit_to_pb(cim: PowerElectronicsWindUnit) -> PBPowerElectronicsWindUnit:
    return PBPowerElectronicsWindUnit(peu=powerelectronicsunit_to_pb(cim))


def aclinesegment_to_pb(cim: AcLineSegment) -> PBAcLineSegment:
    return PBAcLineSegment(cd=conductor_to_pb(cim), perLengthSequenceImpedanceMRID=mrid_or_empty(cim.per_length_sequence_impedance))


def breaker_to_pb(cim: Breaker) -> PBBreaker:
    return PBBreaker(sw=protectedswitch_to_pb(cim))


def conductor_to_pb(cim: Conductor) -> PBConductor:
    return PBConductor(ce=conductingequipment_to_pb(cim), length=cim.length)


def connector_to_pb(cim: Connector) -> PBConnector:
    return PBConnector(ce=conductingequipment_to_pb(cim))


def disconnector_to_pb(cim: Disconnector) -> PBDisconnector:
    return PBDisconnector(sw=switch_to_pb(cim))


def energyconnection_to_pb(cim: EnergyConnection) -> PBEnergyConnection:
    return PBEnergyConnection(ce=conductingequipment_to_pb(cim))


def energyconsumer_to_pb(cim: EnergyConsumer) -> PBEnergyConsumer:
    return PBEnergyConsumer(ec=energyconnection_to_pb(cim),
                            energyConsumerPhasesMRIDs=[str(io.mrid) for io in cim.phases],
                            customerCount=cim.customer_count,
                            grounded=cim.grounded,
                            p=cim.p,
                            pFixed=cim.p_fixed,
                            phaseConnection=PBPhaseShuntConnectionKind.Enum.Value(cim.phase_connection.short_name),
                            q=cim.q,
                            qFixed=cim.q_fixed)


def energyconsumerphase_to_pb(cim: EnergyConsumerPhase) -> PBEnergyConsumerPhase:
    return PBEnergyConsumerPhase(psr=powersystemresource_to_pb(cim),
                                 energyConsumerMRID=mrid_or_empty(cim.energy_consumer),
                                 phase=PBSinglePhaseKind.Value(cim.phase.short_name),
                                 p=cim.p,
                                 pFixed=cim.p_fixed,
                                 q=cim.q,
                                 qFixed=cim.q_fixed)


def energysource_to_pb(cim: EnergySource) -> PBEnergySource:
    return PBEnergySource(ec=energyconnection_to_pb(cim),
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


def energysourcephase_to_pb(cim: EnergySourcePhase) -> PBEnergySourcePhase:
    return PBEnergySourcePhase(psr=powersystemresource_to_pb(cim),
                               energySourceMRID=mrid_or_empty(cim.energy_source),
                               phase=PBSinglePhaseKind.Value(cim.phase.short_name))


def fuse_to_pb(cim: Fuse) -> PBFuse:
    return PBFuse(sw=switch_to_pb(cim))


def jumper_to_pb(cim: Jumper) -> PBJumper:
    return PBJumper(sw=switch_to_pb(cim))


def junction_to_pb(cim: Junction) -> PBJunction:
    return PBJunction(cn=connector_to_pb(cim))


def busbarsection_to_pb(cim: BusbarSection) -> PBBusbarSection:
    return PBBusbarSection(cn=connector_to_pb(cim))


def line_to_pb(cim: Line) -> PBLine:
    return PBLine(ec=equipmentcontainer_to_pb(cim))


def linearshuntcompensator_to_pb(cim: LinearShuntCompensator) -> PBLinearShuntCompensator:
    return PBLinearShuntCompensator(sc=shuntcompensator_to_pb(cim),
                                    b0PerSection=cim.b0_per_section,
                                    bPerSection=cim.b_per_section,
                                    g0PerSection=cim.g0_per_section,
                                    gPerSection=cim.g_per_section)


def loadbreakswitch_to_pb(cim: LoadBreakSwitch) -> PBLoadBreakSwitch:
    return PBLoadBreakSwitch(ps=protectedswitch_to_pb(cim))


def perlengthlineparameter_to_pb(cim: PerLengthLineParameter) -> PBPerLengthLineParameter:
    return PBPerLengthLineParameter(io=identifiedobject_to_pb(cim))


def perlengthimpedance_to_pb(cim: PerLengthImpedance) -> PBPerLengthImpedance:
    return PBPerLengthImpedance(lp=perlengthlineparameter_to_pb(cim))


def perlengthsequenceimpedance_to_pb(cim: PerLengthSequenceImpedance) -> PBPerLengthSequenceImpedance:
    return PBPerLengthSequenceImpedance(pli=perlengthimpedance_to_pb(cim),
                                        r=cim.r,
                                        x=cim.x,
                                        r0=cim.r0,
                                        x0=cim.x0,
                                        bch=cim.bch,
                                        gch=cim.gch,
                                        b0ch=cim.b0ch,
                                        g0ch=cim.g0ch)


def powerelectronicsconnection_to_pb(cim: PowerElectronicsConnection) -> PBPowerElectronicsConnection:
    return PBPowerElectronicsConnection(rce=regulatingcondeq_to_pb(cim),
                                        powerElectronicsUnitMRIDs=[str(io.mrid) for io in cim.units],
                                        powerElectronicsConnectionPhaseMRIDs=[str(io.mrid) for io in cim.phases],
                                        maxIFault = cim.max_i_fault,
                                        maxQ=cim.max_q,
                                        minQ=cim.min_q,
                                        p=cim.p,
                                        q=cim.q,
                                        ratedS=cim.rated_s,
                                        ratedU=cim.rated_u)


def powerelectronicsconnectionphase_to_pb(cim: PowerElectronicsConnectionPhase) -> PBPowerElectronicsConnectionPhase:
    return PBPowerElectronicsConnectionPhase(psr=powersystemresource_to_pb(cim),
                                             powerElectronicsConnectionMRID=mrid_or_empty(cim.power_electronics_connection),
                                             p=cim.p,
                                             q=cim.q,
                                             phase=PBSinglePhaseKind.Value(cim.phase.short_name))


def powertransformer_to_pb(cim: PowerTransformer) -> PBPowerTransformer:
    return PBPowerTransformer(ce=conductingequipment_to_pb(cim),
                              powerTransformerEndMRIDs=[str(io.mrid) for io in cim.ends],
                              vectorGroup=PBVectorGroup.Value(cim.vector_group.short_name),
                              transformerUtilisation=cim.transformer_utilisation)


def powertransformerend_to_pb(cim: PowerTransformerEnd) -> PBPowerTransformerEnd:
    return PBPowerTransformerEnd(te=transformerend_to_pb(cim),
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


def protectedswitch_to_pb(cim: ProtectedSwitch) -> PBProtectedSwitch:
    return PBProtectedSwitch(sw=switch_to_pb(cim))


def ratiotapchanger_to_pb(cim: RatioTapChanger) -> PBRatioTapChanger:
    return PBRatioTapChanger(tc=tapchanger_to_pb(cim),
                             transformerEndMRID=mrid_or_empty(cim.transformer_end),
                             stepVoltageIncrement=cim.step_voltage_increment)


def recloser_to_pb(cim: Recloser) -> PBRecloser:
    return PBRecloser(sw=protectedswitch_to_pb(cim))


def regulatingcondeq_to_pb(cim: RegulatingCondEq) -> PBRegulatingCondEq:
    return PBRegulatingCondEq(ec=energyconnection_to_pb(cim), controlEnabled=cim.control_enabled)


def shuntcompensator_to_pb(cim: ShuntCompensator) -> PBShuntCompensator:
    return PBShuntCompensator(rce=regulatingcondeq_to_pb(cim),
                              sections=cim.sections,
                              grounded=cim.grounded,
                              nomU=cim.nom_u,
                              phaseConnection=PBPhaseShuntConnectionKind.Value(cim.phase_connection))


def switch_to_pb(cim: Switch) -> PBSwitch:
    return PBSwitch(ce=conductingequipment_to_pb(cim),
                    normalOpen=cim.get_normal_state(),
                    open=cim.get_state())


def tapchanger_to_pb(cim: TapChanger) -> PBTapChanger:
    return PBTapChanger(psr=powersystemresource_to_pb(cim),
                        highStep=cim.high_step,
                        lowStep=cim.low_step,
                        step=cim.step,
                        neutralStep=cim.neutral_step,
                        neutralU=cim.neutral_u,
                        normalStep=cim.normal_step,
                        controlEnabled=cim.control_enabled)


def transformerend_to_pb(cim: TransformerEnd) -> PBTransformerEnd:
    return PBTransformerEnd(io=identifiedobject_to_pb(cim),
                            terminalMRID=mrid_or_empty(cim.terminal),
                            baseVoltageMRID=mrid_or_empty(cim.base_voltage),
                            ratioTapChangerMRID=mrid_or_empty(cim.ratio_tap_changer),
                            endNumber=cim.end_number,
                            grounded=cim.grounded,
                            rGround=cim.r_ground,
                            xGround=cim.x_ground)


def circuit_to_pb(cim: Circuit) -> PBCircuit:
    return PBCircuit(l=line_to_pb(cim),
                     loopMRID=mrid_or_empty(cim.loop.mrid),
                     endTerminalMRIDs=[str(io.mrid) for io in cim.end_terminals],
                     endSubstationMRIDs=[str(io.mrid) for io in cim.end_substations])


def loop_to_pb(cim: Loop) -> PBLoop:
    return PBLoop(io=identifiedobject_to_pb(cim),
                  circuitMRIDs=[str(io.mrid) for io in cim.circuits],
                  substationMRIDs=[str(io.mrid) for io in cim.substations],
                  normalEnergizingSubstationMRIDs=[str(io.mrid) for io in cim.energizing_substations])


# IEC61970 MEAS #
def control_to_pb(cim: Control) -> PBControl:
    return PBControl(ip=iopoint_to_pb(cim),
                     remoteControlMRID=mrid_or_empty(cim.remote_control),
                     powerSystemResourceMRID=cim.power_system_resource_mrid)


def iopoint_to_pb(cim: IoPoint) -> PBIoPoint:
    return PBIoPoint(io=identifiedobject_to_pb(cim))


def accumulator_to_pb(cim: Accumulator) -> PBAccumulator:
    return PBAccumulator(measurement=measurement_to_pb(cim))


def analog_to_pb(cim: Analog) -> PBAnalog:
    return PBAnalog(measurement=measurement_to_pb(cim), positiveFlowIn=cim.positive_flow_in)


def discrete_to_pb(cim: Discrete) -> PBDiscrete:
    return PBDiscrete(measurement=measurement_to_pb(cim))


def measurement_to_pb(cim: Measurement) -> PBMeasurement:
    return PBMeasurement(io=identifiedobject_to_pb(cim),
                         remoteSourceMRID=mrid_or_empty(cim.remote_source),
                         powerSystemResourceMRID=cim.power_system_resource_mrid,
                         terminalMRID=cim.terminal_mrid,
                         phases=PBPhaseCode.Value(cim.phases.short_name),
                         unitSymbol=PBUnitSymbol.Value(cim.unitSymbol.short_name))


# IEC61970 SCADA #
def remotecontrol_to_pb(cim: RemoteControl) -> PBRemoteControl:
    return PBRemoteControl(rp=remotepoint_to_pb(cim), controlMRID=mrid_or_empty(cim.control))


def remotepoint_to_pb(cim: RemotePoint) -> PBRemotePoint:
    return PBRemotePoint(io=identifiedobject_to_pb(cim))


def remotesource_to_pb(cim: RemoteSource) -> PBRemoteSource:
    return PBRemoteSource(rp=remotepoint_to_pb(cim), measurementMRID=mrid_or_empty(cim.measurement))


# MODEL #
def tracedphases_to_pb(cim: TracedPhases) -> PBTracedPhases:
    return PBTracedPhases(normalStatus=cim._normal_status, currentStatus=cim._current_status)


# Extension functions for each CIM type.
CableInfo.to_pb = lambda self: cableinfo_to_pb(self)
OverheadWireInfo.to_pb = lambda self: overheadwireinfo_to_pb(self)
WireInfo.to_pb = lambda self: wireinfo_to_pb(self)
PowerTransformerInfo.to_pb = lambda self: power_transformer_info_to_pb(self)
Asset.to_pb = lambda self: asset_to_pb(self)
AssetContainer.to_pb = lambda self: assetcontainer_to_pb(self)
AssetInfo.to_pb = lambda self: assetinfo_to_pb(self)
AssetOrganisationRole.to_pb = lambda self: assetorganisationrole_to_pb(self)
AssetOwner.to_pb = lambda self: assetowner_to_pb(self)
Pole.to_pb = lambda self: pole_to_pb(self)
Streetlight.to_pb = lambda self: streetlight_to_pb(self)
Structure.to_pb = lambda self: structure_to_pb(self)
PositionPoint.to_pb = lambda self: positionpoint_to_pb(self)
TownDetail.to_pb = lambda self: towndetail_to_pb(self)
StreetAddress.to_pb = lambda self: streetaddress_to_pb(self)
Location.to_pb = lambda self: location_to_pb(self)
EndDevice.to_pb = lambda self: enddevice_to_pb(self)
Meter.to_pb = lambda self: meter_to_pb(self)
UsagePoint.to_pb = lambda self: usagepoint_to_pb(self)
OperationalRestriction.to_pb = lambda self: operationalrestriction_to_pb(self)
AuxiliaryEquipment.to_pb = lambda self: auxiliaryequipment_to_pb(self)
FaultIndicator.to_pb = lambda self: faultindicator_to_pb(self)
AcDcTerminal.to_pb = lambda self: acdcterminal_to_pb(self)
BaseVoltage.to_pb = lambda self: basevoltage_to_pb(self)
ConductingEquipment.to_pb = lambda self: conductingequipment_to_pb(self)
ConnectivityNode.to_pb = lambda self: connectivitynode_to_pb(self)
ConnectivityNodeContainer.to_pb = lambda self: connectivitynodecontainer_to_pb(self)
Equipment.to_pb = lambda self: equipment_to_pb(self)
EquipmentContainer.to_pb = lambda self: equipmentcontainer_to_pb(self)
Feeder.to_pb = lambda self: feeder_to_pb(self)
GeographicalRegion.to_pb = lambda self: geographicalregion_to_pb(self)
PowerSystemResource.to_pb = lambda self: powersystemresource_to_pb(self)
Site.to_pb = lambda self: site_to_pb(self)
SubGeographicalRegion.to_pb = lambda self: subgeographicalregion_to_pb(self)
Substation.to_pb = lambda self: substation_to_pb(self)
Terminal.to_pb = lambda self: terminal_to_pb(self)
PerLengthLineParameter.to_pb = lambda self: perlengthlineparameter_to_pb(self)
PerLengthImpedance.to_pb = lambda self: perlengthimpedance_to_pb(self)
PowerElectronicsUnit.to_pb = powerelectronicsunit_to_pb
BatteryUnit.to_pb = batteryunit_to_pb
PhotoVoltaicUnit.to_pb = photovoltaicunit_to_pb
PowerElectronicsWindUnit.to_pb = powerelectronicswindunit_to_pb
AcLineSegment.to_pb = lambda self: aclinesegment_to_pb(self)
Breaker.to_pb = lambda self: breaker_to_pb(self)
Conductor.to_pb = lambda self: conductor_to_pb(self)
Connector.to_pb = lambda self: connector_to_pb(self)
Disconnector.to_pb = lambda self: disconnector_to_pb(self)
EnergyConnection.to_pb = lambda self: energyconnection_to_pb(self)
EnergyConsumer.to_pb = lambda self: energyconsumer_to_pb(self)
EnergyConsumerPhase.to_pb = lambda self: energyconsumerphase_to_pb(self)
EnergySource.to_pb = lambda self: energysource_to_pb(self)
EnergySourcePhase.to_pb = lambda self: energysourcephase_to_pb(self)
Fuse.to_pb = lambda self: fuse_to_pb(self)
Jumper.to_pb = lambda self: jumper_to_pb(self)
Junction.to_pb = lambda self: junction_to_pb(self)
BusbarSection.to_pb = busbarsection_to_pb
Line.to_pb = line_to_pb
LinearShuntCompensator.to_pb = lambda self: linearshuntcompensator_to_pb(self)
LoadBreakSwitch.to_pb = loadbreakswitch_to_pb
PerLengthSequenceImpedance.to_pb = lambda self: perlengthsequenceimpedance_to_pb(self)
PowerElectronicsConnection.to_pb = powerelectronicsconnection_to_pb
PowerElectronicsConnectionPhase.to_pb = powerelectronicsconnectionphase_to_pb
PowerTransformer.to_pb = lambda self: powertransformer_to_pb(self)
PowerTransformerEnd.to_pb = lambda self: powertransformerend_to_pb(self)
ProtectedSwitch.to_pb = lambda self: protectedswitch_to_pb(self)
RatioTapChanger.to_pb = lambda self: ratiotapchanger_to_pb(self)
Recloser.to_pb = lambda self: recloser_to_pb(self)
RegulatingCondEq.to_pb = lambda self: regulatingcondeq_to_pb(self)
ShuntCompensator.to_pb = lambda self: shuntcompensator_to_pb(self)
Switch.to_pb = lambda self: switch_to_pb(self)
TapChanger.to_pb = lambda self: tapchanger_to_pb(self)
TransformerEnd.to_pb = lambda self: transformerend_to_pb(self)
Circuit.to_pb = circuit_to_pb
Loop.to_pb = loop_to_pb
Control.to_pb = control_to_pb
IoPoint.to_pb = iopoint_to_pb
Accumulator.to_pb = accumulator_to_pb
Analog.to_pb = analog_to_pb
Discrete.to_pb = discrete_to_pb
Measurement.to_pb = measurement_to_pb
RemoteControl.to_pb = remotecontrol_to_pb
RemotePoint.to_pb = remotepoint_to_pb
RemoteSource.to_pb = remotesource_to_pb
TracedPhases.to_pb = tracedphases_to_pb
