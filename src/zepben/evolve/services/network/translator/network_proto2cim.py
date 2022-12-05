#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Optional

from zepben.protobuf.cim.iec61968.assetinfo.CableInfo_pb2 import CableInfo as PBCableInfo
from zepben.protobuf.cim.iec61968.assetinfo.NoLoadTest_pb2 import NoLoadTest as PBNoLoadTest
from zepben.protobuf.cim.iec61968.assetinfo.OpenCircuitTest_pb2 import OpenCircuitTest as PBOpenCircuitTest
from zepben.protobuf.cim.iec61968.assetinfo.OverheadWireInfo_pb2 import OverheadWireInfo as PBOverheadWireInfo
from zepben.protobuf.cim.iec61968.assetinfo.PowerTransformerInfo_pb2 import PowerTransformerInfo as PBPowerTransformerInfo
from zepben.protobuf.cim.iec61968.assetinfo.ShortCircuitTest_pb2 import ShortCircuitTest as PBShortCircuitTest
from zepben.protobuf.cim.iec61968.assetinfo.ShuntCompensatorInfo_pb2 import ShuntCompensatorInfo as PBShuntCompensatorInfo
from zepben.protobuf.cim.iec61968.assetinfo.TransformerEndInfo_pb2 import TransformerEndInfo as PBTransformerEndInfo
from zepben.protobuf.cim.iec61968.assetinfo.TransformerTankInfo_pb2 import TransformerTankInfo as PBTransformerTankInfo
from zepben.protobuf.cim.iec61968.assetinfo.TransformerTest_pb2 import TransformerTest as PBTransformerTest
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
from zepben.protobuf.cim.iec61968.common.StreetDetail_pb2 import StreetDetail as PBStreetDetail
from zepben.protobuf.cim.iec61968.common.TownDetail_pb2 import TownDetail as PBTownDetail
from zepben.protobuf.cim.iec61968.infiec61968.infassetinfo.CurrentTransformerInfo_pb2 import CurrentTransformerInfo as PBCurrentTransformerInfo
from zepben.protobuf.cim.iec61968.infiec61968.infassetinfo.PotentialTransformerInfo_pb2 import PotentialTransformerInfo as PBPotentialTransformerInfo
from zepben.protobuf.cim.iec61968.infiec61968.infcommon.Ratio_pb2 import Ratio as PBRatio
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
from zepben.protobuf.cim.iec61970.base.core.EquipmentContainer_pb2 import EquipmentContainer as PBEquipmentContainer
from zepben.protobuf.cim.iec61970.base.core.Equipment_pb2 import Equipment as PBEquipment
from zepben.protobuf.cim.iec61970.base.core.Feeder_pb2 import Feeder as PBFeeder
from zepben.protobuf.cim.iec61970.base.core.GeographicalRegion_pb2 import GeographicalRegion as PBGeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.PowerSystemResource_pb2 import PowerSystemResource as PBPowerSystemResource
from zepben.protobuf.cim.iec61970.base.core.Site_pb2 import Site as PBSite
from zepben.protobuf.cim.iec61970.base.core.SubGeographicalRegion_pb2 import SubGeographicalRegion as PBSubGeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.Substation_pb2 import Substation as PBSubstation
from zepben.protobuf.cim.iec61970.base.core.Terminal_pb2 import Terminal as PBTerminal
from zepben.protobuf.cim.iec61970.base.equivalents.EquivalentBranch_pb2 import EquivalentBranch as PBEquivalentBranch
from zepben.protobuf.cim.iec61970.base.equivalents.EquivalentEquipment_pb2 import EquivalentEquipment as PBEquivalentEquipment
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
from zepben.protobuf.cim.iec61970.base.wires.PowerElectronicsConnectionPhase_pb2 import PowerElectronicsConnectionPhase as PBPowerElectronicsConnectionPhase
from zepben.protobuf.cim.iec61970.base.wires.PowerElectronicsConnection_pb2 import PowerElectronicsConnection as PBPowerElectronicsConnection
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
from zepben.protobuf.cim.iec61970.base.wires.TransformerStarImpedance_pb2 import TransformerStarImpedance as PBTransformerStarImpedance
from zepben.protobuf.cim.iec61970.base.wires.generation.production.BatteryUnit_pb2 import BatteryUnit as PBBatteryUnit
from zepben.protobuf.cim.iec61970.base.wires.generation.production.PhotoVoltaicUnit_pb2 import PhotoVoltaicUnit as PBPhotoVoltaicUnit
from zepben.protobuf.cim.iec61970.base.wires.generation.production.PowerElectronicsUnit_pb2 import PowerElectronicsUnit as PBPowerElectronicsUnit
from zepben.protobuf.cim.iec61970.base.wires.generation.production.PowerElectronicsWindUnit_pb2 import PowerElectronicsWindUnit as PBPowerElectronicsWindUnit
from zepben.protobuf.cim.iec61970.infiec61970.feeder.Circuit_pb2 import Circuit as PBCircuit
from zepben.protobuf.cim.iec61970.infiec61970.feeder.Loop_pb2 import Loop as PBLoop
from zepben.protobuf.cim.iec61970.infiec61970.feeder.LvFeeder_pb2 import LvFeeder as PBLvFeeder

from zepben.evolve.model.cim.iec61968.assetinfo.no_load_test import *
from zepben.evolve.model.cim.iec61968.assetinfo.open_circuit_test import *
from zepben.evolve.model.cim.iec61968.assetinfo.power_transformer_info import *
from zepben.evolve.model.cim.iec61968.assetinfo.short_circuit_test import *
from zepben.evolve.model.cim.iec61968.assetinfo.shunt_compensator_info import *
from zepben.evolve.model.cim.iec61968.assetinfo.transformer_end_info import *
from zepben.evolve.model.cim.iec61968.assetinfo.transformer_tank_info import *
from zepben.evolve.model.cim.iec61968.assetinfo.transformer_test import *
from zepben.evolve.model.cim.iec61968.assetinfo.wire_info import *
from zepben.evolve.model.cim.iec61968.assetinfo.wire_material_kind import *
from zepben.evolve.model.cim.iec61968.assets.asset import *
from zepben.evolve.model.cim.iec61968.assets.asset_info import *
from zepben.evolve.model.cim.iec61968.assets.asset_organisation_role import *
from zepben.evolve.model.cim.iec61968.assets.pole import *
from zepben.evolve.model.cim.iec61968.assets.streetlight import *
from zepben.evolve.model.cim.iec61968.assets.structure import *
from zepben.evolve.model.cim.iec61968.common.location import *
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.current_transformer_info import *
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.potential_transformer_info import *
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.transformer_construction_kind import *
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.transformer_function_kind import *
from zepben.evolve.model.cim.iec61968.infiec61968.infcommon.ratio import *
from zepben.evolve.model.cim.iec61968.metering.metering import *
from zepben.evolve.model.cim.iec61968.operations.operational_restriction import *
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.auxiliary_equipment import *
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.current_transformer import *
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.potential_transformer import *
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.potential_transformer_kind import *
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.sensor import *
from zepben.evolve.model.cim.iec61970.base.core.base_voltage import *
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import *
from zepben.evolve.model.cim.iec61970.base.core.connectivity_node import *
from zepben.evolve.model.cim.iec61970.base.core.connectivity_node_container import *
from zepben.evolve.model.cim.iec61970.base.core.equipment import *
from zepben.evolve.model.cim.iec61970.base.core.equipment_container import *
from zepben.evolve.model.cim.iec61970.base.core.phase_code import *
from zepben.evolve.model.cim.iec61970.base.core.power_system_resource import *
from zepben.evolve.model.cim.iec61970.base.core.regions import *
from zepben.evolve.model.cim.iec61970.base.core.substation import *
from zepben.evolve.model.cim.iec61970.base.core.terminal import *
from zepben.evolve.model.cim.iec61970.base.domain.unit_symbol import *
from zepben.evolve.model.cim.iec61970.base.equivalents.equivalent_branch import *
from zepben.evolve.model.cim.iec61970.base.equivalents.equivalent_equipment import *
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
from zepben.evolve.model.cim.iec61970.base.wires.generation.production.battery_state_kind import *
from zepben.evolve.model.cim.iec61970.base.wires.generation.production.power_electronics_unit import *
from zepben.evolve.model.cim.iec61970.base.wires.line import *
from zepben.evolve.model.cim.iec61970.base.wires.per_length import *
from zepben.evolve.model.cim.iec61970.base.wires.phase_shunt_connection_kind import *
from zepben.evolve.model.cim.iec61970.base.wires.power_electronics_connection import *
from zepben.evolve.model.cim.iec61970.base.wires.power_transformer import *
from zepben.evolve.model.cim.iec61970.base.wires.shunt_compensator import *
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import *
from zepben.evolve.model.cim.iec61970.base.wires.switch import *
from zepben.evolve.model.cim.iec61970.base.wires.transformer_star_impedance import *
from zepben.evolve.model.cim.iec61970.base.wires.vector_group import *
from zepben.evolve.model.cim.iec61970.base.wires.winding_connection import *
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.circuit import *
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.loop import *
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.lv_feeder import *
from zepben.evolve.model.phases import TracedPhases

import zepben.evolve.services.common.resolver as resolver
from zepben.evolve.services.common.translator.base_proto2cim import identified_object_to_cim, organisation_role_to_cim, document_to_cim
from zepben.evolve.services.common.translator.util import int_or_none, float_or_none, long_or_none, str_or_none, uint_or_none
from zepben.evolve.services.network.network_service import NetworkService
from zepben.evolve.services.network.tracing.feeder.feeder_direction import FeederDirection

__all__ = [
    "cable_info_to_cim", "no_load_test_to_cim", "open_circuit_test_to_cim", "overhead_wire_info_to_cim", "power_transformer_info_to_cim",
    "short_circuit_test_to_cim", "shunt_compensator_info_to_cim", "transformer_end_info_to_cim", "transformer_tank_info_to_cim", "transformer_test_to_cim",
    "wire_info_to_cim", "asset_to_cim", "asset_container_to_cim", "asset_info_to_cim", "asset_organisation_role_to_cim", "asset_owner_to_cim", "pole_to_cim",
    "streetlight_to_cim", "structure_to_cim", "location_to_cim", "position_point_to_cim", "street_address_to_cim", "town_detail_to_cim", "end_device_to_cim",
    "meter_to_cim", "usage_point_to_cim", "operational_restriction_to_cim", "auxiliary_equipment_to_cim", "fault_indicator_to_cim", "ac_dc_terminal_to_cim",
    "base_voltage_to_cim", "conducting_equipment_to_cim", "connectivity_node_to_cim", "connectivity_node_container_to_cim", "equipment_to_cim",
    "equipment_container_to_cim", "feeder_to_cim", "geographical_region_to_cim", "power_system_resource_to_cim", "site_to_cim",
    "sub_geographical_region_to_cim", "substation_to_cim", "terminal_to_cim", "equivalent_branch_to_cim", "equivalent_equipment_to_cim", "accumulator_to_cim",
    "analog_to_cim", "control_to_cim", "discrete_to_cim", "io_point_to_cim", "measurement_to_cim", "remote_control_to_cim", "remote_point_to_cim",
    "remote_source_to_cim", "battery_unit_to_cim", "photo_voltaic_unit_to_cim", "power_electronics_unit_to_cim", "power_electronics_wind_unit_to_cim",
    "ac_line_segment_to_cim", "breaker_to_cim", "conductor_to_cim", "connector_to_cim", "disconnector_to_cim", "energy_connection_to_cim",
    "energy_consumer_to_cim", "energy_consumer_phase_to_cim", "energy_source_to_cim", "energy_source_phase_to_cim", "fuse_to_cim", "jumper_to_cim",
    "junction_to_cim", "busbar_section_to_cim", "line_to_cim", "linear_shunt_compensator_to_cim", "load_break_switch_to_cim",
    "per_length_line_parameter_to_cim", "per_length_impedance_to_cim", "per_length_sequence_impedance_to_cim", "power_electronics_connection_to_cim",
    "power_electronics_connection_phase_to_cim", "power_transformer_to_cim", "power_transformer_end_to_cim", "transformer_star_impedance_to_cim",
    "protected_switch_to_cim", "ratio_tap_changer_to_cim", "recloser_to_cim", "regulating_cond_eq_to_cim", "shunt_compensator_to_cim", "switch_to_cim",
    "tap_changer_to_cim", "transformer_end_to_cim", "circuit_to_cim", "loop_to_cim", "lv_feeder_to_cim", "current_transformer_info_to_cim",
    "potential_transformer_info_to_cim", "current_transformer_to_cim", "potential_transformer_to_cim"
]


#######################
# IEC61968 ASSET INFO #
#######################


def cable_info_to_cim(pb: PBCableInfo, network_service: NetworkService) -> Optional[CableInfo]:
    # noinspection PyArgumentList
    cim = CableInfo(mrid=pb.mrid())

    wire_info_to_cim(pb.wi, cim, network_service)
    return cim if network_service.add(cim) else None


def no_load_test_to_cim(pb: PBNoLoadTest, network_service: NetworkService) -> Optional[NoLoadTest]:
    # noinspection PyArgumentList
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
    # noinspection PyArgumentList
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
    # noinspection PyArgumentList
    cim = OverheadWireInfo(mrid=pb.mrid())

    wire_info_to_cim(pb.wi, cim, network_service)
    return cim if network_service.add(cim) else None


def power_transformer_info_to_cim(pb: PBPowerTransformerInfo, network_service: NetworkService) -> Optional[PowerTransformerInfo]:
    cim = PowerTransformerInfo(mrid=pb.mrid())

    for mrid in pb.transformerTankInfoMRIDs:
        network_service.resolve_or_defer_reference(resolver.power_transformer_info_transformer_tank_info(cim), mrid)

    asset_info_to_cim(pb.ai, cim, network_service)
    return cim if network_service.add(cim) else None


def short_circuit_test_to_cim(pb: PBShortCircuitTest, network_service: NetworkService) -> Optional[ShortCircuitTest]:
    # noinspection PyArgumentList
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
    cim = ShuntCompensatorInfo(
        mrid=pb.mrid(),
        max_power_loss=int_or_none(pb.maxPowerLoss),
        rated_current=int_or_none(pb.ratedCurrent),
        rated_reactive_power=int_or_none(pb.ratedReactivePower),
        rated_voltage=int_or_none(pb.ratedVoltage),
    )

    asset_info_to_cim(pb.ai, cim, network_service)
    return cim if network_service.add(cim) else None


def transformer_end_info_to_cim(pb: PBTransformerEndInfo, network_service: NetworkService) -> Optional[TransformerEndInfo]:
    # noinspection PyArgumentList
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
PBTransformerEndInfo.to_cim = transformer_end_info_to_cim
PBTransformerTankInfo.to_cim = transformer_tank_info_to_cim
PBTransformerTest.to_cim = transformer_test_to_cim
PBWireInfo.to_cim = wire_info_to_cim


###################
# IEC61968 ASSETS #
###################

def asset_to_cim(pb: PBAsset, cim: Asset, network_service: NetworkService):
    network_service.resolve_or_defer_reference(resolver.at_location(cim), pb.locationMRID)

    for mrid in pb.organisationRoleMRIDs:
        network_service.resolve_or_defer_reference(resolver.organisation_roles(cim), mrid)

    identified_object_to_cim(pb.io, cim, network_service)


def asset_container_to_cim(pb: PBAssetContainer, cim: AssetContainer, network_service: NetworkService):
    asset_to_cim(pb.at, cim, network_service)


def asset_info_to_cim(pb: PBAssetInfo, cim: AssetInfo, network_service: NetworkService):
    identified_object_to_cim(pb.io, cim, network_service)


def asset_organisation_role_to_cim(pb: PBAssetOrganisationRole, cim: AssetOrganisationRole,
                                   network_service: NetworkService):
    organisation_role_to_cim(getattr(pb, 'or'), cim, network_service)


def asset_owner_to_cim(pb: PBAssetOwner, network_service: NetworkService) -> Optional[AssetOwner]:
    # noinspection PyArgumentList
    cim = AssetOwner(mrid=pb.mrid())

    asset_organisation_role_to_cim(pb.aor, cim, network_service)
    return cim if network_service.add(cim) else None


def pole_to_cim(pb: PBPole, network_service: NetworkService) -> Optional[Pole]:
    cim = Pole(mrid=pb.mrid(), classification=pb.classification)

    for mrid in pb.streetlightMRIDs:
        network_service.resolve_or_defer_reference(resolver.streetlights(cim), mrid)

    structure_to_cim(pb.st, cim, network_service)
    return cim if network_service.add(cim) else None


def streetlight_to_cim(pb: PBStreetlight, network_service: NetworkService) -> Optional[Streetlight]:
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


PBAsset.to_cim = asset_to_cim
PBAssetContainer.to_cim = asset_container_to_cim
PBAssetInfo.to_cim = asset_info_to_cim
PBAssetOrganisationRole.to_cim = asset_organisation_role_to_cim
PBAssetOwner.to_cim = asset_owner_to_cim
PBPole.to_cim = pole_to_cim
PBStreetlight.to_cim = streetlight_to_cim
PBStructure.to_cim = structure_to_cim


###################
# IEC61968 COMMON #
###################

def location_to_cim(pb: PBLocation, network_service: NetworkService) -> Optional[Location]:
    cim = Location(mrid=pb.mrid(), main_address=street_address_to_cim(pb.mainAddress) if pb.HasField('mainAddress') else None)

    for point in pb.positionPoints:
        cim.add_point(position_point_to_cim(point))

    identified_object_to_cim(pb.io, cim, network_service)
    return cim if network_service.add(cim) else None


def position_point_to_cim(pb: PBPositionPoint) -> Optional[PositionPoint]:
    # noinspection PyArgumentList
    return PositionPoint(pb.xPosition, pb.yPosition)


def street_address_to_cim(pb: PBStreetAddress) -> Optional[StreetAddress]:
    # noinspection PyArgumentList
    return StreetAddress(
        postal_code=pb.postalCode,
        town_detail=town_detail_to_cim(pb.townDetail) if pb.HasField('townDetail') else None,
        po_box=pb.poBox,
        street_detail=street_detail_to_cim(pb.streetDetail) if pb.HasField('streetDetail') else None
    )


def street_detail_to_cim(pb: PBStreetDetail) -> Optional[StreetDetail]:
    # noinspection PyArgumentList
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
    # noinspection PyArgumentList
    return TownDetail(name=pb.name, state_or_province=pb.stateOrProvince)


PBLocation.to_cim = location_to_cim
PBPositionPoint.to_cim = position_point_to_cim
PBStreetAddress.to_cim = street_address_to_cim
PBStreetDetail.to_cim = street_detail_to_cim
PBTownDetail.to_cim = town_detail_to_cim


#####################################
# IEC61968 infIEC61968 InfAssetInfo #
#####################################

def current_transformer_info_to_cim(pb: PBCurrentTransformerInfo, network_service: NetworkService) -> Optional[CurrentTransformerInfo]:
    cim = CurrentTransformerInfo(
        mrid=pb.mrid(),
        accuracy_class=str_or_none(pb.accuracyClass),
        accuracy_limit=float_or_none(pb.accuracyLimit),
        core_count=int_or_none(pb.coreCount),
        ct_class=str_or_none(pb.ctClass),
        knee_point_voltage=int_or_none(pb.kneePointVoltage),
        max_ratio=ratio_to_cim(pb.maxRatio) if pb.HasField('maxRatio') else None,
        nominal_ratio=ratio_to_cim(pb.nominalRatio) if pb.HasField('nominalRatio') else None,
        primary_ratio=float_or_none(pb.primaryRatio),
        rated_current=int_or_none(pb.ratedCurrent),
        secondary_fls_rating=int_or_none(pb.secondaryFlsRating),
        secondary_ratio=float_or_none(pb.secondaryRatio),
        usage=str_or_none(pb.usage)
    )

    asset_info_to_cim(pb.ai, cim, network_service)
    return cim if network_service.add(cim) else None


def potential_transformer_info_to_cim(pb: PBPotentialTransformerInfo, network_service: NetworkService) -> Optional[PotentialTransformerInfo]:
    cim = PotentialTransformerInfo(
        mrid=pb.mrid(),
        accuracy_class=str_or_none(pb.accuracyClass),
        nominal_ratio=ratio_to_cim(pb.nominalRatio) if pb.HasField('nominalRatio') else None,
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
# IEC61968 infIEC61968 InfCommon #
##################################

def ratio_to_cim(pb: PBRatio) -> Ratio:
    return Ratio(pb.numerator, pb.denominator)


PBRatio.to_cim = ratio_to_cim


#####################
# IEC61968 METERING #
#####################


def end_device_to_cim(pb: PBEndDevice, cim: EndDevice, network_service: NetworkService):
    cim.customer_mrid = pb.customerMRID if pb.customerMRID else None

    for mrid in pb.usagePointMRIDs:
        network_service.resolve_or_defer_reference(resolver.ed_usage_points(cim), mrid)

    network_service.resolve_or_defer_reference(resolver.service_location(cim), pb.serviceLocationMRID)
    asset_container_to_cim(pb.ac, cim, network_service)


def meter_to_cim(pb: PBMeter, network_service: NetworkService) -> Optional[Meter]:
    cim = Meter(mrid=pb.mrid())

    end_device_to_cim(pb.ed, cim, network_service)
    return cim if network_service.add(cim) else None


def usage_point_to_cim(pb: PBUsagePoint, network_service: NetworkService) -> Optional[UsagePoint]:
    cim = UsagePoint(mrid=pb.mrid())

    network_service.resolve_or_defer_reference(resolver.usage_point_location(cim), pb.usagePointLocationMRID)
    cim.is_virtual = pb.isVirtual
    cim.connection_category = pb.connectionCategory if pb.connectionCategory else None
    for mrid in pb.equipmentMRIDs:
        network_service.resolve_or_defer_reference(resolver.up_equipment(cim), mrid)
    for mrid in pb.endDeviceMRIDs:
        network_service.resolve_or_defer_reference(resolver.end_devices(cim), mrid)

    identified_object_to_cim(pb.io, cim, network_service)
    return cim if network_service.add(cim) else None


PBEndDevice.to_cim = end_device_to_cim
PBMeter.to_cim = meter_to_cim
PBUsagePoint.to_cim = usage_point_to_cim


#######################
# IEC61968 OPERATIONS #
#######################

def operational_restriction_to_cim(pb: PBOperationalRestriction, network_service: NetworkService) -> Optional[OperationalRestriction]:
    cim = OperationalRestriction(mrid=pb.mrid())
    document_to_cim(pb.doc, cim, network_service)
    return cim if network_service.add(cim) else None


PBOperationalRestriction.to_cim = operational_restriction_to_cim


#####################################
# IEC61970 BASE AUXILIARY EQUIPMENT #
#####################################

def auxiliary_equipment_to_cim(pb: PBAuxiliaryEquipment, cim: AuxiliaryEquipment, network_service: NetworkService):
    network_service.resolve_or_defer_reference(resolver.ae_terminal(cim), pb.terminalMRID)

    equipment_to_cim(pb.eq, cim, network_service)


def current_transformer_to_cim(pb: PBCurrentTransformer, network_service: NetworkService) -> Optional[CurrentTransformer]:
    cim = CurrentTransformer(mrid=pb.mrid(), core_burden=int_or_none(pb.coreBurden))

    network_service.resolve_or_defer_reference(resolver.current_transformer_info(cim), pb.asset_info_mrid())

    sensor_to_cim(pb.sn, cim, network_service)
    return cim if network_service.add(cim) else None


def fault_indicator_to_cim(pb: PBFaultIndicator, network_service: NetworkService) -> Optional[FaultIndicator]:
    cim = FaultIndicator(mrid=pb.mrid())

    auxiliary_equipment_to_cim(pb.ae, cim, network_service)
    return cim if network_service.add(cim) else None


def potential_transformer_to_cim(pb: PBPotentialTransformer, network_service: NetworkService) -> Optional[PotentialTransformer]:
    cim = PotentialTransformer(mrid=pb.mrid(), type=PotentialTransformerKind(pb.type))

    network_service.resolve_or_defer_reference(resolver.potential_transformer_info(cim), pb.asset_info_mrid())

    sensor_to_cim(pb.sn, cim, network_service)
    return cim if network_service.add(cim) else None


def sensor_to_cim(pb: PBSensor, cim: Sensor, network_service: NetworkService):
    auxiliary_equipment_to_cim(pb.ae, cim, network_service)


PBAuxiliaryEquipment.to_cim = auxiliary_equipment_to_cim
PBCurrentTransformer.to_cim = current_transformer_to_cim
PBFaultIndicator.to_cim = fault_indicator_to_cim
PBPotentialTransformer.to_cim = potential_transformer_to_cim
PBSensor.to_cim = sensor_to_cim


######################
# IEC61970 BASE CORE #
######################

def ac_dc_terminal_to_cim(pb: PBAcDcTerminal, cim: AcDcTerminal, network_service: NetworkService):
    identified_object_to_cim(pb.io, cim, network_service)


def base_voltage_to_cim(pb: PBBaseVoltage, network_service: NetworkService) -> Optional[BaseVoltage]:
    # noinspection PyArgumentList
    cim = BaseVoltage(mrid=pb.mrid(), nominal_voltage=pb.nominalVoltage)

    identified_object_to_cim(pb.io, cim, network_service)
    return cim if network_service.add(cim) else None


def conducting_equipment_to_cim(pb: PBConductingEquipment, cim: ConductingEquipment, network_service: NetworkService):
    network_service.resolve_or_defer_reference(resolver.ce_base_voltage(cim), pb.baseVoltageMRID)
    for mrid in pb.terminalMRIDs:
        network_service.resolve_or_defer_reference(resolver.ce_terminals(cim), mrid)

    equipment_to_cim(pb.eq, cim, network_service)


def connectivity_node_to_cim(pb: PBConnectivityNode, network_service: NetworkService) -> Optional[ConnectivityNode]:
    cim = ConnectivityNode(mrid=pb.mrid())

    identified_object_to_cim(pb.io, cim, network_service)
    return cim if network_service.add(cim) else None


def connectivity_node_container_to_cim(pb: PBConnectivityNodeContainer, cim: ConnectivityNodeContainer, network_service: NetworkService):
    power_system_resource_to_cim(pb.psr, cim, network_service)


def equipment_to_cim(pb: PBEquipment, cim: Equipment, network_service: NetworkService):
    cim.in_service = pb.inService
    cim.normally_in_service = pb.normallyInService

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
    cim = Feeder(mrid=pb.mrid())

    network_service.resolve_or_defer_reference(resolver.normal_head_terminal(cim), pb.normalHeadTerminalMRID)
    network_service.resolve_or_defer_reference(resolver.normal_energizing_substation(cim), pb.normalEnergizingSubstationMRID)
    for mrid in pb.normalEnergizedLvFeederMRIDs:
        network_service.resolve_or_defer_reference(resolver.normal_energized_lv_feeders(cim), mrid)

    equipment_container_to_cim(pb.ec, cim, network_service)
    return cim if network_service.add(cim) else None


def geographical_region_to_cim(pb: PBGeographicalRegion, network_service: NetworkService) -> Optional[GeographicalRegion]:
    cim = GeographicalRegion(mrid=pb.mrid())

    for mrid in pb.subGeographicalRegionMRIDs:
        network_service.resolve_or_defer_reference(resolver.sub_geographical_regions(cim), mrid)

    identified_object_to_cim(pb.io, cim, network_service)
    return cim if network_service.add(cim) else None


def power_system_resource_to_cim(pb: PBPowerSystemResource, cim: PowerSystemResource, network_service: NetworkService):
    network_service.resolve_or_defer_reference(resolver.psr_location(cim), pb.locationMRID)

    identified_object_to_cim(pb.io, cim, network_service)


def site_to_cim(pb: PBSite, network_service: NetworkService) -> Optional[Site]:
    # noinspection PyArgumentList
    cim = Site(mrid=pb.mrid())

    equipment_container_to_cim(pb.ec, cim, network_service)
    return cim if network_service.add(cim) else None


def sub_geographical_region_to_cim(pb: PBSubGeographicalRegion, network_service: NetworkService) -> Optional[SubGeographicalRegion]:
    cim = SubGeographicalRegion(mrid=pb.mrid())

    network_service.resolve_or_defer_reference(resolver.geographical_region(cim), pb.geographicalRegionMRID)
    for mrid in pb.substationMRIDs:
        network_service.resolve_or_defer_reference(resolver.substations(cim), mrid)

    identified_object_to_cim(pb.io, cim, network_service)
    return cim if network_service.add(cim) else None


def substation_to_cim(pb: PBSubstation, network_service: NetworkService) -> Optional[Substation]:
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
    # noinspection PyArgumentList
    cim = Terminal(
        mrid=pb.mrid(),
        phases=phase_code_by_id(pb.phases),
        sequence_number=pb.sequenceNumber,
        normal_feeder_direction=FeederDirection(pb.normalFeederDirection),
        current_feeder_direction=FeederDirection(pb.currentFeederDirection),
        traced_phases=TracedPhases(pb.tracedPhases),
    )

    network_service.resolve_or_defer_reference(resolver.conducting_equipment(cim), pb.conductingEquipmentMRID)
    network_service.resolve_or_defer_reference(resolver.connectivity_node(cim), pb.connectivityNodeMRID)

    ac_dc_terminal_to_cim(pb.ad, cim, network_service)
    return cim if network_service.add(cim) else None


PBAcDcTerminal.to_cim = ac_dc_terminal_to_cim
PBBaseVoltage.to_cim = base_voltage_to_cim
PBConductingEquipment.to_cim = conducting_equipment_to_cim
PBConnectivityNode.to_cim = connectivity_node_to_cim
PBConnectivityNodeContainer.to_cim = connectivity_node_container_to_cim
PBEquipment.to_cim = equipment_to_cim
PBEquipmentContainer.to_cim = equipment_container_to_cim
PBFeeder.to_cim = feeder_to_cim
PBGeographicalRegion.to_cim = geographical_region_to_cim
PBPowerSystemResource.to_cim = power_system_resource_to_cim
PBSite.to_cim = site_to_cim
PBSubGeographicalRegion.to_cim = sub_geographical_region_to_cim
PBSubstation.to_cim = substation_to_cim
PBTerminal.to_cim = terminal_to_cim


#############################
# IEC61970 BASE EQUIVALENTS #
#############################

def equivalent_branch_to_cim(pb: PBEquivalentBranch, network_service: NetworkService) -> Optional[EquivalentBranch]:
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


PBEquivalentEquipment.to_cim = equivalent_equipment_to_cim
PBEquivalentBranch.to_cim = equivalent_branch_to_cim


######################
# IEC61970 BASE MEAS #
######################

def accumulator_to_cim(pb: PBAccumulator, network_service: NetworkService) -> Optional[Accumulator]:
    # noinspection PyArgumentList
    cim = Accumulator(mrid=pb.mrid())

    measurement_to_cim(pb.measurement, cim, network_service)
    return cim if network_service.add(cim) else None


def analog_to_cim(pb: PBAnalog, network_service: NetworkService) -> Optional[Analog]:
    # noinspection PyArgumentList
    cim = Analog(mrid=pb.mrid(), positive_flow_in=pb.positiveFlowIn)

    measurement_to_cim(pb.measurement, cim, network_service)
    return cim if network_service.add(cim) else None


def control_to_cim(pb: PBControl, network_service: NetworkService) -> Optional[Control]:
    # noinspection PyArgumentList
    cim = Control(
        mrid=pb.mrid(),
        power_system_resource_mrid=pb.powerSystemResourceMRID if pb.powerSystemResourceMRID else None
    )

    network_service.resolve_or_defer_reference(resolver.remote_control(cim), pb.remoteControlMRID)

    io_point_to_cim(pb.ip, cim, network_service)
    return cim if network_service.add(cim) else None


def discrete_to_cim(pb: PBDiscrete, network_service: NetworkService) -> Optional[Discrete]:
    # noinspection PyArgumentList
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
PBIoPoint.to_cim = io_point_to_cim
PBMeasurement.to_cim = measurement_to_cim


#######################
# IEC61970 BASE SCADA #
#######################

def remote_control_to_cim(pb: PBRemoteControl, network_service: NetworkService) -> Optional[RemoteControl]:
    # noinspection PyArgumentList
    cim = RemoteControl(mrid=pb.mrid())

    network_service.resolve_or_defer_reference(resolver.control(cim), pb.controlMRID)

    remote_point_to_cim(pb.rp, cim, network_service)
    return cim if network_service.add(cim) else None


def remote_point_to_cim(pb: PBRemotePoint, cim: RemotePoint, service: NetworkService):
    identified_object_to_cim(pb.io, cim, service)


def remote_source_to_cim(pb: PBRemoteSource, network_service: NetworkService) -> Optional[RemoteSource]:
    # noinspection PyArgumentList
    cim = RemoteSource(mrid=pb.mrid())

    network_service.resolve_or_defer_reference(resolver.measurement(cim), pb.measurementMRID)

    remote_point_to_cim(pb.rp, cim, network_service)
    return cim if network_service.add(cim) else None


PBRemoteControl.to_cim = remote_control_to_cim
PBRemotePoint.to_cim = remote_point_to_cim
PBRemoteSource.to_cim = remote_source_to_cim


#############################################
# IEC61970 BASE WIRES GENERATION PRODUCTION #
#############################################

def battery_unit_to_cim(pb: PBBatteryUnit, network_service: NetworkService) -> Optional[BatteryUnit]:
    cim = BatteryUnit(
        mrid=pb.mrid(),
        battery_state=BatteryStateKind(pb.batteryState),
        rated_e=long_or_none(pb.ratedE),
        stored_e=long_or_none(pb.storedE),
    )

    power_electronics_unit_to_cim(pb.peu, cim, network_service)
    return cim if network_service.add(cim) else None


def photo_voltaic_unit_to_cim(pb: PBPhotoVoltaicUnit, network_service: NetworkService) -> Optional[PhotoVoltaicUnit]:
    cim = PhotoVoltaicUnit(mrid=pb.mrid())

    power_electronics_unit_to_cim(pb.peu, cim, network_service)
    return cim if network_service.add(cim) else None


def power_electronics_unit_to_cim(pb: PBPowerElectronicsUnit, cim: PowerElectronicsUnit, network_service: NetworkService):
    cim.max_p = int_or_none(pb.maxP)
    cim.min_p = int_or_none(pb.minP)

    network_service.resolve_or_defer_reference(resolver.unit_power_electronics_connection(cim), pb.powerElectronicsConnectionMRID)

    equipment_to_cim(pb.eq, cim, network_service)


def power_electronics_wind_unit_to_cim(pb: PBPowerElectronicsWindUnit, network_service: NetworkService) -> Optional[PowerElectronicsWindUnit]:
    cim = PowerElectronicsWindUnit(mrid=pb.mrid())

    power_electronics_unit_to_cim(pb.peu, cim, network_service)
    return cim if network_service.add(cim) else None


PBBatteryUnit.to_cim = battery_unit_to_cim
PBPhotoVoltaicUnit.to_cim = photo_voltaic_unit_to_cim
PBPowerElectronicsUnit.to_cim = power_electronics_unit_to_cim
PBPowerElectronicsWindUnit.to_cim = power_electronics_wind_unit_to_cim


#######################
# IEC61970 BASE WIRES #
#######################

def ac_line_segment_to_cim(pb: PBAcLineSegment, network_service: NetworkService) -> Optional[AcLineSegment]:
    cim = AcLineSegment(mrid=pb.mrid())

    network_service.resolve_or_defer_reference(resolver.per_length_sequence_impedance(cim), pb.perLengthSequenceImpedanceMRID)

    conductor_to_cim(pb.cd, cim, network_service)
    return cim if network_service.add(cim) else None


def breaker_to_cim(pb: PBBreaker, network_service: NetworkService) -> Optional[Breaker]:
    cim = Breaker(mrid=pb.mrid())

    protected_switch_to_cim(pb.sw, cim, network_service)
    return cim if network_service.add(cim) else None


def conductor_to_cim(pb: PBConductor, cim: Conductor, network_service: NetworkService):
    cim.length = float_or_none(pb.length)

    network_service.resolve_or_defer_reference(resolver.asset_info(cim), pb.asset_info_mrid())

    conducting_equipment_to_cim(pb.ce, cim, network_service)


def connector_to_cim(pb: PBConnector, cim: Connector, network_service: NetworkService):
    conducting_equipment_to_cim(pb.ce, cim, network_service)


def disconnector_to_cim(pb: PBDisconnector, network_service: NetworkService) -> Optional[Disconnector]:
    cim = Disconnector(mrid=pb.mrid())

    switch_to_cim(pb.sw, cim, network_service)
    return cim if network_service.add(cim) else None


def energy_connection_to_cim(pb: PBEnergyConnection, cim: EnergyConnection, network_service: NetworkService):
    conducting_equipment_to_cim(pb.ce, cim, network_service)


def energy_consumer_to_cim(pb: PBEnergyConsumer, network_service: NetworkService) -> Optional[EnergyConsumer]:
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
    cim = EnergySourcePhase(mrid=pb.mrid(), phase=single_phase_kind_by_id(pb.phase))

    network_service.resolve_or_defer_reference(resolver.energy_source(cim), pb.energySourceMRID)

    power_system_resource_to_cim(pb.psr, cim, network_service)
    return cim if network_service.add(cim) else None


def fuse_to_cim(pb: PBFuse, network_service: NetworkService) -> Optional[Fuse]:
    cim = Fuse(mrid=pb.mrid())

    switch_to_cim(pb.sw, cim, network_service)
    return cim if network_service.add(cim) else None


def jumper_to_cim(pb: PBJumper, network_service: NetworkService) -> Optional[Jumper]:
    cim = Jumper(mrid=pb.mrid())

    switch_to_cim(pb.sw, cim, network_service)
    return cim if network_service.add(cim) else None


def junction_to_cim(pb: PBJunction, network_service: NetworkService) -> Optional[Junction]:
    cim = Junction(mrid=pb.mrid())

    connector_to_cim(pb.cn, cim, network_service)
    return cim if network_service.add(cim) else None


def busbar_section_to_cim(pb: PBBusbarSection, network_service: NetworkService) -> Optional[BusbarSection]:
    cim = BusbarSection(mrid=pb.mrid())

    connector_to_cim(pb.cn, cim, network_service)
    return cim if network_service.add(cim) else None


def line_to_cim(pb: PBLine, cim: Line, network_service: NetworkService):
    equipment_container_to_cim(pb.ec, cim, network_service)


def linear_shunt_compensator_to_cim(pb: PBLinearShuntCompensator, network_service: NetworkService) -> Optional[LinearShuntCompensator]:
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
    cim = LoadBreakSwitch(mrid=pb.mrid())

    protected_switch_to_cim(pb.ps, cim, network_service)
    return cim if network_service.add(cim) else None


def per_length_line_parameter_to_cim(pb: PBPerLengthLineParameter, cim: PerLengthLineParameter, network_service: NetworkService):
    identified_object_to_cim(pb.io, cim, network_service)


def per_length_impedance_to_cim(pb: PBPerLengthImpedance, cim: PerLengthImpedance, network_service: NetworkService):
    per_length_line_parameter_to_cim(pb.lp, cim, network_service)


def per_length_sequence_impedance_to_cim(pb: PBPerLengthSequenceImpedance, network_service: NetworkService) -> Optional[PerLengthSequenceImpedance]:
    # noinspection PyArgumentList
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


def power_electronics_connection_to_cim(pb: PBPowerElectronicsConnection, network_service: NetworkService) -> Optional[PowerElectronicsConnection]:
    cim = PowerElectronicsConnection(
        mrid=pb.mrid(),
        max_i_fault=int_or_none(pb.maxIFault),
        p=float_or_none(pb.p),
        q=float_or_none(pb.q),
        max_q=float_or_none(pb.maxQ),
        min_q=float_or_none(pb.minQ),
        rated_s=int_or_none(pb.ratedS),
        rated_u=int_or_none(pb.ratedU)
    )

    for mrid in pb.powerElectronicsUnitMRIDs:
        network_service.resolve_or_defer_reference(resolver.power_electronics_unit(cim), mrid)
    for mrid in pb.powerElectronicsConnectionPhaseMRIDs:
        network_service.resolve_or_defer_reference(resolver.power_electronics_connection_phase(cim), mrid)

    regulating_cond_eq_to_cim(pb.rce, cim, network_service)
    return cim if network_service.add(cim) else None


def power_electronics_connection_phase_to_cim(pb: PBPowerElectronicsConnection, network_service: NetworkService) -> Optional[PowerElectronicsConnectionPhase]:
    # noinspection PyArgumentList
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
    cim = PowerTransformer(
        mrid=pb.mrid(),
        vector_group=VectorGroup(pb.vectorGroup),
        transformer_utilisation=float_or_none(pb.transformerUtilisation),
        construction_kind=TransformerConstructionKind(pb.constructionKind),
        function=TransformerFunctionKind(pb.function)
    )

    for mrid in pb.powerTransformerEndMRIDs:
        network_service.resolve_or_defer_reference(resolver.ends(cim), mrid)
    network_service.resolve_or_defer_reference(resolver.power_transformer_info(cim), pb.asset_info_mrid())

    conducting_equipment_to_cim(pb.ce, cim, network_service)
    return cim if network_service.add(cim) else None


def power_transformer_end_to_cim(pb: PBPowerTransformerEnd, network_service: NetworkService) -> Optional[PowerTransformerEnd]:
    cim = PowerTransformerEnd(
        mrid=pb.mrid(),
        rated_s=int_or_none(pb.ratedS),
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

    # Set end number before associating with power transformer to prevent incorrectly sorted cim.power_transformer.ends
    transformer_end_to_cim(pb.te, cim, network_service)

    network_service.resolve_or_defer_reference(resolver.power_transformer(cim), pb.powerTransformerMRID)
    return cim if network_service.add(cim) else None


def transformer_star_impedance_to_cim(pb: PBTransformerStarImpedance, network_service: NetworkService) -> Optional[TransformerStarImpedance]:
    # noinspection PyArgumentList
    cim = TransformerStarImpedance(mrid=pb.mrid(), r=pb.r, r0=pb.r0, x=pb.x, x0=pb.x0)

    network_service.resolve_or_defer_reference(resolver.star_impedance_transformer_end_info(cim), pb.transformerEndInfoMRID)

    identified_object_to_cim(pb.io, cim, network_service)
    return cim if network_service.add(cim) else None


def protected_switch_to_cim(pb: PBProtectedSwitch, cim: ProtectedSwitch, network_service: NetworkService):
    switch_to_cim(pb.sw, cim, network_service)


def ratio_tap_changer_to_cim(pb: PBRatioTapChanger, network_service: NetworkService) -> Optional[RatioTapChanger]:
    cim = RatioTapChanger(
        mrid=pb.mrid(),
        step_voltage_increment=float_or_none(pb.stepVoltageIncrement)
    )

    network_service.resolve_or_defer_reference(resolver.transformer_end(cim), pb.transformerEndMRID)

    tap_changer_to_cim(pb.tc, cim, network_service)
    return cim if network_service.add(cim) else None


def recloser_to_cim(pb: PBRecloser, network_service: NetworkService) -> Optional[Recloser]:
    cim = Recloser(mrid=pb.mrid())

    protected_switch_to_cim(pb.sw, cim, network_service)
    return cim if network_service.add(cim) else None


def regulating_cond_eq_to_cim(pb: PBRegulatingCondEq, cim: RegulatingCondEq, network_service: NetworkService):
    cim.control_enabled = pb.controlEnabled

    energy_connection_to_cim(pb.ec, cim, network_service)


def shunt_compensator_to_cim(pb: PBShuntCompensator, cim: ShuntCompensator, network_service: NetworkService):
    network_service.resolve_or_defer_reference(resolver.shunt_compensator_info(cim), pb.asset_info_mrid())
    cim.sections = float_or_none(pb.sections)
    cim.grounded = pb.grounded
    cim.nom_u = int_or_none(pb.nomU)
    cim.phase_connection = PhaseShuntConnectionKind(pb.phaseConnection)

    regulating_cond_eq_to_cim(pb.rce, cim, network_service)


def switch_to_cim(pb: PBSwitch, cim: Switch, network_service: NetworkService):
    cim.set_normally_open(pb.normalOpen)
    cim.set_open(pb.open)

    conducting_equipment_to_cim(pb.ce, cim, network_service)


def tap_changer_to_cim(pb: PBTapChanger, cim: TapChanger, network_service: NetworkService):
    cim.high_step = int_or_none(pb.highStep)
    cim.step = float_or_none(pb.step)
    cim.neutral_step = int_or_none(pb.neutralStep)
    cim.normal_step = int_or_none(pb.normalStep)
    cim.low_step = int_or_none(pb.lowStep)
    cim.neutral_u = int_or_none(pb.neutralU)
    cim.control_enabled = pb.controlEnabled

    power_system_resource_to_cim(pb.psr, cim, network_service)


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


PBAcLineSegment.to_cim = ac_line_segment_to_cim
PBBreaker.to_cim = breaker_to_cim
PBConductor.to_cim = conductor_to_cim
PBConnector.to_cim = connector_to_cim
PBDisconnector.to_cim = disconnector_to_cim
PBEnergyConnection.to_cim = energy_connection_to_cim
PBEnergyConsumer.to_cim = energy_consumer_to_cim
PBEnergyConsumerPhase.to_cim = energy_consumer_phase_to_cim
PBEnergySource.to_cim = energy_source_to_cim
PBEnergySourcePhase.to_cim = energy_source_phase_to_cim
PBFuse.to_cim = fuse_to_cim
PBJumper.to_cim = jumper_to_cim
PBJunction.to_cim = junction_to_cim
PBBusbarSection.to_cim = busbar_section_to_cim
PBLine.to_cim = line_to_cim
PBLinearShuntCompensator.to_cim = linear_shunt_compensator_to_cim
PBLoadBreakSwitch.to_cim = load_break_switch_to_cim
PBPerLengthSequenceImpedance.to_cim = per_length_sequence_impedance_to_cim
PBPerLengthLineParameter.to_cim = per_length_line_parameter_to_cim
PBPerLengthImpedance.to_cim = per_length_impedance_to_cim
PBPowerElectronicsConnection.to_cim = power_electronics_connection_to_cim
PBPowerElectronicsConnectionPhase.to_cim = power_electronics_connection_phase_to_cim
PBPowerTransformer.to_cim = power_transformer_to_cim
PBPowerTransformerEnd.to_cim = power_transformer_end_to_cim
PBTransformerStarImpedance.to_cim = transformer_star_impedance_to_cim
PBProtectedSwitch.to_cim = protected_switch_to_cim
PBRatioTapChanger.to_cim = ratio_tap_changer_to_cim
PBRecloser.to_cim = recloser_to_cim
PBRegulatingCondEq.to_cim = regulating_cond_eq_to_cim
PBShuntCompensator.to_cim = shunt_compensator_to_cim
PBSwitch.to_cim = switch_to_cim
PBTapChanger.to_cim = tap_changer_to_cim
PBTransformerEnd.to_cim = transformer_end_to_cim


###############################
# IEC61970 INFIEC61970 FEEDER #
###############################

def circuit_to_cim(pb: PBCircuit, network_service: NetworkService) -> Optional[Circuit]:
    cim = Circuit(mrid=pb.mrid())

    network_service.resolve_or_defer_reference(resolver.loop(cim), pb.loopMRID)
    for mrid in pb.endTerminalMRIDs:
        network_service.resolve_or_defer_reference(resolver.end_terminal(cim), mrid)
    for mrid in pb.endSubstationMRIDs:
        network_service.resolve_or_defer_reference(resolver.end_substation(cim), mrid)

    line_to_cim(pb.l, cim, network_service)
    return cim if network_service.add(cim) else None


def loop_to_cim(pb: PBLoop, network_service: NetworkService) -> Optional[Loop]:
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
    cim = LvFeeder(mrid=pb.mrid())

    network_service.resolve_or_defer_reference(resolver.lv_feeder_normal_head_terminal(cim), pb.normalHeadTerminalMRID)
    for mrid in pb.normalEnergizingFeederMRIDs:
        network_service.resolve_or_defer_reference(resolver.normal_energizing_feeders(cim), mrid)

    equipment_container_to_cim(pb.ec, cim, network_service)
    return cim if network_service.add(cim) else None


PBCircuit.to_cim = circuit_to_cim
PBLoop.to_cim = loop_to_cim
PBLvFeeder.to_cim = lv_feeder_to_cim
