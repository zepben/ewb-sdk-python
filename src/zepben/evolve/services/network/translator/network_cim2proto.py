#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.protobuf.cim.iec61968.assetinfo.CableInfo_pb2 import CableInfo as PBCableInfo
from zepben.protobuf.cim.iec61968.assetinfo.NoLoadTest_pb2 import NoLoadTest as PBNoLoadTest
from zepben.protobuf.cim.iec61968.assetinfo.OpenCircuitTest_pb2 import OpenCircuitTest as PBOpenCircuitTest
from zepben.protobuf.cim.iec61968.assetinfo.OverheadWireInfo_pb2 import OverheadWireInfo as PBOverheadWireInfo
from zepben.protobuf.cim.iec61968.assetinfo.PowerTransformerInfo_pb2 import PowerTransformerInfo as PBPowerTransformerInfo
from zepben.protobuf.cim.iec61968.assetinfo.ShortCircuitTest_pb2 import ShortCircuitTest as PBShortCircuitTest
from zepben.protobuf.cim.iec61968.assetinfo.TransformerEndInfo_pb2 import TransformerEndInfo as PBTransformerEndInfo
from zepben.protobuf.cim.iec61968.assetinfo.TransformerTankInfo_pb2 import TransformerTankInfo as PBTransformerTankInfo
from zepben.protobuf.cim.iec61968.assetinfo.TransformerTest_pb2 import TransformerTest as PBTransformerTest
from zepben.protobuf.cim.iec61968.assetinfo.WireInfo_pb2 import WireInfo as PBWireInfo
from zepben.protobuf.cim.iec61968.assetinfo.WireMaterialKind_pb2 import WireMaterialKind as PBWireMaterialKind
from zepben.protobuf.cim.iec61968.assets.AssetContainer_pb2 import AssetContainer as PBAssetContainer
from zepben.protobuf.cim.iec61968.assets.AssetInfo_pb2 import AssetInfo as PBAssetInfo
from zepben.protobuf.cim.iec61968.assets.AssetOrganisationRole_pb2 import AssetOrganisationRole as PBAssetOrganisationRole
from zepben.protobuf.cim.iec61968.assets.AssetOwner_pb2 import AssetOwner as PBAssetOwner
from zepben.protobuf.cim.iec61968.assets.Asset_pb2 import Asset as PBAsset
from zepben.protobuf.cim.iec61968.assets.Pole_pb2 import Pole as PBPole
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
from zepben.protobuf.cim.iec61970.base.scada.RemotePoint_pb2 import RemotePoint as PBRemotePoint
from zepben.protobuf.cim.iec61970.base.scada.RemoteSource_pb2 import RemoteSource as PBRemoteSource
from zepben.protobuf.cim.iec61970.base.wires.AcLineSegment_pb2 import AcLineSegment as PBAcLineSegment
from zepben.protobuf.cim.iec61970.base.wires.Breaker_pb2 import Breaker as PBBreaker
from zepben.protobuf.cim.iec61970.base.wires.BusbarSection_pb2 import BusbarSection as PBBusbarSection
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
from zepben.protobuf.cim.iec61970.base.wires.LoadBreakSwitch_pb2 import LoadBreakSwitch as PBLoadBreakSwitch
from zepben.protobuf.cim.iec61970.base.wires.PerLengthImpedance_pb2 import PerLengthImpedance as PBPerLengthImpedance
from zepben.protobuf.cim.iec61970.base.wires.PerLengthLineParameter_pb2 import PerLengthLineParameter as PBPerLengthLineParameter
from zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance_pb2 import PerLengthSequenceImpedance as PBPerLengthSequenceImpedance
from zepben.protobuf.cim.iec61970.base.wires.PhaseShuntConnectionKind_pb2 import PhaseShuntConnectionKind as PBPhaseShuntConnectionKind
from zepben.protobuf.cim.iec61970.base.wires.PowerElectronicsConnectionPhase_pb2 import PowerElectronicsConnectionPhase as PBPowerElectronicsConnectionPhase
from zepben.protobuf.cim.iec61970.base.wires.PowerElectronicsConnection_pb2 import PowerElectronicsConnection as PBPowerElectronicsConnection
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
from zepben.protobuf.cim.iec61970.base.wires.TransformerStarImpedance_pb2 import TransformerStarImpedance as PBTransformerStarImpedance
from zepben.protobuf.cim.iec61970.base.wires.VectorGroup_pb2 import VectorGroup as PBVectorGroup
from zepben.protobuf.cim.iec61970.base.wires.WindingConnection_pb2 import WindingConnection as PBWindingConnection
from zepben.protobuf.cim.iec61970.base.wires.generation.production.BatteryStateKind_pb2 import BatteryStateKind as PBBatteryStateKind
from zepben.protobuf.cim.iec61970.base.wires.generation.production.BatteryUnit_pb2 import BatteryUnit as PBBatteryUnit
from zepben.protobuf.cim.iec61970.base.wires.generation.production.PhotoVoltaicUnit_pb2 import PhotoVoltaicUnit as PBPhotoVoltaicUnit
from zepben.protobuf.cim.iec61970.base.wires.generation.production.PowerElectronicsUnit_pb2 import PowerElectronicsUnit as PBPowerElectronicsUnit
from zepben.protobuf.cim.iec61970.base.wires.generation.production.PowerElectronicsWindUnit_pb2 import PowerElectronicsWindUnit as PBPowerElectronicsWindUnit
from zepben.protobuf.cim.iec61970.infiec61970.feeder.Circuit_pb2 import Circuit as PBCircuit
from zepben.protobuf.cim.iec61970.infiec61970.feeder.Loop_pb2 import Loop as PBLoop
from zepben.protobuf.network.model.TracedPhases_pb2 import TracedPhases as PBTracedPhases

from zepben.evolve import TransformerTankInfo, TransformerEndInfo, TransformerStarImpedance, NoLoadTest, OpenCircuitTest, ShortCircuitTest, TransformerTest
from zepben.evolve.model.cim.iec61968.assetinfo.power_transformer_info import *
from zepben.evolve.model.cim.iec61968.assetinfo.wire_info import *
from zepben.evolve.model.cim.iec61968.assets.asset import *
from zepben.evolve.model.cim.iec61968.assets.asset_info import *
from zepben.evolve.model.cim.iec61968.assets.asset_organisation_role import *
from zepben.evolve.model.cim.iec61968.assets.pole import *
from zepben.evolve.model.cim.iec61968.assets.streetlight import *
from zepben.evolve.model.cim.iec61968.assets.structure import *
from zepben.evolve.model.cim.iec61968.common.location import *
from zepben.evolve.model.cim.iec61968.metering.metering import *
from zepben.evolve.model.cim.iec61968.operations.operational_restriction import *
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.auxiliary_equipment import *
from zepben.evolve.model.cim.iec61970.base.core.base_voltage import *
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import *
from zepben.evolve.model.cim.iec61970.base.core.connectivity_node import *
from zepben.evolve.model.cim.iec61970.base.core.connectivity_node_container import *
from zepben.evolve.model.cim.iec61970.base.core.equipment import *
from zepben.evolve.model.cim.iec61970.base.core.equipment_container import *
from zepben.evolve.model.cim.iec61970.base.core.power_system_resource import *
from zepben.evolve.model.cim.iec61970.base.core.regions import *
from zepben.evolve.model.cim.iec61970.base.core.substation import *
from zepben.evolve.model.cim.iec61970.base.core.terminal import *
from zepben.evolve.model.cim.iec61970.base.meas.control import *
from zepben.evolve.model.cim.iec61970.base.meas.iopoint import *
from zepben.evolve.model.cim.iec61970.base.meas.measurement import *
from zepben.evolve.model.cim.iec61970.base.scada.remote_control import *
from zepben.evolve.model.cim.iec61970.base.scada.remote_point import *
from zepben.evolve.model.cim.iec61970.base.scada.remote_source import *
from zepben.evolve.model.cim.iec61970.base.wires.aclinesegment import *
from zepben.evolve.model.cim.iec61970.base.wires.connectors import *
from zepben.evolve.model.cim.iec61970.base.wires.energy_connection import *
from zepben.evolve.model.cim.iec61970.base.wires.energy_consumer import *
from zepben.evolve.model.cim.iec61970.base.wires.energy_source import *
from zepben.evolve.model.cim.iec61970.base.wires.energy_source_phase import *
from zepben.evolve.model.cim.iec61970.base.wires.generation.production.power_electronics_unit import *
from zepben.evolve.model.cim.iec61970.base.wires.line import *
from zepben.evolve.model.cim.iec61970.base.wires.per_length import *
from zepben.evolve.model.cim.iec61970.base.wires.power_electronics_connection import *
from zepben.evolve.model.cim.iec61970.base.wires.power_transformer import *
from zepben.evolve.model.cim.iec61970.base.wires.shunt_compensator import *
from zepben.evolve.model.cim.iec61970.base.wires.switch import *
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.circuit import *
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.loop import *
from zepben.evolve.model.phases import *
from zepben.evolve.services.common.translator.base_cim2proto import identified_object_to_pb, organisation_role_to_pb, document_to_pb
from zepben.evolve.services.common.translator.util import mrid_or_empty, from_nullable_int, from_nullable_float, from_nullable_long, from_nullable_uint

__all__ = [
    "CimTranslationException", "cable_info_to_pb", "no_load_test_to_pb", "open_circuit_test_to_pb", "overhead_wire_info_to_pb", "power_transformer_info_to_pb",
    "short_circuit_test_to_pb", "transformer_end_info_to_pb", "transformer_tank_info_to_pb", "transformer_test_to_pb", "wire_info_to_pb", "asset_to_pb",
    "asset_container_to_pb", "asset_info_to_pb", "asset_organisation_role_to_pb", "asset_owner_to_pb", "pole_to_pb", "streetlight_to_pb", "structure_to_pb",
    "location_to_pb", "position_point_to_pb", "street_address_to_pb", "town_detail_to_pb", "end_device_to_pb", "meter_to_pb", "usage_point_to_pb",
    "operational_restriction_to_pb", "auxiliary_equipment_to_pb", "fault_indicator_to_pb", "ac_dc_terminal_to_pb", "base_voltage_to_pb",
    "conducting_equipment_to_pb", "connectivity_node_to_pb", "connectivity_node_container_to_pb", "equipment_to_pb", "equipment_container_to_pb",
    "feeder_to_pb", "geographical_region_to_pb", "power_system_resource_to_pb", "site_to_pb", "sub_geographical_region_to_pb", "substation_to_pb",
    "terminal_to_pb", "control_to_pb", "io_point_to_pb", "accumulator_to_pb", "analog_to_pb", "discrete_to_pb", "measurement_to_pb", "remote_control_to_pb",
    "remote_point_to_pb", "remote_source_to_pb", "battery_unit_to_pb", "photo_voltaic_unit_to_pb", "power_electronics_unit_to_pb",
    "power_electronics_wind_unit_to_pb", "ac_line_segment_to_pb", "breaker_to_pb", "conductor_to_pb", "connector_to_pb", "disconnector_to_pb",
    "energy_connection_to_pb", "energy_consumer_to_pb", "energy_consumer_phase_to_pb", "energy_source_to_pb", "energy_source_phase_to_pb", "fuse_to_pb",
    "jumper_to_pb", "junction_to_pb", "busbar_section_to_pb", "line_to_pb", "linear_shunt_compensator_to_pb", "load_break_switch_to_pb",
    "per_length_line_parameter_to_pb", "per_length_impedance_to_pb", "per_length_sequence_impedance_to_pb", "power_electronics_connection_to_pb",
    "power_electronics_connection_phase_to_pb", "power_transformer_to_pb", "power_transformer_end_to_pb", "protected_switch_to_pb", "ratio_tap_changer_to_pb",
    "recloser_to_pb", "regulating_cond_eq_to_pb", "shunt_compensator_to_pb", "switch_to_pb", "tap_changer_to_pb", "transformer_end_to_pb", "circuit_to_pb",
    "loop_to_pb", "transformer_star_impedance_to_pb", "traced_phases_to_pb",
]


def _get_or_none(getter, obj) -> object:
    return getter(obj) if obj else None


class CimTranslationException(Exception):
    pass


# IEC61968 ASSET INFO #
#######################

def cable_info_to_pb(cim: CableInfo) -> PBCableInfo:
    return PBCableInfo(wi=wire_info_to_pb(cim))


def no_load_test_to_pb(cim: NoLoadTest) -> PBNoLoadTest:
    return PBNoLoadTest(
        tt=transformer_test_to_pb(cim),
        energisedEndVoltage=from_nullable_int(cim.energised_end_voltage),
        excitingCurrent=from_nullable_float(cim.exciting_current),
        excitingCurrentZero=from_nullable_float(cim.exciting_current_zero),
        loss=from_nullable_int(cim.loss),
        lossZero=from_nullable_int(cim.loss_zero),
    )


def open_circuit_test_to_pb(cim: OpenCircuitTest) -> PBOpenCircuitTest:
    return PBOpenCircuitTest(
        tt=transformer_test_to_pb(cim),
        energisedEndStep=from_nullable_int(cim.energised_end_step),
        energisedEndVoltage=from_nullable_int(cim.energised_end_voltage),
        openEndStep=from_nullable_int(cim.open_end_step),
        openEndVoltage=from_nullable_int(cim.open_end_voltage),
        phaseShift=from_nullable_float(cim.phase_shift),
    )


def overhead_wire_info_to_pb(cim: OverheadWireInfo) -> PBOverheadWireInfo:
    return PBOverheadWireInfo(wi=wire_info_to_pb(cim))


def power_transformer_info_to_pb(cim: PowerTransformerInfo) -> PBPowerTransformerInfo:
    return PBPowerTransformerInfo(
        ai=asset_info_to_pb(cim),
        transformerTankInfoMRIDs=[tti.mrid for tti in cim.transformer_tank_infos]
    )


def short_circuit_test_to_pb(cim: ShortCircuitTest) -> PBShortCircuitTest:
    return PBShortCircuitTest(
        tt=transformer_test_to_pb(cim),
        current=from_nullable_float(cim.current),
        energisedEndStep=from_nullable_int(cim.energised_end_step),
        groundedEndStep=from_nullable_int(cim.grounded_end_step),
        leakageImpedance=from_nullable_float(cim.leakage_impedance),
        leakageImpedanceZero=from_nullable_float(cim.leakage_impedance_zero),
        loss=from_nullable_int(cim.loss),
        lossZero=from_nullable_int(cim.loss_zero),
        power=from_nullable_int(cim.power),
        voltage=from_nullable_float(cim.voltage),
        voltageOhmicPart=from_nullable_float(cim.voltage_ohmic_part),
    )


def transformer_end_info_to_pb(cim: TransformerEndInfo) -> PBTransformerEndInfo:
    return PBTransformerEndInfo(
        ai=asset_info_to_pb(cim),
        connectionKind=PBWindingConnection.Value(cim.connection_kind.short_name),
        emergencyS=from_nullable_int(cim.emergency_s),
        endNumber=from_nullable_int(cim.end_number),
        insulationU=from_nullable_int(cim.insulation_u),
        phaseAngleClock=from_nullable_int(cim.phase_angle_clock),
        r=from_nullable_float(cim.r),
        ratedS=from_nullable_int(cim.rated_s),
        ratedU=from_nullable_int(cim.rated_u),
        shortTermS=from_nullable_int(cim.short_term_s),
        transformerTankInfoMRID=mrid_or_empty(cim.transformer_tank_info),
        transformerStarImpedanceMRID=mrid_or_empty(cim.transformer_star_impedance),
        energisedEndNoLoadTestsMRID=mrid_or_empty(cim.energised_end_no_load_tests),
        energisedEndShortCircuitTestsMRID=mrid_or_empty(cim.energised_end_short_circuit_tests),
        groundedEndShortCircuitTestsMRID=mrid_or_empty(cim.grounded_end_short_circuit_tests),
        openEndOpenCircuitTestsMRID=mrid_or_empty(cim.open_end_open_circuit_tests),
        energisedEndOpenCircuitTestsMRID=mrid_or_empty(cim.energised_end_open_circuit_tests),
    )


def transformer_tank_info_to_pb(cim: TransformerTankInfo) -> PBTransformerTankInfo:
    return PBTransformerTankInfo(
        ai=asset_info_to_pb(cim),
        transformerEndInfoMRIDs=[str(tei.mrid) for tei in cim.transformer_end_infos]
    )


def transformer_test_to_pb(cim: TransformerTest) -> PBTransformerTest:
    return PBTransformerTest(
        io=identified_object_to_pb(cim),
        basePower=from_nullable_int(cim.base_power),
        temperature=from_nullable_float(cim.temperature),
    )


def wire_info_to_pb(cim: WireInfo) -> PBWireInfo:
    return PBWireInfo(
        ai=asset_info_to_pb(cim),
        ratedCurrent=from_nullable_int(cim.rated_current),
        material=PBWireMaterialKind.Value(cim.material.short_name)
    )


###################
# IEC61968 ASSETS #
###################

def asset_to_pb(cim: Asset) -> PBAsset:
    return PBAsset(
        io=identified_object_to_pb(cim),
        locationMRID=cim.location.mrid if cim.location else None,
        organisationRoleMRIDs=[str(io.mrid) for io in cim.organisation_roles]
    )


def asset_container_to_pb(cim: AssetContainer) -> PBAssetContainer:
    return PBAssetContainer(at=asset_to_pb(cim))


def asset_info_to_pb(cim: AssetInfo) -> PBAssetInfo:
    return PBAssetInfo(io=identified_object_to_pb(cim))


def asset_organisation_role_to_pb(cim: AssetOrganisationRole) -> PBAssetOrganisationRole:
    pb = PBAssetOrganisationRole()
    getattr(pb, "or").CopyFrom(organisation_role_to_pb(cim))
    return pb


def asset_owner_to_pb(cim: AssetOwner) -> PBAssetOwner:
    return PBAssetOwner(aor=asset_organisation_role_to_pb(cim))


def pole_to_pb(cim: Pole) -> PBPole:
    return PBPole(
        st=structure_to_pb(cim),
        streetlightMRIDs=[str(io.mrid) for io in cim.streetlights],
        classification=cim.classification
    )


def streetlight_to_pb(cim: Streetlight) -> PBStreetlight:
    return PBStreetlight(
        at=asset_to_pb(cim),
        poleMRID=mrid_or_empty(cim.pole),
        lightRating=from_nullable_uint(cim.light_rating),
        lampKind=PBStreetlightLampKind.Value(cim.lamp_kind.short_name)
    )


def structure_to_pb(cim: Structure) -> PBStructure:
    return PBStructure(ac=asset_container_to_pb(cim))


###################
# IEC61968 COMMON #
###################

def location_to_pb(cim: Location) -> PBLocation:
    return PBLocation(
        io=identified_object_to_pb(cim),
        mainAddress=_get_or_none(street_address_to_pb, cim.main_address),
        positionPoints=[position_point_to_pb(point) for point in cim.points]
    )


def position_point_to_pb(cim: PositionPoint) -> PBPositionPoint:
    return PBPositionPoint(xPosition=cim.x_position, yPosition=cim.y_position)


def street_address_to_pb(cim: StreetAddress) -> PBStreetAddress:
    return PBStreetAddress(postalCode=cim.postal_code, townDetail=_get_or_none(town_detail_to_pb, cim.town_detail))


def town_detail_to_pb(cim: TownDetail) -> PBTownDetail:
    return PBTownDetail(name=cim.name, stateOrProvince=cim.state_or_province)


#####################
# IEC61968 METERING #
#####################

def end_device_to_pb(cim: EndDevice) -> PBEndDevice:
    return PBEndDevice(
        ac=asset_container_to_pb(cim),
        usagePointMRIDs=[str(io.mrid) for io in cim.usage_points],
        customerMRID=cim.customer_mrid,
        serviceLocationMRID=mrid_or_empty(cim.service_location)
    )


def meter_to_pb(cim: Meter) -> PBMeter:
    return PBMeter(ed=end_device_to_pb(cim))


def usage_point_to_pb(cim: UsagePoint) -> PBUsagePoint:
    return PBUsagePoint(
        io=identified_object_to_pb(cim),
        usagePointLocationMRID=mrid_or_empty(cim.usage_point_location),
        equipmentMRIDs=[str(io.mrid) for io in cim.equipment],
        endDeviceMRIDs=[str(io.mrid) for io in cim.end_devices]
    )


#######################
# IEC61968 OPERATIONS #
#######################

def operational_restriction_to_pb(cim: OperationalRestriction) -> PBOperationalRestriction:
    return PBOperationalRestriction(doc=document_to_pb(cim))


#####################################
# IEC61970 BASE AUXILIARY EQUIPMENT #
#####################################

def auxiliary_equipment_to_pb(cim: AuxiliaryEquipment) -> PBAuxiliaryEquipment:
    return PBAuxiliaryEquipment(
        eq=equipment_to_pb(cim),
        terminalMRID=mrid_or_empty(cim.terminal)
    )


def fault_indicator_to_pb(cim: FaultIndicator) -> PBFaultIndicator:
    return PBFaultIndicator(ae=auxiliary_equipment_to_pb(cim))


######################
# IEC61970 BASE CORE #
######################

def ac_dc_terminal_to_pb(cim: AcDcTerminal) -> PBAcDcTerminal:
    return PBAcDcTerminal(io=identified_object_to_pb(cim))


def base_voltage_to_pb(cim: BaseVoltage) -> PBBaseVoltage:
    return PBBaseVoltage(
        io=identified_object_to_pb(cim),
        nominalVoltage=cim.nominal_voltage
    )


def conducting_equipment_to_pb(cim: ConductingEquipment, include_asset_info: bool = False) -> PBConductingEquipment:
    return PBConductingEquipment(
        eq=equipment_to_pb(cim, include_asset_info),
        baseVoltageMRID=mrid_or_empty(cim.base_voltage),
        terminalMRIDs=[str(io.mrid) for io in cim.terminals]
    )


def connectivity_node_to_pb(cim: ConnectivityNode) -> PBConnectivityNode:
    return PBConnectivityNode(io=identified_object_to_pb(cim))


def connectivity_node_container_to_pb(cim: ConnectivityNodeContainer) -> PBConnectivityNodeContainer:
    return PBConnectivityNodeContainer(psr=power_system_resource_to_pb(cim))


def equipment_to_pb(cim: Equipment, include_asset_info: bool = False) -> PBEquipment:
    return PBEquipment(
        psr=power_system_resource_to_pb(cim, include_asset_info),
        inService=cim.in_service,
        normallyInService=cim.normally_in_service,
        equipmentContainerMRIDs=[str(io.mrid) for io in cim.containers],
        usagePointMRIDs=[str(io.mrid) for io in cim.usage_points],
        operationalRestrictionMRIDs=[str(io.mrid) for io in cim.operational_restrictions],
        currentFeederMRIDs=[str(io.mrid) for io in cim.current_feeders]
    )


def equipment_container_to_pb(cim: EquipmentContainer) -> PBEquipmentContainer:
    return PBEquipmentContainer(cnc=connectivity_node_container_to_pb(cim))


def feeder_to_pb(cim: Feeder) -> PBFeeder:
    return PBFeeder(
        ec=equipment_container_to_pb(cim),
        normalHeadTerminalMRID=mrid_or_empty(cim.normal_head_terminal),
        normalEnergizingSubstationMRID=mrid_or_empty(cim.normal_energizing_substation)
    )


def geographical_region_to_pb(cim: GeographicalRegion) -> PBGeographicalRegion:
    return PBGeographicalRegion(
        io=identified_object_to_pb(cim),
        subGeographicalRegionMRIDs=[str(io.mrid) for io in cim.sub_geographical_regions]
    )


def power_system_resource_to_pb(cim: PowerSystemResource, include_asset_info: bool = False) -> PBPowerSystemResource:
    return PBPowerSystemResource(
        io=identified_object_to_pb(cim),
        assetInfoMRID=mrid_or_empty(cim.asset_info) if include_asset_info else None,
        locationMRID=mrid_or_empty(cim.location)
    )


def site_to_pb(cim: Site) -> PBSite:
    return PBSite(ec=equipment_container_to_pb(cim))


def sub_geographical_region_to_pb(cim: SubGeographicalRegion) -> PBSubGeographicalRegion:
    return PBSubGeographicalRegion(
        io=identified_object_to_pb(cim),
        geographicalRegionMRID=mrid_or_empty(cim.geographical_region),
        substationMRIDs=[str(io.mrid) for io in cim.substations]
    )


def substation_to_pb(cim: Substation) -> PBSubstation:
    return PBSubstation(
        ec=equipment_container_to_pb(cim),
        subGeographicalRegionMRID=mrid_or_empty(cim.sub_geographical_region),
        normalEnergizedFeederMRIDs=[str(io.mrid) for io in cim.feeders],
        loopMRIDs=[str(io.mrid) for io in cim.loops],
        normalEnergizedLoopMRIDs=[str(io.mrid) for io in cim.energized_loops],
        circuitMRIDs=[str(io.mrid) for io in cim.circuits]
    )


def terminal_to_pb(cim: Terminal) -> PBTerminal:
    return PBTerminal(
        ad=ac_dc_terminal_to_pb(cim),
        conductingEquipmentMRID=mrid_or_empty(cim.conducting_equipment),
        connectivityNodeMRID=mrid_or_empty(cim.connectivity_node),
        tracedPhases=traced_phases_to_pb(cim.traced_phases),
        phases=PBPhaseCode.Value(cim.phases.short_name),
        sequenceNumber=cim.sequence_number
    )


######################
# IEC61970 BASE MEAS #
######################

def control_to_pb(cim: Control) -> PBControl:
    return PBControl(
        ip=io_point_to_pb(cim),
        remoteControlMRID=mrid_or_empty(cim.remote_control),
        powerSystemResourceMRID=cim.power_system_resource_mrid
    )


def io_point_to_pb(cim: IoPoint) -> PBIoPoint:
    return PBIoPoint(io=identified_object_to_pb(cim))


def accumulator_to_pb(cim: Accumulator) -> PBAccumulator:
    return PBAccumulator(measurement=measurement_to_pb(cim))


def analog_to_pb(cim: Analog) -> PBAnalog:
    return PBAnalog(
        measurement=measurement_to_pb(cim),
        positiveFlowIn=cim.positive_flow_in
    )


def discrete_to_pb(cim: Discrete) -> PBDiscrete:
    return PBDiscrete(measurement=measurement_to_pb(cim))


def measurement_to_pb(cim: Measurement) -> PBMeasurement:
    return PBMeasurement(
        io=identified_object_to_pb(cim),
        remoteSourceMRID=mrid_or_empty(cim.remote_source),
        powerSystemResourceMRID=cim.power_system_resource_mrid,
        terminalMRID=cim.terminal_mrid,
        phases=PBPhaseCode.Value(cim.phases.short_name),
        unitSymbol=PBUnitSymbol.Value(cim.unit_symbol.short_name)
    )


#######################
# IEC61970 BASE SCADA #
#######################

def remote_control_to_pb(cim: RemoteControl) -> PBRemoteControl:
    return PBRemoteControl(
        rp=remote_point_to_pb(cim),
        controlMRID=mrid_or_empty(cim.control)
    )


def remote_point_to_pb(cim: RemotePoint) -> PBRemotePoint:
    return PBRemotePoint(io=identified_object_to_pb(cim))


def remote_source_to_pb(cim: RemoteSource) -> PBRemoteSource:
    return PBRemoteSource(
        rp=remote_point_to_pb(cim),
        measurementMRID=mrid_or_empty(cim.measurement)
    )


#############################################
# IEC61970 BASE WIRES GENERATION PRODUCTION #
#############################################

def battery_unit_to_pb(cim: BatteryUnit) -> PBBatteryUnit:
    return PBBatteryUnit(
        peu=power_electronics_unit_to_pb(cim),
        ratedE=from_nullable_long(cim.rated_e),
        storedE=from_nullable_long(cim.stored_e),
        batteryState=PBBatteryStateKind.Value(cim.battery_state.short_name)
    )


def photo_voltaic_unit_to_pb(cim: PhotoVoltaicUnit) -> PBPhotoVoltaicUnit:
    return PBPhotoVoltaicUnit(peu=power_electronics_unit_to_pb(cim))


def power_electronics_unit_to_pb(cim: PowerElectronicsUnit) -> PBPowerElectronicsUnit:
    return PBPowerElectronicsUnit(
        eq=equipment_to_pb(cim),
        maxP=from_nullable_int(cim.max_p),
        minP=from_nullable_int(cim.min_p),
        powerElectronicsConnectionMRID=mrid_or_empty(cim.power_electronics_connection)
    )


def power_electronics_wind_unit_to_pb(cim: PowerElectronicsWindUnit) -> PBPowerElectronicsWindUnit:
    return PBPowerElectronicsWindUnit(peu=power_electronics_unit_to_pb(cim))


#######################
# IEC61970 BASE WIRES #
#######################

def ac_line_segment_to_pb(cim: AcLineSegment) -> PBAcLineSegment:
    return PBAcLineSegment(
        cd=conductor_to_pb(cim),
        perLengthSequenceImpedanceMRID=mrid_or_empty(cim.per_length_sequence_impedance)
    )


def breaker_to_pb(cim: Breaker) -> PBBreaker:
    return PBBreaker(sw=protected_switch_to_pb(cim))


def conductor_to_pb(cim: Conductor) -> PBConductor:
    return PBConductor(
        ce=conducting_equipment_to_pb(cim, True),
        length=from_nullable_float(cim.length)
    )


def connector_to_pb(cim: Connector) -> PBConnector:
    return PBConnector(ce=conducting_equipment_to_pb(cim))


def disconnector_to_pb(cim: Disconnector) -> PBDisconnector:
    return PBDisconnector(sw=switch_to_pb(cim))


def energy_connection_to_pb(cim: EnergyConnection) -> PBEnergyConnection:
    return PBEnergyConnection(ce=conducting_equipment_to_pb(cim))


def energy_consumer_to_pb(cim: EnergyConsumer) -> PBEnergyConsumer:
    return PBEnergyConsumer(
        ec=energy_connection_to_pb(cim),
        energyConsumerPhasesMRIDs=[str(io.mrid) for io in cim.phases],
        customerCount=from_nullable_int(cim.customer_count),
        grounded=cim.grounded,
        phaseConnection=PBPhaseShuntConnectionKind.Enum.Value(cim.phase_connection.short_name),
        p=from_nullable_float(cim.p),
        pFixed=from_nullable_float(cim.p_fixed),
        q=from_nullable_float(cim.q),
        qFixed=from_nullable_float(cim.q_fixed)
    )


def energy_consumer_phase_to_pb(cim: EnergyConsumerPhase) -> PBEnergyConsumerPhase:
    return PBEnergyConsumerPhase(
        psr=power_system_resource_to_pb(cim),
        energyConsumerMRID=mrid_or_empty(cim.energy_consumer),
        phase=PBSinglePhaseKind.Value(cim.phase.short_name),
        p=from_nullable_float(cim.p),
        pFixed=from_nullable_float(cim.p_fixed),
        q=from_nullable_float(cim.q),
        qFixed=from_nullable_float(cim.q_fixed)
    )


def energy_source_to_pb(cim: EnergySource) -> PBEnergySource:
    return PBEnergySource(
        ec=energy_connection_to_pb(cim),
        energySourcePhasesMRIDs=[str(io.mrid) for io in cim.phases],
        activePower=from_nullable_float(cim.active_power),
        reactivePower=from_nullable_float(cim.reactive_power),
        voltageAngle=from_nullable_float(cim.voltage_angle),
        voltageMagnitude=from_nullable_float(cim.voltage_magnitude),
        r=from_nullable_float(cim.r),
        x=from_nullable_float(cim.x),
        pMax=from_nullable_float(cim.p_max),
        pMin=from_nullable_float(cim.p_min),
        r0=from_nullable_float(cim.r0),
        rn=from_nullable_float(cim.rn),
        x0=from_nullable_float(cim.x0),
        xn=from_nullable_float(cim.xn)
    )


def energy_source_phase_to_pb(cim: EnergySourcePhase) -> PBEnergySourcePhase:
    return PBEnergySourcePhase(
        psr=power_system_resource_to_pb(cim),
        energySourceMRID=mrid_or_empty(cim.energy_source),
        phase=PBSinglePhaseKind.Value(cim.phase.short_name)
    )


def fuse_to_pb(cim: Fuse) -> PBFuse:
    return PBFuse(sw=switch_to_pb(cim))


def jumper_to_pb(cim: Jumper) -> PBJumper:
    return PBJumper(sw=switch_to_pb(cim))


def junction_to_pb(cim: Junction) -> PBJunction:
    return PBJunction(cn=connector_to_pb(cim))


def busbar_section_to_pb(cim: BusbarSection) -> PBBusbarSection:
    return PBBusbarSection(cn=connector_to_pb(cim))


def line_to_pb(cim: Line) -> PBLine:
    return PBLine(ec=equipment_container_to_pb(cim))


def linear_shunt_compensator_to_pb(cim: LinearShuntCompensator) -> PBLinearShuntCompensator:
    return PBLinearShuntCompensator(
        sc=shunt_compensator_to_pb(cim),
        b0PerSection=from_nullable_float(cim.b0_per_section),
        bPerSection=from_nullable_float(cim.b_per_section),
        g0PerSection=from_nullable_float(cim.g0_per_section),
        gPerSection=from_nullable_float(cim.g_per_section)
    )


def load_break_switch_to_pb(cim: LoadBreakSwitch) -> PBLoadBreakSwitch:
    return PBLoadBreakSwitch(ps=protected_switch_to_pb(cim))


def per_length_line_parameter_to_pb(cim: PerLengthLineParameter) -> PBPerLengthLineParameter:
    return PBPerLengthLineParameter(io=identified_object_to_pb(cim))


def per_length_impedance_to_pb(cim: PerLengthImpedance) -> PBPerLengthImpedance:
    return PBPerLengthImpedance(lp=per_length_line_parameter_to_pb(cim))


def per_length_sequence_impedance_to_pb(cim: PerLengthSequenceImpedance) -> PBPerLengthSequenceImpedance:
    return PBPerLengthSequenceImpedance(
        pli=per_length_impedance_to_pb(cim),
        r=from_nullable_float(cim.r),
        x=from_nullable_float(cim.x),
        r0=from_nullable_float(cim.r0),
        x0=from_nullable_float(cim.x0),
        bch=from_nullable_float(cim.bch),
        gch=from_nullable_float(cim.gch),
        b0ch=from_nullable_float(cim.b0ch),
        g0ch=from_nullable_float(cim.g0ch)
    )


def power_electronics_connection_to_pb(cim: PowerElectronicsConnection) -> PBPowerElectronicsConnection:
    return PBPowerElectronicsConnection(
        rce=regulating_cond_eq_to_pb(cim),
        powerElectronicsUnitMRIDs=[str(io.mrid) for io in cim.units],
        powerElectronicsConnectionPhaseMRIDs=[str(io.mrid) for io in cim.phases],
        maxIFault=from_nullable_int(cim.max_i_fault),
        maxQ=from_nullable_float(cim.max_q),
        minQ=from_nullable_float(cim.min_q),
        p=from_nullable_float(cim.p),
        q=from_nullable_float(cim.q),
        ratedS=from_nullable_int(cim.rated_s),
        ratedU=from_nullable_int(cim.rated_u)
    )


def power_electronics_connection_phase_to_pb(cim: PowerElectronicsConnectionPhase) -> PBPowerElectronicsConnectionPhase:
    return PBPowerElectronicsConnectionPhase(
        psr=power_system_resource_to_pb(cim),
        powerElectronicsConnectionMRID=mrid_or_empty(cim.power_electronics_connection),
        p=from_nullable_float(cim.p),
        q=from_nullable_float(cim.q),
        phase=PBSinglePhaseKind.Value(cim.phase.short_name)
    )


def power_transformer_to_pb(cim: PowerTransformer) -> PBPowerTransformer:
    return PBPowerTransformer(
        ce=conducting_equipment_to_pb(cim, True),
        powerTransformerEndMRIDs=[str(io.mrid) for io in cim.ends],
        vectorGroup=PBVectorGroup.Value(cim.vector_group.short_name),
        transformerUtilisation=from_nullable_float(cim.transformer_utilisation)
    )


def power_transformer_end_to_pb(cim: PowerTransformerEnd) -> PBPowerTransformerEnd:
    return PBPowerTransformerEnd(
        te=transformer_end_to_pb(cim),
        powerTransformerMRID=mrid_or_empty(cim.power_transformer),
        ratedS=from_nullable_int(cim.rated_s),
        ratedU=from_nullable_int(cim.rated_u),
        r=from_nullable_float(cim.r),
        r0=from_nullable_float(cim.r0),
        x=from_nullable_float(cim.x),
        x0=from_nullable_float(cim.x0),
        connectionKind=PBWindingConnection.Value(cim.connection_kind.short_name),
        b=from_nullable_float(cim.b),
        b0=from_nullable_float(cim.b0),
        g=from_nullable_float(cim.g),
        g0=from_nullable_float(cim.g0),
        phaseAngleClock=from_nullable_int(cim.phase_angle_clock)
    )


def protected_switch_to_pb(cim: ProtectedSwitch) -> PBProtectedSwitch:
    return PBProtectedSwitch(sw=switch_to_pb(cim))


def ratio_tap_changer_to_pb(cim: RatioTapChanger) -> PBRatioTapChanger:
    return PBRatioTapChanger(
        tc=tap_changer_to_pb(cim),
        transformerEndMRID=mrid_or_empty(cim.transformer_end),
        stepVoltageIncrement=from_nullable_float(cim.step_voltage_increment)
    )


def recloser_to_pb(cim: Recloser) -> PBRecloser:
    return PBRecloser(sw=protected_switch_to_pb(cim))


def regulating_cond_eq_to_pb(cim: RegulatingCondEq) -> PBRegulatingCondEq:
    return PBRegulatingCondEq(
        ec=energy_connection_to_pb(cim),
        controlEnabled=cim.control_enabled
    )


def shunt_compensator_to_pb(cim: ShuntCompensator) -> PBShuntCompensator:
    return PBShuntCompensator(
        rce=regulating_cond_eq_to_pb(cim),
        sections=from_nullable_float(cim.sections),
        grounded=cim.grounded,
        nomU=from_nullable_int(cim.nom_u),
        phaseConnection=PBPhaseShuntConnectionKind.Enum.Value(cim.phase_connection.short_name)
    )


def switch_to_pb(cim: Switch) -> PBSwitch:
    return PBSwitch(
        ce=conducting_equipment_to_pb(cim),
        normalOpen=cim.get_normal_state(),
        open=cim.get_state()
    )


def tap_changer_to_pb(cim: TapChanger) -> PBTapChanger:
    return PBTapChanger(
        psr=power_system_resource_to_pb(cim),
        highStep=from_nullable_int(cim.high_step),
        lowStep=from_nullable_int(cim.low_step),
        step=from_nullable_float(cim.step),
        neutralStep=from_nullable_int(cim.neutral_step),
        neutralU=from_nullable_int(cim.neutral_u),
        normalStep=from_nullable_int(cim.normal_step),
        controlEnabled=cim.control_enabled
    )


def transformer_end_to_pb(cim: TransformerEnd) -> PBTransformerEnd:
    return PBTransformerEnd(
        io=identified_object_to_pb(cim),
        terminalMRID=mrid_or_empty(cim.terminal),
        baseVoltageMRID=mrid_or_empty(cim.base_voltage),
        ratioTapChangerMRID=mrid_or_empty(cim.ratio_tap_changer),
        starImpedanceMRID=mrid_or_empty(cim.star_impedance),
        endNumber=cim.end_number,
        grounded=cim.grounded,
        rGround=from_nullable_float(cim.r_ground),
        xGround=from_nullable_float(cim.x_ground)
    )


def circuit_to_pb(cim: Circuit) -> PBCircuit:
    return PBCircuit(
        l=line_to_pb(cim),
        loopMRID=mrid_or_empty(cim.loop),
        endTerminalMRIDs=[str(io.mrid) for io in cim.end_terminals],
        endSubstationMRIDs=[str(io.mrid) for io in cim.end_substations]
    )


def loop_to_pb(cim: Loop) -> PBLoop:
    return PBLoop(
        io=identified_object_to_pb(cim),
        circuitMRIDs=[str(io.mrid) for io in cim.circuits],
        substationMRIDs=[str(io.mrid) for io in cim.substations],
        normalEnergizingSubstationMRIDs=[str(io.mrid) for io in cim.energizing_substations]
    )


def transformer_star_impedance_to_pb(cim: TransformerStarImpedance) -> PBTransformerStarImpedance:
    return PBTransformerStarImpedance(
        io=identified_object_to_pb(cim),
        r=cim.r if cim.r else 0.0,
        r0=cim.r0 if cim.r0 else 0.0,
        x=cim.x if cim.x else 0.0,
        x0=cim.x0 if cim.x0 else 0.0,
        transformerEndInfoMRID=mrid_or_empty(cim.transformer_end_info)
    )


#########
# MODEL #
#########

def traced_phases_to_pb(cim: TracedPhases) -> PBTracedPhases:
    # noinspection PyProtectedMember
    return PBTracedPhases(normalStatus=cim._normal_status, currentStatus=cim._current_status)


# Extension functions for each CIM type.
CableInfo.to_pb = lambda self: cable_info_to_pb(self)
NoLoadTest.to_pb = no_load_test_to_pb
OpenCircuitTest.to_pb = open_circuit_test_to_pb
OverheadWireInfo.to_pb = lambda self: overhead_wire_info_to_pb(self)
PowerTransformerInfo.to_pb = lambda self: power_transformer_info_to_pb(self)
ShortCircuitTest.to_pb = short_circuit_test_to_pb
TransformerEndInfo.to_pb = transformer_end_info_to_pb
TransformerTankInfo.to_pb = transformer_tank_info_to_pb
TransformerTest.to_pb = transformer_test_to_pb
WireInfo.to_pb = lambda self: wire_info_to_pb(self)
Asset.to_pb = lambda self: asset_to_pb(self)
AssetContainer.to_pb = lambda self: asset_container_to_pb(self)
AssetInfo.to_pb = lambda self: asset_info_to_pb(self)
AssetOrganisationRole.to_pb = lambda self: asset_organisation_role_to_pb(self)
AssetOwner.to_pb = lambda self: asset_owner_to_pb(self)
Pole.to_pb = lambda self: pole_to_pb(self)
Streetlight.to_pb = lambda self: streetlight_to_pb(self)
Structure.to_pb = lambda self: structure_to_pb(self)
PositionPoint.to_pb = lambda self: position_point_to_pb(self)
TownDetail.to_pb = lambda self: town_detail_to_pb(self)
StreetAddress.to_pb = lambda self: street_address_to_pb(self)
Location.to_pb = lambda self: location_to_pb(self)
EndDevice.to_pb = lambda self: end_device_to_pb(self)
Meter.to_pb = lambda self: meter_to_pb(self)
UsagePoint.to_pb = lambda self: usage_point_to_pb(self)
OperationalRestriction.to_pb = lambda self: operational_restriction_to_pb(self)
AuxiliaryEquipment.to_pb = lambda self: auxiliary_equipment_to_pb(self)
FaultIndicator.to_pb = lambda self: fault_indicator_to_pb(self)
AcDcTerminal.to_pb = lambda self: ac_dc_terminal_to_pb(self)
BaseVoltage.to_pb = lambda self: base_voltage_to_pb(self)
ConductingEquipment.to_pb = lambda self: conducting_equipment_to_pb(self)
ConnectivityNode.to_pb = lambda self: connectivity_node_to_pb(self)
ConnectivityNodeContainer.to_pb = lambda self: connectivity_node_container_to_pb(self)
Equipment.to_pb = lambda self: equipment_to_pb(self)
EquipmentContainer.to_pb = lambda self: equipment_container_to_pb(self)
Feeder.to_pb = lambda self: feeder_to_pb(self)
GeographicalRegion.to_pb = lambda self: geographical_region_to_pb(self)
PowerSystemResource.to_pb = lambda self: power_system_resource_to_pb(self)
Site.to_pb = lambda self: site_to_pb(self)
SubGeographicalRegion.to_pb = lambda self: sub_geographical_region_to_pb(self)
Substation.to_pb = lambda self: substation_to_pb(self)
Terminal.to_pb = lambda self: terminal_to_pb(self)
PerLengthLineParameter.to_pb = lambda self: per_length_line_parameter_to_pb(self)
PerLengthImpedance.to_pb = lambda self: per_length_impedance_to_pb(self)
PowerElectronicsUnit.to_pb = power_electronics_unit_to_pb
BatteryUnit.to_pb = battery_unit_to_pb
PhotoVoltaicUnit.to_pb = photo_voltaic_unit_to_pb
PowerElectronicsWindUnit.to_pb = power_electronics_wind_unit_to_pb
AcLineSegment.to_pb = lambda self: ac_line_segment_to_pb(self)
Breaker.to_pb = lambda self: breaker_to_pb(self)
Conductor.to_pb = lambda self: conductor_to_pb(self)
Connector.to_pb = lambda self: connector_to_pb(self)
Disconnector.to_pb = lambda self: disconnector_to_pb(self)
EnergyConnection.to_pb = lambda self: energy_connection_to_pb(self)
EnergyConsumer.to_pb = lambda self: energy_consumer_to_pb(self)
EnergyConsumerPhase.to_pb = lambda self: energy_consumer_phase_to_pb(self)
EnergySource.to_pb = lambda self: energy_source_to_pb(self)
EnergySourcePhase.to_pb = lambda self: energy_source_phase_to_pb(self)
Fuse.to_pb = lambda self: fuse_to_pb(self)
Jumper.to_pb = lambda self: jumper_to_pb(self)
Junction.to_pb = lambda self: junction_to_pb(self)
BusbarSection.to_pb = busbar_section_to_pb
Line.to_pb = line_to_pb
LinearShuntCompensator.to_pb = lambda self: linear_shunt_compensator_to_pb(self)
LoadBreakSwitch.to_pb = load_break_switch_to_pb
PerLengthSequenceImpedance.to_pb = lambda self: per_length_sequence_impedance_to_pb(self)
PowerElectronicsConnection.to_pb = power_electronics_connection_to_pb
PowerElectronicsConnectionPhase.to_pb = power_electronics_connection_phase_to_pb
PowerTransformer.to_pb = lambda self: power_transformer_to_pb(self)
PowerTransformerEnd.to_pb = lambda self: power_transformer_end_to_pb(self)
TransformerStarImpedance.to_pb = transformer_star_impedance_to_pb
ProtectedSwitch.to_pb = lambda self: protected_switch_to_pb(self)
RatioTapChanger.to_pb = lambda self: ratio_tap_changer_to_pb(self)
Recloser.to_pb = lambda self: recloser_to_pb(self)
RegulatingCondEq.to_pb = lambda self: regulating_cond_eq_to_pb(self)
ShuntCompensator.to_pb = lambda self: shunt_compensator_to_pb(self)
Switch.to_pb = lambda self: switch_to_pb(self)
TapChanger.to_pb = lambda self: tap_changer_to_pb(self)
TransformerEnd.to_pb = lambda self: transformer_end_to_pb(self)
Circuit.to_pb = circuit_to_pb
Loop.to_pb = loop_to_pb
Control.to_pb = control_to_pb
IoPoint.to_pb = io_point_to_pb
Accumulator.to_pb = accumulator_to_pb
Analog.to_pb = analog_to_pb
Discrete.to_pb = discrete_to_pb
Measurement.to_pb = measurement_to_pb
RemoteControl.to_pb = remote_control_to_pb
RemotePoint.to_pb = remote_point_to_pb
RemoteSource.to_pb = remote_source_to_pb
TracedPhases.to_pb = traced_phases_to_pb
