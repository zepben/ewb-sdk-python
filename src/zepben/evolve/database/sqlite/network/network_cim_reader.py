#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["NetworkCimReader"]

import sys
from typing import Callable, Optional

# `assert_never` changed packages with the release of 3.11, so import it from the old spot while we still support 3.9 and 3.10.
v = sys.version_info
if v.major == 3 and v.minor < 11:
    from typing_extensions import assert_never
else:
    from typing import assert_never

from zepben.evolve.database.sqlite.common.base_cim_reader import BaseCimReader
from zepben.evolve.database.sqlite.extensions.result_set import ResultSet
from zepben.evolve.database.sqlite.tables.associations.loop_substation_relationship import LoopSubstationRelationship
from zepben.evolve.database.sqlite.tables.associations.table_asset_organisation_roles_assets import TableAssetOrganisationRolesAssets
from zepben.evolve.database.sqlite.tables.associations.table_circuits_substations import TableCircuitsSubstations
from zepben.evolve.database.sqlite.tables.associations.table_circuits_terminals import TableCircuitsTerminals
from zepben.evolve.database.sqlite.tables.associations.table_equipment_equipment_containers import TableEquipmentEquipmentContainers
from zepben.evolve.database.sqlite.tables.associations.table_equipment_operational_restrictions import TableEquipmentOperationalRestrictions
from zepben.evolve.database.sqlite.tables.associations.table_equipment_usage_points import TableEquipmentUsagePoints
from zepben.evolve.database.sqlite.tables.associations.table_loops_substations import TableLoopsSubstations
from zepben.evolve.database.sqlite.tables.associations.table_protection_relay_functions_protected_switches import TableProtectionRelayFunctionsProtectedSwitches
from zepben.evolve.database.sqlite.tables.associations.table_protection_relay_functions_sensors import TableProtectionRelayFunctionsSensors
from zepben.evolve.database.sqlite.tables.associations.table_protection_relay_schemes_protection_relay_functions import \
    TableProtectionRelaySchemesProtectionRelayFunctions
from zepben.evolve.database.sqlite.tables.associations.table_usage_points_end_devices import TableUsagePointsEndDevices
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_cable_info import TableCableInfo
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_no_load_tests import TableNoLoadTests
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_open_circuit_tests import TableOpenCircuitTests
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_overhead_wire_info import TableOverheadWireInfo
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_power_transformer_info import TablePowerTransformerInfo
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_short_circuit_tests import TableShortCircuitTests
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_shunt_compensator_info import TableShuntCompensatorInfo
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_switch_info import TableSwitchInfo
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_transformer_end_info import TableTransformerEndInfo
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_transformer_tank_info import TableTransformerTankInfo
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_transformer_test import TableTransformerTest
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_wire_info import TableWireInfo
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_containers import TableAssetContainers
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_info import TableAssetInfo
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_organisation_roles import TableAssetOrganisationRoles
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_owners import TableAssetOwners
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_assets import TableAssets
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_poles import TablePoles
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_streetlights import TableStreetlights
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_structures import TableStructures
from zepben.evolve.database.sqlite.tables.iec61968.common.table_location_street_address_field import TableLocationStreetAddressField
from zepben.evolve.database.sqlite.tables.iec61968.common.table_location_street_addresses import TableLocationStreetAddresses
from zepben.evolve.database.sqlite.tables.iec61968.common.table_locations import TableLocations
from zepben.evolve.database.sqlite.tables.iec61968.common.table_position_points import TablePositionPoints
from zepben.evolve.database.sqlite.tables.iec61968.common.table_street_addresses import TableStreetAddresses
from zepben.evolve.database.sqlite.tables.iec61968.common.table_town_details import TableTownDetails
from zepben.evolve.database.sqlite.tables.iec61968.infiec61968.infassetinfo.table_current_transformer_info import TableCurrentTransformerInfo
from zepben.evolve.database.sqlite.tables.iec61968.infiec61968.infassetinfo.table_potential_transformer_info import TablePotentialTransformerInfo
from zepben.evolve.database.sqlite.tables.iec61968.infiec61968.infassetinfo.table_reclose_delays import TableRecloseDelays
from zepben.evolve.database.sqlite.tables.iec61968.infiec61968.infassetinfo.table_relay_info import TableRelayInfo
from zepben.evolve.database.sqlite.tables.iec61968.metering.table_end_devices import TableEndDevices
from zepben.evolve.database.sqlite.tables.iec61968.metering.table_meters import TableMeters
from zepben.evolve.database.sqlite.tables.iec61968.metering.table_usage_points import TableUsagePoints
from zepben.evolve.database.sqlite.tables.iec61968.operations.table_operational_restrictions import TableOperationalRestrictions
from zepben.evolve.database.sqlite.tables.iec61970.base.auxiliaryequipment.table_auxiliary_equipment import TableAuxiliaryEquipment
from zepben.evolve.database.sqlite.tables.iec61970.base.auxiliaryequipment.table_current_transformers import TableCurrentTransformers
from zepben.evolve.database.sqlite.tables.iec61970.base.auxiliaryequipment.table_fault_indicators import TableFaultIndicators
from zepben.evolve.database.sqlite.tables.iec61970.base.auxiliaryequipment.table_potential_transformers import TablePotentialTransformers
from zepben.evolve.database.sqlite.tables.iec61970.base.auxiliaryequipment.table_sensors import TableSensors
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_ac_dc_terminals import TableAcDcTerminals
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_base_voltages import TableBaseVoltages
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_conducting_equipment import TableConductingEquipment
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_connectivity_node_containers import TableConnectivityNodeContainers
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_connectivity_nodes import TableConnectivityNodes
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_equipment import TableEquipment
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_equipment_containers import TableEquipmentContainers
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_feeders import TableFeeders
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_geographical_regions import TableGeographicalRegions
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_power_system_resources import TablePowerSystemResources
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_sites import TableSites
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_sub_geographical_regions import TableSubGeographicalRegions
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_substations import TableSubstations
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_terminals import TableTerminals
from zepben.evolve.database.sqlite.tables.iec61970.base.equivalents.table_equivalent_branches import TableEquivalentBranches
from zepben.evolve.database.sqlite.tables.iec61970.base.equivalents.table_equivalent_equipment import TableEquivalentEquipment
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_accumulators import TableAccumulators
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_analogs import TableAnalogs
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_controls import TableControls
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_discretes import TableDiscretes
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_io_points import TableIoPoints
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_measurements import TableMeasurements
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_current_relays import TableCurrentRelays
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_distance_relays import TableDistanceRelays
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_protection_relay_function_thresholds import TableProtectionRelayFunctionThresholds
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_protection_relay_function_time_limits import TableProtectionRelayFunctionTimeLimits
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_protection_relay_functions import TableProtectionRelayFunctions
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_protection_relay_schemes import TableProtectionRelaySchemes
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_protection_relay_systems import TableProtectionRelaySystems
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_voltage_relays import TableVoltageRelays
from zepben.evolve.database.sqlite.tables.iec61970.base.scada.table_remote_controls import TableRemoteControls
from zepben.evolve.database.sqlite.tables.iec61970.base.scada.table_remote_points import TableRemotePoints
from zepben.evolve.database.sqlite.tables.iec61970.base.scada.table_remote_sources import TableRemoteSources
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.generation.production.table_battery_units import TableBatteryUnits
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.generation.production.table_photo_voltaic_units import TablePhotoVoltaicUnits
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.generation.production.table_power_electronics_units import TablePowerElectronicsUnits
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.generation.production.table_power_electronics_wind_units import TablePowerElectronicsWindUnits
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_ac_line_segments import TableAcLineSegments
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_breakers import TableBreakers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_busbar_sections import TableBusbarSections
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_conductors import TableConductors
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_connectors import TableConnectors
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_disconnectors import TableDisconnectors
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_connections import TableEnergyConnections
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_consumer_phases import TableEnergyConsumerPhases
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_consumers import TableEnergyConsumers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_source_phases import TableEnergySourcePhases
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_sources import TableEnergySources
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_fuses import TableFuses
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_ground_disconnectors import TableGroundDisconnectors
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_grounds import TableGrounds
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_jumpers import TableJumpers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_junctions import TableJunctions
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_linear_shunt_compensators import TableLinearShuntCompensators
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_lines import TableLines
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_load_break_switches import TableLoadBreakSwitches
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_per_length_impedances import TablePerLengthImpedances
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_per_length_line_parameters import TablePerLengthLineParameters
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_per_length_sequence_impedances import TablePerLengthSequenceImpedances
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_electronics_connection_phases import TablePowerElectronicsConnectionPhases
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_electronics_connections import TablePowerElectronicsConnections
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_transformer_end_ratings import TablePowerTransformerEndRatings
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_transformer_ends import TablePowerTransformerEnds
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_transformers import TablePowerTransformers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_protected_switches import TableProtectedSwitches
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_ratio_tap_changers import TableRatioTapChangers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_reclosers import TableReclosers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_regulating_cond_eq import TableRegulatingCondEq
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_regulating_controls import TableRegulatingControls
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_series_compensators import TableSeriesCompensators
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_shunt_compensators import TableShuntCompensators
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_switches import TableSwitches
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_tap_changer_controls import TableTapChangerControls
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_tap_changers import TableTapChangers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_transformer_ends import TableTransformerEnds
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_transformer_star_impedances import TableTransformerStarImpedances
from zepben.evolve.database.sqlite.tables.iec61970.infiec61970.feeder.table_circuits import TableCircuits
from zepben.evolve.database.sqlite.tables.iec61970.infiec61970.feeder.table_loops import TableLoops
from zepben.evolve.database.sqlite.tables.iec61970.infiec61970.feeder.table_lv_feeders import TableLvFeeders
from zepben.evolve.database.sqlite.tables.iec61970.infiec61970.wires.generation.production.table_ev_charging_units import TableEvChargingUnits
from zepben.evolve.model.cim.iec61968.assetinfo.no_load_test import NoLoadTest
from zepben.evolve.model.cim.iec61968.assetinfo.open_circuit_test import OpenCircuitTest
from zepben.evolve.model.cim.iec61968.assetinfo.power_transformer_info import PowerTransformerInfo
from zepben.evolve.model.cim.iec61968.assetinfo.short_circuit_test import ShortCircuitTest
from zepben.evolve.model.cim.iec61968.assetinfo.shunt_compensator_info import ShuntCompensatorInfo
from zepben.evolve.model.cim.iec61968.assetinfo.switch_info import SwitchInfo
from zepben.evolve.model.cim.iec61968.assetinfo.transformer_end_info import TransformerEndInfo
from zepben.evolve.model.cim.iec61968.assetinfo.transformer_tank_info import TransformerTankInfo
from zepben.evolve.model.cim.iec61968.assetinfo.transformer_test import TransformerTest
from zepben.evolve.model.cim.iec61968.assetinfo.wire_info import CableInfo, OverheadWireInfo, WireInfo
from zepben.evolve.model.cim.iec61968.assetinfo.wire_material_kind import WireMaterialKind
from zepben.evolve.model.cim.iec61968.assets.asset import Asset, AssetContainer
from zepben.evolve.model.cim.iec61968.assets.asset_info import AssetInfo
from zepben.evolve.model.cim.iec61968.assets.asset_organisation_role import AssetOrganisationRole, AssetOwner
from zepben.evolve.model.cim.iec61968.assets.pole import Pole
from zepben.evolve.model.cim.iec61968.assets.streetlight import Streetlight, StreetlightLampKind
from zepben.evolve.model.cim.iec61968.assets.structure import Structure
from zepben.evolve.model.cim.iec61968.common.location import Location, PositionPoint, StreetAddress, StreetDetail, TownDetail
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.current_transformer_info import CurrentTransformerInfo
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.potential_transformer_info import PotentialTransformerInfo
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.relay_info import RelayInfo
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.transformer_construction_kind import TransformerConstructionKind
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.transformer_function_kind import TransformerFunctionKind
from zepben.evolve.model.cim.iec61968.metering.metering import EndDevice, Meter, UsagePoint
from zepben.evolve.model.cim.iec61968.operations.operational_restriction import OperationalRestriction
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.auxiliary_equipment import AuxiliaryEquipment, FaultIndicator
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.current_transformer import CurrentTransformer
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.potential_transformer import PotentialTransformer
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.potential_transformer_kind import PotentialTransformerKind
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.sensor import Sensor
from zepben.evolve.model.cim.iec61970.base.core.base_voltage import BaseVoltage
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.connectivity_node import ConnectivityNode
from zepben.evolve.model.cim.iec61970.base.core.connectivity_node_container import ConnectivityNodeContainer
from zepben.evolve.model.cim.iec61970.base.core.equipment import Equipment
from zepben.evolve.model.cim.iec61970.base.core.equipment_container import EquipmentContainer, Feeder, Site
from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.evolve.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.evolve.model.cim.iec61970.base.core.regions import GeographicalRegion, SubGeographicalRegion
from zepben.evolve.model.cim.iec61970.base.core.substation import Substation
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal, AcDcTerminal
from zepben.evolve.model.cim.iec61970.base.domain.unit_symbol import UnitSymbol
from zepben.evolve.model.cim.iec61970.base.equivalents.equivalent_branch import EquivalentBranch
from zepben.evolve.model.cim.iec61970.base.equivalents.equivalent_equipment import EquivalentEquipment
from zepben.evolve.model.cim.iec61970.base.meas.control import Control
from zepben.evolve.model.cim.iec61970.base.meas.iopoint import IoPoint
from zepben.evolve.model.cim.iec61970.base.meas.measurement import Accumulator, Analog, Discrete, Measurement
from zepben.evolve.model.cim.iec61970.base.protection.current_relay import CurrentRelay
from zepben.evolve.model.cim.iec61970.base.protection.distance_relay import DistanceRelay
from zepben.evolve.model.cim.iec61970.base.protection.protection_relay_function import ProtectionRelayFunction
from zepben.evolve.model.cim.iec61970.base.protection.protection_relay_scheme import ProtectionRelayScheme
from zepben.evolve.model.cim.iec61970.base.protection.protection_relay_system import ProtectionRelaySystem
from zepben.evolve.model.cim.iec61970.base.protection.relay_setting import RelaySetting
from zepben.evolve.model.cim.iec61970.base.protection.voltage_relay import VoltageRelay
from zepben.evolve.model.cim.iec61970.base.scada.remote_control import RemoteControl
from zepben.evolve.model.cim.iec61970.base.scada.remote_point import RemotePoint
from zepben.evolve.model.cim.iec61970.base.scada.remote_source import RemoteSource
from zepben.evolve.model.cim.iec61970.base.wires.aclinesegment import AcLineSegment, Conductor
from zepben.evolve.model.cim.iec61970.base.wires.breaker import Breaker
from zepben.evolve.model.cim.iec61970.base.wires.connectors import BusbarSection, Connector, Junction
from zepben.evolve.model.cim.iec61970.base.wires.disconnector import Disconnector
from zepben.evolve.model.cim.iec61970.base.wires.energy_connection import EnergyConnection, RegulatingCondEq
from zepben.evolve.model.cim.iec61970.base.wires.energy_consumer import EnergyConsumer, EnergyConsumerPhase
from zepben.evolve.model.cim.iec61970.base.wires.energy_source import EnergySource
from zepben.evolve.model.cim.iec61970.base.wires.energy_source_phase import EnergySourcePhase
from zepben.evolve.model.cim.iec61970.base.wires.fuse import Fuse
from zepben.evolve.model.cim.iec61970.base.wires.generation.production.battery_state_kind import BatteryStateKind
from zepben.evolve.model.cim.iec61970.base.wires.generation.production.power_electronics_unit import BatteryUnit, PhotoVoltaicUnit, PowerElectronicsUnit, \
    PowerElectronicsWindUnit
from zepben.evolve.model.cim.iec61970.base.wires.ground import Ground
from zepben.evolve.model.cim.iec61970.base.wires.ground_disconnector import GroundDisconnector
from zepben.evolve.model.cim.iec61970.base.wires.jumper import Jumper
from zepben.evolve.model.cim.iec61970.base.wires.line import Line
from zepben.evolve.model.cim.iec61970.base.wires.load_break_switch import LoadBreakSwitch
from zepben.evolve.model.cim.iec61970.base.wires.per_length import PerLengthSequenceImpedance, PerLengthImpedance, PerLengthLineParameter
from zepben.evolve.model.cim.iec61970.base.wires.phase_shunt_connection_kind import PhaseShuntConnectionKind
from zepben.evolve.model.cim.iec61970.base.wires.power_electronics_connection import PowerElectronicsConnection, PowerElectronicsConnectionPhase
from zepben.evolve.model.cim.iec61970.base.wires.power_transformer import PowerTransformer, PowerTransformerEnd, RatioTapChanger, TransformerEnd, TapChanger
from zepben.evolve.model.cim.iec61970.base.wires.protected_switch import ProtectedSwitch
from zepben.evolve.model.cim.iec61970.base.wires.recloser import Recloser
from zepben.evolve.model.cim.iec61970.base.wires.regulating_control import RegulatingControl
from zepben.evolve.model.cim.iec61970.base.wires.regulating_control_mode_kind import RegulatingControlModeKind
from zepben.evolve.model.cim.iec61970.base.wires.series_compensator import SeriesCompensator
from zepben.evolve.model.cim.iec61970.base.wires.shunt_compensator import LinearShuntCompensator, ShuntCompensator
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.model.cim.iec61970.base.wires.switch import Switch
from zepben.evolve.model.cim.iec61970.base.wires.tap_changer_control import TapChangerControl
from zepben.evolve.model.cim.iec61970.base.wires.transformer_cooling_type import TransformerCoolingType
from zepben.evolve.model.cim.iec61970.base.wires.transformer_star_impedance import TransformerStarImpedance
from zepben.evolve.model.cim.iec61970.base.wires.vector_group import VectorGroup
from zepben.evolve.model.cim.iec61970.base.wires.winding_connection import WindingConnection
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.circuit import Circuit
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.loop import Loop
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.lv_feeder import LvFeeder
from zepben.evolve.model.cim.iec61970.infiec61970.protection.power_direction_kind import PowerDirectionKind
from zepben.evolve.model.cim.iec61970.infiec61970.protection.protection_kind import ProtectionKind
from zepben.evolve.model.cim.iec61970.infiec61970.wires.generation.production.ev_charging_unit import EvChargingUnit
from zepben.evolve.services.common import resolver
from zepben.evolve.services.network.network_service import NetworkService


class NetworkCimReader(BaseCimReader):
    """
    A class for reading the `NetworkService` tables from the database.
    
    :param service: The `NetworkService` to populate from the database.
    """

    def __init__(self, service: NetworkService):
        super().__init__(service)

        self._service = service
        """The `NetworkService` used to store any items read from the database."""

    #######################
    # IEC61968 Asset Info #
    #######################

    def load_cable_info(self, table: TableCableInfo, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `CableInfo` and populate its fields from `TableCableInfo`.

        :param table: The database table to read the `CableInfo` fields from.
        :param result_set: The record in the database table containing the fields for this `CableInfo`.
        :param set_identifier: A callback to register the mRID of this `CableInfo` for logging purposes.

        :return: True if the `CableInfo` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        cable_info = CableInfo(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_wire_info(cable_info, table, result_set) and self._add_or_throw(cable_info)

    def load_no_load_tests(self, table: TableNoLoadTests, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `NoLoadTest` and populate its fields from `TableNoLoadTests`.

        :param table: The database table to read the `NoLoadTest` fields from.
        :param result_set: The record in the database table containing the fields for this `NoLoadTest`.
        :param set_identifier: A callback to register the mRID of this `NoLoadTest` for logging purposes.

        :return: True if the `NoLoadTest` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        no_load_test = NoLoadTest(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        no_load_test.energised_end_voltage = result_set.get_int(table.energised_end_voltage.query_index, on_none=None)
        no_load_test.exciting_current = result_set.get_float(table.exciting_current.query_index, on_none=None)
        no_load_test.exciting_current_zero = result_set.get_float(table.exciting_current_zero.query_index, on_none=None)
        no_load_test.loss = result_set.get_int(table.loss.query_index, on_none=None)
        no_load_test.loss_zero = result_set.get_int(table.loss_zero.query_index, on_none=None)

        return self._load_transformer_test(no_load_test, table, result_set) and self._add_or_throw(no_load_test)

    def load_open_circuit_tests(self, table: TableOpenCircuitTests, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create an `OpenCircuitTest` and populate its fields from `TableOpenCircuitTests`.

        :param table: The database table to read the `OpenCircuitTest` fields from.
        :param result_set: The record in the database table containing the fields for this `OpenCircuitTest`.
        :param set_identifier: A callback to register the mRID of this `OpenCircuitTest` for logging purposes.

        :return: True if the `OpenCircuitTest` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        open_circuit_test = OpenCircuitTest(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        open_circuit_test.energised_end_step = result_set.get_int(table.energised_end_step.query_index, on_none=None)
        open_circuit_test.energised_end_voltage = result_set.get_int(table.energised_end_voltage.query_index, on_none=None)
        open_circuit_test.open_end_step = result_set.get_int(table.open_end_step.query_index, on_none=None)
        open_circuit_test.open_end_voltage = result_set.get_int(table.open_end_voltage.query_index, on_none=None)
        open_circuit_test.phase_shift = result_set.get_float(table.phase_shift.query_index, on_none=None)

        return self._load_transformer_test(open_circuit_test, table, result_set) and self._add_or_throw(open_circuit_test)

    def load_overhead_wire_info(self, table: TableOverheadWireInfo, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create an `OverheadWireInfo` and populate its fields from `TableOverheadWireInfo`.

        :param table: The database table to read the `OverheadWireInfo` fields from.
        :param result_set: The record in the database table containing the fields for this `OverheadWireInfo`.
        :param set_identifier: A callback to register the mRID of this `OverheadWireInfo` for logging purposes.

        :return: True if the `OverheadWireInfo` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        overhead_wire_info = OverheadWireInfo(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_wire_info(overhead_wire_info, table, result_set) and self._add_or_throw(overhead_wire_info)

    def load_power_transformer_info(self, table: TablePowerTransformerInfo, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `PowerTransformerInfo` and populate its fields from `TablePowerTransformerInfo`.

        :param table: The database table to read the `PowerTransformerInfo` fields from.
        :param result_set: The record in the database table containing the fields for this `PowerTransformerInfo`.
        :param set_identifier: A callback to register the mRID of this `PowerTransformerInfo` for logging purposes.

        :return: True if the `PowerTransformerInfo` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        power_transformer_info = PowerTransformerInfo(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_asset_info(power_transformer_info, table, result_set) and self._add_or_throw(power_transformer_info)

    def load_short_circuit_tests(self, table: TableShortCircuitTests, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `ShortCircuitTest` and populate its fields from `TableShortCircuitTests`.

        :param table: The database table to read the `ShortCircuitTest` fields from.
        :param result_set: The record in the database table containing the fields for this `ShortCircuitTest`.
        :param set_identifier: A callback to register the mRID of this `ShortCircuitTest` for logging purposes.

        :return: True if the `ShortCircuitTest` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        short_circuit_test = ShortCircuitTest(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        short_circuit_test.current = result_set.get_float(table.current.query_index, on_none=None)
        short_circuit_test.energised_end_step = result_set.get_int(table.energised_end_step.query_index, on_none=None)
        short_circuit_test.grounded_end_step = result_set.get_int(table.grounded_end_step.query_index, on_none=None)
        short_circuit_test.leakage_impedance = result_set.get_float(table.leakage_impedance.query_index, on_none=None)
        short_circuit_test.leakage_impedance_zero = result_set.get_float(table.leakage_impedance_zero.query_index, on_none=None)
        short_circuit_test.loss = result_set.get_int(table.loss.query_index, on_none=None)
        short_circuit_test.loss_zero = result_set.get_int(table.loss_zero.query_index, on_none=None)
        short_circuit_test.power = result_set.get_int(table.power.query_index, on_none=None)
        short_circuit_test.voltage = result_set.get_float(table.voltage.query_index, on_none=None)
        short_circuit_test.voltage_ohmic_part = result_set.get_float(table.voltage_ohmic_part.query_index, on_none=None)

        return self._load_transformer_test(short_circuit_test, table, result_set) and self._add_or_throw(short_circuit_test)

    def load_shunt_compensator_info(self, table: TableShuntCompensatorInfo, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `ShuntCompensatorInfo` and populate its fields from `TableShuntCompensatorInfo`.

        :param table: The database table to read the `ShuntCompensatorInfo` fields from.
        :param result_set: The record in the database table containing the fields for this `ShuntCompensatorInfo`.
        :param set_identifier: A callback to register the mRID of this `ShuntCompensatorInfo` for logging purposes.

        :return: True if the `ShuntCompensatorInfo` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        shunt_compensator_info = ShuntCompensatorInfo(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        shunt_compensator_info.max_power_loss = result_set.get_int(table.max_power_loss.query_index, on_none=None)
        shunt_compensator_info.rated_current = result_set.get_int(table.rated_current.query_index, on_none=None)
        shunt_compensator_info.rated_reactive_power = result_set.get_int(table.rated_reactive_power.query_index, on_none=None)
        shunt_compensator_info.rated_voltage = result_set.get_int(table.rated_voltage.query_index, on_none=None)

        return self._load_asset_info(shunt_compensator_info, table, result_set) and self._add_or_throw(shunt_compensator_info)

    def load_switch_info(self, table: TableSwitchInfo, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `SwitchInfo` and populate its fields from `TableSwitchInfo`.

        :param table: The database table to read the `SwitchInfo` fields from.
        :param result_set: The record in the database table containing the fields for this `SwitchInfo`.
        :param set_identifier: A callback to register the mRID of this `SwitchInfo` for logging purposes.

        :return: True if the `SwitchInfo` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        switch_info = SwitchInfo(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        switch_info.rated_interrupting_time = result_set.get_float(table.rated_interrupting_time.query_index, on_none=None)

        return self._load_asset_info(switch_info, table, result_set) and self._add_or_throw(switch_info)

    def load_transformer_end_info(self, table: TableTransformerEndInfo, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `TransformerEndInfo` and populate its fields from `TableTransformerEndInfo`.

        :param table: The database table to read the `TransformerEndInfo` fields from.
        :param result_set: The record in the database table containing the fields for this `TransformerEndInfo`.
        :param set_identifier: A callback to register the mRID of this `TransformerEndInfo` for logging purposes.

        :return: True if the `TransformerEndInfo` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        transformer_end_info = TransformerEndInfo(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        transformer_end_info.connection_kind = WindingConnection[result_set.get_string(table.connection_kind.query_index)]
        transformer_end_info.emergency_s = result_set.get_int(table.emergency_s.query_index, on_none=None)
        transformer_end_info.end_number = result_set.get_int(table.end_number.query_index)
        transformer_end_info.insulation_u = result_set.get_int(table.insulation_u.query_index, on_none=None)
        transformer_end_info.phase_angle_clock = result_set.get_int(table.phase_angle_clock.query_index, on_none=None)
        transformer_end_info.r = result_set.get_float(table.r.query_index, on_none=None)
        transformer_end_info.rated_s = result_set.get_int(table.rated_s.query_index, on_none=None)
        transformer_end_info.rated_u = result_set.get_int(table.rated_u.query_index, on_none=None)
        transformer_end_info.short_term_s = result_set.get_int(table.short_term_s.query_index, on_none=None)

        transformer_end_info.transformer_tank_info = self._ensure_get(
            result_set.get_string(table.transformer_tank_info_mrid.query_index, on_none=None),
            TransformerTankInfo
        )
        transformer_end_info.energised_end_no_load_tests = self._ensure_get(
            result_set.get_string(table.energised_end_no_load_tests.query_index, on_none=None),
            NoLoadTest
        )
        transformer_end_info.energised_end_short_circuit_tests = self._ensure_get(
            result_set.get_string(table.energised_end_short_circuit_tests.query_index, on_none=None),
            ShortCircuitTest
        )
        transformer_end_info.grounded_end_short_circuit_tests = self._ensure_get(
            result_set.get_string(table.grounded_end_short_circuit_tests.query_index, on_none=None),
            ShortCircuitTest
        )
        transformer_end_info.open_end_open_circuit_tests = self._ensure_get(
            result_set.get_string(table.open_end_open_circuit_tests.query_index, on_none=None),
            OpenCircuitTest
        )
        transformer_end_info.energised_end_open_circuit_tests = self._ensure_get(
            result_set.get_string(table.energised_end_open_circuit_tests.query_index, on_none=None),
            OpenCircuitTest
        )

        if transformer_end_info.transformer_tank_info is not None:
            transformer_end_info.transformer_tank_info.add_transformer_end_info(transformer_end_info)

        return self._load_asset_info(transformer_end_info, table, result_set) and self._add_or_throw(transformer_end_info)

    def load_transformer_tank_info(self, table: TableTransformerTankInfo, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `TransformerTankInfo` and populate its fields from `TableTransformerTankInfo`.

        :param table: The database table to read the `TransformerTankInfo` fields from.
        :param result_set: The record in the database table containing the fields for this `TransformerTankInfo`.
        :param set_identifier: A callback to register the mRID of this `TransformerTankInfo` for logging purposes.

        :return: True if the `TransformerTankInfo` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        transformer_tank_info = TransformerTankInfo(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        transformer_tank_info.power_transformer_info = self._ensure_get(
            result_set.get_string(table.power_transformer_info_mrid.query_index, on_none=None),
            PowerTransformerInfo
        )
        if transformer_tank_info.power_transformer_info is not None:
            transformer_tank_info.power_transformer_info.add_transformer_tank_info(transformer_tank_info)

        return self._load_asset_info(transformer_tank_info, table, result_set) and self._add_or_throw(transformer_tank_info)

    def _load_transformer_test(self, transformer_test: TransformerTest, table: TableTransformerTest, result_set: ResultSet) -> bool:
        transformer_test.base_power = result_set.get_int(table.base_power.query_index, on_none=None)
        transformer_test.temperature = result_set.get_float(table.temperature.query_index, on_none=None)

        return self._load_identified_object(transformer_test, table, result_set)

    def _load_wire_info(self, wire_info: WireInfo, table: TableWireInfo, result_set: ResultSet) -> bool:
        wire_info.rated_current = result_set.get_int(table.rated_current.query_index, on_none=None)
        wire_info.material = WireMaterialKind[result_set.get_string(table.material.query_index)]

        return self._load_asset_info(wire_info, table, result_set)

    ###################
    # IEC61968 Assets #
    ###################

    def _load_asset(self, asset: Asset, table: TableAssets, result_set: ResultSet) -> bool:
        asset.location = self._ensure_get(
            result_set.get_string(table.location_mrid.query_index, on_none=None),
            Location
        )

        return self._load_identified_object(asset, table, result_set)

    def _load_asset_container(self, asset_container: AssetContainer, table: TableAssetContainers, result_set: ResultSet) -> bool:
        return self._load_asset(asset_container, table, result_set)

    def _load_asset_info(self, asset_info: AssetInfo, table: TableAssetInfo, result_set: ResultSet) -> bool:
        return self._load_identified_object(asset_info, table, result_set)

    def _load_asset_organisation_role(self, asset_organisation_role: AssetOrganisationRole, table: TableAssetOrganisationRoles, result_set: ResultSet) -> bool:
        return self._load_organisation_role(asset_organisation_role, table, result_set)

    def _load_structure(self, structure: Structure, table: TableStructures, result_set: ResultSet) -> bool:
        return self._load_asset_container(structure, table, result_set)

    def load_asset_owners(self, table: TableAssetOwners, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create an `AssetOwner` and populate its fields from `TableAssetOwners`.

        :param table: The database table to read the `AssetOwner` fields from.
        :param result_set: The record in the database table containing the fields for this `AssetOwner`.
        :param set_identifier: A callback to register the mRID of this `AssetOwner` for logging purposes.

        :return: True if the `AssetOwner` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        asset_owner = AssetOwner(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_asset_organisation_role(asset_owner, table, result_set) and self._add_or_throw(asset_owner)

    def load_poles(self, table: TablePoles, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `Pole` and populate its fields from `TablePoles`.

        :param table: The database table to read the `Pole` fields from.
        :param result_set: The record in the database table containing the fields for this `Pole`.
        :param set_identifier: A callback to register the mRID of this `Pole` for logging purposes.

        :return: True if the `Pole` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        pole = Pole(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        pole.classification = result_set.get_string(table.classification.query_index, on_none="")

        return self._load_structure(pole, table, result_set) and self._add_or_throw(pole)

    def load_streetlights(self, table: TableStreetlights, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `Streetlight` and populate its fields from `TableStreetlights`.

        :param table: The database table to read the `Streetlight` fields from.
        :param result_set: The record in the database table containing the fields for this `Streetlight`.
        :param set_identifier: A callback to register the mRID of this `Streetlight` for logging purposes.

        :return: True if the `Streetlight` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        streetlight = Streetlight(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        streetlight.lamp_kind = StreetlightLampKind[result_set.get_string(table.lamp_kind.query_index)]
        streetlight.light_rating = result_set.get_int(table.light_rating.query_index, on_none=None)
        streetlight.pole = self._ensure_get(
            result_set.get_string(table.pole_mrid.query_index, on_none=None),
            Pole
        )
        if streetlight.pole is not None:
            streetlight.pole.add_streetlight(streetlight)

        return self._load_asset(streetlight, table, result_set) and self._add_or_throw(streetlight)

    ###################
    # IEC61968 Common #
    ###################

    def load_locations(self, table: TableLocations, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `Location` and populate its fields from `TableLocations`.

        :param table: The database table to read the `Location` fields from.
        :param result_set: The record in the database table containing the fields for this `Location`.
        :param set_identifier: A callback to register the mRID of this `Location` for logging purposes.

        :return: True if the `Location` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        location = Location(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_identified_object(location, table, result_set) and self._add_or_throw(location)

    def load_location_street_addresses(self, table: TableLocationStreetAddresses, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `set_identifier` and populate its fields from `TableLocationStreetAddresses`.

        :param table: The database table to read the `set_identifier` fields from.
        :param result_set: The record in the database table containing the fields for this `set_identifier`.
        :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

        :return: True if the `set_identifier` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        location_mrid = set_identifier(result_set.get_string(table.location_mrid.query_index))
        field = TableLocationStreetAddressField[result_set.get_string(table.address_field.query_index)]

        location = self._service.get(location_mrid, Location)

        if field == TableLocationStreetAddressField.mainAddress:
            location.main_address = self._load_street_address(table, result_set)

        return True

    """
    Create a `set_identifier` and populate its fields from `TablePositionPoints`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_position_points(self, table: TablePositionPoints, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        location_mrid = set_identifier(result_set.get_string(table.location_mrid.query_index))
        sequence_number = result_set.get_int(table.sequence_number.query_index)

        location = self._service.get(location_mrid, Location)

        location.insert_point(
            PositionPoint(
                result_set.get_float(table.x_position.query_index),
                result_set.get_float(table.y_position.query_index)
            ),
            sequence_number
        )

        return True

    def _load_street_address(self, table: TableStreetAddresses, result_set: ResultSet) -> StreetAddress:
        return StreetAddress(
            result_set.get_string(table.postal_code.query_index, on_none=""),
            self._load_town_detail(table, result_set),
            result_set.get_string(table.po_box.query_index, on_none=""),
            self._load_street_detail(table, result_set)
        )

    @staticmethod
    def _load_street_detail(table: TableStreetAddresses, result_set: ResultSet) -> Optional[StreetDetail]:
        sd = StreetDetail(
            result_set.get_string(table.building_name.query_index, on_none=""),
            result_set.get_string(table.floor_identification.query_index, on_none=""),
            result_set.get_string(table.street_name.query_index, on_none=""),
            result_set.get_string(table.number.query_index, on_none=""),
            result_set.get_string(table.suite_number.query_index, on_none=""),
            result_set.get_string(table.type.query_index, on_none=""),
            result_set.get_string(table.display_address.query_index, on_none="")
        )

        return sd if not sd.all_fields_empty() else None

    @staticmethod
    def _load_town_detail(table: TableTownDetails, result_set: ResultSet) -> Optional[TownDetail]:
        td = TownDetail(
            result_set.get_string(table.town_name.query_index, on_none=None),
            result_set.get_string(table.state_or_province.query_index, on_none=None)
        )

        return td if not td.all_fields_null_or_empty() else None

    #####################################
    # IEC61968 infIEC61968 InfAssetInfo #
    #####################################

    """
    Create a `RelayInfo` and populate its fields from `TableRelayInfo`.

    :param table: The database table to read the `RelayInfo` fields from.
    :param result_set: The record in the database table containing the fields for this `RelayInfo`.
    :param set_identifier: A callback to register the mRID of this `RelayInfo` for logging purposes.

    :return: True if the `RelayInfo` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_relay_info(self, table: TableRelayInfo, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        relay_info = RelayInfo(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        relay_info.curve_setting = result_set.get_string(table.curve_setting.query_index, on_none=None)
        relay_info.reclose_fast = result_set.get_boolean(table.reclose_fast.query_index, on_none=None)

        return self._load_asset_info(relay_info, table, result_set) and self._add_or_throw(relay_info)

    """
    Adds a delay to a `RelayInfo` and populate its fields from `TableRecloseDelays`.

    :param table: The database table to read the delay fields from.
    :param result_set: The record in the database table containing the fields for this delay.
    :param set_identifier: A callback to register the mRID of this delay for logging purposes.

    :return: True if the delay was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_reclose_delays(self, table: TableRecloseDelays, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        # Note TableRecloseDelays.selectSql ensures we process ratings in the correct order.
        relay_info_mrid = result_set.get_string(table.relay_info_mrid.query_index)
        reclose_delay = result_set.get_float(table.reclose_delay.query_index)
        set_identifier(f"{relay_info_mrid}.s{reclose_delay}")

        cri = self._ensure_get(relay_info_mrid, RelayInfo)
        if cri:
            cri.add_delay(reclose_delay)

        return True

    """
    Create a `CurrentTransformerInfo` and populate its fields from `TableCurrentTransformerInfo`.

    :param table: The database table to read the `CurrentTransformerInfo` fields from.
    :param result_set: The record in the database table containing the fields for this `CurrentTransformerInfo`.
    :param set_identifier: A callback to register the mRID of this `CurrentTransformerInfo` for logging purposes.

    :return: True if the `CurrentTransformerInfo` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_current_transformer_info(self, table: TableCurrentTransformerInfo, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        current_transformer_info = CurrentTransformerInfo(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        current_transformer_info.accuracy_class = result_set.get_string(table.accuracy_class.query_index, on_none=None)
        current_transformer_info.accuracy_limit = result_set.get_float(table.accuracy_limit.query_index, on_none=None)
        current_transformer_info.core_count = result_set.get_int(table.core_count.query_index, on_none=None)
        current_transformer_info.ct_class = result_set.get_string(table.ct_class.query_index, on_none=None)
        current_transformer_info.knee_point_voltage = result_set.get_int(table.knee_point_voltage.query_index, on_none=None)
        current_transformer_info.max_ratio = result_set.get_ratio(table.max_ratio_numerator.query_index, table.max_ratio_denominator.query_index, on_none=None)
        current_transformer_info.nominal_ratio = result_set.get_ratio(
            table.nominal_ratio_numerator.query_index,
            table.nominal_ratio_denominator.query_index,
            on_none=None
        )
        current_transformer_info.primary_ratio = result_set.get_float(table.primary_ratio.query_index, on_none=None)
        current_transformer_info.rated_current = result_set.get_int(table.rated_current.query_index, on_none=None)
        current_transformer_info.secondary_fls_rating = result_set.get_int(table.secondary_fls_rating.query_index, on_none=None)
        current_transformer_info.secondary_ratio = result_set.get_float(table.secondary_ratio.query_index, on_none=None)
        current_transformer_info.usage = result_set.get_string(table.usage.query_index, on_none=None)

        return self._load_asset_info(current_transformer_info, table, result_set) and self._add_or_throw(current_transformer_info)

    """
    Create a `PotentialTransformerInfo` and populate its fields from `TablePotentialTransformerInfo`.

    :param table: The database table to read the `PotentialTransformerInfo` fields from.
    :param result_set: The record in the database table containing the fields for this `PotentialTransformerInfo`.
    :param set_identifier: A callback to register the mRID of this `PotentialTransformerInfo` for logging purposes.

    :return: True if the `PotentialTransformerInfo` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_potential_transformer_info(self, table: TablePotentialTransformerInfo, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        potential_transformer_info = PotentialTransformerInfo(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        potential_transformer_info.accuracy_class = result_set.get_string(table.accuracy_class.query_index, on_none=None)
        potential_transformer_info.nominal_ratio = result_set.get_ratio(
            table.nominal_ratio_numerator.query_index,
            table.nominal_ratio_denominator.query_index,
            on_none=None
        )
        potential_transformer_info.primary_ratio = result_set.get_float(table.primary_ratio.query_index, on_none=None)
        potential_transformer_info.pt_class = result_set.get_string(table.pt_class.query_index, on_none=None)
        potential_transformer_info.rated_voltage = result_set.get_int(table.rated_voltage.query_index, on_none=None)
        potential_transformer_info.secondary_ratio = result_set.get_float(table.secondary_ratio.query_index, on_none=None)

        return self._load_asset_info(potential_transformer_info, table, result_set) and self._add_or_throw(potential_transformer_info)

    #####################
    # IEC61968 Metering #
    #####################

    def _load_end_device(self, end_device: EndDevice, table: TableEndDevices, result_set: ResultSet) -> bool:
        end_device.customer_mrid = result_set.get_string(table.customer_mrid.query_index, on_none=None)
        end_device.service_location = self._ensure_get(
            result_set.get_string(table.service_location_mrid.query_index, on_none=None),
            Location
        )

        return self._load_asset_container(end_device, table, result_set)

    """
    Create a `Meter` and populate its fields from `TableMeters`.

    :param table: The database table to read the `Meter` fields from.
    :param result_set: The record in the database table containing the fields for this `Meter`.
    :param set_identifier: A callback to register the mRID of this `Meter` for logging purposes.

    :return: True if the `Meter` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_meters(self, table: TableMeters, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        meter = Meter(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_end_device(meter, table, result_set) and self._add_or_throw(meter)

    """
    Create a `UsagePoint` and populate its fields from `TableUsagePoints`.

    :param table: The database table to read the `UsagePoint` fields from.
    :param result_set: The record in the database table containing the fields for this `UsagePoint`.
    :param set_identifier: A callback to register the mRID of this `UsagePoint` for logging purposes.

    :return: True if the `UsagePoint` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_usage_points(self, table: TableUsagePoints, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        usage_point = UsagePoint(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        usage_point.usage_point_location = self._ensure_get(
            result_set.get_string(table.location_mrid.query_index, on_none=None),
            Location
        )
        usage_point.is_virtual = result_set.get_boolean(table.is_virtual.query_index)
        usage_point.connection_category = result_set.get_string(table.connection_category.query_index, on_none=None)
        usage_point.rated_power = result_set.get_int(table.rated_power.query_index, on_none=None)
        usage_point.approved_inverter_capacity = result_set.get_int(table.approved_inverter_capacity.query_index, on_none=None)

        return self._load_identified_object(usage_point, table, result_set) and self._add_or_throw(usage_point)

    #######################
    # IEC61968 Operations #
    #######################

    """
    Create an `OperationalRestriction` and populate its fields from `TableOperationalRestrictions`.

    :param table: The database table to read the `OperationalRestriction` fields from.
    :param result_set: The record in the database table containing the fields for this `OperationalRestriction`.
    :param set_identifier: A callback to register the mRID of this `OperationalRestriction` for logging purposes.

    :return: True if the `OperationalRestriction` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_operational_restrictions(self, table: TableOperationalRestrictions, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        operational_restriction = OperationalRestriction(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_document(operational_restriction, table, result_set) and self._add_or_throw(operational_restriction)

    #####################################
    # IEC61970 Base Auxiliary Equipment #
    #####################################

    def _load_auxiliary_equipment(self, auxiliary_equipment: AuxiliaryEquipment, table: TableAuxiliaryEquipment, result_set: ResultSet) -> bool:
        auxiliary_equipment.terminal = self._ensure_get(
            result_set.get_string(table.terminal_mrid.query_index, on_none=None),
            Terminal
        )

        return self._load_equipment(auxiliary_equipment, table, result_set)

    """
    Create a `CurrentTransformer` and populate its fields from `TableCurrentTransformers`.

    :param table: The database table to read the `CurrentTransformer` fields from.
    :param result_set: The record in the database table containing the fields for this `CurrentTransformer`.
    :param set_identifier: A callback to register the mRID of this `CurrentTransformer` for logging purposes.

    :return: True if the `CurrentTransformer` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_current_transformers(self, table: TableCurrentTransformers, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        current_transformer = CurrentTransformer(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        current_transformer.asset_info = self._ensure_get(
            result_set.get_string(table.current_transformer_info_mrid.query_index, on_none=None),
            CurrentTransformerInfo
        )
        current_transformer.core_burden = result_set.get_int(table.core_burden.query_index, on_none=None)

        return self._load_sensor(current_transformer, table, result_set) and self._add_or_throw(current_transformer)

    """
    Create a `FaultIndicator` and populate its fields from `TableFaultIndicators`.

    :param table: The database table to read the `FaultIndicator` fields from.
    :param result_set: The record in the database table containing the fields for this `FaultIndicator`.
    :param set_identifier: A callback to register the mRID of this `FaultIndicator` for logging purposes.

    :return: True if the `FaultIndicator` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_fault_indicators(self, table: TableFaultIndicators, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        fault_indicator = FaultIndicator(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_auxiliary_equipment(fault_indicator, table, result_set) and self._add_or_throw(fault_indicator)

    """
    Create a `PotentialTransformer` and populate its fields from `TablePotentialTransformers`.

    :param table: The database table to read the `PotentialTransformer` fields from.
    :param result_set: The record in the database table containing the fields for this `PotentialTransformer`.
    :param set_identifier: A callback to register the mRID of this `PotentialTransformer` for logging purposes.

    :return: True if the `PotentialTransformer` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_potential_transformers(self, table: TablePotentialTransformers, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        potential_transformer = PotentialTransformer(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        potential_transformer.asset_info = self._ensure_get(
            result_set.get_string(table.potential_transformer_info_mrid.query_index, on_none=None),
            PotentialTransformerInfo
        )
        potential_transformer.type = PotentialTransformerKind[result_set.get_string(table.type.query_index)]

        return self._load_sensor(potential_transformer, table, result_set) and self._add_or_throw(potential_transformer)

    def _load_sensor(self, sensor: Sensor, table: TableSensors, result_set: ResultSet) -> bool:
        return self._load_auxiliary_equipment(sensor, table, result_set)

    ######################
    # IEC61970 Base Core #
    ######################

    def _load_ac_dc_terminal(self, ac_dc_terminal: AcDcTerminal, table: TableAcDcTerminals, result_set: ResultSet) -> bool:
        return self._load_identified_object(ac_dc_terminal, table, result_set)

    """
    Create a `BaseVoltage` and populate its fields from `TableBaseVoltages`.

    :param table: The database table to read the `BaseVoltage` fields from.
    :param result_set: The record in the database table containing the fields for this `BaseVoltage`.
    :param set_identifier: A callback to register the mRID of this `BaseVoltage` for logging purposes.

    :return: True if the `BaseVoltage` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_base_voltages(self, table: TableBaseVoltages, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        base_voltage = BaseVoltage(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        base_voltage.nominal_voltage = result_set.get_int(table.nominal_voltage.query_index)

        return self._load_identified_object(base_voltage, table, result_set) and self._add_or_throw(base_voltage)

    def _load_conducting_equipment(self, conducting_equipment: ConductingEquipment, table: TableConductingEquipment, result_set: ResultSet) -> bool:
        conducting_equipment.base_voltage = self._ensure_get(
            result_set.get_string(table.base_voltage_mrid.query_index, on_none=None),
            BaseVoltage
        )

        return self._load_equipment(conducting_equipment, table, result_set)

    """
    Create a `ConnectivityNode` and populate its fields from `TableConnectivityNodes`.

    :param table: The database table to read the `ConnectivityNode` fields from.
    :param result_set: The record in the database table containing the fields for this `ConnectivityNode`.
    :param set_identifier: A callback to register the mRID of this `ConnectivityNode` for logging purposes.

    :return: True if the `ConnectivityNode` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_connectivity_nodes(self, table: TableConnectivityNodes, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        connectivity_node = ConnectivityNode(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_identified_object(connectivity_node, table, result_set) and self._add_or_throw(connectivity_node)

    def _load_connectivity_node_container(
        self,
        connectivity_node_container: ConnectivityNodeContainer,
        table: TableConnectivityNodeContainers,
        result_set: ResultSet
    ) -> bool:
        return self._load_power_system_resource(connectivity_node_container, table, result_set)

    def _load_equipment(self, equipment: Equipment, table: TableEquipment, result_set: ResultSet) -> bool:
        equipment.normally_in_service = result_set.get_boolean(table.normally_in_service.query_index)
        equipment.in_service = result_set.get_boolean(table.in_service.query_index)
        equipment.commissioned_date = result_set.get_instant(table.commissioned_date.query_index, on_none=None)

        return self._load_power_system_resource(equipment, table, result_set)

    def _load_equipment_container(self, equipment_container: EquipmentContainer, table: TableEquipmentContainers, result_set: ResultSet) -> bool:
        return self._load_connectivity_node_container(equipment_container, table, result_set)

    """
    Create a `Feeder` and populate its fields from `TableFeeders`.

    :param table: The database table to read the `Feeder` fields from.
    :param result_set: The record in the database table containing the fields for this `Feeder`.
    :param set_identifier: A callback to register the mRID of this `Feeder` for logging purposes.

    :return: True if the `Feeder` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_feeders(self, table: TableFeeders, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        feeder = Feeder(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        feeder.normal_head_terminal = self._ensure_get(
            result_set.get_string(table.normal_head_terminal_mrid.query_index, on_none=None),
            Terminal
        )
        feeder.normal_energizing_substation = self._ensure_get(
            result_set.get_string(table.normal_energizing_substation_mrid.query_index, on_none=None),
            Substation
        )

        if feeder.normal_energizing_substation:
            feeder.normal_energizing_substation.add_feeder(feeder)

        return self._load_equipment_container(feeder, table, result_set) and self._add_or_throw(feeder)

    """
    Create a `GeographicalRegion` and populate its fields from `TableGeographicalRegions`.

    :param table: The database table to read the `GeographicalRegion` fields from.
    :param result_set: The record in the database table containing the fields for this `GeographicalRegion`.
    :param set_identifier: A callback to register the mRID of this `GeographicalRegion` for logging purposes.

    :return: True if the `GeographicalRegion` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_geographical_regions(self, table: TableGeographicalRegions, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        geographical_region = GeographicalRegion(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_identified_object(geographical_region, table, result_set) and self._add_or_throw(geographical_region)

    def _load_power_system_resource(self, power_system_resource: PowerSystemResource, table: TablePowerSystemResources, result_set: ResultSet) -> bool:
        power_system_resource.location = self._ensure_get(
            result_set.get_string(table.location_mrid.query_index, on_none=None),
            Location
        )
        power_system_resource.num_controls = result_set.get_int(table.num_controls.query_index)

        return self._load_identified_object(power_system_resource, table, result_set)

    """
    Create a `Site` and populate its fields from `TableSites`.

    :param table: The database table to read the `Site` fields from.
    :param result_set: The record in the database table containing the fields for this `Site`.
    :param set_identifier: A callback to register the mRID of this `Site` for logging purposes.

    :return: True if the `Site` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_sites(self, table: TableSites, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        site = Site(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_equipment_container(site, table, result_set) and self._add_or_throw(site)

    """
    Create a `SubGeographicalRegion` and populate its fields from `TableSubGeographicalRegions`.

    :param table: The database table to read the `SubGeographicalRegion` fields from.
    :param result_set: The record in the database table containing the fields for this `SubGeographicalRegion`.
    :param set_identifier: A callback to register the mRID of this `SubGeographicalRegion` for logging purposes.

    :return: True if the `SubGeographicalRegion` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_sub_geographical_regions(self, table: TableSubGeographicalRegions, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        sub_geographical_region = SubGeographicalRegion(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        sub_geographical_region.geographical_region = self._ensure_get(
            result_set.get_string(table.geographical_region_mrid.query_index, on_none=None),
            GeographicalRegion
        )

        if sub_geographical_region.geographical_region:
            sub_geographical_region.geographical_region.add_sub_geographical_region(sub_geographical_region)

        return self._load_identified_object(sub_geographical_region, table, result_set) and self._add_or_throw(sub_geographical_region)

    """
    Create a `Substation` and populate its fields from `TableSubstations`.

    :param table: The database table to read the `Substation` fields from.
    :param result_set: The record in the database table containing the fields for this `Substation`.
    :param set_identifier: A callback to register the mRID of this `Substation` for logging purposes.

    :return: True if the `Substation` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_substations(self, table: TableSubstations, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        substation = Substation(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        substation.sub_geographical_region = self._ensure_get(
            result_set.get_string(table.sub_geographical_region_mrid.query_index, on_none=None),
            SubGeographicalRegion
        )

        if substation.sub_geographical_region:
            substation.sub_geographical_region.add_substation(substation)

        return self._load_equipment_container(substation, table, result_set) and self._add_or_throw(substation)

    """
    Create a `Terminal` and populate its fields from `TableTerminals`.

    :param table: The database table to read the `Terminal` fields from.
    :param result_set: The record in the database table containing the fields for this `Terminal`.
    :param set_identifier: A callback to register the mRID of this `Terminal` for logging purposes.

    :return: True if the `Terminal` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_terminals(self, table: TableTerminals, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        terminal = Terminal(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        terminal.sequence_number = result_set.get_int(table.sequence_number.query_index)
        terminal.conducting_equipment = self._ensure_get(
            result_set.get_string(table.conducting_equipment_mrid.query_index, on_none=None),
            ConductingEquipment
        )
        terminal.phases = PhaseCode[result_set.get_string(table.phases.query_index)]

        if terminal.conducting_equipment:
            terminal.conducting_equipment.add_terminal(terminal)

        self._service.connect_by_mrid(terminal, result_set.get_string(table.connectivity_node_mrid.query_index, on_none=None))

        return self._load_ac_dc_terminal(terminal, table, result_set) and self._add_or_throw(terminal)

    #############################
    # IEC61970 Base Equivalents #
    #############################

    """
    Create an `EquivalentBranch` and populate its fields from `TableEquivalentBranches`.

    :param table: The database table to read the `EquivalentBranch` fields from.
    :param result_set: The record in the database table containing the fields for this `EquivalentBranch`.
    :param set_identifier: A callback to register the mRID of this `EquivalentBranch` for logging purposes.

    :return: True if the `EquivalentBranch` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_equivalent_branches(self, table: TableEquivalentBranches, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        equivalent_branch = EquivalentBranch(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        equivalent_branch.negative_r12 = result_set.get_float(table.negative_r12.query_index, on_none=None)
        equivalent_branch.negative_r21 = result_set.get_float(table.negative_r21.query_index, on_none=None)
        equivalent_branch.negative_x12 = result_set.get_float(table.negative_x12.query_index, on_none=None)
        equivalent_branch.negative_x21 = result_set.get_float(table.negative_x21.query_index, on_none=None)
        equivalent_branch.positive_r12 = result_set.get_float(table.positive_r12.query_index, on_none=None)
        equivalent_branch.positive_r21 = result_set.get_float(table.positive_r21.query_index, on_none=None)
        equivalent_branch.positive_x12 = result_set.get_float(table.positive_x12.query_index, on_none=None)
        equivalent_branch.positive_x21 = result_set.get_float(table.positive_x21.query_index, on_none=None)
        equivalent_branch.r = result_set.get_float(table.r.query_index, on_none=None)
        equivalent_branch.r21 = result_set.get_float(table.r21.query_index, on_none=None)
        equivalent_branch.x = result_set.get_float(table.x.query_index, on_none=None)
        equivalent_branch.x21 = result_set.get_float(table.x21.query_index, on_none=None)
        equivalent_branch.zero_r12 = result_set.get_float(table.zero_r12.query_index, on_none=None)
        equivalent_branch.zero_r21 = result_set.get_float(table.zero_r21.query_index, on_none=None)
        equivalent_branch.zero_x12 = result_set.get_float(table.zero_x12.query_index, on_none=None)
        equivalent_branch.zero_x21 = result_set.get_float(table.zero_x21.query_index, on_none=None)

        return self._load_equivalent_equipment(equivalent_branch, table, result_set) and self._add_or_throw(equivalent_branch)

    def _load_equivalent_equipment(self, equivalent_equipment: EquivalentEquipment, table: TableEquivalentEquipment, result_set: ResultSet) -> bool:
        return self._load_conducting_equipment(equivalent_equipment, table, result_set)

    ######################
    # IEC61970 Base Meas #
    ######################

    """
    Create an `Accumulator` and populate its fields from `TableAccumulators`.

    :param table: The database table to read the `Accumulator` fields from.
    :param result_set: The record in the database table containing the fields for this `Accumulator`.
    :param set_identifier: A callback to register the mRID of this `Accumulator` for logging purposes.

    :return: True if the `Accumulator` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_accumulators(self, table: TableAccumulators, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        meas = Accumulator(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_measurement(meas, table, result_set) and self._add_or_throw(meas)

    """
    Create an `Analog` and populate its fields from `TableAnalogs`.

    :param table: The database table to read the `Analog` fields from.
    :param result_set: The record in the database table containing the fields for this `Analog`.
    :param set_identifier: A callback to register the mRID of this `Analog` for logging purposes.

    :return: True if the `Analog` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_analogs(self, table: TableAnalogs, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        meas = Analog(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        meas.positive_flow_in = result_set.get_boolean(table.positive_flow_in.query_index)

        return self._load_measurement(meas, table, result_set) and self._add_or_throw(meas)

    """
    Create a `Control` and populate its fields from `TableControls`.

    :param table: The database table to read the `Control` fields from.
    :param result_set: The record in the database table containing the fields for this `Control`.
    :param set_identifier: A callback to register the mRID of this `Control` for logging purposes.

    :return: True if the `Control` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_controls(self, table: TableControls, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        control = Control(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        control.power_system_resource_mrid = result_set.get_string(table.power_system_resource_mrid.query_index, on_none=None)

        return self._load_io_point(control, table, result_set) and self._add_or_throw(control)

    """
    Create a `Discrete` and populate its fields from `TableDiscretes`.

    :param table: The database table to read the `Discrete` fields from.
    :param result_set: The record in the database table containing the fields for this `Discrete`.
    :param set_identifier: A callback to register the mRID of this `Discrete` for logging purposes.

    :return: True if the `Discrete` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_discretes(self, table: TableDiscretes, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        meas = Discrete(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_measurement(meas, table, result_set) and self._add_or_throw(meas)

    def _load_io_point(self, io_point: IoPoint, table: TableIoPoints, result_set: ResultSet) -> bool:
        return self._load_identified_object(io_point, table, result_set)

    def _load_measurement(self, measurement: Measurement, table: TableMeasurements, result_set: ResultSet) -> bool:
        measurement.power_system_resource_mrid = result_set.get_string(table.power_system_resource_mrid.query_index, on_none=None)
        measurement.remote_source = self._ensure_get(
            result_set.get_string(table.remote_source_mrid.query_index, on_none=None),
            RemoteSource
        )
        measurement.terminal_mrid = result_set.get_string(table.terminal_mrid.query_index, on_none=None)
        measurement.phases = PhaseCode[result_set.get_string(table.phases.query_index)]
        measurement.unit_symbol = UnitSymbol[result_set.get_string(table.unit_symbol.query_index)]

        if measurement.remote_source:
            measurement.remote_source.measurement = measurement

        return self._load_identified_object(measurement, table, result_set)

    ############################
    # IEC61970 Base Protection #
    ############################

    """
    Create a `CurrentRelay` and populate its fields from `TableCurrentRelays`.

    :param table: The database table to read the `CurrentRelay` fields from.
    :param result_set: The record in the database table containing the fields for this `CurrentRelay`.
    :param set_identifier: A callback to register the mRID of this `CurrentRelay` for logging purposes.

    :return: True if the `CurrentRelay` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_current_relays(self, table: TableCurrentRelays, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        current_relay = CurrentRelay(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        current_relay.current_limit_1 = result_set.get_float(table.current_limit_1.query_index, on_none=None)
        current_relay.inverse_time_flag = result_set.get_boolean(table.inverse_time_flag.query_index, on_none=None)
        current_relay.time_delay_1 = result_set.get_float(table.time_delay_1.query_index, on_none=None)

        return self._load_protection_relay_function(current_relay, table, result_set) and self._add_or_throw(current_relay)

    """
    Create a `DistanceRelay` and populate its fields from `TableDistanceRelays`.

    :param table: The database table to read the `DistanceRelay` fields from.
    :param result_set: The record in the database table containing the fields for this `DistanceRelay`.
    :param set_identifier: A callback to register the mRID of this `DistanceRelay` for logging purposes.

    :return: True if the `DistanceRelay` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_distance_relays(self, table: TableDistanceRelays, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        distance_relay = DistanceRelay(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        distance_relay.backward_blind = result_set.get_float(table.backward_blind.query_index, on_none=None)
        distance_relay.backward_reach = result_set.get_float(table.backward_reach.query_index, on_none=None)
        distance_relay.backward_reactance = result_set.get_float(table.backward_reactance.query_index, on_none=None)
        distance_relay.forward_blind = result_set.get_float(table.forward_blind.query_index, on_none=None)
        distance_relay.forward_reach = result_set.get_float(table.forward_reach.query_index, on_none=None)
        distance_relay.forward_reactance = result_set.get_float(table.forward_reactance.query_index, on_none=None)
        distance_relay.operation_phase_angle1 = result_set.get_float(table.operation_phase_angle1.query_index, on_none=None)
        distance_relay.operation_phase_angle2 = result_set.get_float(table.operation_phase_angle2.query_index, on_none=None)
        distance_relay.operation_phase_angle3 = result_set.get_float(table.operation_phase_angle3.query_index, on_none=None)

        return self._load_protection_relay_function(distance_relay, table, result_set) and self._add_or_throw(distance_relay)

    def _load_protection_relay_function(self,
                                        protection_relay_function: ProtectionRelayFunction,
                                        table: TableProtectionRelayFunctions,
                                        result_set: ResultSet
                                        ) -> bool:
        protection_relay_function.asset_info = self._ensure_get(
            result_set.get_string(table.relay_info_mrid.query_index, on_none=None),
            RelayInfo
        )
        protection_relay_function.model = result_set.get_string(table.model.query_index, on_none=None)
        protection_relay_function.reclosing = result_set.get_boolean(table.reclosing.query_index, on_none=None)
        protection_relay_function.relay_delay_time = result_set.get_float(table.relay_delay_time.query_index, on_none=None)
        protection_relay_function.protection_kind = ProtectionKind[result_set.get_string(table.protection_kind.query_index)]
        protection_relay_function.directable = result_set.get_boolean(table.directable.query_index, on_none=None)
        protection_relay_function.power_direction = PowerDirectionKind[result_set.get_string(table.power_direction.query_index)]

        return self._load_power_system_resource(protection_relay_function, table, result_set)

    """
    Create a `set_identifier` and populate its fields from `TableProtectionRelayFunctionThresholds`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_protection_relay_function_thresholds(
        self,
        table: TableProtectionRelayFunctionThresholds,
        result_set: ResultSet,
        set_identifier: Callable[[str], str]
    ) -> bool:
        protection_relay_function_mrid = set_identifier(result_set.get_string(table.protection_relay_function_mrid.query_index))
        sequence_number = result_set.get_int(table.sequence_number.query_index)

        set_identifier(f"{protection_relay_function_mrid}-threshold{sequence_number}")
        protection_relay_function = self._service.get(protection_relay_function_mrid, ProtectionRelayFunction)

        protection_relay_function.add_threshold(
            RelaySetting(
                UnitSymbol[result_set.get_string(table.unit_symbol.query_index)],
                result_set.get_float(table.value.query_index),
                result_set.get_string(table.name_.query_index, on_none=None)
            ),
            sequence_number
        )

        return True

    """
    Adds a time limit to a `ProtectionRelayFunction` and populate its fields from `TableProtectionRelayFunctionTimeLimits`.

    :param table: The database table to read the time limit fields from.
    :param result_set: The record in the database table containing the fields for this time limit.
    :param set_identifier: A callback to register the mRID of this time limit for logging purposes.

    :return: True if the time limit was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_protection_relay_function_time_limits(
        self,
        table: TableProtectionRelayFunctionTimeLimits,
        result_set: ResultSet,
        set_identifier: Callable[[str], str]
    ) -> bool:
        # Note TableProtectionRelayFunctionTimeLimits.selectSql ensures we process ratings in the correct order.
        protection_relay_function_mrid = set_identifier(result_set.get_string(table.protection_relay_function_mrid.query_index))
        sequence_number = result_set.get_int(table.sequence_number.query_index)
        time_limit = result_set.get_float(table.time_limit.query_index)

        set_identifier(f"{protection_relay_function_mrid} time limit {sequence_number}")

        protection_relay_function = self._service.get(protection_relay_function_mrid, ProtectionRelayFunction)
        protection_relay_function.add_time_limit(time_limit)

        return True

    """
    Create a `ProtectionRelayScheme` and populate its fields from `TableProtectionRelaySchemes`.

    :param table: The database table to read the `ProtectionRelayScheme` fields from.
    :param result_set: The record in the database table containing the fields for this `ProtectionRelayScheme`.
    :param set_identifier: A callback to register the mRID of this `ProtectionRelayScheme` for logging purposes.

    :return: True if the `ProtectionRelayScheme` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_protection_relay_schemes(self, table: TableProtectionRelaySchemes, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        protection_relay_scheme = ProtectionRelayScheme(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        protection_relay_scheme.system = self._ensure_get(
            result_set.get_string(table.system_mrid.query_index, on_none=None),
            ProtectionRelaySystem
        )
        if protection_relay_scheme.system:
            protection_relay_scheme.system.add_scheme(protection_relay_scheme)

        return self._load_identified_object(protection_relay_scheme, table, result_set) and self._add_or_throw(protection_relay_scheme)

    """
    Create a `ProtectionRelaySystem` and populate its fields from `TableProtectionRelaySystems`.

    :param table: The database table to read the `ProtectionRelaySystem` fields from.
    :param result_set: The record in the database table containing the fields for this `ProtectionRelaySystem`.
    :param set_identifier: A callback to register the mRID of this `ProtectionRelaySystem` for logging purposes.

    :return: True if the `ProtectionRelaySystem` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_protection_relay_systems(self, table: TableProtectionRelaySystems, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        protection_relay_system = ProtectionRelaySystem(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        protection_relay_system.protection_kind = ProtectionKind[result_set.get_string(table.protection_kind.query_index)]

        return self._load_equipment(protection_relay_system, table, result_set) and self._add_or_throw(protection_relay_system)

    """
    Create a `VoltageRelay` and populate its fields from `TableVoltageRelays`.

    :param table: The database table to read the `VoltageRelay` fields from.
    :param result_set: The record in the database table containing the fields for this `VoltageRelay`.
    :param set_identifier: A callback to register the mRID of this `VoltageRelay` for logging purposes.

    :return: True if the `VoltageRelay` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_voltage_relays(self, table: TableVoltageRelays, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        voltage_relay = VoltageRelay(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_protection_relay_function(voltage_relay, table, result_set) and self._add_or_throw(voltage_relay)

    #######################
    # IEC61970 Base SCADA #
    #######################

    """
    Create a `RemoteControl` and populate its fields from `TableRemoteControls`.

    :param table: The database table to read the `RemoteControl` fields from.
    :param result_set: The record in the database table containing the fields for this `RemoteControl`.
    :param set_identifier: A callback to register the mRID of this `RemoteControl` for logging purposes.

    :return: True if the `RemoteControl` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_remote_controls(self, table: TableRemoteControls, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        remote_control = RemoteControl(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        remote_control.control = self._ensure_get(
            result_set.get_string(table.control_mrid.query_index, on_none=None),
            Control
        )
        if remote_control.control:
            remote_control.control.remote_control = remote_control

        return self._load_remote_point(remote_control, table, result_set) and self._add_or_throw(remote_control)

    def _load_remote_point(self, remote_point: RemotePoint, table: TableRemotePoints, result_set: ResultSet) -> bool:
        return self._load_identified_object(remote_point, table, result_set)

    """
    Create a `RemoteSource` and populate its fields from `TableRemoteSources`.

    :param table: The database table to read the `RemoteSource` fields from.
    :param result_set: The record in the database table containing the fields for this `RemoteSource`.
    :param set_identifier: A callback to register the mRID of this `RemoteSource` for logging purposes.

    :return: True if the `RemoteSource` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_remote_sources(self, table: TableRemoteSources, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        remote_source = RemoteSource(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_remote_point(remote_source, table, result_set) and self._add_or_throw(remote_source)

    #############################################
    # IEC61970 Base Wires Generation Production #
    #############################################

    """
    Create a `BatteryUnit` and populate its fields from `TableBatteryUnits`.

    :param table: The database table to read the `BatteryUnit` fields from.
    :param result_set: The record in the database table containing the fields for this `BatteryUnit`.
    :param set_identifier: A callback to register the mRID of this `BatteryUnit` for logging purposes.

    :return: True if the `BatteryUnit` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_battery_units(self, table: TableBatteryUnits, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        battery_unit = BatteryUnit(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        battery_unit.battery_state = BatteryStateKind[result_set.get_string(table.battery_state.query_index)]
        battery_unit.rated_e = result_set.get_int(table.rated_e.query_index, on_none=None)
        battery_unit.stored_e = result_set.get_int(table.stored_e.query_index, on_none=None)

        return self._load_power_electronics_unit(battery_unit, table, result_set) and self._add_or_throw(battery_unit)

    """
    Create a `PhotoVoltaicUnit` and populate its fields from `TablePhotoVoltaicUnits`.

    :param table: The database table to read the `PhotoVoltaicUnit` fields from.
    :param result_set: The record in the database table containing the fields for this `PhotoVoltaicUnit`.
    :param set_identifier: A callback to register the mRID of this `PhotoVoltaicUnit` for logging purposes.

    :return: True if the `PhotoVoltaicUnit` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_photo_voltaic_units(self, table: TablePhotoVoltaicUnits, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        photo_voltaic_unit = PhotoVoltaicUnit(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_power_electronics_unit(photo_voltaic_unit, table, result_set) and self._add_or_throw(photo_voltaic_unit)

    def _load_power_electronics_unit(self, power_electronics_unit: PowerElectronicsUnit, table: TablePowerElectronicsUnits, result_set: ResultSet) -> bool:
        power_electronics_unit.power_electronics_connection = self._ensure_get(
            result_set.get_string(table.power_electronics_connection_mrid.query_index, on_none=None),
            PowerElectronicsConnection
        )
        power_electronics_unit.max_p = result_set.get_int(table.max_p.query_index, on_none=None)
        power_electronics_unit.min_p = result_set.get_int(table.min_p.query_index, on_none=None)

        if power_electronics_unit.power_electronics_connection:
            power_electronics_unit.power_electronics_connection.add_unit(power_electronics_unit)

        return self._load_equipment(power_electronics_unit, table, result_set)

    """
    Create a `PowerElectronicsWindUnit` and populate its fields from `TablePowerElectronicsWindUnits`.

    :param table: The database table to read the `PowerElectronicsWindUnit` fields from.
    :param result_set: The record in the database table containing the fields for this `PowerElectronicsWindUnit`.
    :param set_identifier: A callback to register the mRID of this `PowerElectronicsWindUnit` for logging purposes.

    :return: True if the `PowerElectronicsWindUnit` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_power_electronics_wind_units(self, table: TablePowerElectronicsWindUnits, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        power_electronics_wind_unit = PowerElectronicsWindUnit(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_power_electronics_unit(power_electronics_wind_unit, table, result_set) and self._add_or_throw(power_electronics_wind_unit)

    #######################
    # IEC61970 Base Wires #
    #######################

    """
    Create an `AcLineSegment` and populate its fields from `TableAcLineSegments`.

    :param table: The database table to read the `AcLineSegment` fields from.
    :param result_set: The record in the database table containing the fields for this `AcLineSegment`.
    :param set_identifier: A callback to register the mRID of this `AcLineSegment` for logging purposes.

    :return: True if the `AcLineSegment` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_ac_line_segments(self, table: TableAcLineSegments, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        ac_line_segment = AcLineSegment(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        ac_line_segment.per_length_sequence_impedance = self._ensure_get(
            result_set.get_string(table.per_length_sequence_impedance_mrid.query_index, on_none=None),
            PerLengthSequenceImpedance
        )

        return self._load_conductor(ac_line_segment, table, result_set) and self._add_or_throw(ac_line_segment)

    """
    Create a `Breaker` and populate its fields from `TableBreakers`.

    :param table: The database table to read the `Breaker` fields from.
    :param result_set: The record in the database table containing the fields for this `Breaker`.
    :param set_identifier: A callback to register the mRID of this `Breaker` for logging purposes.

    :return: True if the `Breaker` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_breakers(self, table: TableBreakers, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        breaker = Breaker(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        breaker.in_transit_time = result_set.get_float(table.in_transit_time.query_index, on_none=None)

        return self._load_protected_switch(breaker, table, result_set) and self._add_or_throw(breaker)

    """
    Create a `LoadBreakSwitch` and populate its fields from `TableLoadBreakSwitches`.

    :param table: The database table to read the `LoadBreakSwitch` fields from.
    :param result_set: The record in the database table containing the fields for this `LoadBreakSwitch`.
    :param set_identifier: A callback to register the mRID of this `LoadBreakSwitch` for logging purposes.

    :return: True if the `LoadBreakSwitch` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_load_break_switches(self, table: TableLoadBreakSwitches, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        load_break_switch = LoadBreakSwitch(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_protected_switch(load_break_switch, table, result_set) and self._add_or_throw(load_break_switch)

    """
    Create a `BusbarSection` and populate its fields from `TableBusbarSections`.

    :param table: The database table to read the `BusbarSection` fields from.
    :param result_set: The record in the database table containing the fields for this `BusbarSection`.
    :param set_identifier: A callback to register the mRID of this `BusbarSection` for logging purposes.

    :return: True if the `BusbarSection` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_busbar_sections(self, table: TableBusbarSections, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        busbar_section = BusbarSection(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_connector(busbar_section, table, result_set) and self._add_or_throw(busbar_section)

    def _load_conductor(self, conductor: Conductor, table: TableConductors, result_set: ResultSet) -> bool:
        conductor.length = result_set.get_float(table.length.query_index, on_none=None)
        conductor.asset_info = self._ensure_get(
            result_set.get_string(table.wire_info_mrid.query_index, on_none=None),
            WireInfo
        )

        return self._load_conducting_equipment(conductor, table, result_set)

    def _load_connector(self, connector: Connector, table: TableConnectors, result_set: ResultSet) -> bool:
        return self._load_conducting_equipment(connector, table, result_set)

    """
    Create a `Disconnector` and populate its fields from `TableDisconnectors`.

    :param table: The database table to read the `Disconnector` fields from.
    :param result_set: The record in the database table containing the fields for this `Disconnector`.
    :param set_identifier: A callback to register the mRID of this `Disconnector` for logging purposes.

    :return: True if the `Disconnector` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_disconnectors(self, table: TableDisconnectors, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        disconnector = Disconnector(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_switch(disconnector, table, result_set) and self._add_or_throw(disconnector)

    def _load_energy_connection(self, energy_connection: EnergyConnection, table: TableEnergyConnections, result_set: ResultSet) -> bool:
        return self._load_conducting_equipment(energy_connection, table, result_set)

    """
    Create an `EnergyConsumer` and populate its fields from `TableEnergyConsumers`.

    :param table: The database table to read the `EnergyConsumer` fields from.
    :param result_set: The record in the database table containing the fields for this `EnergyConsumer`.
    :param set_identifier: A callback to register the mRID of this `EnergyConsumer` for logging purposes.

    :return: True if the `EnergyConsumer` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_energy_consumers(self, table: TableEnergyConsumers, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        energy_consumer = EnergyConsumer(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        energy_consumer.customer_count = result_set.get_int(table.customer_count.query_index, on_none=None)
        energy_consumer.grounded = result_set.get_boolean(table.grounded.query_index)
        energy_consumer.p = result_set.get_float(table.p.query_index, on_none=None)
        energy_consumer.q = result_set.get_float(table.q.query_index, on_none=None)
        energy_consumer.p_fixed = result_set.get_float(table.p_fixed.query_index, on_none=None)
        energy_consumer.q_fixed = result_set.get_float(table.q_fixed.query_index, on_none=None)
        energy_consumer.phase_connection = PhaseShuntConnectionKind[result_set.get_string(table.phase_connection.query_index)]

        return self._load_energy_connection(energy_consumer, table, result_set) and self._add_or_throw(energy_consumer)

    """
    Create an `EnergyConsumerPhase` and populate its fields from `TableEnergyConsumerPhases`.

    :param table: The database table to read the `EnergyConsumerPhase` fields from.
    :param result_set: The record in the database table containing the fields for this `EnergyConsumerPhase`.
    :param set_identifier: A callback to register the mRID of this `EnergyConsumerPhase` for logging purposes.

    :return: True if the `EnergyConsumerPhase` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_energy_consumer_phases(self, table: TableEnergyConsumerPhases, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        energy_consumer_phase = EnergyConsumerPhase(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        energy_consumer_phase.energy_consumer = self._ensure_get(
            result_set.get_string(table.energy_consumer_mrid.query_index),
            EnergyConsumer
        )
        energy_consumer_phase.phase = SinglePhaseKind[result_set.get_string(table.phase.query_index)]
        energy_consumer_phase.p = result_set.get_float(table.p.query_index, on_none=None)
        energy_consumer_phase.q = result_set.get_float(table.q.query_index, on_none=None)
        energy_consumer_phase.p_fixed = result_set.get_float(table.p_fixed.query_index, on_none=None)
        energy_consumer_phase.q_fixed = result_set.get_float(table.q_fixed.query_index, on_none=None)

        if energy_consumer_phase.energy_consumer:
            energy_consumer_phase.energy_consumer.add_phase(energy_consumer_phase)

        return self._load_power_system_resource(energy_consumer_phase, table, result_set) and self._add_or_throw(energy_consumer_phase)

    """
    Create an `EnergySource` and populate its fields from `TableEnergySources`.

    :param table: The database table to read the `EnergySource` fields from.
    :param result_set: The record in the database table containing the fields for this `EnergySource`.
    :param set_identifier: A callback to register the mRID of this `EnergySource` for logging purposes.

    :return: True if the `EnergySource` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_energy_sources(self, table: TableEnergySources, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        energy_source = EnergySource(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        energy_source.active_power = result_set.get_float(table.active_power.query_index, on_none=None)
        energy_source.reactive_power = result_set.get_float(table.reactive_power.query_index, on_none=None)
        energy_source.voltage_angle = result_set.get_float(table.voltage_angle.query_index, on_none=None)
        energy_source.voltage_magnitude = result_set.get_float(table.voltage_magnitude.query_index, on_none=None)
        energy_source.p_max = result_set.get_float(table.p_max.query_index, on_none=None)
        energy_source.p_min = result_set.get_float(table.p_min.query_index, on_none=None)
        energy_source.r = result_set.get_float(table.r.query_index, on_none=None)
        energy_source.r0 = result_set.get_float(table.r0.query_index, on_none=None)
        energy_source.rn = result_set.get_float(table.rn.query_index, on_none=None)
        energy_source.x = result_set.get_float(table.x.query_index, on_none=None)
        energy_source.x0 = result_set.get_float(table.x0.query_index, on_none=None)
        energy_source.xn = result_set.get_float(table.xn.query_index, on_none=None)
        energy_source.is_external_grid = result_set.get_boolean(table.is_external_grid.query_index)
        energy_source.r_min = result_set.get_float(table.r_min.query_index, on_none=None)
        energy_source.rn_min = result_set.get_float(table.rn_min.query_index, on_none=None)
        energy_source.r0_min = result_set.get_float(table.r0_min.query_index, on_none=None)
        energy_source.x_min = result_set.get_float(table.x_min.query_index, on_none=None)
        energy_source.xn_min = result_set.get_float(table.xn_min.query_index, on_none=None)
        energy_source.x0_min = result_set.get_float(table.x0_min.query_index, on_none=None)
        energy_source.r_max = result_set.get_float(table.r_max.query_index, on_none=None)
        energy_source.rn_max = result_set.get_float(table.rn_max.query_index, on_none=None)
        energy_source.r0_max = result_set.get_float(table.r0_max.query_index, on_none=None)
        energy_source.x_max = result_set.get_float(table.x_max.query_index, on_none=None)
        energy_source.xn_max = result_set.get_float(table.xn_max.query_index, on_none=None)
        energy_source.x0_max = result_set.get_float(table.x0_max.query_index, on_none=None)

        return self._load_energy_connection(energy_source, table, result_set) and self._add_or_throw(energy_source)

    """
    Create an `EnergySourcePhase` and populate its fields from `TableEnergySourcePhases`.

    :param table: The database table to read the `EnergySourcePhase` fields from.
    :param result_set: The record in the database table containing the fields for this `EnergySourcePhase`.
    :param set_identifier: A callback to register the mRID of this `EnergySourcePhase` for logging purposes.

    :return: True if the `EnergySourcePhase` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_energy_source_phases(self, table: TableEnergySourcePhases, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        energy_source_phase = EnergySourcePhase(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        energy_source_phase.energy_source = self._ensure_get(
            result_set.get_string(table.energy_source_mrid.query_index),
            EnergySource
        )
        energy_source_phase.phase = SinglePhaseKind[result_set.get_string(table.phase.query_index)]

        if energy_source_phase.energy_source:
            energy_source_phase.energy_source.add_phase(energy_source_phase)

        return self._load_power_system_resource(energy_source_phase, table, result_set) and self._add_or_throw(energy_source_phase)

    """
    Create a `Fuse` and populate its fields from `TableFuses`.

    :param table: The database table to read the `Fuse` fields from.
    :param result_set: The record in the database table containing the fields for this `Fuse`.
    :param set_identifier: A callback to register the mRID of this `Fuse` for logging purposes.

    :return: True if the `Fuse` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_fuses(self, table: TableFuses, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        fuse = Fuse(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        fuse.function = self._ensure_get(
            result_set.get_string(table.function_mrid.query_index, on_none=None),
            ProtectionRelayFunction
        )

        return self._load_switch(fuse, table, result_set) and self._add_or_throw(fuse)

    """
    Create a `Ground` and populate its fields from `TableGrounds`.

    :param table: The database table to read the `Ground` fields from.
    :param result_set: The record in the database table containing the fields for this `Ground`.
    :param set_identifier: A callback to register the mRID of this `Ground` for logging purposes.

    :return: True if the `Ground` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_grounds(self, table: TableGrounds, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        ground = Ground(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_conducting_equipment(ground, table, result_set) and self._add_or_throw(ground)

    """
    Create a `GroundDisconnector` and populate its fields from `TableGroundDisconnectors`.

    :param table: The database table to read the `GroundDisconnector` fields from.
    :param result_set: The record in the database table containing the fields for this `GroundDisconnector`.
    :param set_identifier: A callback to register the mRID of this `GroundDisconnector` for logging purposes.

    :return: True if the `GroundDisconnector` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_ground_disconnectors(self, table: TableGroundDisconnectors, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        ground_disconnector = GroundDisconnector(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_switch(ground_disconnector, table, result_set) and self._add_or_throw(ground_disconnector)

    """
    Create a `Jumper` and populate its fields from `TableJumpers`.

    :param table: The database table to read the `Jumper` fields from.
    :param result_set: The record in the database table containing the fields for this `Jumper`.
    :param set_identifier: A callback to register the mRID of this `Jumper` for logging purposes.

    :return: True if the `Jumper` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_jumpers(self, table: TableJumpers, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        jumper = Jumper(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_switch(jumper, table, result_set) and self._add_or_throw(jumper)

    """
    Create a `Junction` and populate its fields from `TableJunctions`.

    :param table: The database table to read the `Junction` fields from.
    :param result_set: The record in the database table containing the fields for this `Junction`.
    :param set_identifier: A callback to register the mRID of this `Junction` for logging purposes.

    :return: True if the `Junction` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_junctions(self, table: TableJunctions, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        junction = Junction(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_connector(junction, table, result_set) and self._add_or_throw(junction)

    def _load_line(self, line: Line, table: TableLines, result_set: ResultSet) -> bool:
        return self._load_equipment_container(line, table, result_set)

    """
    Create a `LinearShuntCompensator` and populate its fields from `TableLinearShuntCompensators`.

    :param table: The database table to read the `LinearShuntCompensator` fields from.
    :param result_set: The record in the database table containing the fields for this `LinearShuntCompensator`.
    :param set_identifier: A callback to register the mRID of this `LinearShuntCompensator` for logging purposes.

    :return: True if the `LinearShuntCompensator` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_linear_shunt_compensators(self, table: TableLinearShuntCompensators, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        linear_shunt_compensator = LinearShuntCompensator(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        linear_shunt_compensator.b0_per_section = result_set.get_float(table.b0_per_section.query_index, on_none=None)
        linear_shunt_compensator.b_per_section = result_set.get_float(table.b_per_section.query_index, on_none=None)
        linear_shunt_compensator.g0_per_section = result_set.get_float(table.g0_per_section.query_index, on_none=None)
        linear_shunt_compensator.g_per_section = result_set.get_float(table.g_per_section.query_index, on_none=None)

        return self._load_shunt_compensator(linear_shunt_compensator, table, result_set) and self._add_or_throw(linear_shunt_compensator)

    def _load_per_length_impedance(self, per_length_impedance: PerLengthImpedance, table: TablePerLengthImpedances, result_set: ResultSet) -> bool:
        return self._load_per_length_line_parameter(per_length_impedance, table, result_set)

    def _load_per_length_line_parameter(
        self,
        per_length_line_parameter: PerLengthLineParameter,
        table: TablePerLengthLineParameters,
        result_set: ResultSet
    ) -> bool:
        return self._load_identified_object(per_length_line_parameter, table, result_set)

    """
    Create a `PerLengthSequenceImpedance` and populate its fields from `TablePerLengthSequenceImpedances`.

    :param table: The database table to read the `PerLengthSequenceImpedance` fields from.
    :param result_set: The record in the database table containing the fields for this `PerLengthSequenceImpedance`.
    :param set_identifier: A callback to register the mRID of this `PerLengthSequenceImpedance` for logging purposes.

    :return: True if the `PerLengthSequenceImpedance` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_per_length_sequence_impedances(self, table: TablePerLengthSequenceImpedances, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        per_length_sequence_impedance = PerLengthSequenceImpedance(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        per_length_sequence_impedance.r = result_set.get_float(table.r.query_index, on_none=None)
        per_length_sequence_impedance.x = result_set.get_float(table.x.query_index, on_none=None)
        per_length_sequence_impedance.r0 = result_set.get_float(table.r0.query_index, on_none=None)
        per_length_sequence_impedance.x0 = result_set.get_float(table.x0.query_index, on_none=None)
        per_length_sequence_impedance.bch = result_set.get_float(table.bch.query_index, on_none=None)
        per_length_sequence_impedance.gch = result_set.get_float(table.gch.query_index, on_none=None)
        per_length_sequence_impedance.b0ch = result_set.get_float(table.b0ch.query_index, on_none=None)
        per_length_sequence_impedance.g0ch = result_set.get_float(table.g0ch.query_index, on_none=None)

        return self._load_per_length_impedance(per_length_sequence_impedance, table, result_set) and self._add_or_throw(per_length_sequence_impedance)

    """
    Create a `PowerElectronicsConnection` and populate its fields from `TablePowerElectronicsConnections`.

    :param table: The database table to read the `PowerElectronicsConnection` fields from.
    :param result_set: The record in the database table containing the fields for this `PowerElectronicsConnection`.
    :param set_identifier: A callback to register the mRID of this `PowerElectronicsConnection` for logging purposes.

    :return: True if the `PowerElectronicsConnection` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_power_electronics_connections(self, table: TablePowerElectronicsConnections, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        power_electronics_connection = PowerElectronicsConnection(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        power_electronics_connection.max_i_fault = result_set.get_int(table.max_i_fault.query_index, on_none=None)
        power_electronics_connection.max_q = result_set.get_float(table.max_q.query_index, on_none=None)
        power_electronics_connection.min_q = result_set.get_float(table.min_q.query_index, on_none=None)
        power_electronics_connection.p = result_set.get_float(table.p.query_index, on_none=None)
        power_electronics_connection.q = result_set.get_float(table.q.query_index, on_none=None)
        power_electronics_connection.rated_u = result_set.get_int(table.rated_u.query_index, on_none=None)
        power_electronics_connection.rated_s = result_set.get_int(table.rated_s.query_index, on_none=None)
        power_electronics_connection.inverter_standard = result_set.get_string(table.inverter_standard.query_index, on_none=None)
        power_electronics_connection.sustain_op_overvolt_limit = result_set.get_int(table.sustain_op_overvolt_limit.query_index, on_none=None)
        power_electronics_connection.stop_at_over_freq = result_set.get_float(table.stop_at_over_freq.query_index, on_none=None)
        power_electronics_connection.stop_at_under_freq = result_set.get_float(table.stop_at_under_freq.query_index, on_none=None)
        power_electronics_connection.inv_volt_watt_resp_mode = result_set.get_boolean(table.inv_volt_watt_resp_mode.query_index, on_none=None)
        power_electronics_connection.inv_watt_resp_v1 = result_set.get_int(table.inv_watt_resp_v1.query_index, on_none=None)
        power_electronics_connection.inv_watt_resp_v2 = result_set.get_int(table.inv_watt_resp_v2.query_index, on_none=None)
        power_electronics_connection.inv_watt_resp_v3 = result_set.get_int(table.inv_watt_resp_v3.query_index, on_none=None)
        power_electronics_connection.inv_watt_resp_v4 = result_set.get_int(table.inv_watt_resp_v4.query_index, on_none=None)
        power_electronics_connection.inv_watt_resp_p_at_v1 = result_set.get_float(table.inv_watt_resp_p_at_v1.query_index, on_none=None)
        power_electronics_connection.inv_watt_resp_p_at_v2 = result_set.get_float(table.inv_watt_resp_p_at_v2.query_index, on_none=None)
        power_electronics_connection.inv_watt_resp_p_at_v3 = result_set.get_float(table.inv_watt_resp_p_at_v3.query_index, on_none=None)
        power_electronics_connection.inv_watt_resp_p_at_v4 = result_set.get_float(table.inv_watt_resp_p_at_v4.query_index, on_none=None)
        power_electronics_connection.inv_volt_var_resp_mode = result_set.get_boolean(table.inv_volt_var_resp_mode.query_index, on_none=None)
        power_electronics_connection.inv_var_resp_v1 = result_set.get_int(table.inv_var_resp_v1.query_index, on_none=None)
        power_electronics_connection.inv_var_resp_v2 = result_set.get_int(table.inv_var_resp_v2.query_index, on_none=None)
        power_electronics_connection.inv_var_resp_v3 = result_set.get_int(table.inv_var_resp_v3.query_index, on_none=None)
        power_electronics_connection.inv_var_resp_v4 = result_set.get_int(table.inv_var_resp_v4.query_index, on_none=None)
        power_electronics_connection.inv_var_resp_q_at_v1 = result_set.get_float(table.inv_var_resp_q_at_v1.query_index, on_none=None)
        power_electronics_connection.inv_var_resp_q_at_v2 = result_set.get_float(table.inv_var_resp_q_at_v2.query_index, on_none=None)
        power_electronics_connection.inv_var_resp_q_at_v3 = result_set.get_float(table.inv_var_resp_q_at_v3.query_index, on_none=None)
        power_electronics_connection.inv_var_resp_q_at_v4 = result_set.get_float(table.inv_var_resp_q_at_v4.query_index, on_none=None)
        power_electronics_connection.inv_reactive_power_mode = result_set.get_boolean(table.inv_reactive_power_mode.query_index, on_none=None)
        power_electronics_connection.inv_fix_reactive_power = result_set.get_float(table.inv_fix_reactive_power.query_index, on_none=None)

        return self._load_regulating_cond_eq(power_electronics_connection, table, result_set) and self._add_or_throw(power_electronics_connection)

    """
    Create a `PowerElectronicsConnectionPhase` and populate its fields from `TablePowerElectronicsConnectionPhases`.

    :param table: The database table to read the `PowerElectronicsConnectionPhase` fields from.
    :param result_set: The record in the database table containing the fields for this `PowerElectronicsConnectionPhase`.
    :param set_identifier: A callback to register the mRID of this `PowerElectronicsConnectionPhase` for logging purposes.

    :return: True if the `PowerElectronicsConnectionPhase` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_power_electronics_connection_phases(
        self,
        table: TablePowerElectronicsConnectionPhases,
        result_set: ResultSet,
        set_identifier: Callable[[str], str]
    ) -> bool:
        power_electronics_connection_phase = PowerElectronicsConnectionPhase(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        power_electronics_connection_phase.power_electronics_connection = self._ensure_get(
            result_set.get_string(table.power_electronics_connection_mrid.query_index, on_none=None),
            PowerElectronicsConnection
        )
        power_electronics_connection_phase.phase = SinglePhaseKind[result_set.get_string(table.phase.query_index)]
        power_electronics_connection_phase.p = result_set.get_float(table.p.query_index, on_none=None)
        power_electronics_connection_phase.phase = SinglePhaseKind[result_set.get_string(table.phase.query_index)]
        power_electronics_connection_phase.q = result_set.get_float(table.q.query_index, on_none=None)

        if power_electronics_connection_phase.power_electronics_connection:
            power_electronics_connection_phase.power_electronics_connection.add_phase(power_electronics_connection_phase)

        return self._load_power_system_resource(power_electronics_connection_phase, table, result_set) and self._add_or_throw(
            power_electronics_connection_phase)

    """
    Create a `PowerTransformer` and populate its fields from `TablePowerTransformers`.

    :param table: The database table to read the `PowerTransformer` fields from.
    :param result_set: The record in the database table containing the fields for this `PowerTransformer`.
    :param set_identifier: A callback to register the mRID of this `PowerTransformer` for logging purposes.

    :return: True if the `PowerTransformer` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_power_transformers(self, table: TablePowerTransformers, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        power_transformer = PowerTransformer(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        power_transformer.vector_group = VectorGroup[result_set.get_string(table.vector_group.query_index)]
        power_transformer.transformer_utilisation = result_set.get_float(table.transformer_utilisation.query_index, on_none=None)
        power_transformer.construction_kind = TransformerConstructionKind[result_set.get_string(table.construction_kind.query_index)]
        power_transformer.function = TransformerFunctionKind[result_set.get_string(table.function.query_index)]
        power_transformer.asset_info = self._ensure_get(
            result_set.get_string(table.power_transformer_info_mrid.query_index, on_none=None),
            PowerTransformerInfo
        )

        return self._load_conducting_equipment(power_transformer, table, result_set) and self._add_or_throw(power_transformer)

    """
    Create a `PowerTransformerEnd` and populate its fields from `TablePowerTransformerEnds`.

    :param table: The database table to read the `PowerTransformerEnd` fields from.
    :param result_set: The record in the database table containing the fields for this `PowerTransformerEnd`.
    :param set_identifier: A callback to register the mRID of this `PowerTransformerEnd` for logging purposes.

    :return: True if the `PowerTransformerEnd` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_power_transformer_ends(self, table: TablePowerTransformerEnds, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        power_transformer_end = PowerTransformerEnd(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        power_transformer_end.end_number = result_set.get_int(table.end_number.query_index)
        power_transformer_end.power_transformer = self._ensure_get(
            result_set.get_string(table.power_transformer_mrid.query_index, on_none=None),
            PowerTransformer
        )
        power_transformer_end.connection_kind = WindingConnection[result_set.get_string(table.connection_kind.query_index)]
        power_transformer_end.phase_angle_clock = result_set.get_int(table.phase_angle_clock.query_index, on_none=None)
        power_transformer_end.b = result_set.get_float(table.b.query_index, on_none=None)
        power_transformer_end.b0 = result_set.get_float(table.b0.query_index, on_none=None)
        power_transformer_end.g = result_set.get_float(table.g.query_index, on_none=None)
        power_transformer_end.g0 = result_set.get_float(table.g0.query_index, on_none=None)
        power_transformer_end.r = result_set.get_float(table.r.query_index, on_none=None)
        power_transformer_end.r0 = result_set.get_float(table.r0.query_index, on_none=None)
        power_transformer_end.rated_u = result_set.get_int(table.rated_u.query_index, on_none=None)
        power_transformer_end.x = result_set.get_float(table.x.query_index, on_none=None)
        power_transformer_end.x0 = result_set.get_float(table.x0.query_index, on_none=None)

        if power_transformer_end.power_transformer:
            power_transformer_end.power_transformer.add_end(power_transformer_end)

        return self._load_transformer_end(power_transformer_end, table, result_set) and self._add_or_throw(power_transformer_end)

    """
    Adds a rating to a `PowerTransformerEnd` from `TablePowerTransformerEndRatings`.

    :param table: The database table to read the rating fields from.
    :param result_set: The record in the database table containing the fields for this rating.
    :param set_identifier: A callback to register the mRID of this rating for logging purposes.

    :return: True if the rating was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_power_transformer_end_ratings(self, table: TablePowerTransformerEndRatings, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        # Note TablePowerTransformerEndRatings.selectSql ensures we process ratings in the correct order.
        power_transformer_end_mrid = result_set.get_string(table.power_transformer_end_mrid.query_index)
        rated_s = result_set.get_int(table.rated_s.query_index)
        set_identifier(f"{power_transformer_end_mrid}.s{rated_s}")

        pte = self._ensure_get(power_transformer_end_mrid, PowerTransformerEnd)
        if pte:
            cooling_type = TransformerCoolingType[result_set.get_string(table.cooling_type.query_index)]
            pte.add_rating(rated_s, cooling_type)

        return True

    def _load_protected_switch(self, protected_switch: ProtectedSwitch, table: TableProtectedSwitches, result_set: ResultSet) -> bool:
        protected_switch.breaking_capacity = result_set.get_int(table.breaking_capacity.query_index, on_none=None)

        return self._load_switch(protected_switch, table, result_set)

    """
    Create a `RatioTapChanger` and populate its fields from `TableRatioTapChangers`.

    :param table: The database table to read the `RatioTapChanger` fields from.
    :param result_set: The record in the database table containing the fields for this `RatioTapChanger`.
    :param set_identifier: A callback to register the mRID of this `RatioTapChanger` for logging purposes.

    :return: True if the `RatioTapChanger` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_ratio_tap_changers(self, table: TableRatioTapChangers, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        ratio_tap_changer = RatioTapChanger(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        ratio_tap_changer.transformer_end = self._ensure_get(
            result_set.get_string(table.transformer_end_mrid.query_index, on_none=None),
            TransformerEnd
        )
        ratio_tap_changer.step_voltage_increment = result_set.get_float(table.step_voltage_increment.query_index, on_none=None)

        if ratio_tap_changer.transformer_end:
            ratio_tap_changer.transformer_end.ratio_tap_changer = ratio_tap_changer

        return self._load_tap_changer(ratio_tap_changer, table, result_set) and self._add_or_throw(ratio_tap_changer)

    """
    Create a `Recloser` and populate its fields from `TableReclosers`.

    :param table: The database table to read the `Recloser` fields from.
    :param result_set: The record in the database table containing the fields for this `Recloser`.
    :param set_identifier: A callback to register the mRID of this `Recloser` for logging purposes.

    :return: True if the `Recloser` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_reclosers(self, table: TableReclosers, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        recloser = Recloser(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_protected_switch(recloser, table, result_set) and self._add_or_throw(recloser)

    def _load_regulating_cond_eq(self, regulating_cond_eq: RegulatingCondEq, table: TableRegulatingCondEq, result_set: ResultSet) -> bool:
        regulating_cond_eq.control_enabled = result_set.get_boolean(table.control_enabled.query_index)
        # We use a resolver here because there is an ordering conflict between terminals, RegulatingCondEq, and RegulatingControls
        # We check this resolver has actually been resolved in the postLoad of the database read and throw there if it hasn't.
        self._service.resolve_or_defer_reference(
            resolver.rce_regulating_control(regulating_cond_eq),
            result_set.get_string(table.regulating_control_mrid.query_index, on_none=None)
        )

        return self._load_energy_connection(regulating_cond_eq, table, result_set)

    def _load_regulating_control(self, regulating_control: RegulatingControl, table: TableRegulatingControls, result_set: ResultSet) -> bool:
        regulating_control.discrete = result_set.get_boolean(table.discrete.query_index, on_none=None)
        regulating_control.mode = RegulatingControlModeKind[result_set.get_string(table.mode.query_index)]
        regulating_control.monitored_phase = PhaseCode[result_set.get_string(table.monitored_phase.query_index)]
        regulating_control.target_deadband = result_set.get_float(table.target_deadband.query_index, on_none=None)
        regulating_control.target_value = result_set.get_float(table.target_value.query_index, on_none=None)
        regulating_control.enabled = result_set.get_boolean(table.enabled.query_index, on_none=None)
        regulating_control.max_allowed_target_value = result_set.get_float(table.max_allowed_target_value.query_index, on_none=None)
        regulating_control.min_allowed_target_value = result_set.get_float(table.min_allowed_target_value.query_index, on_none=None)
        regulating_control.rated_current = result_set.get_float(table.rated_current.query_index, on_none=None)
        regulating_control.terminal = self._ensure_get(
            result_set.get_string(table.terminal_mrid.query_index, on_none=None),
            Terminal
        )

        return self._load_power_system_resource(regulating_control, table, result_set)

    """
    Create a `SeriesCompensator` and populate its fields from `TableSeriesCompensators`.

    :param table: The database table to read the `SeriesCompensator` fields from.
    :param result_set: The record in the database table containing the fields for this `SeriesCompensator`.
    :param set_identifier: A callback to register the mRID of this `SeriesCompensator` for logging purposes.

    :return: True if the `SeriesCompensator` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_series_compensators(self, table: TableSeriesCompensators, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        series_compensator = SeriesCompensator(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        series_compensator.r = result_set.get_float(table.r.query_index, on_none=None)
        series_compensator.r0 = result_set.get_float(table.r0.query_index, on_none=None)
        series_compensator.x = result_set.get_float(table.x.query_index, on_none=None)
        series_compensator.x0 = result_set.get_float(table.x0.query_index, on_none=None)
        series_compensator.varistor_rated_current = result_set.get_int(table.varistor_rated_current.query_index, on_none=None)
        series_compensator.varistor_voltage_threshold = result_set.get_int(table.varistor_voltage_threshold.query_index, on_none=None)

        return self._load_conducting_equipment(series_compensator, table, result_set) and self._add_or_throw(series_compensator)

    def _load_shunt_compensator(self, shunt_compensator: ShuntCompensator, table: TableShuntCompensators, result_set: ResultSet) -> bool:
        shunt_compensator.asset_info = self._ensure_get(
            result_set.get_string(table.shunt_compensator_info_mrid.query_index, on_none=None),
            ShuntCompensatorInfo
        )

        shunt_compensator.grounded = result_set.get_boolean(table.grounded.query_index)
        shunt_compensator.nom_u = result_set.get_int(table.nom_u.query_index, on_none=None)
        shunt_compensator.phase_connection = PhaseShuntConnectionKind[result_set.get_string(table.phase_connection.query_index)]
        shunt_compensator.sections = result_set.get_float(table.sections.query_index, on_none=None)

        return self._load_regulating_cond_eq(shunt_compensator, table, result_set)

    def _load_switch(self, switch: Switch, table: TableSwitches, result_set: ResultSet) -> bool:
        switch.asset_info = self._ensure_get(
            result_set.get_string(table.switch_info_mrid.query_index, on_none=None),
            SwitchInfo
        )
        switch.rated_current = result_set.get_int(table.rated_current.query_index, on_none=None)
        switch._normally_open = result_set.get_int(table.normal_open.query_index)
        switch._open = result_set.get_int(table.open.query_index)

        return self._load_conducting_equipment(switch, table, result_set)

    def _load_tap_changer(self, tap_changer: TapChanger, table: TableTapChangers, result_set: ResultSet) -> bool:
        tap_changer.control_enabled = result_set.get_boolean(table.control_enabled.query_index)
        tap_changer.high_step = result_set.get_int(table.high_step.query_index, on_none=None)
        tap_changer.low_step = result_set.get_int(table.low_step.query_index, on_none=None)
        tap_changer.neutral_step = result_set.get_int(table.neutral_step.query_index, on_none=None)
        tap_changer.neutral_u = result_set.get_int(table.neutral_u.query_index, on_none=None)
        tap_changer.normal_step = result_set.get_int(table.normal_step.query_index, on_none=None)
        tap_changer.step = result_set.get_float(table.step.query_index, on_none=None)
        tap_changer.tap_changer_control = self._ensure_get(
            result_set.get_string(table.tap_changer_control_mrid.query_index, on_none=None),
            TapChangerControl
        )

        return self._load_power_system_resource(tap_changer, table, result_set)

    """
    Create a `TapChangerControl` and populate its fields from `TableTapChangerControls`.

    :param table: The database table to read the `TapChangerControl` fields from.
    :param result_set: The record in the database table containing the fields for this `TapChangerControl`.
    :param set_identifier: A callback to register the mRID of this `TapChangerControl` for logging purposes.

    :return: True if the `TapChangerControl` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_tap_changer_controls(self, table: TableTapChangerControls, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        tap_changer_control = TapChangerControl(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        tap_changer_control.limit_voltage = result_set.get_int(table.limit_voltage.query_index, on_none=None)
        tap_changer_control.line_drop_compensation = result_set.get_boolean(table.line_drop_compensation.query_index, on_none=None)
        tap_changer_control.line_drop_r = result_set.get_float(table.line_drop_r.query_index, on_none=None)
        tap_changer_control.line_drop_x = result_set.get_float(table.line_drop_x.query_index, on_none=None)
        tap_changer_control.reverse_line_drop_r = result_set.get_float(table.reverse_line_drop_r.query_index, on_none=None)
        tap_changer_control.reverse_line_drop_x = result_set.get_float(table.reverse_line_drop_x.query_index, on_none=None)
        tap_changer_control.forward_ldc_blocking = result_set.get_boolean(table.forward_ldc_blocking.query_index, on_none=None)
        tap_changer_control.time_delay = result_set.get_float(table.time_delay.query_index, on_none=None)
        tap_changer_control.co_generation_enabled = result_set.get_boolean(table.co_generation_enabled.query_index, on_none=None)

        return self._load_regulating_control(tap_changer_control, table, result_set) and self._add_or_throw(tap_changer_control)

    def _load_transformer_end(self, transformer_end: TransformerEnd, table: TableTransformerEnds, result_set: ResultSet) -> bool:
        transformer_end.terminal = self._ensure_get(
            result_set.get_string(table.terminal_mrid.query_index, on_none=None),
            Terminal
        )
        transformer_end.base_voltage = self._ensure_get(
            result_set.get_string(table.base_voltage_mrid.query_index, on_none=None),
            BaseVoltage
        )
        transformer_end.grounded = result_set.get_boolean(table.grounded.query_index)
        transformer_end.r_ground = result_set.get_float(table.r_ground.query_index, on_none=None)
        transformer_end.x_ground = result_set.get_float(table.x_ground.query_index, on_none=None)
        transformer_end.star_impedance = self._ensure_get(
            result_set.get_string(table.star_impedance_mrid.query_index, on_none=None),
            TransformerStarImpedance
        )

        return self._load_identified_object(transformer_end, table, result_set)

    """
    Create a `TransformerStarImpedance` and populate its fields from `TableTransformerStarImpedances`.

    :param table: The database table to read the `TransformerStarImpedance` fields from.
    :param result_set: The record in the database table containing the fields for this `TransformerStarImpedance`.
    :param set_identifier: A callback to register the mRID of this `TransformerStarImpedance` for logging purposes.

    :return: True if the `TransformerStarImpedance` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_transformer_star_impedances(self, table: TableTransformerStarImpedances, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        transformer_star_impedance = TransformerStarImpedance(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        transformer_star_impedance.r = result_set.get_float(table.r.query_index, on_none=None)
        transformer_star_impedance.r0 = result_set.get_float(table.r0.query_index, on_none=None)
        transformer_star_impedance.x = result_set.get_float(table.x.query_index, on_none=None)
        transformer_star_impedance.x0 = result_set.get_float(table.x0.query_index, on_none=None)

        transformer_star_impedance.transformer_end_info = self._ensure_get(
            result_set.get_string(table.transformer_end_info_mrid.query_index, on_none=None),
            TransformerEndInfo
        )
        if transformer_star_impedance.transformer_end_info:
            transformer_star_impedance.transformer_end_info.transformer_star_impedance = transformer_star_impedance

        return self._load_identified_object(transformer_star_impedance, table, result_set) and self._add_or_throw(transformer_star_impedance)

    ###############################
    # IEC61970 InfIEC61970 Feeder #
    ###############################

    """
    Create a `Circuit` and populate its fields from `TableCircuits`.

    :param table: The database table to read the `Circuit` fields from.
    :param result_set: The record in the database table containing the fields for this `Circuit`.
    :param set_identifier: A callback to register the mRID of this `Circuit` for logging purposes.

    :return: True if the `Circuit` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_circuits(self, table: TableCircuits, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        circuit = Circuit(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        circuit.loop = self._ensure_get(
            result_set.get_string(table.loop_mrid.query_index, on_none=None),
            Loop
        )
        if circuit.loop:
            circuit.loop.add_circuit(circuit)

        return self._load_line(circuit, table, result_set) and self._add_or_throw(circuit)

    """
    Create a `Loop` and populate its fields from `TableLoops`.

    :param table: The database table to read the `Loop` fields from.
    :param result_set: The record in the database table containing the fields for this `Loop`.
    :param set_identifier: A callback to register the mRID of this `Loop` for logging purposes.

    :return: True if the `Loop` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_loops(self, table: TableLoops, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        loop = Loop(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_identified_object(loop, table, result_set) and self._add_or_throw(loop)

    """
    Create a `LvFeeder` and populate its fields from `TableLvFeeders`.

    :param table: The database table to read the `LvFeeder` fields from.
    :param result_set: The record in the database table containing the fields for this `LvFeeder`.
    :param set_identifier: A callback to register the mRID of this `LvFeeder` for logging purposes.

    :return: True if the `LvFeeder` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_lv_feeders(self, table: TableLvFeeders, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        lv_feeder = LvFeeder(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        lv_feeder.normal_head_terminal = self._ensure_get(
            result_set.get_string(table.normal_head_terminal_mrid.query_index, on_none=None),
            Terminal
        )

        return self._load_equipment_container(lv_feeder, table, result_set) and self._add_or_throw(lv_feeder)

    ####################################################
    # IEC61970 InfIEC61970 Wires Generation Production #
    ####################################################

    """
    Create an `EvChargingUnit` and populate its fields from `TableEvChargingUnits`.

    :param table: The database table to read the `EvChargingUnit` fields from.
    :param result_set: The record in the database table containing the fields for this `EvChargingUnit`.
    :param set_identifier: A callback to register the mRID of this `EvChargingUnit` for logging purposes.

    :return: True if the `EvChargingUnit` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_ev_charging_units(self, table: TableEvChargingUnits, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        ev_charging_unit = EvChargingUnit(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_power_electronics_unit(ev_charging_unit, table, result_set) and self._add_or_throw(ev_charging_unit)

    ################
    # Associations #
    ################

    """
    Create a `set_identifier` and populate its fields from `TableAssetOrganisationRolesAssets`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_asset_organisation_roles_assets(self, table: TableAssetOrganisationRolesAssets, result_set: ResultSet,
                                             set_identifier: Callable[[str], str]) -> bool:
        asset_organisation_role_mrid = set_identifier(result_set.get_string(table.asset_organisation_role_mrid.query_index))
        set_identifier(f"{asset_organisation_role_mrid}-to-UNKNOWN")

        asset_mrid = result_set.get_string(table.asset_mrid.query_index)
        set_identifier(f"{asset_organisation_role_mrid}-to-{asset_mrid}")

        asset_organisation_role = self._service.get(asset_organisation_role_mrid, AssetOrganisationRole)
        asset = self._service.get(asset_mrid, Asset)

        asset.add_organisation_role(asset_organisation_role)

        return True

    """
    Create a `set_identifier` and populate its fields from `TableEquipmentEquipmentContainers`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_equipment_equipment_containers(self, table: TableEquipmentEquipmentContainers, result_set: ResultSet,
                                            set_identifier: Callable[[str], str]) -> bool:
        equipment_mrid = set_identifier(result_set.get_string(table.equipment_mrid.query_index))
        set_identifier(f"{equipment_mrid}-to-UNKNOWN")

        equipment_container_mrid = result_set.get_string(table.equipment_container_mrid.query_index)
        set_identifier(f"{equipment_mrid}-to-{equipment_container_mrid}")

        equipment = self._service.get(equipment_mrid, Equipment)
        equipment_container = self._service.get(equipment_container_mrid, EquipmentContainer)

        equipment_container.add_equipment(equipment)
        equipment.add_container(equipment_container)

        return True

    """
    Create a `set_identifier` and populate its fields from `TableEquipmentOperationalRestrictions`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_equipment_operational_restrictions(self, table: TableEquipmentOperationalRestrictions, result_set: ResultSet,
                                                set_identifier: Callable[[str], str]) -> bool:
        equipment_mrid = set_identifier(result_set.get_string(table.equipment_mrid.query_index))
        set_identifier(f"{equipment_mrid}-to-UNKNOWN")

        operational_restriction_mrid = result_set.get_string(table.operational_restriction_mrid.query_index)
        set_identifier(f"{equipment_mrid}-to-{operational_restriction_mrid}")

        equipment = self._service.get(equipment_mrid, Equipment)
        operational_restriction = self._service.get(operational_restriction_mrid, OperationalRestriction)

        operational_restriction.add_equipment(equipment)
        equipment.add_operational_restriction(operational_restriction)

        return True

    """
    Create a `set_identifier` and populate its fields from `TableEquipmentUsagePoints`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_equipment_usage_points(self, table: TableEquipmentUsagePoints, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        equipment_mrid = set_identifier(result_set.get_string(table.equipment_mrid.query_index))
        set_identifier(f"{equipment_mrid}-to-UNKNOWN")

        usage_point_mrid = result_set.get_string(table.usage_point_mrid.query_index)
        set_identifier(f"{equipment_mrid}-to-{usage_point_mrid}")

        equipment = self._service.get(equipment_mrid, Equipment)
        usage_point = self._service.get(usage_point_mrid, UsagePoint)

        usage_point.add_equipment(equipment)
        equipment.add_usage_point(usage_point)

        return True

    """
    Create a `set_identifier` and populate its fields from `TableUsagePointsEndDevices`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_usage_points_end_devices(self, table: TableUsagePointsEndDevices, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        usage_point_mrid = set_identifier(result_set.get_string(table.usage_point_mrid.query_index))
        set_identifier(f"{usage_point_mrid}-to-UNKNOWN")

        end_device_mrid = result_set.get_string(table.end_device_mrid.query_index)
        set_identifier(f"{usage_point_mrid}-to-{end_device_mrid}")

        usage_point = self._service.get(usage_point_mrid, UsagePoint)
        end_device = self._service.get(end_device_mrid, EndDevice)

        end_device.add_usage_point(usage_point)
        usage_point.add_end_device(end_device)

        return True

    """
    Create a `set_identifier` and populate its fields from `TableCircuitsSubstations`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_circuits_substations(self, table: TableCircuitsSubstations, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        circuit_mrid = set_identifier(result_set.get_string(table.circuit_mrid.query_index))
        set_identifier(f"{circuit_mrid}-to-UNKNOWN")

        substation_mrid = result_set.get_string(table.substation_mrid.query_index)
        set_identifier(f"{circuit_mrid}-to-{substation_mrid}")

        circuit = self._service.get(circuit_mrid, Circuit)
        substation = self._service.get(substation_mrid, Substation)

        substation.add_circuit(circuit)
        circuit.add_end_substation(substation)

        return True

    """
    Create a `set_identifier` and populate its fields from `TableCircuitsTerminals`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_circuits_terminals(self, table: TableCircuitsTerminals, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        circuit_mrid = set_identifier(result_set.get_string(table.circuit_mrid.query_index))
        set_identifier(f"{circuit_mrid}-to-UNKNOWN")

        terminal_mrid = result_set.get_string(table.terminal_mrid.query_index)
        set_identifier(f"{circuit_mrid}-to-{terminal_mrid}")

        circuit = self._service.get(circuit_mrid, Circuit)
        terminal = self._service.get(terminal_mrid, Terminal)

        circuit.add_end_terminal(terminal)

        return True

    """
    Create a `set_identifier` and populate its fields from `TableLoopsSubstations`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_loops_substations(self, table: TableLoopsSubstations, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        asset_organisation_role_mrid = set_identifier(result_set.get_string(table.loop_mrid.query_index))
        set_identifier(f"{asset_organisation_role_mrid}-to-UNKNOWN")

        asset_mrid = result_set.get_string(table.substation_mrid.query_index)
        set_identifier(f"{asset_organisation_role_mrid}-to-{asset_mrid}")

        loop = self._service.get(asset_organisation_role_mrid, Loop)
        substation = self._service.get(asset_mrid, Substation)

        relationship = LoopSubstationRelationship[result_set.get_string(table.relationship.query_index)]
        if relationship is LoopSubstationRelationship.LOOP_ENERGIZES_SUBSTATION:
            substation.add_loop(loop)
            loop.add_substation(substation)
        elif relationship is LoopSubstationRelationship.SUBSTATION_ENERGIZES_LOOP:
            substation.add_energized_loop(loop)
            loop.add_energizing_substation(substation)
        else:
            assert_never(relationship)

        return True

    """
    Create a `set_identifier` and populate its fields from `TableProtectionRelayFunctionsProtectedSwitches`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_protection_relay_functions_protected_switches(self, table: TableProtectionRelayFunctionsProtectedSwitches, result_set: ResultSet,
                                                           set_identifier: Callable[[str], str]) -> bool:
        protection_relay_function_mrid = set_identifier(result_set.get_string(table.protection_relay_function_mrid.query_index))
        set_identifier(f"{protection_relay_function_mrid}-to-UNKNOWN")

        protected_switch_mrid = result_set.get_string(table.protected_switch_mrid.query_index)
        set_identifier(f"{protection_relay_function_mrid}-to-{protected_switch_mrid}")

        protection_relay_function = self._service.get(protection_relay_function_mrid, ProtectionRelayFunction)
        protected_switch = self._service.get(protected_switch_mrid, ProtectedSwitch)

        protection_relay_function.add_protected_switch(protected_switch)
        protected_switch.add_relay_function(protection_relay_function)

        return True

    """
    Create a `set_identifier` and populate its fields from `TableProtectionRelayFunctionsSensors`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_protection_relay_functions_sensors(self, table: TableProtectionRelayFunctionsSensors, result_set: ResultSet,
                                                set_identifier: Callable[[str], str]) -> bool:
        protection_relay_function_mrid = set_identifier(result_set.get_string(table.protection_relay_function_mrid.query_index))
        set_identifier(f"{protection_relay_function_mrid}-to-UNKNOWN")

        sensor_mrid = result_set.get_string(table.sensor_mrid.query_index)
        set_identifier(f"{protection_relay_function_mrid}-to-{sensor_mrid}")

        protection_relay_function = self._service.get(protection_relay_function_mrid, ProtectionRelayFunction)
        sensor = self._service.get(sensor_mrid, Sensor)

        protection_relay_function.add_sensor(sensor)
        sensor.add_relay_function(protection_relay_function)

        return True

    """
    Create a `set_identifier` and populate its fields from `TableProtectionRelaySchemesProtectionRelayFunctions`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """

    def load_protection_relay_schemes_protection_relay_functions(self, table: TableProtectionRelaySchemesProtectionRelayFunctions, result_set: ResultSet,
                                                                 set_identifier: Callable[[str], str]) -> bool:
        protection_relay_scheme_mrid = set_identifier(result_set.get_string(table.protection_relay_scheme_mrid.query_index))
        set_identifier(f"{protection_relay_scheme_mrid}-to-UNKNOWN")

        protection_relay_function_mrid = result_set.get_string(table.protection_relay_function_mrid.query_index)
        set_identifier(f"{protection_relay_scheme_mrid}-to-{protection_relay_function_mrid}")

        protection_relay_scheme = self._service.get(protection_relay_scheme_mrid, ProtectionRelayScheme)
        protection_relay_function = self._service.get(protection_relay_function_mrid, ProtectionRelayFunction)

        protection_relay_scheme.add_function(protection_relay_function)
        protection_relay_function.add_scheme(protection_relay_scheme)

        return True
