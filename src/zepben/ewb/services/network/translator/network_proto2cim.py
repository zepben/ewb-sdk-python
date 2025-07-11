#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = [
    "cable_info_to_cim", "no_load_test_to_cim", "open_circuit_test_to_cim", "overhead_wire_info_to_cim", "power_transformer_info_to_cim",
    "short_circuit_test_to_cim", "shunt_compensator_info_to_cim", "switch_info_to_cim", "transformer_end_info_to_cim", "transformer_tank_info_to_cim",
    "transformer_test_to_cim", "wire_info_to_cim", "asset_to_cim", "asset_container_to_cim", "asset_info_to_cim", "asset_organisation_role_to_cim",
    "asset_owner_to_cim", "pole_to_cim", "streetlight_to_cim", "structure_to_cim", "location_to_cim", "position_point_to_cim", "street_address_to_cim",
    "street_detail_to_cim", "town_detail_to_cim", "relay_info_to_cim", "current_transformer_info_to_cim", "potential_transformer_info_to_cim",
    "ratio_to_cim", "end_device_to_cim", "meter_to_cim", "usage_point_to_cim", "operational_restriction_to_cim", "auxiliary_equipment_to_cim",
    "current_transformer_to_cim", "fault_indicator_to_cim", "potential_transformer_to_cim", "sensor_to_cim", "ac_dc_terminal_to_cim", "base_voltage_to_cim",
    "conducting_equipment_to_cim", "connectivity_node_to_cim", "connectivity_node_container_to_cim", "equipment_to_cim", "equipment_container_to_cim",
    "feeder_to_cim", "geographical_region_to_cim", "power_system_resource_to_cim", "site_to_cim", "sub_geographical_region_to_cim", "substation_to_cim",
    "terminal_to_cim", "equivalent_branch_to_cim", "equivalent_equipment_to_cim", "accumulator_to_cim", "analog_to_cim", "control_to_cim", "discrete_to_cim",
    "io_point_to_cim", "measurement_to_cim", "current_relay_to_cim", "protection_relay_function_to_cim", "remote_control_to_cim", "remote_point_to_cim",
    "remote_source_to_cim", "battery_unit_to_cim", "photo_voltaic_unit_to_cim", "power_electronics_unit_to_cim", "power_electronics_wind_unit_to_cim",
    "ac_line_segment_to_cim", "breaker_to_cim", "conductor_to_cim", "connector_to_cim", "disconnector_to_cim", "energy_connection_to_cim",
    "energy_consumer_to_cim", "energy_consumer_phase_to_cim", "energy_source_to_cim", "energy_source_phase_to_cim", "fuse_to_cim", "jumper_to_cim",
    "junction_to_cim", "busbar_section_to_cim", "line_to_cim", "linear_shunt_compensator_to_cim", "load_break_switch_to_cim",
    "per_length_line_parameter_to_cim", "per_length_impedance_to_cim", "per_length_sequence_impedance_to_cim", "power_electronics_connection_to_cim",
    "power_electronics_connection_phase_to_cim", "power_transformer_to_cim", "power_transformer_end_to_cim", "transformer_star_impedance_to_cim",
    "protected_switch_to_cim", "ratio_tap_changer_to_cim", "recloser_to_cim", "regulating_cond_eq_to_cim", "shunt_compensator_to_cim", "switch_to_cim",
    "tap_changer_to_cim", "transformer_end_to_cim", "circuit_to_cim", "loop_to_cim", "lv_feeder_to_cim", "ev_charging_unit_to_cim",
    "transformer_end_rated_s_to_cim", "tap_changer_control_to_cim", "regulating_control_to_cim", "distance_relay_to_cim", "protection_relay_scheme_to_cim",
    "protection_relay_system_to_cim", "relay_setting_to_cim", "voltage_relay_to_cim", "ground_to_cim", "ground_disconnector_to_cim",
    "series_compensator_to_cim", "pan_demand_response_function_to_cim", 'battery_control_to_cim', "asset_function_to_cim", "end_device_function_to_cim",
    "static_var_compensator_to_cim", "clamp_to_cim", "cut_to_cim"
]

from typing import Optional

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

import zepben.ewb.services.common.resolver as resolver
from zepben.ewb.model.cim.extensions.iec61968.assetinfo.relay_info import *
from zepben.ewb.model.cim.extensions.iec61968.metering.pan_demand_reponse_function import PanDemandResponseFunction
from zepben.ewb.model.cim.extensions.iec61970.base.core.site import *
from zepben.ewb.model.cim.extensions.iec61970.base.feeder.loop import *
from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_feeder import *
from zepben.ewb.model.cim.extensions.iec61970.base.generation.production.ev_charging_unit import *
from zepben.ewb.model.cim.extensions.iec61970.base.protection.distance_relay import *
from zepben.ewb.model.cim.extensions.iec61970.base.protection.power_direction_kind import *
from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_kind import *
from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_function import *
from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_scheme import *
from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_system import *
from zepben.ewb.model.cim.extensions.iec61970.base.protection.relay_setting import *
from zepben.ewb.model.cim.extensions.iec61970.base.protection.voltage_relay import *
from zepben.ewb.model.cim.extensions.iec61970.base.wires.battery_control import BatteryControl
from zepben.ewb.model.cim.extensions.iec61970.base.wires.battery_control_mode import BatteryControlMode
from zepben.ewb.model.cim.extensions.iec61970.base.wires.transformer_cooling_type import *
from zepben.ewb.model.cim.extensions.iec61970.base.wires.transformer_end_rated_s import TransformerEndRatedS
from zepben.ewb.model.cim.extensions.iec61970.base.wires.vector_group import *
from zepben.ewb.model.cim.iec61968.assetinfo.cable_info import CableInfo
from zepben.ewb.model.cim.iec61968.assetinfo.no_load_test import *
from zepben.ewb.model.cim.iec61968.assetinfo.open_circuit_test import *
from zepben.ewb.model.cim.iec61968.assetinfo.overhead_wire_info import OverheadWireInfo
from zepben.ewb.model.cim.iec61968.assetinfo.power_transformer_info import *
from zepben.ewb.model.cim.iec61968.assetinfo.short_circuit_test import *
from zepben.ewb.model.cim.iec61968.assetinfo.shunt_compensator_info import *
from zepben.ewb.model.cim.iec61968.assetinfo.switch_info import *
from zepben.ewb.model.cim.iec61968.assetinfo.transformer_end_info import *
from zepben.ewb.model.cim.iec61968.assetinfo.transformer_tank_info import *
from zepben.ewb.model.cim.iec61968.assetinfo.transformer_test import *
from zepben.ewb.model.cim.iec61968.assetinfo.wire_info import *
from zepben.ewb.model.cim.iec61968.assetinfo.wire_material_kind import *
from zepben.ewb.model.cim.iec61968.assets.asset import *
from zepben.ewb.model.cim.iec61968.assets.asset_container import *
from zepben.ewb.model.cim.iec61968.assets.asset_function import AssetFunction
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
from zepben.ewb.model.cim.iec61968.infiec61968.infassetinfo.transformer_construction_kind import *
from zepben.ewb.model.cim.iec61968.infiec61968.infassetinfo.transformer_function_kind import *
from zepben.ewb.model.cim.iec61968.infiec61968.infassets.pole import *
from zepben.ewb.model.cim.iec61968.infiec61968.infassets.streetlight_lamp_kind import StreetlightLampKind
from zepben.ewb.model.cim.iec61968.infiec61968.infcommon.ratio import *
from zepben.ewb.model.cim.iec61968.metering.end_device import *
from zepben.ewb.model.cim.iec61968.metering.end_device_function import *
from zepben.ewb.model.cim.iec61968.metering.end_device_function_kind import *
from zepben.ewb.model.cim.iec61968.metering.meter import *
from zepben.ewb.model.cim.iec61968.metering.usage_point import *
from zepben.ewb.model.cim.iec61968.operations.operational_restriction import *
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.auxiliary_equipment import *
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.current_transformer import *
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.fault_indicator import *
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.potential_transformer import *
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.potential_transformer_kind import *
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.sensor import *
from zepben.ewb.model.cim.iec61970.base.core.ac_dc_terminal import AcDcTerminal
from zepben.ewb.model.cim.iec61970.base.core.base_voltage import *
from zepben.ewb.model.cim.iec61970.base.core.conducting_equipment import *
from zepben.ewb.model.cim.iec61970.base.core.connectivity_node import *
from zepben.ewb.model.cim.iec61970.base.core.connectivity_node_container import *
from zepben.ewb.model.cim.iec61970.base.core.curve import Curve
from zepben.ewb.model.cim.iec61970.base.core.curve_data import CurveData
from zepben.ewb.model.cim.iec61970.base.core.equipment import *
from zepben.ewb.model.cim.iec61970.base.core.equipment_container import *
from zepben.ewb.model.cim.iec61970.base.core.feeder import *
from zepben.ewb.model.cim.iec61970.base.core.geographical_region import GeographicalRegion
from zepben.ewb.model.cim.iec61970.base.core.phase_code import *
from zepben.ewb.model.cim.iec61970.base.core.power_system_resource import *
from zepben.ewb.model.cim.iec61970.base.core.sub_geographical_region import SubGeographicalRegion
from zepben.ewb.model.cim.iec61970.base.core.substation import *
from zepben.ewb.model.cim.iec61970.base.core.terminal import *
from zepben.ewb.model.cim.iec61970.base.domain.unit_symbol import *
from zepben.ewb.model.cim.iec61970.base.equivalents.equivalent_branch import *
from zepben.ewb.model.cim.iec61970.base.equivalents.equivalent_equipment import *
from zepben.ewb.model.cim.iec61970.base.generation.production.battery_state_kind import *
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
from zepben.ewb.model.cim.iec61970.base.wires.breaker import Breaker
from zepben.ewb.model.cim.iec61970.base.wires.busbar_section import *
from zepben.ewb.model.cim.iec61970.base.wires.clamp import *
from zepben.ewb.model.cim.iec61970.base.wires.conductor import *
from zepben.ewb.model.cim.iec61970.base.wires.connector import *
from zepben.ewb.model.cim.iec61970.base.wires.cut import *
from zepben.ewb.model.cim.iec61970.base.wires.disconnector import Disconnector
from zepben.ewb.model.cim.iec61970.base.wires.earth_fault_compensator import EarthFaultCompensator
from zepben.ewb.model.cim.iec61970.base.wires.energy_connection import *
from zepben.ewb.model.cim.iec61970.base.wires.energy_consumer import *
from zepben.ewb.model.cim.iec61970.base.wires.energy_consumer_phase import *
from zepben.ewb.model.cim.iec61970.base.wires.energy_source import *
from zepben.ewb.model.cim.iec61970.base.wires.energy_source_phase import *
from zepben.ewb.model.cim.iec61970.base.wires.fuse import Fuse
from zepben.ewb.model.cim.iec61970.base.wires.ground import *
from zepben.ewb.model.cim.iec61970.base.wires.ground_disconnector import *
from zepben.ewb.model.cim.iec61970.base.wires.grounding_impedance import GroundingImpedance
from zepben.ewb.model.cim.iec61970.base.wires.jumper import Jumper
from zepben.ewb.model.cim.iec61970.base.wires.junction import *
from zepben.ewb.model.cim.iec61970.base.wires.line import *
from zepben.ewb.model.cim.iec61970.base.wires.linear_shunt_compensator import LinearShuntCompensator
from zepben.ewb.model.cim.iec61970.base.wires.load_break_switch import LoadBreakSwitch
from zepben.ewb.model.cim.iec61970.base.wires.per_length_impedance import PerLengthImpedance
from zepben.ewb.model.cim.iec61970.base.wires.per_length_line_parameter import PerLengthLineParameter
from zepben.ewb.model.cim.iec61970.base.wires.per_length_phase_impedance import *
from zepben.ewb.model.cim.iec61970.base.wires.per_length_sequence_impedance import PerLengthSequenceImpedance
from zepben.ewb.model.cim.iec61970.base.wires.petersen_coil import PetersenCoil
from zepben.ewb.model.cim.iec61970.base.wires.phase_impedance_data import *
from zepben.ewb.model.cim.iec61970.base.wires.phase_shunt_connection_kind import *
from zepben.ewb.model.cim.iec61970.base.wires.power_electronics_connection import *
from zepben.ewb.model.cim.iec61970.base.wires.power_electronics_connection_phase import PowerElectronicsConnectionPhase
from zepben.ewb.model.cim.iec61970.base.wires.power_transformer import *
from zepben.ewb.model.cim.iec61970.base.wires.power_transformer_end import PowerTransformerEnd
from zepben.ewb.model.cim.iec61970.base.wires.protected_switch import ProtectedSwitch
from zepben.ewb.model.cim.iec61970.base.wires.ratio_tap_changer import RatioTapChanger
from zepben.ewb.model.cim.iec61970.base.wires.reactive_capability_curve import ReactiveCapabilityCurve
from zepben.ewb.model.cim.iec61970.base.wires.recloser import Recloser
from zepben.ewb.model.cim.iec61970.base.wires.regulating_cond_eq import *
from zepben.ewb.model.cim.iec61970.base.wires.regulating_control import *
from zepben.ewb.model.cim.iec61970.base.wires.regulating_control_mode_kind import *
from zepben.ewb.model.cim.iec61970.base.wires.rotating_machine import RotatingMachine
from zepben.ewb.model.cim.iec61970.base.wires.series_compensator import *
from zepben.ewb.model.cim.iec61970.base.wires.shunt_compensator import *
from zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind import *
from zepben.ewb.model.cim.iec61970.base.wires.static_var_compensator import StaticVarCompensator
from zepben.ewb.model.cim.iec61970.base.wires.svc_control_mode import SVCControlMode
from zepben.ewb.model.cim.iec61970.base.wires.switch import *
from zepben.ewb.model.cim.iec61970.base.wires.synchronous_machine import SynchronousMachine
from zepben.ewb.model.cim.iec61970.base.wires.synchronous_machine_kind import SynchronousMachineKind
from zepben.ewb.model.cim.iec61970.base.wires.tap_changer import TapChanger
from zepben.ewb.model.cim.iec61970.base.wires.tap_changer_control import *
from zepben.ewb.model.cim.iec61970.base.wires.transformer_end import TransformerEnd
from zepben.ewb.model.cim.iec61970.base.wires.transformer_star_impedance import *
from zepben.ewb.model.cim.iec61970.base.wires.winding_connection import *
from zepben.ewb.model.cim.iec61970.infiec61970.feeder.circuit import *
from zepben.ewb.services.common.translator.base_proto2cim import identified_object_to_cim, organisation_role_to_cim, document_to_cim
from zepben.ewb.services.common.translator.util import int_or_none, float_or_none, long_or_none, str_or_none, uint_or_none
from zepben.ewb.services.network.network_service import NetworkService
from zepben.ewb.services.network.tracing.feeder.feeder_direction import FeederDirection


##################################
# Extensions IEC61968 Asset Info #
##################################

def relay_info_to_cim(pb: PBRelayInfo, network_service: NetworkService) -> Optional[RelayInfo]:
    # noinspection PyUnresolvedReferences
    cim = RelayInfo(
        mrid=pb.mrid(),
        curve_setting=str_or_none(pb.curveSetting),
        reclose_fast=None if pb.HasField("recloseFastNull") else pb.recloseFastSet,
        reclose_delays=list(pb.recloseDelays)
    )

    asset_info_to_cim(pb.ai, cim, network_service)
    return cim if network_service.add(cim) else None


PBRelayInfo.to_cim = relay_info_to_cim


################################
# Extensions IEC61968 Metering #
################################

def pan_demand_response_function_to_cim(pb: PBPanDemandResponseFunction, network_service: NetworkService) -> PanDemandResponseFunction:
    """
    Convert the protobuf :class:`PBPanDemandResponseFunction` into its CIM counterpart.
    :param pb: The protobuf :class:`PBPanDemandResponseFunction` to convert
    :param network_service: The :class:`NetworkService` the converted CIM object will be added to.
    :return: The converted `pb` as a CIM :class:`PanDemandResponseFunction`
    """
    # noinspection PyUnresolvedReferences
    cim = PanDemandResponseFunction(mrid=pb.mrid())
    cim.appliance = int_or_none(pb.appliance)
    cim.kind = EndDeviceFunctionKind(pb.kind)
    end_device_function_to_cim(pb.edf, cim, network_service)

    return cim if network_service.add(cim) else None


PBPanDemandResponseFunction.to_cim = pan_demand_response_function_to_cim


#################################
# Extensions IEC61970 Base Core #
#################################

def site_to_cim(pb: PBSite, network_service: NetworkService) -> Optional[Site]:
    # noinspection PyUnresolvedReferences
    cim = Site(mrid=pb.mrid())

    equipment_container_to_cim(pb.ec, cim, network_service)
    return cim if network_service.add(cim) else None


PBSite.to_cim = site_to_cim


###################################
# Extensions IEC61970 Base Feeder #
###################################

def loop_to_cim(pb: PBLoop, network_service: NetworkService) -> Optional[Loop]:
    # noinspection PyUnresolvedReferences
    cim = Loop(mrid=pb.mrid())

    for mrid in pb.circuitMRIDs:
        network_service.resolve_or_defer_reference(resolver.loop_circuits(cim), mrid)
    for mrid in pb.substationMRIDs:
        network_service.resolve_or_defer_reference(resolver.loop_substations(cim), mrid)
    for mrid in pb.normalEnergizingSubstationMRIDs:
        network_service.resolve_or_defer_reference(resolver.loop_energizing_substations(cim), mrid)

    identified_object_to_cim(pb.io, cim, network_service)
    return cim if network_service.add(cim) else None


def lv_feeder_to_cim(pb: PBLvFeeder, network_service: NetworkService) -> Optional[LvFeeder]:
    # noinspection PyUnresolvedReferences
    cim = LvFeeder(mrid=pb.mrid())

    network_service.resolve_or_defer_reference(resolver.lv_feeder_normal_head_terminal(cim), pb.normalHeadTerminalMRID)
    for mrid in pb.normalEnergizingFeederMRIDs:
        network_service.resolve_or_defer_reference(resolver.normal_energizing_feeders(cim), mrid)
    for mrid in pb.currentlyEnergizingFeederMRIDs:
        network_service.resolve_or_defer_reference(resolver.current_energizing_feeders(cim), mrid)

    equipment_container_to_cim(pb.ec, cim, network_service)
    return cim if network_service.add(cim) else None


PBLoop.to_cim = loop_to_cim
PBLvFeeder.to_cim = lv_feeder_to_cim


##################################################
# Extensions IEC61970 Base Generation Production #
##################################################

def ev_charging_unit_to_cim(pb: PBEvChargingUnit, network_service: NetworkService) -> Optional[EvChargingUnit]:
    # noinspection PyUnresolvedReferences
    cim = EvChargingUnit(mrid=pb.mrid())
    power_electronics_unit_to_cim(pb.peu, cim, network_service)
    return cim if network_service.add(cim) else None


PBEvChargingUnit.to_cim = ev_charging_unit_to_cim


#######################################
# Extensions IEC61970 Base Protection #
#######################################

def distance_relay_to_cim(pb: PBDistanceRelay, network_service: NetworkService) -> Optional[DistanceRelay]:
    # noinspection PyUnresolvedReferences
    cim = DistanceRelay(
        mrid=pb.mrid(),
        backward_blind=float_or_none(pb.backwardBlind),
        backward_reach=float_or_none(pb.backwardReach),
        backward_reactance=float_or_none(pb.backwardReactance),
        forward_blind=float_or_none(pb.forwardBlind),
        forward_reach=float_or_none(pb.forwardReach),
        forward_reactance=float_or_none(pb.forwardReactance),
        operation_phase_angle1=float_or_none(pb.operationPhaseAngle1),
        operation_phase_angle2=float_or_none(pb.operationPhaseAngle2),
        operation_phase_angle3=float_or_none(pb.operationPhaseAngle3)
    )

    protection_relay_function_to_cim(pb.prf, cim, network_service)
    return cim if network_service.add(cim) else None


def protection_relay_function_to_cim(pb: PBProtectionRelayFunction, cim: ProtectionRelayFunction, network_service: NetworkService):
    cim.model = str_or_none(pb.model)
    cim.reclosing = None if pb.HasField("reclosingNull") else pb.reclosingSet
    for time_limit in pb.timeLimits:
        cim.add_time_limit(time_limit)
    for threshold in pb.thresholds:
        cim.add_threshold(relay_setting_to_cim(threshold))
    cim.relay_delay_time = float_or_none(pb.relayDelayTime)
    cim.protection_kind = ProtectionKind(pb.protectionKind)
    for mrid in pb.protectedSwitchMRIDs:
        network_service.resolve_or_defer_reference(resolver.prf_protected_switch(cim), mrid)
    cim.directable = None if pb.HasField("directableNull") else pb.directableSet
    cim.power_direction = PowerDirectionKind(pb.powerDirection)
    for mrid in pb.sensorMRIDs:
        network_service.resolve_or_defer_reference(resolver.prf_sensor(cim), mrid)
    for mrid in pb.schemeMRIDs:
        network_service.resolve_or_defer_reference(resolver.prf_scheme(cim), mrid)
    # noinspection PyUnresolvedReferences
    network_service.resolve_or_defer_reference(resolver.relay_info(cim), pb.asset_info_mrid())

    power_system_resource_to_cim(pb.psr, cim, network_service)


def protection_relay_scheme_to_cim(pb: PBProtectionRelayScheme, network_service: NetworkService) -> Optional[ProtectionRelayScheme]:
    # noinspection PyUnresolvedReferences
    cim = ProtectionRelayScheme(
        mrid=pb.mrid()
    )

    # TODO: I think I just throw the nullable mrid at the bound resolver safely?
    network_service.resolve_or_defer_reference(resolver.prscheme_system(cim), pb.systemMRID)

    for mrid in pb.functionMRIDs:
        network_service.resolve_or_defer_reference(resolver.prscheme_function(cim), mrid)

    identified_object_to_cim(pb.io, cim, network_service)
    return cim if network_service.add(cim) else None


def protection_relay_system_to_cim(pb: PBProtectionRelaySystem, network_service: NetworkService) -> Optional[ProtectionRelaySystem]:
    # noinspection PyUnresolvedReferences
    cim = ProtectionRelaySystem(
        mrid=pb.mrid(),
        protection_kind=ProtectionKind(pb.protectionKind)
    )

    for mrid in pb.schemeMRIDs:
        network_service.resolve_or_defer_reference(resolver.prsystem_scheme(cim), mrid)

    equipment_to_cim(pb.eq, cim, network_service)
    return cim if network_service.add(cim) else None


def relay_setting_to_cim(pb: PBRelaySetting) -> Optional[RelaySetting]:
    return RelaySetting(
        name=pb.name,
        unit_symbol=unit_symbol_from_id(pb.unitSymbol),
        value=float_or_none(pb.value)
    )


def voltage_relay_to_cim(pb: PBVoltageRelay, network_service: NetworkService) -> Optional[VoltageRelay]:
    # noinspection PyUnresolvedReferences
    cim = VoltageRelay(mrid=pb.mrid())

    protection_relay_function_to_cim(pb.prf, cim, network_service)
    return cim if network_service.add(cim) else None


PBDistanceRelay.to_cim = distance_relay_to_cim
PBProtectionRelayScheme.to_cim = protection_relay_scheme_to_cim
PBProtectionRelaySystem.to_cim = protection_relay_system_to_cim
PBVoltageRelay.to_cim = voltage_relay_to_cim


##################################
# Extensions IEC61970 Base Wires #
##################################

def battery_control_to_cim(pb: PBBatteryControl, network_service: NetworkService) -> BatteryControl:
    """
    Convert the protobuf :class:`PBBatteryControl` into its CIM counterpart.
    :param pb: The protobuf :class:`PBBatteryControl` to convert
    :param network_service: The :class:`NetworkService` the converted CIM object will be added to.
    :return: The converted `pb` as a CIM :class:`BatteryControl`
    """
    # noinspection PyUnresolvedReferences
    cim = BatteryControl(
        mrid=pb.mrid(),
        charging_rate=float_or_none(pb.chargingRate),
        discharging_rate=float_or_none(pb.dischargingRate),
        reserve_percent=float_or_none(pb.reservePercent),
        control_mode=BatteryControlMode(pb.controlMode)
    )

    regulating_control_to_cim(pb.rc, cim, network_service)

    return cim if network_service.add(cim) else None


PBBatteryControl.to_cim = battery_control_to_cim


#######################
# IEC61968 Asset Info #
#######################


def cable_info_to_cim(pb: PBCableInfo, network_service: NetworkService) -> Optional[CableInfo]:
    # noinspection PyUnresolvedReferences
    cim = CableInfo(mrid=pb.mrid())

    wire_info_to_cim(pb.wi, cim, network_service)
    return cim if network_service.add(cim) else None


def no_load_test_to_cim(pb: PBNoLoadTest, network_service: NetworkService) -> Optional[NoLoadTest]:
    # noinspection PyUnresolvedReferences
    cim = NoLoadTest(
        mrid=pb.mrid(),
        energised_end_voltage=int_or_none(pb.energisedEndVoltage),
        exciting_current=float_or_none(pb.excitingCurrent),
        exciting_current_zero=float_or_none(pb.excitingCurrentZero),
        loss=int_or_none(pb.loss),
        loss_zero=int_or_none(pb.lossZero),
    )

    transformer_test_to_cim(pb.tt, cim, network_service)
    return cim if network_service.add(cim) else None


def open_circuit_test_to_cim(pb: PBOpenCircuitTest, network_service: NetworkService) -> Optional[OpenCircuitTest]:
    # noinspection PyUnresolvedReferences
    cim = OpenCircuitTest(
        mrid=pb.mrid(),
        energised_end_step=int_or_none(pb.energisedEndStep),
        energised_end_voltage=int_or_none(pb.energisedEndVoltage),
        open_end_step=int_or_none(pb.openEndStep),
        open_end_voltage=int_or_none(pb.openEndVoltage),
        phase_shift=float_or_none(pb.phaseShift),
    )

    transformer_test_to_cim(pb.tt, cim, network_service)
    return cim if network_service.add(cim) else None


def overhead_wire_info_to_cim(pb: PBOverheadWireInfo, network_service: NetworkService) -> Optional[OverheadWireInfo]:
    # noinspection PyUnresolvedReferences
    cim = OverheadWireInfo(mrid=pb.mrid())

    wire_info_to_cim(pb.wi, cim, network_service)
    return cim if network_service.add(cim) else None


def power_transformer_info_to_cim(pb: PBPowerTransformerInfo, network_service: NetworkService) -> Optional[PowerTransformerInfo]:
    # noinspection PyUnresolvedReferences
    cim = PowerTransformerInfo(mrid=pb.mrid())

    for mrid in pb.transformerTankInfoMRIDs:
        network_service.resolve_or_defer_reference(resolver.power_transformer_info_transformer_tank_info(cim), mrid)

    asset_info_to_cim(pb.ai, cim, network_service)
    return cim if network_service.add(cim) else None


def short_circuit_test_to_cim(pb: PBShortCircuitTest, network_service: NetworkService) -> Optional[ShortCircuitTest]:
    # noinspection PyUnresolvedReferences
    cim = ShortCircuitTest(
        mrid=pb.mrid(),
        current=float_or_none(pb.current),
        energised_end_step=int_or_none(pb.energisedEndStep),
        grounded_end_step=int_or_none(pb.groundedEndStep),
        leakage_impedance=float_or_none(pb.leakageImpedance),
        leakage_impedance_zero=float_or_none(pb.leakageImpedanceZero),
        loss=int_or_none(pb.loss),
        loss_zero=int_or_none(pb.lossZero),
        power=int_or_none(pb.power),
        voltage=float_or_none(pb.voltage),
        voltage_ohmic_part=float_or_none(pb.voltageOhmicPart),
    )

    transformer_test_to_cim(pb.tt, cim, network_service)
    return cim if network_service.add(cim) else None


def shunt_compensator_info_to_cim(pb: PBShuntCompensatorInfo, network_service: NetworkService) -> Optional[ShuntCompensatorInfo]:
    # noinspection PyUnresolvedReferences
    cim = ShuntCompensatorInfo(
        mrid=pb.mrid(),
        max_power_loss=int_or_none(pb.maxPowerLoss),
        rated_current=int_or_none(pb.ratedCurrent),
        rated_reactive_power=int_or_none(pb.ratedReactivePower),
        rated_voltage=int_or_none(pb.ratedVoltage),
    )

    asset_info_to_cim(pb.ai, cim, network_service)
    return cim if network_service.add(cim) else None


def switch_info_to_cim(pb: PBSwitchInfo, network_service: NetworkService) -> Optional[SwitchInfo]:
    # noinspection PyUnresolvedReferences
    cim = SwitchInfo(
        mrid=pb.mrid(),
        rated_interrupting_time=float_or_none(pb.ratedInterruptingTime)
    )

    asset_info_to_cim(pb.ai, cim, network_service)
    return cim if network_service.add(cim) else None


def transformer_end_info_to_cim(pb: PBTransformerEndInfo, network_service: NetworkService) -> Optional[TransformerEndInfo]:
    # noinspection PyUnresolvedReferences
    cim = TransformerEndInfo(
        mrid=pb.mrid(),
        connection_kind=WindingConnection(pb.connectionKind),
        emergency_s=int_or_none(pb.emergencyS),
        end_number=pb.endNumber,
        insulation_u=int_or_none(pb.insulationU),
        phase_angle_clock=int_or_none(pb.phaseAngleClock),
        r=float_or_none(pb.r),
        rated_s=int_or_none(pb.ratedS),
        rated_u=int_or_none(pb.ratedU),
        short_term_s=int_or_none(pb.shortTermS),
    )

    network_service.resolve_or_defer_reference(resolver.transformer_tank_info(cim), pb.transformerTankInfoMRID)
    network_service.resolve_or_defer_reference(resolver.transformer_star_impedance(cim), pb.transformerStarImpedanceMRID)
    network_service.resolve_or_defer_reference(resolver.energised_end_no_load_tests(cim), pb.energisedEndNoLoadTestsMRID)
    network_service.resolve_or_defer_reference(resolver.energised_end_short_circuit_tests(cim), pb.energisedEndShortCircuitTestsMRID)
    network_service.resolve_or_defer_reference(resolver.grounded_end_short_circuit_tests(cim), pb.groundedEndShortCircuitTestsMRID)
    network_service.resolve_or_defer_reference(resolver.open_end_open_circuit_tests(cim), pb.openEndOpenCircuitTestsMRID)
    network_service.resolve_or_defer_reference(resolver.energised_end_open_circuit_tests(cim), pb.energisedEndOpenCircuitTestsMRID)

    asset_info_to_cim(pb.ai, cim, network_service)
    return cim if network_service.add(cim) else None


def transformer_tank_info_to_cim(pb: PBTransformerTankInfo, network_service: NetworkService) -> Optional[TransformerTankInfo]:
    # noinspection PyUnresolvedReferences
    cim = TransformerTankInfo(mrid=pb.mrid())

    for mrid in pb.transformerEndInfoMRIDs:
        network_service.resolve_or_defer_reference(resolver.transformer_end_info(cim), mrid)

    asset_info_to_cim(pb.ai, cim, network_service)
    return cim if network_service.add(cim) else None


def transformer_test_to_cim(pb: PBTransformerTest, cim: TransformerTest, network_service: NetworkService):
    cim.base_power = int_or_none(pb.basePower)
    cim.temperature = float_or_none(pb.temperature)

    identified_object_to_cim(pb.io, cim, network_service)


def wire_info_to_cim(pb: PBWireInfo, cim: WireInfo, network_service: NetworkService):
    cim.rated_current = int_or_none(pb.ratedCurrent)
    cim.material = WireMaterialKind(pb.material)

    asset_info_to_cim(pb.ai, cim, network_service)


PBCableInfo.to_cim = cable_info_to_cim
PBNoLoadTest.to_cim = no_load_test_to_cim
PBOpenCircuitTest.to_cim = open_circuit_test_to_cim
PBOverheadWireInfo.to_cim = overhead_wire_info_to_cim
PBPowerTransformerInfo.to_cim = power_transformer_info_to_cim
PBShortCircuitTest.to_cim = short_circuit_test_to_cim
PBShuntCompensatorInfo.to_cim = shunt_compensator_info_to_cim
PBSwitchInfo.to_cim = switch_info_to_cim
PBTransformerEndInfo.to_cim = transformer_end_info_to_cim
PBTransformerTankInfo.to_cim = transformer_tank_info_to_cim


###################
# IEC61968 Assets #
###################

def asset_to_cim(pb: PBAsset, cim: Asset, network_service: NetworkService):
    network_service.resolve_or_defer_reference(resolver.at_location(cim), pb.locationMRID)

    for mrid in pb.organisationRoleMRIDs:
        network_service.resolve_or_defer_reference(resolver.organisation_roles(cim), mrid)

    for mrid in pb.powerSystemResourceMRIDs:
        network_service.resolve_or_defer_reference(resolver.power_system_resources(cim), mrid)

    identified_object_to_cim(pb.io, cim, network_service)


def asset_container_to_cim(pb: PBAssetContainer, cim: AssetContainer, network_service: NetworkService):
    asset_to_cim(pb.at, cim, network_service)


def asset_function_to_cim(pb: PBAssetFunction, cim: AssetFunction, network_service: NetworkService):
    """
    Convert the protobuf :class:`PBAssetFunction` into its CIM counterpart.
    :param pb: The protobuf :class:`PBAssetFunction` to convert.
    :param cim: The CIM :class:`AssetFunction` undergoing construction.
    :param network_service: The :class:`NetworkService` the converted CIM object will be added to.
    :return: The converted `pb` as a CIM :class:`AssetFunction`
    """
    identified_object_to_cim(pb.io, cim, network_service)


def asset_info_to_cim(pb: PBAssetInfo, cim: AssetInfo, network_service: NetworkService):
    identified_object_to_cim(pb.io, cim, network_service)


def asset_organisation_role_to_cim(pb: PBAssetOrganisationRole, cim: AssetOrganisationRole,
                                   network_service: NetworkService):
    organisation_role_to_cim(getattr(pb, "or"), cim, network_service)


def asset_owner_to_cim(pb: PBAssetOwner, network_service: NetworkService) -> Optional[AssetOwner]:
    # noinspection PyUnresolvedReferences
    cim = AssetOwner(mrid=pb.mrid())

    asset_organisation_role_to_cim(pb.aor, cim, network_service)
    return cim if network_service.add(cim) else None


def streetlight_to_cim(pb: PBStreetlight, network_service: NetworkService) -> Optional[Streetlight]:
    # noinspection PyUnresolvedReferences
    cim = Streetlight(
        mrid=pb.mrid(),
        light_rating=uint_or_none(pb.lightRating),
        lamp_kind=StreetlightLampKind(pb.lampKind)
    )

    network_service.resolve_or_defer_reference(resolver.pole(cim), pb.poleMRID)

    asset_to_cim(pb.at, cim, network_service)
    return cim if network_service.add(cim) else None


def structure_to_cim(pb: PBStructure, cim: Structure, network_service: NetworkService):
    asset_container_to_cim(pb.ac, cim, network_service)


PBAssetOwner.to_cim = asset_owner_to_cim
PBStreetlight.to_cim = streetlight_to_cim


###################
# IEC61968 Common #
###################

def location_to_cim(pb: PBLocation, network_service: NetworkService) -> Optional[Location]:
    # noinspection PyUnresolvedReferences
    cim = Location(mrid=pb.mrid(), main_address=street_address_to_cim(pb.mainAddress) if pb.HasField("mainAddress") else None)

    for point in pb.positionPoints:
        cim.add_point(position_point_to_cim(point))

    identified_object_to_cim(pb.io, cim, network_service)
    return cim if network_service.add(cim) else None


def position_point_to_cim(pb: PBPositionPoint) -> Optional[PositionPoint]:
    return PositionPoint(pb.xPosition, pb.yPosition)


def street_address_to_cim(pb: PBStreetAddress) -> Optional[StreetAddress]:
    return StreetAddress(
        postal_code=pb.postalCode,
        town_detail=town_detail_to_cim(pb.townDetail) if pb.HasField("townDetail") else None,
        po_box=pb.poBox,
        street_detail=street_detail_to_cim(pb.streetDetail) if pb.HasField("streetDetail") else None
    )


def street_detail_to_cim(pb: PBStreetDetail) -> Optional[StreetDetail]:
    return StreetDetail(
        building_name=pb.buildingName,
        floor_identification=pb.floorIdentification,
        name=pb.name,
        number=pb.number,
        suite_number=pb.suiteNumber,
        type=pb.type,
        display_address=pb.displayAddress
    )


def town_detail_to_cim(pb: PBTownDetail) -> Optional[TownDetail]:
    return TownDetail(name=pb.name, state_or_province=pb.stateOrProvince)


PBLocation.to_cim = location_to_cim
PBPositionPoint.to_cim = position_point_to_cim


#####################################
# IEC61968 InfIEC61968 InfAssetInfo #
#####################################

def current_transformer_info_to_cim(pb: PBCurrentTransformerInfo, network_service: NetworkService) -> Optional[CurrentTransformerInfo]:
    # noinspection PyUnresolvedReferences
    cim = CurrentTransformerInfo(
        mrid=pb.mrid(),
        accuracy_class=str_or_none(pb.accuracyClass),
        accuracy_limit=float_or_none(pb.accuracyLimit),
        core_count=int_or_none(pb.coreCount),
        ct_class=str_or_none(pb.ctClass),
        knee_point_voltage=int_or_none(pb.kneePointVoltage),
        max_ratio=ratio_to_cim(pb.maxRatio) if pb.HasField("maxRatio") else None,
        nominal_ratio=ratio_to_cim(pb.nominalRatio) if pb.HasField("nominalRatio") else None,
        primary_ratio=float_or_none(pb.primaryRatio),
        rated_current=int_or_none(pb.ratedCurrent),
        secondary_fls_rating=int_or_none(pb.secondaryFlsRating),
        secondary_ratio=float_or_none(pb.secondaryRatio),
        usage=str_or_none(pb.usage)
    )

    asset_info_to_cim(pb.ai, cim, network_service)
    return cim if network_service.add(cim) else None


def potential_transformer_info_to_cim(pb: PBPotentialTransformerInfo, network_service: NetworkService) -> Optional[PotentialTransformerInfo]:
    # noinspection PyUnresolvedReferences
    cim = PotentialTransformerInfo(
        mrid=pb.mrid(),
        accuracy_class=str_or_none(pb.accuracyClass),
        nominal_ratio=ratio_to_cim(pb.nominalRatio) if pb.HasField("nominalRatio") else None,
        primary_ratio=float_or_none(pb.primaryRatio),
        pt_class=str_or_none(pb.ptClass),
        rated_voltage=int_or_none(pb.ratedVoltage),
        secondary_ratio=float_or_none(pb.secondaryRatio)
    )

    asset_info_to_cim(pb.ai, cim, network_service)
    return cim if network_service.add(cim) else None


PBCurrentTransformerInfo.to_cim = current_transformer_info_to_cim
PBPotentialTransformerInfo.to_cim = potential_transformer_info_to_cim


##################################
# IEC61968 InfIEC61968 InfAssets #
##################################

def pole_to_cim(pb: PBPole, network_service: NetworkService) -> Optional[Pole]:
    # noinspection PyUnresolvedReferences
    cim = Pole(mrid=pb.mrid(), classification=pb.classification)

    for mrid in pb.streetlightMRIDs:
        network_service.resolve_or_defer_reference(resolver.streetlights(cim), mrid)

    structure_to_cim(pb.st, cim, network_service)
    return cim if network_service.add(cim) else None


PBPole.to_cim = pole_to_cim


##################################
# IEC61968 InfIEC61968 InfCommon #
##################################

def ratio_to_cim(pb: PBRatio) -> Ratio:
    return Ratio(pb.numerator, pb.denominator)


PBRatio.to_cim = ratio_to_cim


#####################
# IEC61968 Metering #
#####################


def end_device_to_cim(pb: PBEndDevice, cim: EndDevice, network_service: NetworkService):
    """
    Convert the protobuf :class:`PBEndDevice` into its CIM counterpart.
    :param pb: The protobuf :class:`PBEndDevice` to convert.
    :param cim: The CIM :class:`EndDevice` undergoing construction.
    :param network_service: The :class:`NetworkService` the converted CIM object will be added to.
    :return: The converted `pb` as a CIM :class:`EndDevice`
    """
    cim.customer_mrid = pb.customerMRID if pb.customerMRID else None

    for mrid in pb.usagePointMRIDs:
        network_service.resolve_or_defer_reference(resolver.ed_usage_points(cim), mrid)

    for mrid in pb.endDeviceFunctionMRIDs:
        network_service.resolve_or_defer_reference(resolver.end_device_functions(cim), mrid)

    network_service.resolve_or_defer_reference(resolver.service_location(cim), pb.serviceLocationMRID)
    asset_container_to_cim(pb.ac, cim, network_service)


def end_device_function_to_cim(pb: PBEndDeviceFunction, cim: EndDeviceFunction, network_service: NetworkService):
    """
    Convert the protobuf :class:`PBEndDeviceFunction` into its CIM counterpart.
    :param pb: The protobuf :class:`PBEndDeviceFunction` to convert.
    :param cim: The CIM :class:`EndDeviceFunction` undergoing construction.
    :param network_service: The :class:`NetworkService` the converted CIM object will be added to.
    :return: The converted `pb` as a CIM :class:`EndDeviceFunction`
    """
    cim.enabled = None if pb.HasField("enabledNull") else pb.enabledSet
    asset_function_to_cim(pb.af, cim, network_service)


def meter_to_cim(pb: PBMeter, network_service: NetworkService) -> Optional[Meter]:
    # noinspection PyUnresolvedReferences
    cim = Meter(mrid=pb.mrid())

    end_device_to_cim(pb.ed, cim, network_service)
    return cim if network_service.add(cim) else None


def usage_point_to_cim(pb: PBUsagePoint, network_service: NetworkService) -> Optional[UsagePoint]:
    # noinspection PyUnresolvedReferences
    cim = UsagePoint(mrid=pb.mrid())

    network_service.resolve_or_defer_reference(resolver.usage_point_location(cim), pb.usagePointLocationMRID)
    cim.is_virtual = pb.isVirtual
    cim.connection_category = pb.connectionCategory if pb.connectionCategory else None
    cim.rated_power = int_or_none(pb.ratedPower)
    cim.approved_inverter_capacity = int_or_none(pb.approvedInverterCapacity)
    cim.phase_code = phase_code_by_id(pb.phaseCode)

    for mrid in pb.equipmentMRIDs:
        network_service.resolve_or_defer_reference(resolver.up_equipment(cim), mrid)
    for mrid in pb.endDeviceMRIDs:
        network_service.resolve_or_defer_reference(resolver.end_devices(cim), mrid)

    identified_object_to_cim(pb.io, cim, network_service)
    return cim if network_service.add(cim) else None


PBMeter.to_cim = meter_to_cim
PBUsagePoint.to_cim = usage_point_to_cim


#######################
# IEC61968 Operations #
#######################

def operational_restriction_to_cim(pb: PBOperationalRestriction, network_service: NetworkService) -> Optional[OperationalRestriction]:
    # noinspection PyUnresolvedReferences
    cim = OperationalRestriction(mrid=pb.mrid())
    document_to_cim(pb.doc, cim, network_service)
    return cim if network_service.add(cim) else None


PBOperationalRestriction.to_cim = operational_restriction_to_cim


#####################################
# IEC61970 Base Auxiliary Equipment #
#####################################

def auxiliary_equipment_to_cim(pb: PBAuxiliaryEquipment, cim: AuxiliaryEquipment, network_service: NetworkService):
    network_service.resolve_or_defer_reference(resolver.ae_terminal(cim), pb.terminalMRID)

    equipment_to_cim(pb.eq, cim, network_service)


def current_transformer_to_cim(pb: PBCurrentTransformer, network_service: NetworkService) -> Optional[CurrentTransformer]:
    # noinspection PyUnresolvedReferences
    cim = CurrentTransformer(mrid=pb.mrid(), core_burden=int_or_none(pb.coreBurden))

    # noinspection PyUnresolvedReferences
    network_service.resolve_or_defer_reference(resolver.current_transformer_info(cim), pb.asset_info_mrid())

    sensor_to_cim(pb.sn, cim, network_service)
    return cim if network_service.add(cim) else None


def fault_indicator_to_cim(pb: PBFaultIndicator, network_service: NetworkService) -> Optional[FaultIndicator]:
    # noinspection PyUnresolvedReferences
    cim = FaultIndicator(mrid=pb.mrid())

    auxiliary_equipment_to_cim(pb.ae, cim, network_service)
    return cim if network_service.add(cim) else None


def potential_transformer_to_cim(pb: PBPotentialTransformer, network_service: NetworkService) -> Optional[PotentialTransformer]:
    # noinspection PyUnresolvedReferences
    cim = PotentialTransformer(mrid=pb.mrid(), type=PotentialTransformerKind(pb.type))

    # noinspection PyUnresolvedReferences
    network_service.resolve_or_defer_reference(resolver.potential_transformer_info(cim), pb.asset_info_mrid())

    sensor_to_cim(pb.sn, cim, network_service)
    return cim if network_service.add(cim) else None


def sensor_to_cim(pb: PBSensor, cim: Sensor, network_service: NetworkService):
    for mrid in pb.relayFunctionMRIDs:
        network_service.resolve_or_defer_reference(resolver.sen_relay_function(cim), mrid)
    auxiliary_equipment_to_cim(pb.ae, cim, network_service)


PBCurrentTransformer.to_cim = current_transformer_to_cim
PBFaultIndicator.to_cim = fault_indicator_to_cim
PBPotentialTransformer.to_cim = potential_transformer_to_cim


######################
# IEC61970 Base Core #
######################

def ac_dc_terminal_to_cim(pb: PBAcDcTerminal, cim: AcDcTerminal, network_service: NetworkService):
    identified_object_to_cim(pb.io, cim, network_service)


def base_voltage_to_cim(pb: PBBaseVoltage, network_service: NetworkService) -> Optional[BaseVoltage]:
    # noinspection PyUnresolvedReferences
    cim = BaseVoltage(mrid=pb.mrid(), nominal_voltage=pb.nominalVoltage)

    identified_object_to_cim(pb.io, cim, network_service)
    return cim if network_service.add(cim) else None


def conducting_equipment_to_cim(pb: PBConductingEquipment, cim: ConductingEquipment, network_service: NetworkService):
    network_service.resolve_or_defer_reference(resolver.ce_base_voltage(cim), pb.baseVoltageMRID)
    for mrid in pb.terminalMRIDs:
        network_service.resolve_or_defer_reference(resolver.ce_terminals(cim), mrid)

    equipment_to_cim(pb.eq, cim, network_service)


def connectivity_node_to_cim(pb: PBConnectivityNode, network_service: NetworkService) -> Optional[ConnectivityNode]:
    # noinspection PyUnresolvedReferences
    cim = ConnectivityNode(mrid=pb.mrid())

    identified_object_to_cim(pb.io, cim, network_service)
    return cim if network_service.add(cim) else None


def connectivity_node_container_to_cim(pb: PBConnectivityNodeContainer, cim: ConnectivityNodeContainer, network_service: NetworkService):
    power_system_resource_to_cim(pb.psr, cim, network_service)


def curve_to_cim(pb: PBCurve, cim: Curve, network_service: NetworkService):
    for curve_data in pb.curveData:
        cim.add_curve_data(curve_data_to_cim(curve_data))

    identified_object_to_cim(pb.io, cim, network_service)


def curve_data_to_cim(pb: PBCurveData) -> Optional[CurveData]:
    return CurveData(pb.xValue, pb.y1Value, float_or_none(pb.y2Value), float_or_none(pb.y3Value))


def equipment_to_cim(pb: PBEquipment, cim: Equipment, network_service: NetworkService):
    cim.in_service = pb.inService
    cim.normally_in_service = pb.normallyInService
    cim.commissioned_date = pb.commissionedDate.ToDatetime() if pb.HasField("commissionedDate") else None

    for mrid in pb.equipmentContainerMRIDs:
        network_service.resolve_or_defer_reference(resolver.containers(cim), mrid)
    for mrid in pb.usagePointMRIDs:
        network_service.resolve_or_defer_reference(resolver.eq_usage_points(cim), mrid)
    for mrid in pb.operationalRestrictionMRIDs:
        network_service.resolve_or_defer_reference(resolver.operational_restrictions(cim), mrid)
    for mrid in pb.currentContainerMRIDs:
        network_service.resolve_or_defer_reference(resolver.current_containers(cim), mrid)

    power_system_resource_to_cim(pb.psr, cim, network_service)


def equipment_container_to_cim(pb: PBEquipmentContainer, cim: EquipmentContainer, network_service: NetworkService):
    connectivity_node_container_to_cim(pb.cnc, cim, network_service)


def feeder_to_cim(pb: PBFeeder, network_service: NetworkService) -> Optional[Feeder]:
    # noinspection PyUnresolvedReferences
    cim = Feeder(mrid=pb.mrid())

    network_service.resolve_or_defer_reference(resolver.normal_head_terminal(cim), pb.normalHeadTerminalMRID)
    network_service.resolve_or_defer_reference(resolver.normal_energizing_substation(cim), pb.normalEnergizingSubstationMRID)
    for mrid in pb.normalEnergizedLvFeederMRIDs:
        network_service.resolve_or_defer_reference(resolver.normal_energized_lv_feeders(cim), mrid)
    for mrid in pb.currentlyEnergizedLvFeedersMRIDs:
        network_service.resolve_or_defer_reference(resolver.current_energized_lv_feeders(cim), mrid)

    equipment_container_to_cim(pb.ec, cim, network_service)
    return cim if network_service.add(cim) else None


def geographical_region_to_cim(pb: PBGeographicalRegion, network_service: NetworkService) -> Optional[GeographicalRegion]:
    # noinspection PyUnresolvedReferences
    cim = GeographicalRegion(mrid=pb.mrid())

    for mrid in pb.subGeographicalRegionMRIDs:
        network_service.resolve_or_defer_reference(resolver.sub_geographical_regions(cim), mrid)

    identified_object_to_cim(pb.io, cim, network_service)
    return cim if network_service.add(cim) else None


def power_system_resource_to_cim(pb: PBPowerSystemResource, cim: PowerSystemResource, network_service: NetworkService):
    network_service.resolve_or_defer_reference(resolver.psr_location(cim), pb.locationMRID)

    for mrid in pb.assetMRIDs:
        network_service.resolve_or_defer_reference(resolver.assets(cim), mrid)

    identified_object_to_cim(pb.io, cim, network_service)


def sub_geographical_region_to_cim(pb: PBSubGeographicalRegion, network_service: NetworkService) -> Optional[SubGeographicalRegion]:
    # noinspection PyUnresolvedReferences
    cim = SubGeographicalRegion(mrid=pb.mrid())

    network_service.resolve_or_defer_reference(resolver.geographical_region(cim), pb.geographicalRegionMRID)
    for mrid in pb.substationMRIDs:
        network_service.resolve_or_defer_reference(resolver.substations(cim), mrid)

    identified_object_to_cim(pb.io, cim, network_service)
    return cim if network_service.add(cim) else None


def substation_to_cim(pb: PBSubstation, network_service: NetworkService) -> Optional[Substation]:
    # noinspection PyUnresolvedReferences
    cim = Substation(mrid=pb.mrid())

    network_service.resolve_or_defer_reference(resolver.sub_geographical_region(cim), pb.subGeographicalRegionMRID)
    for mrid in pb.normalEnergizedFeederMRIDs:
        network_service.resolve_or_defer_reference(resolver.normal_energized_feeders(cim), mrid)
    for mrid in pb.loopMRIDs:
        network_service.resolve_or_defer_reference(resolver.loops(cim), mrid)
    for mrid in pb.normalEnergizedLoopMRIDs:
        network_service.resolve_or_defer_reference(resolver.normal_energized_loops(cim), mrid)
    for mrid in pb.circuitMRIDs:
        network_service.resolve_or_defer_reference(resolver.circuits(cim), mrid)

    equipment_container_to_cim(pb.ec, cim, network_service)
    return cim if network_service.add(cim) else None


def terminal_to_cim(pb: PBTerminal, network_service: NetworkService) -> Optional[Terminal]:
    # noinspection PyUnresolvedReferences
    cim = Terminal(
        mrid=pb.mrid(),
        phases=phase_code_by_id(pb.phases),
        sequence_number=pb.sequenceNumber,
        normal_feeder_direction=FeederDirection(pb.normalFeederDirection),
        current_feeder_direction=FeederDirection(pb.currentFeederDirection),
    )

    network_service.resolve_or_defer_reference(resolver.conducting_equipment(cim), pb.conductingEquipmentMRID)
    network_service.resolve_or_defer_reference(resolver.connectivity_node(cim), pb.connectivityNodeMRID)

    ac_dc_terminal_to_cim(pb.ad, cim, network_service)
    return cim if network_service.add(cim) else None


PBBaseVoltage.to_cim = base_voltage_to_cim
PBConnectivityNode.to_cim = connectivity_node_to_cim
PBFeeder.to_cim = feeder_to_cim
PBGeographicalRegion.to_cim = geographical_region_to_cim
PBSubGeographicalRegion.to_cim = sub_geographical_region_to_cim
PBSubstation.to_cim = substation_to_cim
PBTerminal.to_cim = terminal_to_cim


#############################
# IEC61970 Base Equivalents #
#############################

def equivalent_branch_to_cim(pb: PBEquivalentBranch, network_service: NetworkService) -> Optional[EquivalentBranch]:
    # noinspection PyUnresolvedReferences
    cim = EquivalentBranch(
        mrid=pb.mrid(),
        negative_r12=float_or_none(pb.negativeR12),
        negative_r21=float_or_none(pb.negativeR21),
        negative_x12=float_or_none(pb.negativeX12),
        negative_x21=float_or_none(pb.negativeX21),
        positive_r12=float_or_none(pb.positiveR12),
        positive_r21=float_or_none(pb.positiveR21),
        positive_x12=float_or_none(pb.positiveX12),
        positive_x21=float_or_none(pb.positiveX21),
        r=float_or_none(pb.r),
        r21=float_or_none(pb.r21),
        x=float_or_none(pb.x),
        x21=float_or_none(pb.x21),
        zero_r12=float_or_none(pb.zeroR12),
        zero_r21=float_or_none(pb.zeroR21),
        zero_x12=float_or_none(pb.zeroX12),
        zero_x21=float_or_none(pb.zeroX21),
    )

    equivalent_equipment_to_cim(pb.ee, cim, network_service)
    return cim if network_service.add(cim) else None


def equivalent_equipment_to_cim(pb: PBEquivalentEquipment, cim: EquivalentEquipment, network_service: NetworkService):
    conducting_equipment_to_cim(pb.ce, cim, network_service)


PBEquivalentBranch.to_cim = equivalent_branch_to_cim


#######################################
# IEC61970 Base Generation Production #
#######################################

def battery_unit_to_cim(pb: PBBatteryUnit, network_service: NetworkService) -> Optional[BatteryUnit]:
    """
    Convert the protobuf :class:`PBBatteryUnit` into its CIM counterpart.
    :param pb: The protobuf :class:`PBBatteryUnit` to convert.
    :param network_service: The :class:`NetworkService` the converted CIM object will be added to.
    :return: The converted `pb` as a CIM :class:`BatteryUnit`
    """
    # noinspection PyUnresolvedReferences
    cim = BatteryUnit(
        mrid=pb.mrid(),
        battery_state=BatteryStateKind(pb.batteryState),
        rated_e=long_or_none(pb.ratedE),
        stored_e=long_or_none(pb.storedE),
    )

    for mrid in pb.batteryControlMRIDs:
        network_service.resolve_or_defer_reference(resolver.battery_controls(cim), mrid)

    power_electronics_unit_to_cim(pb.peu, cim, network_service)
    return cim if network_service.add(cim) else None


def photo_voltaic_unit_to_cim(pb: PBPhotoVoltaicUnit, network_service: NetworkService) -> Optional[PhotoVoltaicUnit]:
    # noinspection PyUnresolvedReferences
    cim = PhotoVoltaicUnit(mrid=pb.mrid())

    power_electronics_unit_to_cim(pb.peu, cim, network_service)
    return cim if network_service.add(cim) else None


def power_electronics_unit_to_cim(pb: PBPowerElectronicsUnit, cim: PowerElectronicsUnit, network_service: NetworkService):
    cim.max_p = int_or_none(pb.maxP)
    cim.min_p = int_or_none(pb.minP)

    network_service.resolve_or_defer_reference(resolver.unit_power_electronics_connection(cim), pb.powerElectronicsConnectionMRID)

    equipment_to_cim(pb.eq, cim, network_service)


def power_electronics_wind_unit_to_cim(pb: PBPowerElectronicsWindUnit, network_service: NetworkService) -> Optional[PowerElectronicsWindUnit]:
    # noinspection PyUnresolvedReferences
    cim = PowerElectronicsWindUnit(mrid=pb.mrid())

    power_electronics_unit_to_cim(pb.peu, cim, network_service)
    return cim if network_service.add(cim) else None


PBBatteryUnit.to_cim = battery_unit_to_cim
PBPhotoVoltaicUnit.to_cim = photo_voltaic_unit_to_cim
PBPowerElectronicsWindUnit.to_cim = power_electronics_wind_unit_to_cim


######################
# IEC61970 Base Meas #
######################

def accumulator_to_cim(pb: PBAccumulator, network_service: NetworkService) -> Optional[Accumulator]:
    # noinspection PyUnresolvedReferences
    cim = Accumulator(mrid=pb.mrid())

    measurement_to_cim(pb.measurement, cim, network_service)
    return cim if network_service.add(cim) else None


def analog_to_cim(pb: PBAnalog, network_service: NetworkService) -> Optional[Analog]:
    # noinspection PyUnresolvedReferences
    cim = Analog(mrid=pb.mrid(), positive_flow_in=pb.positiveFlowIn)

    measurement_to_cim(pb.measurement, cim, network_service)
    return cim if network_service.add(cim) else None


def control_to_cim(pb: PBControl, network_service: NetworkService) -> Optional[Control]:
    # noinspection PyUnresolvedReferences
    cim = Control(
        mrid=pb.mrid(),
        # noinspection PyUnresolvedReferences
        power_system_resource_mrid=pb.powerSystemResourceMRID if pb.powerSystemResourceMRID else None
    )

    network_service.resolve_or_defer_reference(resolver.remote_control(cim), pb.remoteControlMRID)

    io_point_to_cim(pb.ip, cim, network_service)
    return cim if network_service.add(cim) else None


def discrete_to_cim(pb: PBDiscrete, network_service: NetworkService) -> Optional[Discrete]:
    # noinspection PyUnresolvedReferences
    cim = Discrete(mrid=pb.mrid())

    measurement_to_cim(pb.measurement, cim, network_service)
    return cim if network_service.add(cim) else None


def io_point_to_cim(pb: PBIoPoint, cim: IoPoint, service: NetworkService):
    identified_object_to_cim(pb.io, cim, service)


def measurement_to_cim(pb: PBMeasurement, cim: Measurement, service: NetworkService):
    cim.power_system_resource_mrid = str_or_none(pb.powerSystemResourceMRID)
    cim.terminal_mrid = str_or_none(pb.terminalMRID)
    cim.phases = phase_code_by_id(pb.phases)
    cim.unit_symbol = unit_symbol_from_id(pb.unitSymbol)

    service.resolve_or_defer_reference(resolver.remote_source(cim), pb.remoteSourceMRID)

    identified_object_to_cim(pb.io, cim, service)


PBAccumulator.to_cim = accumulator_to_cim
PBAnalog.to_cim = analog_to_cim
PBControl.to_cim = control_to_cim
PBDiscrete.to_cim = discrete_to_cim


############################
# IEC61970 Base Protection #
############################

def current_relay_to_cim(pb: PBCurrentRelay, network_service: NetworkService) -> Optional[CurrentRelay]:
    # noinspection PyUnresolvedReferences
    cim = CurrentRelay(
        mrid=pb.mrid(),
        current_limit_1=float_or_none(pb.currentLimit1),
        inverse_time_flag=None if pb.HasField("inverseTimeFlagNull") else pb.inverseTimeFlagSet,
        time_delay_1=float_or_none(pb.timeDelay1)
    )

    protection_relay_function_to_cim(pb.prf, cim, network_service)
    return cim if network_service.add(cim) else None


PBCurrentRelay.to_cim = current_relay_to_cim


#######################
# IEC61970 Base Scada #
#######################

def remote_control_to_cim(pb: PBRemoteControl, network_service: NetworkService) -> Optional[RemoteControl]:
    # noinspection PyUnresolvedReferences
    cim = RemoteControl(mrid=pb.mrid())

    network_service.resolve_or_defer_reference(resolver.control(cim), pb.controlMRID)

    remote_point_to_cim(pb.rp, cim, network_service)
    return cim if network_service.add(cim) else None


def remote_point_to_cim(pb: PBRemotePoint, cim: RemotePoint, service: NetworkService):
    identified_object_to_cim(pb.io, cim, service)


def remote_source_to_cim(pb: PBRemoteSource, network_service: NetworkService) -> Optional[RemoteSource]:
    # noinspection PyUnresolvedReferences
    cim = RemoteSource(mrid=pb.mrid())

    network_service.resolve_or_defer_reference(resolver.measurement(cim), pb.measurementMRID)

    remote_point_to_cim(pb.rp, cim, network_service)
    return cim if network_service.add(cim) else None


PBRemoteControl.to_cim = remote_control_to_cim
PBRemoteSource.to_cim = remote_source_to_cim


#######################
# IEC61970 Base Wires #
#######################

def ac_line_segment_to_cim(pb: PBAcLineSegment, network_service: NetworkService) -> Optional[AcLineSegment]:
    """
    Convert the protobuf :class:`PBAcLineSegment` into its CIM counterpart.
    :param pb: The protobuf :class:`PBAcLineSegment` to convert.
    :param network_service: The :class:`NetworkService` the converted CIM object will be added to.
    :return: The converted `pb` as a CIM :class:`AcLineSegment`
    """
    # noinspection PyUnresolvedReferences
    cim = AcLineSegment(mrid=pb.mrid())

    network_service.resolve_or_defer_reference(resolver.per_length_impedance(cim), pb.perLengthImpedanceMRID)
    for mrid in pb.cutMRIDs:
        network_service.resolve_or_defer_reference(resolver.cuts(cim), mrid)
    for mrid in pb.clampMRIDs:
        network_service.resolve_or_defer_reference(resolver.clamps(cim), mrid)

    conductor_to_cim(pb.cd, cim, network_service)
    return cim if network_service.add(cim) else None


def breaker_to_cim(pb: PBBreaker, network_service: NetworkService) -> Optional[Breaker]:
    # noinspection PyUnresolvedReferences
    cim = Breaker(
        mrid=pb.mrid(),
        in_transit_time=float_or_none(pb.inTransitTime)
    )

    protected_switch_to_cim(pb.sw, cim, network_service)
    return cim if network_service.add(cim) else None


def busbar_section_to_cim(pb: PBBusbarSection, network_service: NetworkService) -> Optional[BusbarSection]:
    # noinspection PyUnresolvedReferences
    cim = BusbarSection(mrid=pb.mrid())

    connector_to_cim(pb.cn, cim, network_service)
    return cim if network_service.add(cim) else None


def clamp_to_cim(pb: PBClamp, network_service: NetworkService) -> Optional[Clamp]:
    # noinspection PyUnresolvedReferences
    cim = Clamp(mrid=pb.mrid())

    cim.length_from_terminal_1 = float_or_none(pb.lengthFromTerminal1)
    network_service.resolve_or_defer_reference(resolver.clamp_ac_line_segment(cim), pb.acLineSegmentMRID)

    conducting_equipment_to_cim(pb.ce, cim, network_service)
    return cim if network_service.add(cim) else None


def conductor_to_cim(pb: PBConductor, cim: Conductor, network_service: NetworkService):
    cim.length = float_or_none(pb.length)
    cim.design_temperature = int_or_none(pb.designTemperature)
    cim.design_rating = float_or_none(pb.designRating)

    # noinspection PyUnresolvedReferences
    network_service.resolve_or_defer_reference(resolver.wire_info(cim), pb.asset_info_mrid())

    conducting_equipment_to_cim(pb.ce, cim, network_service)


def connector_to_cim(pb: PBConnector, cim: Connector, network_service: NetworkService):
    conducting_equipment_to_cim(pb.ce, cim, network_service)


def cut_to_cim(pb: PBCut, network_service: NetworkService) -> Optional[Cut]:
    # noinspection PyUnresolvedReferences
    cim = Cut(mrid=pb.mrid())

    cim.length_from_terminal_1 = float_or_none(pb.lengthFromTerminal1)
    network_service.resolve_or_defer_reference(resolver.cut_ac_line_segment(cim), pb.acLineSegmentMRID)

    switch_to_cim(pb.sw, cim, network_service)
    return cim if network_service.add(cim) else None


def disconnector_to_cim(pb: PBDisconnector, network_service: NetworkService) -> Optional[Disconnector]:
    # noinspection PyUnresolvedReferences
    cim = Disconnector(mrid=pb.mrid())

    switch_to_cim(pb.sw, cim, network_service)
    return cim if network_service.add(cim) else None


def earth_fault_compensator_to_cim(pb: PBEarthFaultCompensator, cim: EarthFaultCompensator, network_service: NetworkService):
    cim.r = float_or_none(pb.r)

    conducting_equipment_to_cim(pb.ce, cim, network_service)


def energy_connection_to_cim(pb: PBEnergyConnection, cim: EnergyConnection, network_service: NetworkService):
    conducting_equipment_to_cim(pb.ce, cim, network_service)


def energy_consumer_to_cim(pb: PBEnergyConsumer, network_service: NetworkService) -> Optional[EnergyConsumer]:
    # noinspection PyUnresolvedReferences
    cim = EnergyConsumer(
        mrid=pb.mrid(),
        customer_count=int_or_none(pb.customerCount),
        grounded=pb.grounded,
        phase_connection=PhaseShuntConnectionKind(pb.phaseConnection),
        p=float_or_none(pb.p),
        p_fixed=float_or_none(pb.pFixed),
        q=float_or_none(pb.q),
        q_fixed=float_or_none(pb.qFixed)
    )

    for mrid in pb.energyConsumerPhasesMRIDs:
        network_service.resolve_or_defer_reference(resolver.ec_phases(cim), mrid)

    energy_connection_to_cim(pb.ec, cim, network_service)
    return cim if network_service.add(cim) else None


def energy_consumer_phase_to_cim(pb: PBEnergyConsumerPhase, network_service: NetworkService) -> Optional[EnergyConsumerPhase]:
    # noinspection PyUnresolvedReferences
    cim = EnergyConsumerPhase(
        mrid=pb.mrid(),
        phase=single_phase_kind_by_id(pb.phase),
        p=float_or_none(pb.p),
        p_fixed=float_or_none(pb.pFixed),
        q=float_or_none(pb.q),
        q_fixed=float_or_none(pb.qFixed)
    )

    network_service.resolve_or_defer_reference(resolver.energy_consumer(cim), pb.energyConsumerMRID)

    power_system_resource_to_cim(pb.psr, cim, network_service)
    return cim if network_service.add(cim) else None


def energy_source_to_cim(pb: PBEnergySource, network_service: NetworkService) -> Optional[EnergySource]:
    # noinspection PyUnresolvedReferences
    cim = EnergySource(
        mrid=pb.mrid(),
        active_power=float_or_none(pb.activePower),
        reactive_power=float_or_none(pb.reactivePower),
        voltage_angle=float_or_none(pb.voltageAngle),
        voltage_magnitude=float_or_none(pb.voltageMagnitude),
        r=float_or_none(pb.r),
        x=float_or_none(pb.x),
        p_max=float_or_none(pb.pMax),
        p_min=float_or_none(pb.pMin),
        r0=float_or_none(pb.r0),
        rn=float_or_none(pb.rn),
        x0=float_or_none(pb.x0),
        xn=float_or_none(pb.xn),
        is_external_grid=pb.isExternalGrid,
        r_min=float_or_none(pb.rMin),
        rn_min=float_or_none(pb.rnMin),
        r0_min=float_or_none(pb.r0Min),
        x_min=float_or_none(pb.xMin),
        xn_min=float_or_none(pb.xnMin),
        x0_min=float_or_none(pb.x0Min),
        r_max=float_or_none(pb.rMax),
        rn_max=float_or_none(pb.rnMax),
        r0_max=float_or_none(pb.r0Max),
        x_max=float_or_none(pb.xMax),
        xn_max=float_or_none(pb.xnMax),
        x0_max=float_or_none(pb.x0Max)
    )

    for mrid in pb.energySourcePhasesMRIDs:
        network_service.resolve_or_defer_reference(resolver.es_phases(cim), mrid)

    energy_connection_to_cim(pb.ec, cim, network_service)
    return cim if network_service.add(cim) else None


def energy_source_phase_to_cim(pb: PBEnergySourcePhase, network_service: NetworkService) -> Optional[EnergySourcePhase]:
    # noinspection PyUnresolvedReferences
    cim = EnergySourcePhase(mrid=pb.mrid(), phase=single_phase_kind_by_id(pb.phase))

    network_service.resolve_or_defer_reference(resolver.energy_source(cim), pb.energySourceMRID)

    power_system_resource_to_cim(pb.psr, cim, network_service)
    return cim if network_service.add(cim) else None


def fuse_to_cim(pb: PBFuse, network_service: NetworkService) -> Optional[Fuse]:
    # noinspection PyUnresolvedReferences
    cim = Fuse(mrid=pb.mrid())

    network_service.resolve_or_defer_reference(resolver.fuse_function(cim), pb.functionMRID)

    switch_to_cim(pb.sw, cim, network_service)
    return cim if network_service.add(cim) else None


def ground_to_cim(pb: PBGround, network_service: NetworkService) -> Optional[Ground]:
    # noinspection PyUnresolvedReferences
    cim = Ground(mrid=pb.mrid())

    conducting_equipment_to_cim(pb.ce, cim, network_service)
    return cim if network_service.add(cim) else None


def ground_disconnector_to_cim(pb: PBGroundDisconnector, network_service: NetworkService) -> Optional[GroundDisconnector]:
    # noinspection PyUnresolvedReferences
    cim = GroundDisconnector(mrid=pb.mrid())

    switch_to_cim(pb.sw, cim, network_service)
    return cim if network_service.add(cim) else None


def grounding_impedance_to_cim(pb: PBGroundingImpedance, network_service: NetworkService) -> Optional[GroundingImpedance]:
    # noinspection PyUnresolvedReferences
    cim = GroundingImpedance(mrid=pb.mrid(), x=float_or_none(pb.x))

    earth_fault_compensator_to_cim(pb.efc, cim, network_service)
    return cim if network_service.add(cim) else None


def jumper_to_cim(pb: PBJumper, network_service: NetworkService) -> Optional[Jumper]:
    # noinspection PyUnresolvedReferences
    cim = Jumper(mrid=pb.mrid())

    switch_to_cim(pb.sw, cim, network_service)
    return cim if network_service.add(cim) else None


def junction_to_cim(pb: PBJunction, network_service: NetworkService) -> Optional[Junction]:
    # noinspection PyUnresolvedReferences
    cim = Junction(mrid=pb.mrid())

    connector_to_cim(pb.cn, cim, network_service)
    return cim if network_service.add(cim) else None


def line_to_cim(pb: PBLine, cim: Line, network_service: NetworkService):
    equipment_container_to_cim(pb.ec, cim, network_service)


def linear_shunt_compensator_to_cim(pb: PBLinearShuntCompensator, network_service: NetworkService) -> Optional[LinearShuntCompensator]:
    # noinspection PyUnresolvedReferences
    cim = LinearShuntCompensator(
        mrid=pb.mrid(),
        b0_per_section=float_or_none(pb.b0PerSection),
        b_per_section=float_or_none(pb.bPerSection),
        g0_per_section=float_or_none(pb.g0PerSection),
        g_per_section=float_or_none(pb.gPerSection)
    )

    shunt_compensator_to_cim(pb.sc, cim, network_service)
    return cim if network_service.add(cim) else None


def load_break_switch_to_cim(pb: PBLoadBreakSwitch, network_service: NetworkService) -> Optional[LoadBreakSwitch]:
    # noinspection PyUnresolvedReferences
    cim = LoadBreakSwitch(mrid=pb.mrid())

    protected_switch_to_cim(pb.ps, cim, network_service)
    return cim if network_service.add(cim) else None


def per_length_line_parameter_to_cim(pb: PBPerLengthLineParameter, cim: PerLengthLineParameter, network_service: NetworkService):
    identified_object_to_cim(pb.io, cim, network_service)


def per_length_impedance_to_cim(pb: PBPerLengthImpedance, cim: PerLengthImpedance, network_service: NetworkService):
    per_length_line_parameter_to_cim(pb.lp, cim, network_service)


def per_length_phase_impedance_to_cim(pb: PBPerLengthPhaseImpedance, network_service: NetworkService) -> Optional[PerLengthPhaseImpedance]:
    """
    Convert the protobuf :class:`PBPerLengthPhaseImpedance` into its CIM counterpart.
    :param pb: The protobuf :class:`PBPerLengthPhaseImpedance` to convert.
    :param network_service: The :class:`NetworkService` the converted CIM object will be added to.
    :return: The converted `pb` as a CIM :class:`PerLengthPhaseImpedance`
    """
    # noinspection PyUnresolvedReferences
    cim = PerLengthPhaseImpedance(mrid=pb.mrid())

    for phase_impedance_data in pb.phaseImpedanceData:
        cim.add_data(phase_impedance_data_to_cim(phase_impedance_data))

    per_length_impedance_to_cim(pb.pli, cim, network_service)
    return cim if network_service.add(cim) else None


def per_length_sequence_impedance_to_cim(pb: PBPerLengthSequenceImpedance, network_service: NetworkService) -> Optional[PerLengthSequenceImpedance]:
    # noinspection PyUnresolvedReferences
    cim = PerLengthSequenceImpedance(
        mrid=pb.mrid(),
        r=float_or_none(pb.r),
        x=float_or_none(pb.x),
        r0=float_or_none(pb.r0),
        x0=float_or_none(pb.x0),
        bch=float_or_none(pb.bch),
        gch=float_or_none(pb.gch),
        b0ch=float_or_none(pb.b0ch),
        g0ch=float_or_none(pb.g0ch)
    )

    per_length_impedance_to_cim(pb.pli, cim, network_service)
    return cim if network_service.add(cim) else None


def petersen_coil_to_cim(pb: PBPetersenCoil, network_service: NetworkService) -> Optional[PetersenCoil]:
    # noinspection PyUnresolvedReferences
    cim = PetersenCoil(mrid=pb.mrid(), x_ground_nominal=float_or_none(pb.xGroundNominal))

    earth_fault_compensator_to_cim(pb.efc, cim, network_service)
    return cim if network_service.add(cim) else None


def phase_impedance_data_to_cim(pb: PBPhaseImpedanceData) -> Optional[PhaseImpedanceData]:
    """
    Convert the protobuf :class:`PBPhaseImpedanceData` into its CIM counterpart.
    :param pb: The protobuf :class:`PBPhaseImpedanceData` to convert.
    :return: The converted `pb` as a CIM :class:`PhaseImpedanceData`
    """
    return PhaseImpedanceData(
        single_phase_kind_by_id(pb.fromPhase),
        single_phase_kind_by_id(pb.toPhase),
        float_or_none(pb.b),
        float_or_none(pb.g),
        float_or_none(pb.r),
        float_or_none(pb.x),
    )


def power_electronics_connection_to_cim(pb: PBPowerElectronicsConnection, network_service: NetworkService) -> Optional[PowerElectronicsConnection]:
    # noinspection PyUnresolvedReferences
    cim = PowerElectronicsConnection(
        mrid=pb.mrid(),
        max_i_fault=int_or_none(pb.maxIFault),
        p=float_or_none(pb.p),
        q=float_or_none(pb.q),
        max_q=float_or_none(pb.maxQ),
        min_q=float_or_none(pb.minQ),
        rated_s=int_or_none(pb.ratedS),
        rated_u=int_or_none(pb.ratedU),
        inverter_standard=str_or_none(pb.inverterStandard),
        sustain_op_overvolt_limit=int_or_none(pb.sustainOpOvervoltLimit),
        stop_at_over_freq=float_or_none(pb.stopAtOverFreq),
        stop_at_under_freq=float_or_none(pb.stopAtUnderFreq),
        inv_volt_watt_resp_mode=None if pb.HasField("invVoltWattRespModeNull") else pb.invVoltWattRespModeSet,
        inv_watt_resp_v1=int_or_none(pb.invWattRespV1),
        inv_watt_resp_v2=int_or_none(pb.invWattRespV2),
        inv_watt_resp_v3=int_or_none(pb.invWattRespV3),
        inv_watt_resp_v4=int_or_none(pb.invWattRespV4),
        inv_watt_resp_p_at_v1=float_or_none(pb.invWattRespPAtV1),
        inv_watt_resp_p_at_v2=float_or_none(pb.invWattRespPAtV2),
        inv_watt_resp_p_at_v3=float_or_none(pb.invWattRespPAtV3),
        inv_watt_resp_p_at_v4=float_or_none(pb.invWattRespPAtV4),
        inv_volt_var_resp_mode=None if pb.HasField("invVoltVarRespModeNull") else pb.invVoltVarRespModeSet,
        inv_var_resp_v1=int_or_none(pb.invVarRespV1),
        inv_var_resp_v2=int_or_none(pb.invVarRespV2),
        inv_var_resp_v3=int_or_none(pb.invVarRespV3),
        inv_var_resp_v4=int_or_none(pb.invVarRespV4),
        inv_var_resp_q_at_v1=float_or_none(pb.invVarRespQAtV1),
        inv_var_resp_q_at_v2=float_or_none(pb.invVarRespQAtV2),
        inv_var_resp_q_at_v3=float_or_none(pb.invVarRespQAtV3),
        inv_var_resp_q_at_v4=float_or_none(pb.invVarRespQAtV4),
        inv_reactive_power_mode=None if pb.HasField("invReactivePowerModeNull") else pb.invReactivePowerModeSet,
        inv_fix_reactive_power=float_or_none(pb.invFixReactivePower)
    )

    for mrid in pb.powerElectronicsUnitMRIDs:
        network_service.resolve_or_defer_reference(resolver.power_electronics_unit(cim), mrid)
    for mrid in pb.powerElectronicsConnectionPhaseMRIDs:
        network_service.resolve_or_defer_reference(resolver.power_electronics_connection_phase(cim), mrid)

    regulating_cond_eq_to_cim(pb.rce, cim, network_service)
    return cim if network_service.add(cim) else None


def power_electronics_connection_phase_to_cim(
    pb: PBPowerElectronicsConnectionPhase,
    network_service: NetworkService
) -> Optional[PowerElectronicsConnectionPhase]:
    # noinspection PyUnresolvedReferences
    cim = PowerElectronicsConnectionPhase(
        mrid=pb.mrid(),
        p=float_or_none(pb.p),
        q=float_or_none(pb.q),
        phase=single_phase_kind_by_id(pb.phase)
    )

    network_service.resolve_or_defer_reference(resolver.phase_power_electronics_connection(cim), pb.powerElectronicsConnectionMRID)

    power_system_resource_to_cim(pb.psr, cim, network_service)
    return cim if network_service.add(cim) else None


def power_transformer_to_cim(pb: PBPowerTransformer, network_service: NetworkService) -> Optional[PowerTransformer]:
    # noinspection PyUnresolvedReferences
    cim = PowerTransformer(
        mrid=pb.mrid(),
        vector_group=VectorGroup(pb.vectorGroup),
        transformer_utilisation=float_or_none(pb.transformerUtilisation),
        construction_kind=TransformerConstructionKind(pb.constructionKind),
        function=TransformerFunctionKind(pb.function)
    )

    for mrid in pb.powerTransformerEndMRIDs:
        network_service.resolve_or_defer_reference(resolver.ends(cim), mrid)
    # noinspection PyUnresolvedReferences
    network_service.resolve_or_defer_reference(resolver.power_transformer_info(cim), pb.asset_info_mrid())

    conducting_equipment_to_cim(pb.ce, cim, network_service)
    return cim if network_service.add(cim) else None


def power_transformer_end_to_cim(pb: PBPowerTransformerEnd, network_service: NetworkService) -> Optional[PowerTransformerEnd]:
    # noinspection PyUnresolvedReferences
    cim = PowerTransformerEnd(
        mrid=pb.mrid(),
        rated_u=int_or_none(pb.ratedU),
        r=float_or_none(pb.r),
        r0=float_or_none(pb.r0),
        x=float_or_none(pb.x),
        x0=float_or_none(pb.x0),
        b=float_or_none(pb.b),
        b0=float_or_none(pb.b0),
        g=float_or_none(pb.g),
        g0=float_or_none(pb.g0),
        connection_kind=WindingConnection(pb.connectionKind),
        phase_angle_clock=int_or_none(pb.phaseAngleClock)
    )

    for rating in pb.ratings:
        cim.add_transformer_end_rated_s(transformer_end_rated_s_to_cim(rating))

    # Set end number before associating with power transformer to prevent incorrectly sorted cim.power_transformer.ends
    transformer_end_to_cim(pb.te, cim, network_service)

    network_service.resolve_or_defer_reference(resolver.power_transformer(cim), pb.powerTransformerMRID)
    return cim if network_service.add(cim) else None


def protected_switch_to_cim(pb: PBProtectedSwitch, cim: ProtectedSwitch, network_service: NetworkService):
    cim.breaking_capacity = int_or_none(pb.breakingCapacity)

    for mrid in pb.relayFunctionMRIDs:
        network_service.resolve_or_defer_reference(resolver.ps_relay_function(cim), mrid)

    switch_to_cim(pb.sw, cim, network_service)


def ratio_tap_changer_to_cim(pb: PBRatioTapChanger, network_service: NetworkService) -> Optional[RatioTapChanger]:
    # noinspection PyUnresolvedReferences
    cim = RatioTapChanger(
        mrid=pb.mrid(),
        step_voltage_increment=float_or_none(pb.stepVoltageIncrement)
    )

    network_service.resolve_or_defer_reference(resolver.transformer_end(cim), pb.transformerEndMRID)

    tap_changer_to_cim(pb.tc, cim, network_service)
    return cim if network_service.add(cim) else None


def reactive_capability_curve_to_cim(pb: PBReactiveCapabilityCurve, network_service: NetworkService) -> Optional[ReactiveCapabilityCurve]:
    # noinspection PyUnresolvedReferences
    cim = ReactiveCapabilityCurve(mrid=pb.mrid())

    curve_to_cim(pb.c, cim, network_service)
    return cim if network_service.add(cim) else None


def recloser_to_cim(pb: PBRecloser, network_service: NetworkService) -> Optional[Recloser]:
    # noinspection PyUnresolvedReferences
    cim = Recloser(mrid=pb.mrid())

    protected_switch_to_cim(pb.sw, cim, network_service)
    return cim if network_service.add(cim) else None


def regulating_cond_eq_to_cim(pb: PBRegulatingCondEq, cim: RegulatingCondEq, network_service: NetworkService):
    cim.control_enabled = pb.controlEnabled
    network_service.resolve_or_defer_reference(resolver.rce_regulating_control(cim), pb.regulatingControlMRID)

    energy_connection_to_cim(pb.ec, cim, network_service)


def regulating_control_to_cim(pb: PBRegulatingControl, cim: RegulatingControl, network_service: NetworkService):
    cim.discrete = None if pb.HasField("discreteNull") else pb.discreteSet
    cim.mode = RegulatingControlModeKind(pb.mode)
    cim.monitored_phase = phase_code_by_id(pb.monitoredPhase)
    cim.target_deadband = float_or_none(pb.targetDeadband)
    cim.target_value = float_or_none(pb.targetValue)
    cim.enabled = None if pb.HasField("enabledNull") else pb.enabledSet
    cim.max_allowed_target_value = float_or_none(pb.maxAllowedTargetValue)
    cim.min_allowed_target_value = float_or_none(pb.minAllowedTargetValue)
    cim.rated_current = float_or_none(pb.ratedCurrent)
    network_service.resolve_or_defer_reference(resolver.rc_terminal(cim), pb.terminalMRID)
    for mrid in pb.regulatingCondEqMRIDs:
        network_service.resolve_or_defer_reference(resolver.rc_regulating_cond_eq(cim), mrid)
    cim.ct_primary = float_or_none(pb.ctPrimary)
    cim.min_target_deadband = float_or_none(pb.minTargetDeadband)

    power_system_resource_to_cim(pb.psr, cim, network_service)


def rotating_machine_to_cim(pb: PBRotatingMachine, cim: RotatingMachine, network_service: NetworkService):
    cim.rated_power_factor = float_or_none(pb.ratedPowerFactor)
    cim.rated_s = float_or_none(pb.ratedS)
    cim.rated_u = int_or_none(pb.ratedU)
    cim.p = float_or_none(pb.p)
    cim.q = float_or_none(pb.q)

    regulating_cond_eq_to_cim(pb.rce, cim, network_service)


def series_compensator_to_cim(pb: PBSeriesCompensator, network_service: NetworkService) -> Optional[SeriesCompensator]:
    # noinspection PyUnresolvedReferences
    cim = SeriesCompensator(
        mrid=pb.mrid(),
        r=float_or_none(pb.r),
        r0=float_or_none(pb.r0),
        x=float_or_none(pb.x),
        x0=float_or_none(pb.x0),
        varistor_rated_current=int_or_none(pb.varistorRatedCurrent),
        varistor_voltage_threshold=int_or_none(pb.varistorVoltageThreshold)
    )

    conducting_equipment_to_cim(pb.ce, cim, network_service)
    return cim if network_service.add(cim) else None


def shunt_compensator_to_cim(pb: PBShuntCompensator, cim: ShuntCompensator, network_service: NetworkService):
    # noinspection PyUnresolvedReferences
    network_service.resolve_or_defer_reference(resolver.shunt_compensator_info(cim), pb.asset_info_mrid())
    cim.sections = float_or_none(pb.sections)
    cim.grounded = pb.grounded
    cim.nom_u = int_or_none(pb.nomU)
    cim.phase_connection = PhaseShuntConnectionKind(pb.phaseConnection)

    regulating_cond_eq_to_cim(pb.rce, cim, network_service)


def static_var_compensator_to_cim(pb: PBStaticVarCompensator, network_service: NetworkService):
    """
    Convert the protobuf :class:`PBStaticVarCompensator` into its CIM counterpart.
    :param pb: The protobuf :class:`PBStaticVarCompensator` to convert.
    :param network_service: The :class:`NetworkService` the converted CIM object will be added to.
    :return: The converted `pb` as a CIM :class:`StaticVarCompensator`
    """
    # noinspection PyUnresolvedReferences
    cim = StaticVarCompensator(
        mrid=pb.mrid(),
        capacitive_rating=float_or_none(pb.capacitiveRating),
        inductive_rating=float_or_none(pb.inductiveRating),
        q=float_or_none(pb.q),
        svc_control_mode=SVCControlMode(pb.svcControlMode),
        voltage_set_point=int_or_none(pb.voltageSetPoint)
    )

    regulating_cond_eq_to_cim(pb.rce, cim, network_service)
    return cim if network_service.add(cim) else None


def switch_to_cim(pb: PBSwitch, cim: Switch, network_service: NetworkService):
    # noinspection PyUnresolvedReferences
    network_service.resolve_or_defer_reference(resolver.switch_info(cim), pb.asset_info_mrid())
    cim.rated_current = float_or_none(pb.ratedCurrent)
    cim.set_normally_open(pb.normalOpen)
    cim.set_open(pb.open)

    conducting_equipment_to_cim(pb.ce, cim, network_service)


def synchronous_machine_to_cim(pb: PBSynchronousMachine, network_service: NetworkService) -> Optional[SynchronousMachine]:
    # noinspection PyUnresolvedReferences
    cim = SynchronousMachine(
        mrid=pb.mrid(),
        base_q=float_or_none(pb.baseQ),
        condenser_p=int_or_none(pb.condenserP),
        earthing=pb.earthing,
        earthing_star_point_r=float_or_none(pb.earthingStarPointR),
        earthing_star_point_x=float_or_none(pb.earthingStarPointX),
        ikk=float_or_none(pb.ikk),
        max_q=float_or_none(pb.maxQ),
        max_u=int_or_none(pb.maxU),
        min_q=float_or_none(pb.minQ),
        min_u=int_or_none(pb.minU),
        mu=float_or_none(pb.mu),
        r=float_or_none(pb.r),
        r0=float_or_none(pb.r0),
        r2=float_or_none(pb.r2),
        sat_direct_subtrans_x=float_or_none(pb.satDirectSubtransX),
        sat_direct_sync_x=float_or_none(pb.satDirectSyncX),
        sat_direct_trans_x=float_or_none(pb.satDirectTransX),
        x0=float_or_none(pb.x0),
        x2=float_or_none(pb.x2),
        type=SynchronousMachineKind(pb.type),
        operating_mode=SynchronousMachineKind(pb.operatingMode)
    )

    for mrid in pb.reactiveCapabilityCurveMRIDs:
        network_service.resolve_or_defer_reference(resolver.reactive_capability_curve(cim), mrid)

    rotating_machine_to_cim(pb.rm, cim, network_service)
    return cim if network_service.add(cim) else None


def tap_changer_to_cim(pb: PBTapChanger, cim: TapChanger, network_service: NetworkService):
    cim.high_step = int_or_none(pb.highStep)
    cim.step = float_or_none(pb.step)
    cim.neutral_step = int_or_none(pb.neutralStep)
    cim.normal_step = int_or_none(pb.normalStep)
    cim.low_step = int_or_none(pb.lowStep)
    cim.neutral_u = int_or_none(pb.neutralU)
    cim.control_enabled = pb.controlEnabled
    network_service.resolve_or_defer_reference(resolver.tc_tap_changer_control(cim), pb.tapChangerControlMRID)

    power_system_resource_to_cim(pb.psr, cim, network_service)


def tap_changer_control_to_cim(pb: PBTapChangerControl, network_service: NetworkService) -> Optional[TapChangerControl]:
    # noinspection PyUnresolvedReferences
    cim = TapChangerControl(
        mrid=pb.mrid(),
        limit_voltage=int_or_none(pb.limitVoltage),
        line_drop_compensation=None if pb.HasField("lineDropCompensationNull") else pb.lineDropCompensationSet,
        line_drop_r=float_or_none(pb.lineDropR),
        line_drop_x=float_or_none(pb.lineDropX),
        reverse_line_drop_r=float_or_none(pb.reverseLineDropR),
        reverse_line_drop_x=float_or_none(pb.reverseLineDropX),
        forward_ldc_blocking=None if pb.HasField("forwardLDCBlockingNull") else pb.forwardLDCBlockingSet,
        time_delay=float_or_none(pb.timeDelay),
        co_generation_enabled=None if pb.HasField("coGenerationEnabledNull") else pb.coGenerationEnabledSet
    )

    regulating_control_to_cim(pb.rc, cim, network_service)
    return cim if network_service.add(cim) else None


def transformer_end_to_cim(pb: PBTransformerEnd, cim: TransformerEnd, network_service: NetworkService):
    cim.end_number = pb.endNumber
    cim.grounded = pb.grounded
    cim.r_ground = float_or_none(pb.rGround)
    cim.x_ground = float_or_none(pb.xGround)

    network_service.resolve_or_defer_reference(resolver.te_terminal(cim), pb.terminalMRID)
    network_service.resolve_or_defer_reference(resolver.te_base_voltage(cim), pb.baseVoltageMRID)
    network_service.resolve_or_defer_reference(resolver.ratio_tap_changer(cim), pb.ratioTapChangerMRID)
    network_service.resolve_or_defer_reference(resolver.transformer_end_transformer_star_impedance(cim), pb.starImpedanceMRID)

    identified_object_to_cim(pb.io, cim, network_service)


def transformer_end_rated_s_to_cim(pb: PBTransformerEndRatedS) -> Optional[TransformerEndRatedS]:
    return TransformerEndRatedS(cooling_type=TransformerCoolingType(pb.coolingType), rated_s=pb.ratedS)


def transformer_star_impedance_to_cim(pb: PBTransformerStarImpedance, network_service: NetworkService) -> Optional[TransformerStarImpedance]:
    # noinspection PyUnresolvedReferences
    cim = TransformerStarImpedance(mrid=pb.mrid(), r=pb.r, r0=pb.r0, x=pb.x, x0=pb.x0)

    network_service.resolve_or_defer_reference(resolver.star_impedance_transformer_end_info(cim), pb.transformerEndInfoMRID)

    identified_object_to_cim(pb.io, cim, network_service)
    return cim if network_service.add(cim) else None


PBAcLineSegment.to_cim = ac_line_segment_to_cim
PBBreaker.to_cim = breaker_to_cim
PBBusbarSection.to_cim = busbar_section_to_cim
PBClamp.to_cim = clamp_to_cim
PBCut.to_cim = cut_to_cim
PBDisconnector.to_cim = disconnector_to_cim
PBEnergyConsumer.to_cim = energy_consumer_to_cim
PBEnergyConsumerPhase.to_cim = energy_consumer_phase_to_cim
PBEnergySource.to_cim = energy_source_to_cim
PBEnergySourcePhase.to_cim = energy_source_phase_to_cim
PBFuse.to_cim = fuse_to_cim
PBGround.to_cim = ground_to_cim
PBGroundDisconnector.to_cim = ground_disconnector_to_cim
PBGroundingImpedance.to_cim = grounding_impedance_to_cim
PBJumper.to_cim = jumper_to_cim
PBJunction.to_cim = junction_to_cim
PBLinearShuntCompensator.to_cim = linear_shunt_compensator_to_cim
PBLoadBreakSwitch.to_cim = load_break_switch_to_cim
PBPerLengthPhaseImpedance.to_cim = per_length_phase_impedance_to_cim
PBPerLengthSequenceImpedance.to_cim = per_length_sequence_impedance_to_cim
PBPetersenCoil.to_cim = petersen_coil_to_cim
PBPowerElectronicsConnection.to_cim = power_electronics_connection_to_cim
PBPowerElectronicsConnectionPhase.to_cim = power_electronics_connection_phase_to_cim
PBPowerTransformer.to_cim = power_transformer_to_cim
PBPowerTransformerEnd.to_cim = power_transformer_end_to_cim
PBRatioTapChanger.to_cim = ratio_tap_changer_to_cim
PBReactiveCapabilityCurve.to_cim = reactive_capability_curve_to_cim
PBRecloser.to_cim = recloser_to_cim
PBSeriesCompensator.to_cim = series_compensator_to_cim
PBStaticVarCompensator.to_cim = static_var_compensator_to_cim
PBSynchronousMachine.to_cim = synchronous_machine_to_cim
PBTapChangerControl.to_cim = tap_changer_control_to_cim
PBTransformerStarImpedance.to_cim = transformer_star_impedance_to_cim


###############################
# IEC61970 InfIEC61970 Feeder #
###############################

def circuit_to_cim(pb: PBCircuit, network_service: NetworkService) -> Optional[Circuit]:
    # noinspection PyUnresolvedReferences
    cim = Circuit(mrid=pb.mrid())

    network_service.resolve_or_defer_reference(resolver.loop(cim), pb.loopMRID)
    for mrid in pb.endTerminalMRIDs:
        network_service.resolve_or_defer_reference(resolver.end_terminal(cim), mrid)
    for mrid in pb.endSubstationMRIDs:
        network_service.resolve_or_defer_reference(resolver.end_substation(cim), mrid)

    line_to_cim(pb.l, cim, network_service)
    return cim if network_service.add(cim) else None


PBCircuit.to_cim = circuit_to_cim
