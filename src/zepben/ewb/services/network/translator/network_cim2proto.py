#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = [
    "CimTranslationException", "cable_info_to_pb", "no_load_test_to_pb", "open_circuit_test_to_pb", "overhead_wire_info_to_pb", "power_transformer_info_to_pb",
    "short_circuit_test_to_pb", "shunt_compensator_info_to_pb", "switch_info_to_pb", "transformer_end_info_to_pb", "transformer_tank_info_to_pb",
    "transformer_test_to_pb", "wire_info_to_pb", "asset_to_pb", "asset_container_to_pb", "asset_info_to_pb", "asset_organisation_role_to_pb",
    "asset_owner_to_pb", "pole_to_pb", "streetlight_to_pb", "structure_to_pb", "location_to_pb", "position_point_to_pb", "street_address_to_pb",
    "street_detail_to_pb", "town_detail_to_pb", "relay_info_to_pb", "current_transformer_info_to_pb", "potential_transformer_info_to_pb",
    "ratio_to_pb", "end_device_to_pb", "meter_to_pb", "usage_point_to_pb", "operational_restriction_to_pb", "auxiliary_equipment_to_pb",
    "current_transformer_to_pb", "fault_indicator_to_pb", "potential_transformer_to_pb", "sensor_to_pb", "ac_dc_terminal_to_pb", "base_voltage_to_pb",
    "conducting_equipment_to_pb", "connectivity_node_to_pb", "connectivity_node_container_to_pb", "equipment_to_pb", "equipment_container_to_pb",
    "feeder_to_pb", "geographical_region_to_pb", "power_system_resource_to_pb", "site_to_pb", "sub_geographical_region_to_pb", "substation_to_pb",
    "terminal_to_pb", "equivalent_branch_to_pb", "equivalent_equipment_to_pb", "accumulator_to_pb", "analog_to_pb", "control_to_pb", "discrete_to_pb",
    "io_point_to_pb", "measurement_to_pb", "current_relay_to_pb", "distance_relay_to_pb", "voltage_relay_to_pb", "remote_control_to_pb", "remote_point_to_pb",
    "remote_source_to_pb", "battery_unit_to_pb", "photo_voltaic_unit_to_pb", "power_electronics_unit_to_pb", "power_electronics_wind_unit_to_pb",
    "ac_line_segment_to_pb", "breaker_to_pb", "conductor_to_pb", "connector_to_pb", "disconnector_to_pb", "energy_connection_to_pb", "energy_consumer_to_pb",
    "energy_consumer_phase_to_pb", "energy_source_to_pb", "energy_source_phase_to_pb", "fuse_to_pb", "jumper_to_pb", "junction_to_pb", "busbar_section_to_pb",
    "line_to_pb", "linear_shunt_compensator_to_pb", "load_break_switch_to_pb", "per_length_line_parameter_to_pb", "per_length_impedance_to_pb",
    "per_length_sequence_impedance_to_pb", "power_electronics_connection_to_pb", "power_electronics_connection_phase_to_pb", "power_transformer_to_pb",
    "power_transformer_end_to_pb", "protected_switch_to_pb", "ratio_tap_changer_to_pb", "recloser_to_pb", "regulating_cond_eq_to_pb", "shunt_compensator_to_pb",
    "switch_to_pb", "tap_changer_to_pb", "transformer_end_to_pb", "transformer_star_impedance_to_pb", "circuit_to_pb", "loop_to_pb", "lv_feeder_to_pb",
    "ev_charging_unit", "transformer_end_rated_s_to_pb", "tap_changer_control_to_pb", "regulating_control_to_pb", "protection_relay_function_to_pb",
    "protection_relay_scheme_to_pb", "protection_relay_system_to_pb", "relay_setting_to_pb", "ground_to_pb", "ground_disconnector_to_pb",
    "series_compensator_to_pb", "pan_demand_response_function_to_pb", "battery_control_to_pb", "asset_function_to_pb", "end_device_function_to_pb",
    "static_var_compensator_to_pb", "per_length_phase_impedance_to_pb", "phase_impedance_data_to_pb",
]

from typing import Any, Optional

# noinspection PyPackageRequirements,PyUnresolvedReferences
from google.protobuf.timestamp_pb2 import Timestamp as PBTimestamp
from zepben.protobuf.cim.extensions.iec61968.assetinfo.RelayInfo_pb2 import RelayInfo as PBRelayInfo
from zepben.protobuf.cim.extensions.iec61968.metering.PanDemandResponseFunction_pb2 import PanDemandResponseFunction as PBPanDemandResponseFunction
from zepben.protobuf.cim.extensions.iec61970.base.core.Site_pb2 import Site as PBSite
from zepben.protobuf.cim.extensions.iec61970.base.feeder.Loop_pb2 import Loop as PBLoop
from zepben.protobuf.cim.extensions.iec61970.base.feeder.LvFeeder_pb2 import LvFeeder as PBLvFeeder
from zepben.protobuf.cim.extensions.iec61970.base.generation.production.EvChargingUnit_pb2 import EvChargingUnit as PBEvChargingUnit
from zepben.protobuf.cim.extensions.iec61970.base.protection.DistanceRelay_pb2 import DistanceRelay as PBDistanceRelay
from zepben.protobuf.cim.extensions.iec61970.base.protection.ProtectionRelayFunction_pb2 import ProtectionRelayFunction as PBProtectionRelayFunction
from zepben.protobuf.cim.extensions.iec61970.base.protection.ProtectionRelayScheme_pb2 import ProtectionRelayScheme as PBProtectionRelayScheme
from zepben.protobuf.cim.extensions.iec61970.base.protection.ProtectionRelaySystem_pb2 import ProtectionRelaySystem as PBProtectionRelaySystem
from zepben.protobuf.cim.extensions.iec61970.base.protection.RelaySetting_pb2 import RelaySetting as PBRelaySetting
from zepben.protobuf.cim.extensions.iec61970.base.protection.VoltageRelay_pb2 import VoltageRelay as PBVoltageRelay
from zepben.protobuf.cim.extensions.iec61970.base.wires.BatteryControl_pb2 import BatteryControl as PBBatteryControl
from zepben.protobuf.cim.extensions.iec61970.base.wires.TransformerEndRatedS_pb2 import TransformerEndRatedS as PBTransformerEndRatedS
from zepben.protobuf.cim.iec61968.assetinfo.CableInfo_pb2 import CableInfo as PBCableInfo
from zepben.protobuf.cim.iec61968.assetinfo.NoLoadTest_pb2 import NoLoadTest as PBNoLoadTest
from zepben.protobuf.cim.iec61968.assetinfo.OpenCircuitTest_pb2 import OpenCircuitTest as PBOpenCircuitTest
from zepben.protobuf.cim.iec61968.assetinfo.OverheadWireInfo_pb2 import OverheadWireInfo as PBOverheadWireInfo
from zepben.protobuf.cim.iec61968.assetinfo.PowerTransformerInfo_pb2 import PowerTransformerInfo as PBPowerTransformerInfo
from zepben.protobuf.cim.iec61968.assetinfo.ShortCircuitTest_pb2 import ShortCircuitTest as PBShortCircuitTest
from zepben.protobuf.cim.iec61968.assetinfo.ShuntCompensatorInfo_pb2 import ShuntCompensatorInfo as PBShuntCompensatorInfo
from zepben.protobuf.cim.iec61968.assetinfo.SwitchInfo_pb2 import SwitchInfo as PBSwitchInfo
from zepben.protobuf.cim.iec61968.assetinfo.TransformerEndInfo_pb2 import TransformerEndInfo as PBTransformerEndInfo
from zepben.protobuf.cim.iec61968.assetinfo.TransformerTankInfo_pb2 import TransformerTankInfo as PBTransformerTankInfo
from zepben.protobuf.cim.iec61968.assetinfo.TransformerTest_pb2 import TransformerTest as PBTransformerTest
from zepben.protobuf.cim.iec61968.assetinfo.WireInfo_pb2 import WireInfo as PBWireInfo
from zepben.protobuf.cim.iec61968.assets.AssetContainer_pb2 import AssetContainer as PBAssetContainer
from zepben.protobuf.cim.iec61968.assets.AssetFunction_pb2 import AssetFunction as PBAssetFunction
from zepben.protobuf.cim.iec61968.assets.AssetInfo_pb2 import AssetInfo as PBAssetInfo
from zepben.protobuf.cim.iec61968.assets.AssetOrganisationRole_pb2 import AssetOrganisationRole as PBAssetOrganisationRole
from zepben.protobuf.cim.iec61968.assets.AssetOwner_pb2 import AssetOwner as PBAssetOwner
from zepben.protobuf.cim.iec61968.assets.Asset_pb2 import Asset as PBAsset
from zepben.protobuf.cim.iec61968.assets.Streetlight_pb2 import Streetlight as PBStreetlight
from zepben.protobuf.cim.iec61968.assets.Structure_pb2 import Structure as PBStructure
from zepben.protobuf.cim.iec61968.common.Location_pb2 import Location as PBLocation
from zepben.protobuf.cim.iec61968.common.PositionPoint_pb2 import PositionPoint as PBPositionPoint
from zepben.protobuf.cim.iec61968.common.StreetAddress_pb2 import StreetAddress as PBStreetAddress
from zepben.protobuf.cim.iec61968.common.StreetDetail_pb2 import StreetDetail as PBStreetDetail
from zepben.protobuf.cim.iec61968.common.TownDetail_pb2 import TownDetail as PBTownDetail
from zepben.protobuf.cim.iec61968.infiec61968.infassetinfo.CurrentTransformerInfo_pb2 import CurrentTransformerInfo as PBCurrentTransformerInfo
from zepben.protobuf.cim.iec61968.infiec61968.infassetinfo.PotentialTransformerInfo_pb2 import PotentialTransformerInfo as PBPotentialTransformerInfo
from zepben.protobuf.cim.iec61968.infiec61968.infassets.Pole_pb2 import Pole as PBPole
from zepben.protobuf.cim.iec61968.infiec61968.infcommon.Ratio_pb2 import Ratio as PBRatio
from zepben.protobuf.cim.iec61968.metering.EndDeviceFunction_pb2 import EndDeviceFunction as PBEndDeviceFunction
from zepben.protobuf.cim.iec61968.metering.EndDevice_pb2 import EndDevice as PBEndDevice
from zepben.protobuf.cim.iec61968.metering.Meter_pb2 import Meter as PBMeter
from zepben.protobuf.cim.iec61968.metering.UsagePoint_pb2 import UsagePoint as PBUsagePoint
from zepben.protobuf.cim.iec61968.operations.OperationalRestriction_pb2 import OperationalRestriction as PBOperationalRestriction
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.AuxiliaryEquipment_pb2 import AuxiliaryEquipment as PBAuxiliaryEquipment
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.CurrentTransformer_pb2 import CurrentTransformer as PBCurrentTransformer
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.FaultIndicator_pb2 import FaultIndicator as PBFaultIndicator
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.PotentialTransformer_pb2 import PotentialTransformer as PBPotentialTransformer
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.Sensor_pb2 import Sensor as PBSensor
from zepben.protobuf.cim.iec61970.base.core.AcDcTerminal_pb2 import AcDcTerminal as PBAcDcTerminal
from zepben.protobuf.cim.iec61970.base.core.BaseVoltage_pb2 import BaseVoltage as PBBaseVoltage
from zepben.protobuf.cim.iec61970.base.core.ConductingEquipment_pb2 import ConductingEquipment as PBConductingEquipment
from zepben.protobuf.cim.iec61970.base.core.ConnectivityNodeContainer_pb2 import ConnectivityNodeContainer as PBConnectivityNodeContainer
from zepben.protobuf.cim.iec61970.base.core.ConnectivityNode_pb2 import ConnectivityNode as PBConnectivityNode
from zepben.protobuf.cim.iec61970.base.core.CurveData_pb2 import CurveData as PBCurveData
from zepben.protobuf.cim.iec61970.base.core.Curve_pb2 import Curve as PBCurve
from zepben.protobuf.cim.iec61970.base.core.EquipmentContainer_pb2 import EquipmentContainer as PBEquipmentContainer
from zepben.protobuf.cim.iec61970.base.core.Equipment_pb2 import Equipment as PBEquipment
from zepben.protobuf.cim.iec61970.base.core.Feeder_pb2 import Feeder as PBFeeder
from zepben.protobuf.cim.iec61970.base.core.GeographicalRegion_pb2 import GeographicalRegion as PBGeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.PowerSystemResource_pb2 import PowerSystemResource as PBPowerSystemResource
from zepben.protobuf.cim.iec61970.base.core.SubGeographicalRegion_pb2 import SubGeographicalRegion as PBSubGeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.Substation_pb2 import Substation as PBSubstation
from zepben.protobuf.cim.iec61970.base.core.Terminal_pb2 import Terminal as PBTerminal
from zepben.protobuf.cim.iec61970.base.equivalents.EquivalentBranch_pb2 import EquivalentBranch as PBEquivalentBranch
from zepben.protobuf.cim.iec61970.base.equivalents.EquivalentEquipment_pb2 import EquivalentEquipment as PBEquivalentEquipment
from zepben.protobuf.cim.iec61970.base.generation.production.BatteryUnit_pb2 import BatteryUnit as PBBatteryUnit
from zepben.protobuf.cim.iec61970.base.generation.production.PhotoVoltaicUnit_pb2 import PhotoVoltaicUnit as PBPhotoVoltaicUnit
from zepben.protobuf.cim.iec61970.base.generation.production.PowerElectronicsUnit_pb2 import PowerElectronicsUnit as PBPowerElectronicsUnit
from zepben.protobuf.cim.iec61970.base.generation.production.PowerElectronicsWindUnit_pb2 import PowerElectronicsWindUnit as PBPowerElectronicsWindUnit
from zepben.protobuf.cim.iec61970.base.meas.Accumulator_pb2 import Accumulator as PBAccumulator
from zepben.protobuf.cim.iec61970.base.meas.Analog_pb2 import Analog as PBAnalog
from zepben.protobuf.cim.iec61970.base.meas.Control_pb2 import Control as PBControl
from zepben.protobuf.cim.iec61970.base.meas.Discrete_pb2 import Discrete as PBDiscrete
from zepben.protobuf.cim.iec61970.base.meas.IoPoint_pb2 import IoPoint as PBIoPoint
from zepben.protobuf.cim.iec61970.base.meas.Measurement_pb2 import Measurement as PBMeasurement
from zepben.protobuf.cim.iec61970.base.protection.CurrentRelay_pb2 import CurrentRelay as PBCurrentRelay
from zepben.protobuf.cim.iec61970.base.scada.RemoteControl_pb2 import RemoteControl as PBRemoteControl
from zepben.protobuf.cim.iec61970.base.scada.RemotePoint_pb2 import RemotePoint as PBRemotePoint
from zepben.protobuf.cim.iec61970.base.scada.RemoteSource_pb2 import RemoteSource as PBRemoteSource
from zepben.protobuf.cim.iec61970.base.wires.AcLineSegment_pb2 import AcLineSegment as PBAcLineSegment
from zepben.protobuf.cim.iec61970.base.wires.Breaker_pb2 import Breaker as PBBreaker
from zepben.protobuf.cim.iec61970.base.wires.BusbarSection_pb2 import BusbarSection as PBBusbarSection
from zepben.protobuf.cim.iec61970.base.wires.Clamp_pb2 import Clamp as PBClamp
from zepben.protobuf.cim.iec61970.base.wires.Conductor_pb2 import Conductor as PBConductor
from zepben.protobuf.cim.iec61970.base.wires.Connector_pb2 import Connector as PBConnector
from zepben.protobuf.cim.iec61970.base.wires.Cut_pb2 import Cut as PBCut
from zepben.protobuf.cim.iec61970.base.wires.Disconnector_pb2 import Disconnector as PBDisconnector
from zepben.protobuf.cim.iec61970.base.wires.EarthFaultCompensator_pb2 import EarthFaultCompensator as PBEarthFaultCompensator
from zepben.protobuf.cim.iec61970.base.wires.EnergyConnection_pb2 import EnergyConnection as PBEnergyConnection
from zepben.protobuf.cim.iec61970.base.wires.EnergyConsumerPhase_pb2 import EnergyConsumerPhase as PBEnergyConsumerPhase
from zepben.protobuf.cim.iec61970.base.wires.EnergyConsumer_pb2 import EnergyConsumer as PBEnergyConsumer
from zepben.protobuf.cim.iec61970.base.wires.EnergySourcePhase_pb2 import EnergySourcePhase as PBEnergySourcePhase
from zepben.protobuf.cim.iec61970.base.wires.EnergySource_pb2 import EnergySource as PBEnergySource
from zepben.protobuf.cim.iec61970.base.wires.Fuse_pb2 import Fuse as PBFuse
from zepben.protobuf.cim.iec61970.base.wires.GroundDisconnector_pb2 import GroundDisconnector as PBGroundDisconnector
from zepben.protobuf.cim.iec61970.base.wires.Ground_pb2 import Ground as PBGround
from zepben.protobuf.cim.iec61970.base.wires.GroundingImpedance_pb2 import GroundingImpedance as PBGroundingImpedance
from zepben.protobuf.cim.iec61970.base.wires.Jumper_pb2 import Jumper as PBJumper
from zepben.protobuf.cim.iec61970.base.wires.Junction_pb2 import Junction as PBJunction
from zepben.protobuf.cim.iec61970.base.wires.Line_pb2 import Line as PBLine
from zepben.protobuf.cim.iec61970.base.wires.LinearShuntCompensator_pb2 import LinearShuntCompensator as PBLinearShuntCompensator
from zepben.protobuf.cim.iec61970.base.wires.LoadBreakSwitch_pb2 import LoadBreakSwitch as PBLoadBreakSwitch
from zepben.protobuf.cim.iec61970.base.wires.PerLengthImpedance_pb2 import PerLengthImpedance as PBPerLengthImpedance
from zepben.protobuf.cim.iec61970.base.wires.PerLengthLineParameter_pb2 import PerLengthLineParameter as PBPerLengthLineParameter
from zepben.protobuf.cim.iec61970.base.wires.PerLengthPhaseImpedance_pb2 import PerLengthPhaseImpedance as PBPerLengthPhaseImpedance
from zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance_pb2 import PerLengthSequenceImpedance as PBPerLengthSequenceImpedance
from zepben.protobuf.cim.iec61970.base.wires.PetersenCoil_pb2 import PetersenCoil as PBPetersenCoil
from zepben.protobuf.cim.iec61970.base.wires.PhaseImpedanceData_pb2 import PhaseImpedanceData as PBPhaseImpedanceData
from zepben.protobuf.cim.iec61970.base.wires.PowerElectronicsConnectionPhase_pb2 import PowerElectronicsConnectionPhase as PBPowerElectronicsConnectionPhase
from zepben.protobuf.cim.iec61970.base.wires.PowerElectronicsConnection_pb2 import PowerElectronicsConnection as PBPowerElectronicsConnection
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformerEnd_pb2 import PowerTransformerEnd as PBPowerTransformerEnd
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformer_pb2 import PowerTransformer as PBPowerTransformer
from zepben.protobuf.cim.iec61970.base.wires.ProtectedSwitch_pb2 import ProtectedSwitch as PBProtectedSwitch
from zepben.protobuf.cim.iec61970.base.wires.RatioTapChanger_pb2 import RatioTapChanger as PBRatioTapChanger
from zepben.protobuf.cim.iec61970.base.wires.ReactiveCapabilityCurve_pb2 import ReactiveCapabilityCurve as PBReactiveCapabilityCurve
from zepben.protobuf.cim.iec61970.base.wires.Recloser_pb2 import Recloser as PBRecloser
from zepben.protobuf.cim.iec61970.base.wires.RegulatingCondEq_pb2 import RegulatingCondEq as PBRegulatingCondEq
from zepben.protobuf.cim.iec61970.base.wires.RegulatingControl_pb2 import RegulatingControl as PBRegulatingControl
from zepben.protobuf.cim.iec61970.base.wires.RotatingMachine_pb2 import RotatingMachine as PBRotatingMachine
from zepben.protobuf.cim.iec61970.base.wires.SeriesCompensator_pb2 import SeriesCompensator as PBSeriesCompensator
from zepben.protobuf.cim.iec61970.base.wires.ShuntCompensator_pb2 import ShuntCompensator as PBShuntCompensator
from zepben.protobuf.cim.iec61970.base.wires.StaticVarCompensator_pb2 import StaticVarCompensator as PBStaticVarCompensator
from zepben.protobuf.cim.iec61970.base.wires.Switch_pb2 import Switch as PBSwitch
from zepben.protobuf.cim.iec61970.base.wires.SynchronousMachine_pb2 import SynchronousMachine as PBSynchronousMachine
from zepben.protobuf.cim.iec61970.base.wires.TapChangerControl_pb2 import TapChangerControl as PBTapChangerControl
from zepben.protobuf.cim.iec61970.base.wires.TapChanger_pb2 import TapChanger as PBTapChanger
from zepben.protobuf.cim.iec61970.base.wires.TransformerEnd_pb2 import TransformerEnd as PBTransformerEnd
from zepben.protobuf.cim.iec61970.base.wires.TransformerStarImpedance_pb2 import TransformerStarImpedance as PBTransformerStarImpedance
from zepben.protobuf.cim.iec61970.infiec61970.feeder.Circuit_pb2 import Circuit as PBCircuit

from zepben.ewb.model.cim.extensions.iec61968.assetinfo.relay_info import *
from zepben.ewb.model.cim.extensions.iec61968.metering.pan_demand_reponse_function import *
from zepben.ewb.model.cim.extensions.iec61970.base.core.site import *
from zepben.ewb.model.cim.extensions.iec61970.base.feeder.loop import *
from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_feeder import *
from zepben.ewb.model.cim.extensions.iec61970.base.generation.production.ev_charging_unit import *
from zepben.ewb.model.cim.extensions.iec61970.base.protection.distance_relay import *
from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_function import *
from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_scheme import *
from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_system import *
from zepben.ewb.model.cim.extensions.iec61970.base.protection.relay_setting import *
from zepben.ewb.model.cim.extensions.iec61970.base.protection.voltage_relay import *
from zepben.ewb.model.cim.extensions.iec61970.base.wires.battery_control import *
from zepben.ewb.model.cim.extensions.iec61970.base.wires.transformer_end_rated_s import *
from zepben.ewb.model.cim.iec61968.assetinfo.cable_info import *
from zepben.ewb.model.cim.iec61968.assetinfo.no_load_test import *
from zepben.ewb.model.cim.iec61968.assetinfo.open_circuit_test import *
from zepben.ewb.model.cim.iec61968.assetinfo.overhead_wire_info import *
from zepben.ewb.model.cim.iec61968.assetinfo.power_transformer_info import *
from zepben.ewb.model.cim.iec61968.assetinfo.short_circuit_test import *
from zepben.ewb.model.cim.iec61968.assetinfo.shunt_compensator_info import *
from zepben.ewb.model.cim.iec61968.assetinfo.switch_info import *
from zepben.ewb.model.cim.iec61968.assetinfo.transformer_end_info import *
from zepben.ewb.model.cim.iec61968.assetinfo.transformer_tank_info import *
from zepben.ewb.model.cim.iec61968.assetinfo.transformer_test import *
from zepben.ewb.model.cim.iec61968.assetinfo.wire_info import *
from zepben.ewb.model.cim.iec61968.assets.asset import *
from zepben.ewb.model.cim.iec61968.assets.asset_container import *
from zepben.ewb.model.cim.iec61968.assets.asset_function import *
from zepben.ewb.model.cim.iec61968.assets.asset_info import *
from zepben.ewb.model.cim.iec61968.assets.asset_organisation_role import *
from zepben.ewb.model.cim.iec61968.assets.asset_owner import *
from zepben.ewb.model.cim.iec61968.assets.streetlight import *
from zepben.ewb.model.cim.iec61968.assets.structure import *
from zepben.ewb.model.cim.iec61968.common.location import *
from zepben.ewb.model.cim.iec61968.common.position_point import *
from zepben.ewb.model.cim.iec61968.common.street_address import *
from zepben.ewb.model.cim.iec61968.common.street_detail import *
from zepben.ewb.model.cim.iec61968.common.town_detail import *
from zepben.ewb.model.cim.iec61968.infiec61968.infassetinfo.current_transformer_info import *
from zepben.ewb.model.cim.iec61968.infiec61968.infassetinfo.potential_transformer_info import *
from zepben.ewb.model.cim.iec61968.infiec61968.infassets.pole import *
from zepben.ewb.model.cim.iec61968.infiec61968.infcommon.ratio import *
from zepben.ewb.model.cim.iec61968.metering.end_device import *
from zepben.ewb.model.cim.iec61968.metering.end_device_function import *
from zepben.ewb.model.cim.iec61968.metering.meter import *
from zepben.ewb.model.cim.iec61968.metering.usage_point import *
from zepben.ewb.model.cim.iec61968.operations.operational_restriction import *
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.auxiliary_equipment import *
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.current_transformer import *
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.fault_indicator import *
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.potential_transformer import *
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.sensor import *
from zepben.ewb.model.cim.iec61970.base.core.ac_dc_terminal import *
from zepben.ewb.model.cim.iec61970.base.core.base_voltage import *
from zepben.ewb.model.cim.iec61970.base.core.conducting_equipment import *
from zepben.ewb.model.cim.iec61970.base.core.connectivity_node import *
from zepben.ewb.model.cim.iec61970.base.core.connectivity_node_container import *
from zepben.ewb.model.cim.iec61970.base.core.curve import *
from zepben.ewb.model.cim.iec61970.base.core.curve_data import *
from zepben.ewb.model.cim.iec61970.base.core.equipment import *
from zepben.ewb.model.cim.iec61970.base.core.equipment_container import *
from zepben.ewb.model.cim.iec61970.base.core.feeder import *
from zepben.ewb.model.cim.iec61970.base.core.geographical_region import *
from zepben.ewb.model.cim.iec61970.base.core.power_system_resource import *
from zepben.ewb.model.cim.iec61970.base.core.sub_geographical_region import *
from zepben.ewb.model.cim.iec61970.base.core.substation import *
from zepben.ewb.model.cim.iec61970.base.core.terminal import *
from zepben.ewb.model.cim.iec61970.base.equivalents.equivalent_branch import *
from zepben.ewb.model.cim.iec61970.base.equivalents.equivalent_equipment import *
from zepben.ewb.model.cim.iec61970.base.generation.production.battery_unit import *
from zepben.ewb.model.cim.iec61970.base.generation.production.photo_voltaic_unit import *
from zepben.ewb.model.cim.iec61970.base.generation.production.power_electronics_unit import *
from zepben.ewb.model.cim.iec61970.base.generation.production.power_electronics_wind_unit import *
from zepben.ewb.model.cim.iec61970.base.meas.accumulator import *
from zepben.ewb.model.cim.iec61970.base.meas.analog import *
from zepben.ewb.model.cim.iec61970.base.meas.control import *
from zepben.ewb.model.cim.iec61970.base.meas.discrete import *
from zepben.ewb.model.cim.iec61970.base.meas.iopoint import *
from zepben.ewb.model.cim.iec61970.base.meas.measurement import *
from zepben.ewb.model.cim.iec61970.base.protection.current_relay import *
from zepben.ewb.model.cim.iec61970.base.scada.remote_control import *
from zepben.ewb.model.cim.iec61970.base.scada.remote_point import *
from zepben.ewb.model.cim.iec61970.base.scada.remote_source import *
from zepben.ewb.model.cim.iec61970.base.wires.ac_line_segment import *
from zepben.ewb.model.cim.iec61970.base.wires.breaker import *
from zepben.ewb.model.cim.iec61970.base.wires.busbar_section import *
from zepben.ewb.model.cim.iec61970.base.wires.clamp import *
from zepben.ewb.model.cim.iec61970.base.wires.conductor import *
from zepben.ewb.model.cim.iec61970.base.wires.connector import *
from zepben.ewb.model.cim.iec61970.base.wires.cut import *
from zepben.ewb.model.cim.iec61970.base.wires.disconnector import *
from zepben.ewb.model.cim.iec61970.base.wires.earth_fault_compensator import *
from zepben.ewb.model.cim.iec61970.base.wires.energy_connection import *
from zepben.ewb.model.cim.iec61970.base.wires.energy_consumer import *
from zepben.ewb.model.cim.iec61970.base.wires.energy_consumer_phase import *
from zepben.ewb.model.cim.iec61970.base.wires.energy_source import *
from zepben.ewb.model.cim.iec61970.base.wires.energy_source_phase import *
from zepben.ewb.model.cim.iec61970.base.wires.fuse import *
from zepben.ewb.model.cim.iec61970.base.wires.ground import *
from zepben.ewb.model.cim.iec61970.base.wires.ground_disconnector import *
from zepben.ewb.model.cim.iec61970.base.wires.grounding_impedance import *
from zepben.ewb.model.cim.iec61970.base.wires.jumper import *
from zepben.ewb.model.cim.iec61970.base.wires.junction import *
from zepben.ewb.model.cim.iec61970.base.wires.line import *
from zepben.ewb.model.cim.iec61970.base.wires.linear_shunt_compensator import *
from zepben.ewb.model.cim.iec61970.base.wires.load_break_switch import *
from zepben.ewb.model.cim.iec61970.base.wires.per_length_impedance import *
from zepben.ewb.model.cim.iec61970.base.wires.per_length_line_parameter import *
from zepben.ewb.model.cim.iec61970.base.wires.per_length_phase_impedance import *
from zepben.ewb.model.cim.iec61970.base.wires.per_length_sequence_impedance import *
from zepben.ewb.model.cim.iec61970.base.wires.petersen_coil import *
from zepben.ewb.model.cim.iec61970.base.wires.phase_impedance_data import *
from zepben.ewb.model.cim.iec61970.base.wires.power_electronics_connection import *
from zepben.ewb.model.cim.iec61970.base.wires.power_electronics_connection_phase import *
from zepben.ewb.model.cim.iec61970.base.wires.power_transformer import *
from zepben.ewb.model.cim.iec61970.base.wires.power_transformer_end import *
from zepben.ewb.model.cim.iec61970.base.wires.protected_switch import *
from zepben.ewb.model.cim.iec61970.base.wires.ratio_tap_changer import *
from zepben.ewb.model.cim.iec61970.base.wires.reactive_capability_curve import *
from zepben.ewb.model.cim.iec61970.base.wires.recloser import *
from zepben.ewb.model.cim.iec61970.base.wires.regulating_cond_eq import *
from zepben.ewb.model.cim.iec61970.base.wires.regulating_control import *
from zepben.ewb.model.cim.iec61970.base.wires.rotating_machine import *
from zepben.ewb.model.cim.iec61970.base.wires.series_compensator import *
from zepben.ewb.model.cim.iec61970.base.wires.shunt_compensator import *
from zepben.ewb.model.cim.iec61970.base.wires.static_var_compensator import *
from zepben.ewb.model.cim.iec61970.base.wires.switch import *
from zepben.ewb.model.cim.iec61970.base.wires.synchronous_machine import *
from zepben.ewb.model.cim.iec61970.base.wires.tap_changer import *
from zepben.ewb.model.cim.iec61970.base.wires.tap_changer_control import *
from zepben.ewb.model.cim.iec61970.base.wires.transformer_end import *
from zepben.ewb.model.cim.iec61970.base.wires.transformer_star_impedance import *
from zepben.ewb.model.cim.iec61970.infiec61970.feeder.circuit import *
from zepben.ewb.services.common.translator.base_cim2proto import identified_object_to_pb, organisation_role_to_pb, document_to_pb, bind_to_pb, set_or_null
from zepben.ewb.services.common.translator.util import mrid_or_empty, from_nullable_int, from_nullable_float, from_nullable_long, from_nullable_uint, \
    nullable_bool_settings
# noinspection PyProtectedMember
from zepben.ewb.services.network.translator.network_enum_mappers import _map_battery_control_mode, _map_battery_state_kind, _map_end_device_function_kind, \
    _map_feeder_direction, _map_phase_code, _map_phase_shunt_connection_kind, _map_potential_transformer_kind, _map_power_direction_kind, _map_protection_kind, \
    _map_regulating_control_mode_kind, _map_single_phase_kind, _map_streetlight_lamp_kind, _map_svc_control_mode, _map_synchronous_machine_kind, \
    _map_transformer_construction_kind, _map_transformer_cooling_type, _map_transformer_function_kind, _map_unit_symbol, _map_vector_group, \
    _map_winding_connection, _map_wire_material_kind


def _get_or_none(getter, obj) -> Optional[Any]:
    return getter(obj) if obj else None


class CimTranslationException(Exception):
    pass


##################################
# Extensions IEC61968 Asset Info #
##################################

@bind_to_pb
def relay_info_to_pb(cim: RelayInfo) -> PBRelayInfo:
    return PBRelayInfo(
        ai=asset_info_to_pb(cim),
        recloseDelays=cim.reclose_delays,
        **set_or_null(
            curveSetting=cim.curve_setting,
            recloseFast=cim.reclose_fast,
        )
    )


################################
# Extensions IEC61968 Metering #
################################

@bind_to_pb
def pan_demand_response_function_to_pb(cim: PanDemandResponseFunction) -> PBPanDemandResponseFunction:
    """
    Convert the :class:`PanDemandResponseFunction` into its protobuf counterpart.
    :param cim: The :class:`PanDemandResponseFunction` to convert.
    :return: The protobuf builder.
    """
    # noinspection PyProtectedMember
    return PBPanDemandResponseFunction(
        edf=end_device_function_to_pb(cim),
        kind=_map_end_device_function_kind.to_pb(cim.kind),
        **set_or_null(
            appliance=cim._appliance_bitmask
        )
    )


#################################
# Extensions IEC61970 Base Core #
#################################

@bind_to_pb
def site_to_pb(cim: Site) -> PBSite:
    return PBSite(ec=equipment_container_to_pb(cim))


###################################
# Extensions IEC61970 Base Feeder #
###################################

@bind_to_pb
def loop_to_pb(cim: Loop) -> PBLoop:
    return PBLoop(
        io=identified_object_to_pb(cim),
        circuitMRIDs=[str(io.mrid) for io in cim.circuits],
        substationMRIDs=[str(io.mrid) for io in cim.substations],
        normalEnergizingSubstationMRIDs=[str(io.mrid) for io in cim.energizing_substations]
    )


@bind_to_pb
def lv_feeder_to_pb(cim: LvFeeder) -> PBLvFeeder:
    return PBLvFeeder(
        ec=equipment_container_to_pb(cim),
        normalHeadTerminalMRID=mrid_or_empty(cim.normal_head_terminal),
        normalEnergizingFeederMRIDs=[str(io.mrid) for io in cim.normal_energizing_feeders],
        currentlyEnergizingFeederMRIDs=[str(io.mrid) for io in cim.current_energizing_feeders]
    )


##################################################
# Extensions IEC61970 Base Generation Production #
##################################################

@bind_to_pb
def ev_charging_unit(cim: EvChargingUnit) -> PBEvChargingUnit:
    return PBEvChargingUnit(peu=power_electronics_unit_to_pb(cim))


#######################################
# Extensions IEC61970 Base Protection #
#######################################

@bind_to_pb
def distance_relay_to_pb(cim: DistanceRelay) -> PBDistanceRelay:
    return PBDistanceRelay(
        prf=protection_relay_function_to_pb(cim, True),
        **set_or_null(
            backwardBlind=cim.backward_blind,
            backwardReach=cim.backward_reach,
            backwardReactance=cim.backward_reactance,
            forwardBlind=cim.forward_blind,
            forwardReach=cim.forward_reach,
            forwardReactance=cim.forward_reactance,
            operationPhaseAngle1=cim.operation_phase_angle1,
            operationPhaseAngle2=cim.operation_phase_angle2,
            operationPhaseAngle3=cim.operation_phase_angle3,
        )
    )


def protection_relay_function_to_pb(cim: ProtectionRelayFunction, include_asset_info: bool = False) -> PBProtectionRelayFunction:
    return PBProtectionRelayFunction(
        psr=power_system_resource_to_pb(cim, include_asset_info),
        timeLimits=cim.time_limits,
        thresholds=[relay_setting_to_pb(rs) for rs in cim.thresholds],
        protectionKind=_map_protection_kind.to_pb(cim.protection_kind),
        protectedSwitchMRIDs=[str(io.mrid) for io in cim.protected_switches],
        powerDirection=_map_power_direction_kind.to_pb(cim.power_direction),
        sensorMRIDs=[str(io.mrid) for io in cim.sensors],
        schemeMRIDs=[str(io.mrid) for io in cim.schemes],
        **set_or_null(
            model=cim.model,
            reclosing=cim.reclosing,
            relayDelayTime=cim.relay_delay_time,
            directable=cim.directable,
        )
    )


@bind_to_pb
def protection_relay_scheme_to_pb(cim: ProtectionRelayScheme) -> PBProtectionRelayScheme:
    return PBProtectionRelayScheme(
        io=identified_object_to_pb(cim),
        functionMRIDs=[str(io.mrid) for io in cim.functions],
        systemMRID=mrid_or_empty(cim.system),
    )


@bind_to_pb
def protection_relay_system_to_pb(cim: ProtectionRelaySystem) -> PBProtectionRelaySystem:
    return PBProtectionRelaySystem(
        eq=equipment_to_pb(cim),
        protectionKind=_map_protection_kind.to_pb(cim.protection_kind),
        schemeMRIDs=[str(io.mrid) for io in cim.schemes],
    )


def relay_setting_to_pb(cim: RelaySetting) -> PBRelaySetting:
    return PBRelaySetting(
        unitSymbol=_map_unit_symbol.to_pb(cim.unit_symbol),
        value=from_nullable_float(cim.value),
        **set_or_null(
            name=cim.name,
        )
    )


@bind_to_pb
def voltage_relay_to_pb(cim: VoltageRelay) -> PBVoltageRelay:
    return PBVoltageRelay(
        prf=protection_relay_function_to_pb(cim, True),
    )


##################################
# Extensions IEC61970 Base Wires #
##################################

@bind_to_pb
def battery_control_to_pb(cim: BatteryControl) -> PBBatteryControl:
    """
    Convert the :class:`BatteryControl` into its protobuf counterpart.
    :param cim: The :class:`BatteryControl` to convert.
    :return: The protobuf builder.
    """

    return PBBatteryControl(
        rc=regulating_control_to_pb(cim),
        controlMode=_map_battery_control_mode.to_pb(cim.control_mode),
        **set_or_null(
            chargingRate=cim.charging_rate,
            dischargingRate=cim.discharging_rate,
            reservePercent=cim.reserve_percent,
        )
    )


#######################
# IEC61968 Asset Info #
#######################

@bind_to_pb
def cable_info_to_pb(cim: CableInfo) -> PBCableInfo:
    return PBCableInfo(wi=wire_info_to_pb(cim))


@bind_to_pb
def no_load_test_to_pb(cim: NoLoadTest) -> PBNoLoadTest:
    return PBNoLoadTest(
        tt=transformer_test_to_pb(cim),
        **set_or_null(
            energisedEndVoltage=cim.energised_end_voltage,
            excitingCurrent=cim.exciting_current,
            excitingCurrentZero=cim.exciting_current_zero,
            loss=cim.loss,
            lossZero=cim.loss_zero,
        )
    )


@bind_to_pb
def open_circuit_test_to_pb(cim: OpenCircuitTest) -> PBOpenCircuitTest:
    return PBOpenCircuitTest(
        tt=transformer_test_to_pb(cim),
        **set_or_null(
            energisedEndStep=cim.energised_end_step,
            energisedEndVoltage=cim.energised_end_voltage,
            openEndStep=cim.open_end_step,
            openEndVoltage=cim.open_end_voltage,
            phaseShift=cim.phase_shift,
        )
    )


@bind_to_pb
def overhead_wire_info_to_pb(cim: OverheadWireInfo) -> PBOverheadWireInfo:
    return PBOverheadWireInfo(wi=wire_info_to_pb(cim))


@bind_to_pb
def power_transformer_info_to_pb(cim: PowerTransformerInfo) -> PBPowerTransformerInfo:
    return PBPowerTransformerInfo(
        ai=asset_info_to_pb(cim),
        transformerTankInfoMRIDs=[tti.mrid for tti in cim.transformer_tank_infos]
    )


@bind_to_pb
def short_circuit_test_to_pb(cim: ShortCircuitTest) -> PBShortCircuitTest:
    return PBShortCircuitTest(
        tt=transformer_test_to_pb(cim),
        **set_or_null(
            current=cim.current,
            energisedEndStep=cim.energised_end_step,
            groundedEndStep=cim.grounded_end_step,
            leakageImpedance=cim.leakage_impedance,
            leakageImpedanceZero=cim.leakage_impedance_zero,
            loss=cim.loss,
            lossZero=cim.loss_zero,
            power=cim.power,
            voltage=cim.voltage,
            voltageOhmicPart=cim.voltage_ohmic_part,
        )
    )


@bind_to_pb
def shunt_compensator_info_to_pb(cim: ShuntCompensatorInfo) -> PBShuntCompensatorInfo:
    return PBShuntCompensatorInfo(
        ai=asset_info_to_pb(cim),
        **set_or_null(
            maxPowerLoss=cim.max_power_loss,
            ratedCurrent=cim.rated_current,
            ratedReactivePower=cim.rated_reactive_power,
            ratedVoltage=cim.rated_voltage,
        )
    )


@bind_to_pb
def switch_info_to_pb(cim: SwitchInfo) -> PBSwitchInfo:
    return PBSwitchInfo(
        ai=asset_info_to_pb(cim),
        **set_or_null(
            ratedInterruptingTime=cim.rated_interrupting_time
        )
    )


@bind_to_pb
def transformer_end_info_to_pb(cim: TransformerEndInfo) -> PBTransformerEndInfo:
    return PBTransformerEndInfo(
        ai=asset_info_to_pb(cim),
        connectionKind=_map_winding_connection.to_pb(cim.connection_kind),
        endNumber=cim.end_number,
        transformerTankInfoMRID=mrid_or_empty(cim.transformer_tank_info),
        transformerStarImpedanceMRID=mrid_or_empty(cim.transformer_star_impedance),
        energisedEndNoLoadTestsMRID=mrid_or_empty(cim.energised_end_no_load_tests),
        energisedEndShortCircuitTestsMRID=mrid_or_empty(cim.energised_end_short_circuit_tests),
        groundedEndShortCircuitTestsMRID=mrid_or_empty(cim.grounded_end_short_circuit_tests),
        openEndOpenCircuitTestsMRID=mrid_or_empty(cim.open_end_open_circuit_tests),
        energisedEndOpenCircuitTestsMRID=mrid_or_empty(cim.energised_end_open_circuit_tests),
        **set_or_null(
            emergencyS=cim.emergency_s,
            insulationU=cim.insulation_u,
            phaseAngleClock=cim.phase_angle_clock,
            r=cim.r,
            ratedS=cim.rated_s,
            ratedU=cim.rated_u,
            shortTermS=cim.short_term_s,
        )
    )


@bind_to_pb
def transformer_tank_info_to_pb(cim: TransformerTankInfo) -> PBTransformerTankInfo:
    return PBTransformerTankInfo(
        ai=asset_info_to_pb(cim),
        transformerEndInfoMRIDs=[str(tei.mrid) for tei in cim.transformer_end_infos]
    )


@bind_to_pb
def transformer_test_to_pb(cim: TransformerTest) -> PBTransformerTest:
    return PBTransformerTest(
        io=identified_object_to_pb(cim),
        **set_or_null(
            basePower=cim.base_power,
            temperature=cim.temperature,
        )
    )


@bind_to_pb
def wire_info_to_pb(cim: WireInfo) -> PBWireInfo:
    return PBWireInfo(
        ai=asset_info_to_pb(cim),
        material=_map_wire_material_kind.to_pb(cim.material),
        **set_or_null(
            ratedCurrent=cim.rated_current,
        )
    )


###################
# IEC61968 Assets #
###################

def asset_to_pb(cim: Asset) -> PBAsset:
    return PBAsset(
        io=identified_object_to_pb(cim),
        locationMRID=cim.location.mrid if cim.location else None,
        organisationRoleMRIDs=[str(io.mrid) for io in cim.organisation_roles],
        powerSystemResourceMRIDs=[str(io.mrid) for io in cim.power_system_resources],
    )


def asset_container_to_pb(cim: AssetContainer) -> PBAssetContainer:
    return PBAssetContainer(at=asset_to_pb(cim))


def asset_function_to_pb(cim: AssetFunction) -> PBAssetFunction:
    """
    Convert the :class:`AssetFunction` into its protobuf counterpart.
    :param cim: The :class:`AssetFunction` to convert.
    :return: The protobuf builder.
    """
    return PBAssetFunction(io=identified_object_to_pb(cim))


def asset_info_to_pb(cim: AssetInfo) -> PBAssetInfo:
    return PBAssetInfo(io=identified_object_to_pb(cim))


def asset_organisation_role_to_pb(cim: AssetOrganisationRole) -> PBAssetOrganisationRole:
    pb = PBAssetOrganisationRole()
    getattr(pb, "or").CopyFrom(organisation_role_to_pb(cim))
    return pb


@bind_to_pb
def asset_owner_to_pb(cim: AssetOwner) -> PBAssetOwner:
    return PBAssetOwner(aor=asset_organisation_role_to_pb(cim))


@bind_to_pb
def streetlight_to_pb(cim: Streetlight) -> PBStreetlight:
    return PBStreetlight(
        at=asset_to_pb(cim),
        poleMRID=mrid_or_empty(cim.pole),
        lampKind=_map_streetlight_lamp_kind.to_pb(cim.lamp_kind),
        **set_or_null(
            lightRating=cim.light_rating,
        )
    )


def structure_to_pb(cim: Structure) -> PBStructure:
    return PBStructure(ac=asset_container_to_pb(cim))


###################
# IEC61968 Common #
###################

@bind_to_pb
def location_to_pb(cim: Location) -> PBLocation:
    return PBLocation(
        io=identified_object_to_pb(cim),
        mainAddress=_get_or_none(street_address_to_pb, cim.main_address),
        positionPoints=[position_point_to_pb(point) for point in cim.points]
    )


def position_point_to_pb(cim: PositionPoint) -> PBPositionPoint:
    return PBPositionPoint(
        xPosition=cim.x_position,
        yPosition=cim.y_position
    )


def street_address_to_pb(cim: StreetAddress) -> PBStreetAddress:
    return PBStreetAddress(
        townDetail=_get_or_none(town_detail_to_pb, cim.town_detail),
        streetDetail=_get_or_none(street_detail_to_pb, cim.street_detail),
        **set_or_null(
            postalCode=cim.postal_code,
            poBox=cim.po_box,
        )
    )


def street_detail_to_pb(cim: StreetDetail) -> PBStreetDetail:
    return PBStreetDetail(
        **set_or_null(
            buildingName=cim.building_name,
            floorIdentification=cim.floor_identification,
            name=cim.name,
            number=cim.number,
            suiteNumber=cim.suite_number,
            type=cim.type,
            displayAddress=cim.display_address
        )
    )


def town_detail_to_pb(cim: TownDetail) -> PBTownDetail:
    return PBTownDetail(
        **set_or_null(
            name=cim.name,
            stateOrProvince=cim.state_or_province
        )
    )


#####################################
# IEC61968 InfIEC61968 InfAssetInfo #
#####################################

@bind_to_pb
def current_transformer_info_to_pb(cim: CurrentTransformerInfo) -> PBCurrentTransformerInfo:
    return PBCurrentTransformerInfo(
        ai=asset_info_to_pb(cim),
        maxRatio=_get_or_none(ratio_to_pb, cim.max_ratio),
        nominalRatio=_get_or_none(ratio_to_pb, cim.nominal_ratio),
        **set_or_null(
            accuracyClass=cim.accuracy_class,
            accuracyLimit=cim.accuracy_limit,
            coreCount=cim.core_count,
            ctClass=cim.ct_class,
            kneePointVoltage=cim.knee_point_voltage,
            primaryRatio=cim.primary_ratio,
            ratedCurrent=cim.rated_current,
            secondaryFlsRating=cim.secondary_fls_rating,
            secondaryRatio=cim.secondary_ratio,
            usage=cim.usage,
        )
    )


@bind_to_pb
def potential_transformer_info_to_pb(cim: PotentialTransformerInfo) -> PBPotentialTransformerInfo:
    return PBPotentialTransformerInfo(
        ai=asset_info_to_pb(cim),
        nominalRatio=_get_or_none(ratio_to_pb, cim.nominal_ratio),
        **set_or_null(
            accuracyClass=cim.accuracy_class,
            primaryRatio=cim.primary_ratio,
            ptClass=cim.pt_class,
            ratedVoltage=cim.rated_voltage,
            secondaryRatio=cim.secondary_ratio,

        )
    )


##################################
# IEC61968 InfIEC61968 InfAssets #
##################################

@bind_to_pb
def pole_to_pb(cim: Pole) -> PBPole:
    return PBPole(
        st=structure_to_pb(cim),
        streetlightMRIDs=[str(io.mrid) for io in cim.streetlights],
        **set_or_null(
            classification=cim.classification,
        )
    )


##################################
# IEC61968 InfIEC61968 InfCommon #
##################################

def ratio_to_pb(cim: Ratio) -> PBRatio:
    return PBRatio(denominator=cim.denominator, numerator=cim.numerator)


#####################
# IEC61968 Metering #
#####################

def end_device_to_pb(cim: EndDevice) -> PBEndDevice:
    """
    Convert the :class:`EndDevice` into its protobuf counterpart.
    :param cim: The :class:`EndDevice` to convert.
    :return: The protobuf builder.
    """
    return PBEndDevice(
        ac=asset_container_to_pb(cim),
        usagePointMRIDs=[str(io.mrid) for io in cim.usage_points],
        endDeviceFunctionMRIDs=[str(io.mrid) for io in cim.functions],
        customerMRID=cim.customer_mrid,
        serviceLocationMRID=mrid_or_empty(cim.service_location),
    )


def end_device_function_to_pb(cim: EndDeviceFunction) -> PBEndDeviceFunction:
    """
    Convert the :class:`EndDeviceFunction` into its protobuf counterpart.
    :param cim: The :class:`EndDeviceFunction` to convert.
    :return: The protobuf builder.
    """
    return PBEndDeviceFunction(
        af=asset_function_to_pb(cim),
        **set_or_null(
            enabled=cim.enabled,
        )
    )


@bind_to_pb
def meter_to_pb(cim: Meter) -> PBMeter:
    return PBMeter(ed=end_device_to_pb(cim))


@bind_to_pb
def usage_point_to_pb(cim: UsagePoint) -> PBUsagePoint:
    return PBUsagePoint(
        io=identified_object_to_pb(cim),
        usagePointLocationMRID=mrid_or_empty(cim.usage_point_location),
        equipmentMRIDs=[str(io.mrid) for io in cim.equipment],
        endDeviceMRIDs=[str(io.mrid) for io in cim.end_devices],
        phaseCode=_map_phase_code.to_pb(cim.phase_code),
        **set_or_null(
            isVirtual=cim.is_virtual,
            connectionCategory=cim.connection_category,
            ratedPower=cim.rated_power,
            approvedInverterCapacity=cim.approved_inverter_capacity,
        ),
    )


#######################
# IEC61968 Operations #
#######################

@bind_to_pb
def operational_restriction_to_pb(cim: OperationalRestriction) -> PBOperationalRestriction:
    return PBOperationalRestriction(doc=document_to_pb(cim))


#####################################
# IEC61970 Base Auxiliary Equipment #
#####################################

def auxiliary_equipment_to_pb(cim: AuxiliaryEquipment, include_asset_info: bool = False) -> PBAuxiliaryEquipment:
    return PBAuxiliaryEquipment(
        eq=equipment_to_pb(cim, include_asset_info),
        terminalMRID=mrid_or_empty(cim.terminal)
    )


@bind_to_pb
def current_transformer_to_pb(cim: CurrentTransformer) -> PBCurrentTransformer:
    return PBCurrentTransformer(
        sn=sensor_to_pb(cim, True),
        **set_or_null(
            coreBurden=cim.core_burden,
        )
    )


@bind_to_pb
def fault_indicator_to_pb(cim: FaultIndicator) -> PBFaultIndicator:
    return PBFaultIndicator(ae=auxiliary_equipment_to_pb(cim))


@bind_to_pb
def potential_transformer_to_pb(cim: PotentialTransformer) -> PBPotentialTransformer:
    return PBPotentialTransformer(
        sn=sensor_to_pb(cim, True),
        type=_map_potential_transformer_kind.to_pb(cim.type)
    )


def sensor_to_pb(cim: Sensor, include_asset_info: bool = False) -> PBSensor:
    return PBSensor(
        ae=auxiliary_equipment_to_pb(cim, include_asset_info),
        relayFunctionMRIDs=[str(io.mrid) for io in cim.relay_functions],
    )


######################
# IEC61970 Base Core #
######################

def ac_dc_terminal_to_pb(cim: AcDcTerminal) -> PBAcDcTerminal:
    return PBAcDcTerminal(io=identified_object_to_pb(cim))


@bind_to_pb
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


@bind_to_pb
def connectivity_node_to_pb(cim: ConnectivityNode) -> PBConnectivityNode:
    return PBConnectivityNode(io=identified_object_to_pb(cim))


def connectivity_node_container_to_pb(cim: ConnectivityNodeContainer) -> PBConnectivityNodeContainer:
    return PBConnectivityNodeContainer(psr=power_system_resource_to_pb(cim))


def curve_to_pb(cim: Curve) -> PBCurve:
    return PBCurve(
        io=identified_object_to_pb(cim),
        curveData=[curve_data_to_pb(it) for it in cim.data]
    )


def curve_data_to_pb(cim: CurveData) -> PBCurveData:
    return PBCurveData(
        xValue=cim.x_value,
        y1Value=cim.y1_value,
        **set_or_null(
            y2Value=cim.y2_value,
            y3Value=cim.y3_value
        )
    )


def equipment_to_pb(cim: Equipment, include_asset_info: bool = False) -> PBEquipment:
    ts = None
    if cim.commissioned_date:
        ts = PBTimestamp()
        ts.FromDatetime(cim.commissioned_date)
    return PBEquipment(
        psr=power_system_resource_to_pb(cim, include_asset_info),
        inService=cim.in_service,
        normallyInService=cim.normally_in_service,
        equipmentContainerMRIDs=[str(io.mrid) for io in cim.containers],
        usagePointMRIDs=[str(io.mrid) for io in cim.usage_points],
        operationalRestrictionMRIDs=[str(io.mrid) for io in cim.operational_restrictions],
        currentContainerMRIDs=[str(io.mrid) for io in cim.current_containers],
        commissionedDate=ts,
    )


def equipment_container_to_pb(cim: EquipmentContainer) -> PBEquipmentContainer:
    return PBEquipmentContainer(cnc=connectivity_node_container_to_pb(cim))


@bind_to_pb
def feeder_to_pb(cim: Feeder) -> PBFeeder:
    return PBFeeder(
        ec=equipment_container_to_pb(cim),
        normalHeadTerminalMRID=mrid_or_empty(cim.normal_head_terminal),
        normalEnergizingSubstationMRID=mrid_or_empty(cim.normal_energizing_substation),
        normalEnergizedLvFeederMRIDs=[str(io.mrid) for io in cim.normal_energized_lv_feeders],
        currentlyEnergizedLvFeedersMRIDs=[str(io.mrid) for io in cim.current_energized_lv_feeders]
    )


@bind_to_pb
def geographical_region_to_pb(cim: GeographicalRegion) -> PBGeographicalRegion:
    return PBGeographicalRegion(
        io=identified_object_to_pb(cim),
        subGeographicalRegionMRIDs=[str(io.mrid) for io in cim.sub_geographical_regions]
    )


def power_system_resource_to_pb(cim: PowerSystemResource, include_asset_info: bool = False) -> PBPowerSystemResource:
    return PBPowerSystemResource(
        io=identified_object_to_pb(cim),
        assetInfoMRID=mrid_or_empty(cim.asset_info) if include_asset_info else None,
        locationMRID=mrid_or_empty(cim.location),
        assetMRIDs=[str(io.mrid) for io in cim.assets]
    )


@bind_to_pb
def sub_geographical_region_to_pb(cim: SubGeographicalRegion) -> PBSubGeographicalRegion:
    return PBSubGeographicalRegion(
        io=identified_object_to_pb(cim),
        geographicalRegionMRID=mrid_or_empty(cim.geographical_region),
        substationMRIDs=[str(io.mrid) for io in cim.substations]
    )


@bind_to_pb
def substation_to_pb(cim: Substation) -> PBSubstation:
    return PBSubstation(
        ec=equipment_container_to_pb(cim),
        subGeographicalRegionMRID=mrid_or_empty(cim.sub_geographical_region),
        normalEnergizedFeederMRIDs=[str(io.mrid) for io in cim.feeders],
        loopMRIDs=[str(io.mrid) for io in cim.loops],
        normalEnergizedLoopMRIDs=[str(io.mrid) for io in cim.energized_loops],
        circuitMRIDs=[str(io.mrid) for io in cim.circuits]
    )


@bind_to_pb
def terminal_to_pb(cim: Terminal) -> PBTerminal:
    # noinspection PyProtectedMember
    return PBTerminal(
        ad=ac_dc_terminal_to_pb(cim),
        conductingEquipmentMRID=mrid_or_empty(cim.conducting_equipment),
        connectivityNodeMRID=mrid_or_empty(cim.connectivity_node),
        phases=_map_phase_code.to_pb(cim.phases),
        sequenceNumber=cim.sequence_number,
        normalFeederDirection=_map_feeder_direction.to_pb(cim.normal_feeder_direction),
        currentFeederDirection=_map_feeder_direction.to_pb(cim.current_feeder_direction),
        # phases=cim.pha
    )


#############################
# IEC61970 Base Equivalents #
#############################

@bind_to_pb
def equivalent_branch_to_pb(cim: EquivalentBranch) -> PBEquivalentBranch:
    return PBEquivalentBranch(
        ee=equivalent_equipment_to_pb(cim),
        **set_or_null(
            negativeR12=cim.negative_r12,
            negativeR21=cim.negative_r21,
            negativeX12=cim.negative_x12,
            negativeX21=cim.negative_x21,
            positiveR12=cim.positive_r12,
            positiveR21=cim.positive_r21,
            positiveX12=cim.positive_x12,
            positiveX21=cim.positive_x21,
            r=cim.r,
            r21=cim.r21,
            x=cim.x,
            x21=cim.x21,
            zeroR12=cim.zero_r12,
            zeroR21=cim.zero_r21,
            zeroX12=cim.zero_x12,
            zeroX21=cim.zero_x21,
        )
    )


def equivalent_equipment_to_pb(cim: EquivalentEquipment) -> PBEquivalentEquipment:
    return PBEquivalentEquipment(ce=conducting_equipment_to_pb(cim))


#######################################
# IEC61970 Base Generation Production #
#######################################

@bind_to_pb
def battery_unit_to_pb(cim: BatteryUnit) -> PBBatteryUnit:
    """
    Convert the :class:`BatteryUnit` into its protobuf counterpart.
    :param cim: The :class:`BatteryUnit` to convert.
    :return: The protobuf builder.
    """
    return PBBatteryUnit(
        peu=power_electronics_unit_to_pb(cim),
        batteryControlMRIDs=[str(io.mrid) for io in cim.controls],
        batteryState=_map_battery_state_kind.to_pb(cim.battery_state),
        **set_or_null(
            ratedE=cim.rated_e,
            storedE=cim.stored_e,
        )
    )


@bind_to_pb
def photo_voltaic_unit_to_pb(cim: PhotoVoltaicUnit) -> PBPhotoVoltaicUnit:
    return PBPhotoVoltaicUnit(peu=power_electronics_unit_to_pb(cim))


def power_electronics_unit_to_pb(cim: PowerElectronicsUnit) -> PBPowerElectronicsUnit:
    return PBPowerElectronicsUnit(
        eq=equipment_to_pb(cim),
        powerElectronicsConnectionMRID=mrid_or_empty(cim.power_electronics_connection),
        **set_or_null(
            maxP=cim.max_p,
            minP=cim.min_p,
        )
    )


@bind_to_pb
def power_electronics_wind_unit_to_pb(cim: PowerElectronicsWindUnit) -> PBPowerElectronicsWindUnit:
    return PBPowerElectronicsWindUnit(peu=power_electronics_unit_to_pb(cim))


######################
# IEC61970 Base Meas #
######################

@bind_to_pb
def accumulator_to_pb(cim: Accumulator) -> PBAccumulator:
    return PBAccumulator(measurement=measurement_to_pb(cim))


@bind_to_pb
def analog_to_pb(cim: Analog) -> PBAnalog:
    return PBAnalog(
        measurement=measurement_to_pb(cim),
        **set_or_null(
            positiveFlowIn=cim.positive_flow_in
        )
    )


@bind_to_pb
def control_to_pb(cim: Control) -> PBControl:
    return PBControl(
        ip=io_point_to_pb(cim),
        remoteControlMRID=mrid_or_empty(cim.remote_control),
        powerSystemResourceMRID=cim.power_system_resource_mrid
    )


@bind_to_pb
def discrete_to_pb(cim: Discrete) -> PBDiscrete:
    return PBDiscrete(measurement=measurement_to_pb(cim))


def io_point_to_pb(cim: IoPoint) -> PBIoPoint:
    return PBIoPoint(io=identified_object_to_pb(cim))


def measurement_to_pb(cim: Measurement) -> PBMeasurement:
    return PBMeasurement(
        io=identified_object_to_pb(cim),
        remoteSourceMRID=mrid_or_empty(cim.remote_source),
        powerSystemResourceMRID=cim.power_system_resource_mrid,
        terminalMRID=cim.terminal_mrid,
        phases=_map_phase_code.to_pb(cim.phases),
        unitSymbol=_map_unit_symbol.to_pb(cim.unit_symbol)
    )


############################
# IEC61970 Base Protection #
############################

@bind_to_pb
def current_relay_to_pb(cim: CurrentRelay) -> PBCurrentRelay:
    return PBCurrentRelay(
        prf=protection_relay_function_to_pb(cim, True),
        **set_or_null(
            currentLimit1=cim.current_limit_1,
            inverseTimeFlag=cim.inverse_time_flag,
            timeDelay1=cim.time_delay_1,
        )
    )


#######################
# IEC61970 Base Scada #
#######################

@bind_to_pb
def remote_control_to_pb(cim: RemoteControl) -> PBRemoteControl:
    return PBRemoteControl(
        rp=remote_point_to_pb(cim),
        controlMRID=mrid_or_empty(cim.control)
    )


def remote_point_to_pb(cim: RemotePoint) -> PBRemotePoint:
    return PBRemotePoint(io=identified_object_to_pb(cim))


@bind_to_pb
def remote_source_to_pb(cim: RemoteSource) -> PBRemoteSource:
    return PBRemoteSource(
        rp=remote_point_to_pb(cim),
        measurementMRID=mrid_or_empty(cim.measurement)
    )


#######################
# IEC61970 Base Wires #
#######################

@bind_to_pb
def ac_line_segment_to_pb(cim: AcLineSegment) -> PBAcLineSegment:
    """
    Convert the :class:`AcLineSegment` into its protobuf counterpart.
    :param cim: The :class:`AcLineSegment` to convert.
    :return: The protobuf builder.
    """
    return PBAcLineSegment(
        cd=conductor_to_pb(cim),
        perLengthImpedanceMRID=mrid_or_empty(cim.per_length_impedance),
        cutMRIDs=[str(it.mrid) for it in cim.cuts],
        clampMRIDs=[str(it.mrid) for it in cim.clamps]
    )


@bind_to_pb
def breaker_to_pb(cim: Breaker) -> PBBreaker:
    return PBBreaker(
        sw=protected_switch_to_pb(cim),
        **set_or_null(
            inTransitTime=cim.in_transit_time,
        )
    )


@bind_to_pb
def busbar_section_to_pb(cim: BusbarSection) -> PBBusbarSection:
    return PBBusbarSection(cn=connector_to_pb(cim))


@bind_to_pb
def clamp_to_pb(cim: Clamp) -> PBClamp:
    return PBClamp(
        ce=conducting_equipment_to_pb(cim),
        acLineSegmentMRID=mrid_or_empty(cim.ac_line_segment),
        **set_or_null(
            lengthFromTerminal1=cim.length_from_terminal_1,
        )
    )


def conductor_to_pb(cim: Conductor) -> PBConductor:
    return PBConductor(
        ce=conducting_equipment_to_pb(cim, True),
        **set_or_null(
            length=cim.length,
            designTemperature=cim.design_temperature,
            designRating=cim.design_rating,
        )
    )


def connector_to_pb(cim: Connector) -> PBConnector:
    return PBConnector(ce=conducting_equipment_to_pb(cim))


@bind_to_pb
def cut_to_pb(cim: Cut) -> PBCut:
    return PBCut(
        sw=switch_to_pb(cim),
        acLineSegmentMRID=mrid_or_empty(cim.ac_line_segment),
        **set_or_null(
            lengthFromTerminal1=cim.length_from_terminal_1,
        )
    )


@bind_to_pb
def disconnector_to_pb(cim: Disconnector) -> PBDisconnector:
    return PBDisconnector(sw=switch_to_pb(cim))


def earth_fault_compensator_to_pb(cim: EarthFaultCompensator) -> PBEarthFaultCompensator:
    return PBEarthFaultCompensator(
        ce=conducting_equipment_to_pb(cim),
        **set_or_null(
            r=cim.r
        )
    )


def energy_connection_to_pb(cim: EnergyConnection, include_asset_info=False) -> PBEnergyConnection:
    return PBEnergyConnection(ce=conducting_equipment_to_pb(cim, include_asset_info))


@bind_to_pb
def energy_consumer_to_pb(cim: EnergyConsumer) -> PBEnergyConsumer:
    return PBEnergyConsumer(
        ec=energy_connection_to_pb(cim),
        energyConsumerPhasesMRIDs=[str(io.mrid) for io in cim.phases],
        phaseConnection=_map_phase_shunt_connection_kind.to_pb(cim.phase_connection),
        **set_or_null(
            p=cim.p,
            pFixed=cim.p_fixed,
            q=cim.q,
            qFixed=cim.q_fixed,
            customerCount=cim.customer_count,
            grounded=cim.grounded,
        )
    )


@bind_to_pb
def energy_consumer_phase_to_pb(cim: EnergyConsumerPhase) -> PBEnergyConsumerPhase:
    return PBEnergyConsumerPhase(
        psr=power_system_resource_to_pb(cim),
        energyConsumerMRID=mrid_or_empty(cim.energy_consumer),
        phase=_map_single_phase_kind.to_pb(cim.phase),
        **set_or_null(
            p=cim.p,
            pFixed=cim.p_fixed,
            q=cim.q,
            qFixed=cim.q_fixed,
        )
    )


@bind_to_pb
def energy_source_to_pb(cim: EnergySource) -> PBEnergySource:
    return PBEnergySource(
        ec=energy_connection_to_pb(cim),
        energySourcePhasesMRIDs=[str(io.mrid) for io in cim.phases],
        **set_or_null(
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
            xn=cim.xn,
            isExternalGrid=cim.is_external_grid,
            rMin=cim.r_min,
            rnMin=cim.rn_min,
            r0Min=cim.r0_min,
            xMin=cim.x_min,
            xnMin=cim.xn_min,
            x0Min=cim.x0_min,
            rMax=cim.r_max,
            rnMax=cim.rn_max,
            r0Max=cim.r0_max,
            xMax=cim.x_max,
            xnMax=cim.xn_max,
            x0Max=cim.x0_max,
        )
    )


@bind_to_pb
def energy_source_phase_to_pb(cim: EnergySourcePhase) -> PBEnergySourcePhase:
    return PBEnergySourcePhase(
        psr=power_system_resource_to_pb(cim),
        energySourceMRID=mrid_or_empty(cim.energy_source),
        phase=_map_single_phase_kind.to_pb(cim.phase)
    )


@bind_to_pb
def fuse_to_pb(cim: Fuse) -> PBFuse:
    return PBFuse(
        sw=switch_to_pb(cim),
        functionMRID=mrid_or_empty(cim.function)
    )


@bind_to_pb
def ground_to_pb(cim: Ground) -> PBGround:
    return PBGround(
        ce=conducting_equipment_to_pb(cim, True)
    )


@bind_to_pb
def ground_disconnector_to_pb(cim: GroundDisconnector) -> PBGroundDisconnector:
    return PBGroundDisconnector(
        sw=switch_to_pb(cim)
    )


@bind_to_pb
def grounding_impedance_to_pb(cim: GroundingImpedance) -> PBGroundingImpedance:
    return PBGroundingImpedance(
        efc=earth_fault_compensator_to_pb(cim),
        **set_or_null(
            x=cim.x,
        )
    )


@bind_to_pb
def jumper_to_pb(cim: Jumper) -> PBJumper:
    return PBJumper(sw=switch_to_pb(cim))


@bind_to_pb
def junction_to_pb(cim: Junction) -> PBJunction:
    return PBJunction(cn=connector_to_pb(cim))


def line_to_pb(cim: Line) -> PBLine:
    return PBLine(ec=equipment_container_to_pb(cim))


@bind_to_pb
def linear_shunt_compensator_to_pb(cim: LinearShuntCompensator) -> PBLinearShuntCompensator:
    return PBLinearShuntCompensator(
        sc=shunt_compensator_to_pb(cim),
        **set_or_null(
            b0PerSection=cim.b0_per_section,
            bPerSection=cim.b_per_section,
            g0PerSection=cim.g0_per_section,
            gPerSection=cim.g_per_section,
        )
    )


@bind_to_pb
def load_break_switch_to_pb(cim: LoadBreakSwitch) -> PBLoadBreakSwitch:
    return PBLoadBreakSwitch(ps=protected_switch_to_pb(cim))


def per_length_impedance_to_pb(cim: PerLengthImpedance) -> PBPerLengthImpedance:
    return PBPerLengthImpedance(lp=per_length_line_parameter_to_pb(cim))


def per_length_line_parameter_to_pb(cim: PerLengthLineParameter) -> PBPerLengthLineParameter:
    return PBPerLengthLineParameter(io=identified_object_to_pb(cim))


@bind_to_pb
def per_length_phase_impedance_to_pb(cim: PerLengthPhaseImpedance) -> PBPerLengthPhaseImpedance:
    """
    Convert the :class:`PerLengthPhaseImpedance` into its protobuf counterpart.
    :param cim: The :class:`PerLengthPhaseImpedance` to convert.
    :return: The protobuf builder.
    """
    return PBPerLengthPhaseImpedance(
        pli=per_length_impedance_to_pb(cim),
        phaseImpedanceData=[phase_impedance_data_to_pb(it) for it in cim.data]
    )


@bind_to_pb
def per_length_sequence_impedance_to_pb(cim: PerLengthSequenceImpedance) -> PBPerLengthSequenceImpedance:
    return PBPerLengthSequenceImpedance(
        pli=per_length_impedance_to_pb(cim),
        **set_or_null(
            r=cim.r,
            x=cim.x,
            r0=cim.r0,
            x0=cim.x0,
            bch=cim.bch,
            gch=cim.gch,
            b0ch=cim.b0ch,
            g0ch=cim.g0ch,
        )
    )


@bind_to_pb
def petersen_coil_to_pb(cim: PetersenCoil) -> PBPetersenCoil:
    return PBPetersenCoil(
        efc=earth_fault_compensator_to_pb(cim),
        **set_or_null(
            xGroundNominal=cim.x_ground_nominal
        )
    )


def phase_impedance_data_to_pb(cim: PhaseImpedanceData) -> PBPhaseImpedanceData:
    """
    Convert the :class:`PhaseImpedanceData` into its protobuf counterpart.
    :param cim: The :class:`PhaseImpedanceData` to convert.
    :return: The protobuf builder.
    """
    return PBPhaseImpedanceData(
        fromPhase=_map_single_phase_kind.to_pb(cim.from_phase),
        toPhase=_map_single_phase_kind.to_pb(cim.to_phase),
        **set_or_null(
            b=cim.b,
            g=cim.g,
            r=cim.r,
            x=cim.x,
        )
    )


@bind_to_pb
def power_electronics_connection_to_pb(cim: PowerElectronicsConnection) -> PBPowerElectronicsConnection:
    return PBPowerElectronicsConnection(
        rce=regulating_cond_eq_to_pb(cim),
        powerElectronicsUnitMRIDs=[str(io.mrid) for io in cim.units],
        powerElectronicsConnectionPhaseMRIDs=[str(io.mrid) for io in cim.phases],
        **set_or_null(
            maxIFault=cim.max_i_fault,
            maxQ=cim.max_q,
            minQ=cim.min_q,
            p=cim.p,
            q=cim.q,
            ratedS=cim.rated_s,
            ratedU=cim.rated_u,
            inverterStandard=cim.inverter_standard,
            sustainOpOvervoltLimit=cim.sustain_op_overvolt_limit,
            stopAtOverFreq=cim.stop_at_over_freq,
            stopAtUnderFreq=cim.stop_at_under_freq,
            invVoltWattRespMode=cim.inv_volt_watt_resp_mode,
            invWattRespV1=cim.inv_watt_resp_v1,
            invWattRespV2=cim.inv_watt_resp_v2,
            invWattRespV3=cim.inv_watt_resp_v3,
            invWattRespV4=cim.inv_watt_resp_v4,
            invWattRespPAtV1=cim.inv_watt_resp_p_at_v1,
            invWattRespPAtV2=cim.inv_watt_resp_p_at_v2,
            invWattRespPAtV3=cim.inv_watt_resp_p_at_v3,
            invWattRespPAtV4=cim.inv_watt_resp_p_at_v4,
            invVoltVarRespMode=cim.inv_volt_var_resp_mode,
            invVarRespV1=cim.inv_var_resp_v1,
            invVarRespV2=cim.inv_var_resp_v2,
            invVarRespV3=cim.inv_var_resp_v3,
            invVarRespV4=cim.inv_var_resp_v4,
            invVarRespQAtV1=cim.inv_var_resp_q_at_v1,
            invVarRespQAtV2=cim.inv_var_resp_q_at_v2,
            invVarRespQAtV3=cim.inv_var_resp_q_at_v3,
            invVarRespQAtV4=cim.inv_var_resp_q_at_v4,
            invReactivePowerMode=cim.inv_reactive_power_mode,
            invFixReactivePower=cim.inv_fix_reactive_power,
        )
    )


@bind_to_pb
def power_electronics_connection_phase_to_pb(cim: PowerElectronicsConnectionPhase) -> PBPowerElectronicsConnectionPhase:
    return PBPowerElectronicsConnectionPhase(
        psr=power_system_resource_to_pb(cim),
        powerElectronicsConnectionMRID=mrid_or_empty(cim.power_electronics_connection),
        phase=_map_single_phase_kind.to_pb(cim.phase),
        **set_or_null(
            p=cim.p,
            q=cim.q,
        )
    )


@bind_to_pb
def power_transformer_to_pb(cim: PowerTransformer) -> PBPowerTransformer:
    return PBPowerTransformer(
        ce=conducting_equipment_to_pb(cim, True),
        powerTransformerEndMRIDs=[str(io.mrid) for io in cim.ends],
        vectorGroup=_map_vector_group.to_pb(cim.vector_group),
        constructionKind=_map_transformer_construction_kind.to_pb(cim.construction_kind),
        function=_map_transformer_function_kind.to_pb(cim.function),
        **set_or_null(
            transformerUtilisation=cim.transformer_utilisation,
        )
    )


@bind_to_pb
def power_transformer_end_to_pb(cim: PowerTransformerEnd) -> PBPowerTransformerEnd:
    return PBPowerTransformerEnd(
        te=transformer_end_to_pb(cim),
        powerTransformerMRID=mrid_or_empty(cim.power_transformer),
        connectionKind=_map_winding_connection.to_pb(cim.connection_kind),
        ratings=[transformer_end_rated_s_to_pb(it) for it in cim.s_ratings],
        **set_or_null(
            ratedS=cim.rated_s,
            ratedU=cim.rated_u,
            r=cim.r,
            r0=cim.r0,
            x=cim.x,
            x0=cim.x0,
            b=cim.b,
            b0=cim.b0,
            g=cim.g,
            g0=cim.g0,
            phaseAngleClock=cim.phase_angle_clock,
        )
    )


def protected_switch_to_pb(cim: ProtectedSwitch) -> PBProtectedSwitch:
    return PBProtectedSwitch(
        sw=switch_to_pb(cim),
        relayFunctionMRIDs=[str(io.mrid) for io in cim.relay_functions],
        **set_or_null(
            breakingCapacity=cim.breaking_capacity,
        )
    )


@bind_to_pb
def ratio_tap_changer_to_pb(cim: RatioTapChanger) -> PBRatioTapChanger:
    return PBRatioTapChanger(
        tc=tap_changer_to_pb(cim),
        transformerEndMRID=mrid_or_empty(cim.transformer_end),
        **set_or_null(
            stepVoltageIncrement=cim.step_voltage_increment,
        )
    )


@bind_to_pb
def reactive_capability_curve_to_pb(cim: ReactiveCapabilityCurve) -> PBReactiveCapabilityCurve:
    return PBReactiveCapabilityCurve(c=curve_to_pb(cim))


@bind_to_pb
def recloser_to_pb(cim: Recloser) -> PBRecloser:
    return PBRecloser(sw=protected_switch_to_pb(cim))


def regulating_cond_eq_to_pb(cim: RegulatingCondEq, include_asset_info=False) -> PBRegulatingCondEq:
    return PBRegulatingCondEq(
        ec=energy_connection_to_pb(cim, include_asset_info),
        regulatingControlMRID=mrid_or_empty(cim.regulating_control),
        **set_or_null(
            controlEnabled=cim.control_enabled,
        )
    )


def regulating_control_to_pb(cim: RegulatingControl) -> PBRegulatingControl:
    """
    Convert the :class:`RegulatingControl` into its protobuf counterpart.
    :param cim: The :class:`RegulatingControl` to convert.
    :return: The protobuf builder.
    """
    return PBRegulatingControl(
        psr=power_system_resource_to_pb(cim),
        mode=_map_regulating_control_mode_kind.to_pb(cim.mode),
        monitoredPhase=_map_phase_code.to_pb(cim.monitored_phase),
        terminalMRID=mrid_or_empty(cim.terminal),
        regulatingCondEqMRIDs=[str(io.mrid) for io in cim.regulating_conducting_equipment],
        **set_or_null(
            discrete=cim.discrete,
            targetDeadband=cim.target_deadband,
            targetValue=cim.target_value,
            enabled=cim.enabled,
            maxAllowedTargetValue=cim.max_allowed_target_value,
            minAllowedTargetValue=cim.min_allowed_target_value,
            ratedCurrent=cim.rated_current,
            ctPrimary=cim.ct_primary,
            minTargetDeadband=cim.min_target_deadband,
        )
    )


def rotating_machine_to_pb(cim: RotatingMachine) -> PBRotatingMachine:
    return PBRotatingMachine(
        rce=regulating_cond_eq_to_pb(cim, True),
        **set_or_null(
            ratedPowerFactor=cim.rated_power_factor,
            ratedS=cim.rated_s,
            ratedU=cim.rated_u,
            p=cim.p,
            q=cim.q,
        )
    )


@bind_to_pb
def series_compensator_to_pb(cim: SeriesCompensator) -> PBSeriesCompensator:
    return PBSeriesCompensator(
        ce=conducting_equipment_to_pb(cim, True),
        **set_or_null(
            r=cim.r,
            r0=cim.r0,
            x=cim.x,
            x0=cim.x0,
            varistorRatedCurrent=cim.varistor_rated_current,
            varistorVoltageThreshold=cim.varistor_voltage_threshold,
        )
    )


def shunt_compensator_to_pb(cim: ShuntCompensator) -> PBShuntCompensator:
    return PBShuntCompensator(
        rce=regulating_cond_eq_to_pb(cim, True),
        phaseConnection=_map_phase_shunt_connection_kind.to_pb(cim.phase_connection),
        **set_or_null(
            sections=cim.sections,
            grounded=cim.grounded,
            nomU=cim.nom_u,
        )
    )


@bind_to_pb
def static_var_compensator_to_pb(cim: StaticVarCompensator) -> PBStaticVarCompensator:
    """
    Convert the :class:`StaticVarCompensator` into its protobuf counterpart.
    :param cim: The :class:`StaticVarCompensator` to convert.
    :return: The protobuf builder.
    """
    return PBStaticVarCompensator(
        rce=regulating_cond_eq_to_pb(cim),
        svcControlMode=_map_svc_control_mode.to_pb(cim.svc_control_mode),
        **set_or_null(
            capacitiveRating=cim.capacitive_rating,
            inductiveRating=cim.inductive_rating,
            q=cim.q,
            voltageSetPoint=cim.voltage_set_point,
        )
    )


def switch_to_pb(cim: Switch) -> PBSwitch:
    return PBSwitch(
        ce=conducting_equipment_to_pb(cim, True),
        normalOpen=cim.get_normal_state() != 0,
        open=cim.get_state() != 0,
        **set_or_null(
            ratedCurrent=cim.rated_current,
        )
    )


@bind_to_pb
def synchronous_machine_to_pb(cim: SynchronousMachine) -> PBSynchronousMachine:
    return PBSynchronousMachine(
        rm=rotating_machine_to_pb(cim),

        reactiveCapabilityCurveMRIDs=[str(it.mrid) for it in cim.curves],
        type=_map_synchronous_machine_kind.to_pb(cim.type),
        operatingMode=_map_synchronous_machine_kind.to_pb(cim.operating_mode),
        **set_or_null(
            baseQ=cim.base_q,
            condenserP=cim.condenser_p,
            earthing=cim.earthing,
            earthingStarPointR=cim.earthing_star_point_r,
            earthingStarPointX=cim.earthing_star_point_x,
            ikk=cim.ikk,
            maxQ=cim.max_q,
            maxU=cim.max_u,
            minQ=cim.min_q,
            minU=cim.min_u,
            mu=cim.mu,
            r=cim.r,
            r0=cim.r0,
            r2=cim.r2,
            satDirectSubtransX=cim.sat_direct_subtrans_x,
            satDirectSyncX=cim.sat_direct_sync_x,
            satDirectTransX=cim.sat_direct_trans_x,
            x0=cim.x0,
            x2=cim.x2,
        )
    )


def tap_changer_to_pb(cim: TapChanger) -> PBTapChanger:
    return PBTapChanger(
        psr=power_system_resource_to_pb(cim),
        tapChangerControlMRID=mrid_or_empty(cim.tap_changer_control),
        **set_or_null(
            highStep=cim.high_step,
            lowStep=cim.low_step,
            step=cim.step,
            neutralStep=cim.neutral_step,
            neutralU=cim.neutral_u,
            normalStep=cim.normal_step,
            controlEnabled=cim.control_enabled,
        )
    )


@bind_to_pb
def tap_changer_control_to_pb(cim: TapChangerControl) -> PBTapChangerControl:
    return PBTapChangerControl(
        rc=regulating_control_to_pb(cim),
        **set_or_null(
            limitVoltage=cim.limit_voltage,
            lineDropCompensation=cim.line_drop_compensation,
            lineDropR=cim.line_drop_r,
            lineDropX=cim.line_drop_x,
            reverseLineDropR=cim.reverse_line_drop_r,
            reverseLineDropX=cim.reverse_line_drop_x,
            forwardLDCBlocking=cim.forward_ldc_blocking,
            timeDelay=cim.time_delay,
            coGenerationEnabled=cim.co_generation_enabled
        )
    )


def transformer_end_to_pb(cim: TransformerEnd) -> PBTransformerEnd:
    return PBTransformerEnd(
        io=identified_object_to_pb(cim),
        terminalMRID=mrid_or_empty(cim.terminal),
        baseVoltageMRID=mrid_or_empty(cim.base_voltage),
        ratioTapChangerMRID=mrid_or_empty(cim.ratio_tap_changer),
        starImpedanceMRID=mrid_or_empty(cim.star_impedance),
        endNumber=cim.end_number,
        **set_or_null(
            grounded=cim.grounded,
            rGround=cim.r_ground,
            xGround=cim.x_ground,
        )
    )


def transformer_end_rated_s_to_pb(cim: TransformerEndRatedS) -> PBTransformerEndRatedS:
    return PBTransformerEndRatedS(
        coolingType=_map_transformer_cooling_type.to_pb(cim.cooling_type),
        ratedS=cim.rated_s,
    )


@bind_to_pb
def transformer_star_impedance_to_pb(cim: TransformerStarImpedance) -> PBTransformerStarImpedance:
    return PBTransformerStarImpedance(
        io=identified_object_to_pb(cim),
        transformerEndInfoMRID=mrid_or_empty(cim.transformer_end_info),
        **set_or_null(
            r=cim.r,
            r0=cim.r0,
            x=cim.x,
            x0=cim.x0
        )
    )


###############################
# IEC61970 InfIEC61970 Feeder #
###############################


@bind_to_pb
def circuit_to_pb(cim: Circuit) -> PBCircuit:
    return PBCircuit(
        l=line_to_pb(cim),
        loopMRID=mrid_or_empty(cim.loop),
        endTerminalMRIDs=[str(io.mrid) for io in cim.end_terminals],
        endSubstationMRIDs=[str(io.mrid) for io in cim.end_substations]
    )
