#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional

from zepben.evolve.database.sqlite.common.base_cim_writer import BaseCimWriter
from zepben.evolve.database.sqlite.extensions.prepared_statement import PreparedStatement
from zepben.evolve.database.sqlite.network.network_database_tables import NetworkDatabaseTables
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
from zepben.evolve.database.sqlite.tables.associations.table_synchronous_machines_reactive_capability_curves import \
    TableSynchronousMachinesReactiveCapabilityCurves
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
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_curve_data import TableCurveData
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_curves import TableCurves
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
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_earth_fault_compensators import TableEarthFaultCompensators
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_connections import TableEnergyConnections
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_consumer_phases import TableEnergyConsumerPhases
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_consumers import TableEnergyConsumers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_source_phases import TableEnergySourcePhases
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_sources import TableEnergySources
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_fuses import TableFuses
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_ground_disconnectors import TableGroundDisconnectors
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_grounding_impedances import TableGroundingImpedances
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_grounds import TableGrounds
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_jumpers import TableJumpers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_junctions import TableJunctions
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_linear_shunt_compensators import TableLinearShuntCompensators
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_lines import TableLines
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_load_break_switches import TableLoadBreakSwitches
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_per_length_impedances import TablePerLengthImpedances
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_per_length_line_parameters import TablePerLengthLineParameters
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_per_length_sequence_impedances import TablePerLengthSequenceImpedances
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_petersen_coils import TablePetersenCoils
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_electronics_connection_phases import TablePowerElectronicsConnectionPhases
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_electronics_connections import TablePowerElectronicsConnections
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_transformer_end_ratings import TablePowerTransformerEndRatings
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_transformer_ends import TablePowerTransformerEnds
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_transformers import TablePowerTransformers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_protected_switches import TableProtectedSwitches
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_ratio_tap_changers import TableRatioTapChangers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_reactive_capability_curves import TableReactiveCapabilityCurves
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_reclosers import TableReclosers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_regulating_cond_eq import TableRegulatingCondEq
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_regulating_controls import TableRegulatingControls
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_rotating_machines import TableRotatingMachines
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_series_compensators import TableSeriesCompensators
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_shunt_compensators import TableShuntCompensators
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_switches import TableSwitches
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_synchronous_machines import TableSynchronousMachines
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
from zepben.evolve.model.cim.iec61968.assets.asset import Asset, AssetContainer
from zepben.evolve.model.cim.iec61968.assets.asset_info import AssetInfo
from zepben.evolve.model.cim.iec61968.assets.asset_organisation_role import AssetOrganisationRole, AssetOwner
from zepben.evolve.model.cim.iec61968.assets.pole import Pole
from zepben.evolve.model.cim.iec61968.assets.streetlight import Streetlight
from zepben.evolve.model.cim.iec61968.assets.structure import Structure
from zepben.evolve.model.cim.iec61968.common.location import StreetDetail, TownDetail, Location, StreetAddress, PositionPoint
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.current_transformer_info import CurrentTransformerInfo
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.potential_transformer_info import PotentialTransformerInfo
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.relay_info import RelayInfo
from zepben.evolve.model.cim.iec61968.metering.metering import EndDevice, UsagePoint, Meter
from zepben.evolve.model.cim.iec61968.operations.operational_restriction import OperationalRestriction
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.auxiliary_equipment import AuxiliaryEquipment, FaultIndicator
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.current_transformer import CurrentTransformer
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.potential_transformer import PotentialTransformer
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.sensor import Sensor
from zepben.evolve.model.cim.iec61970.base.core.base_voltage import BaseVoltage
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.connectivity_node import ConnectivityNode
from zepben.evolve.model.cim.iec61970.base.core.connectivity_node_container import ConnectivityNodeContainer
from zepben.evolve.model.cim.iec61970.base.core.curve import Curve
from zepben.evolve.model.cim.iec61970.base.core.curve_data import CurveData
from zepben.evolve.model.cim.iec61970.base.core.equipment import Equipment
from zepben.evolve.model.cim.iec61970.base.core.equipment_container import Feeder, EquipmentContainer, Site
from zepben.evolve.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.evolve.model.cim.iec61970.base.core.regions import GeographicalRegion, SubGeographicalRegion
from zepben.evolve.model.cim.iec61970.base.core.substation import Substation
from zepben.evolve.model.cim.iec61970.base.core.terminal import AcDcTerminal, Terminal
from zepben.evolve.model.cim.iec61970.base.equivalents.equivalent_branch import EquivalentBranch
from zepben.evolve.model.cim.iec61970.base.equivalents.equivalent_equipment import EquivalentEquipment
from zepben.evolve.model.cim.iec61970.base.meas.control import Control
from zepben.evolve.model.cim.iec61970.base.meas.iopoint import IoPoint
from zepben.evolve.model.cim.iec61970.base.meas.measurement import Measurement, Analog, Accumulator, Discrete
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
from zepben.evolve.model.cim.iec61970.base.wires.earth_fault_compensator import EarthFaultCompensator
from zepben.evolve.model.cim.iec61970.base.wires.energy_connection import RegulatingCondEq, EnergyConnection
from zepben.evolve.model.cim.iec61970.base.wires.energy_consumer import EnergyConsumer, EnergyConsumerPhase
from zepben.evolve.model.cim.iec61970.base.wires.energy_source import EnergySource
from zepben.evolve.model.cim.iec61970.base.wires.energy_source_phase import EnergySourcePhase
from zepben.evolve.model.cim.iec61970.base.wires.fuse import Fuse
from zepben.evolve.model.cim.iec61970.base.wires.generation.production.power_electronics_unit import PowerElectronicsUnit, BatteryUnit, PhotoVoltaicUnit, \
    PowerElectronicsWindUnit
from zepben.evolve.model.cim.iec61970.base.wires.ground import Ground
from zepben.evolve.model.cim.iec61970.base.wires.ground_disconnector import GroundDisconnector
from zepben.evolve.model.cim.iec61970.base.wires.grounding_impedance import GroundingImpedance
from zepben.evolve.model.cim.iec61970.base.wires.jumper import Jumper
from zepben.evolve.model.cim.iec61970.base.wires.line import Line
from zepben.evolve.model.cim.iec61970.base.wires.load_break_switch import LoadBreakSwitch
from zepben.evolve.model.cim.iec61970.base.wires.per_length import PerLengthImpedance, PerLengthLineParameter, PerLengthSequenceImpedance
from zepben.evolve.model.cim.iec61970.base.wires.petersen_coil import PetersenCoil
from zepben.evolve.model.cim.iec61970.base.wires.power_electronics_connection import PowerElectronicsConnection, PowerElectronicsConnectionPhase
from zepben.evolve.model.cim.iec61970.base.wires.power_transformer import RatioTapChanger, TapChanger, TransformerEnd, PowerTransformer, PowerTransformerEnd
from zepben.evolve.model.cim.iec61970.base.wires.protected_switch import ProtectedSwitch
from zepben.evolve.model.cim.iec61970.base.wires.reactive_capability_curve import ReactiveCapabilityCurve
from zepben.evolve.model.cim.iec61970.base.wires.recloser import Recloser
from zepben.evolve.model.cim.iec61970.base.wires.regulating_control import RegulatingControl
from zepben.evolve.model.cim.iec61970.base.wires.rotating_machine import RotatingMachine
from zepben.evolve.model.cim.iec61970.base.wires.series_compensator import SeriesCompensator
from zepben.evolve.model.cim.iec61970.base.wires.shunt_compensator import ShuntCompensator, LinearShuntCompensator
from zepben.evolve.model.cim.iec61970.base.wires.switch import Switch
from zepben.evolve.model.cim.iec61970.base.wires.synchronous_machine import SynchronousMachine
from zepben.evolve.model.cim.iec61970.base.wires.tap_changer_control import TapChangerControl
from zepben.evolve.model.cim.iec61970.base.wires.transformer_star_impedance import TransformerStarImpedance
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.circuit import Circuit
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.loop import Loop
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.lv_feeder import LvFeeder
from zepben.evolve.model.cim.iec61970.infiec61970.wires.generation.production.ev_charging_unit import EvChargingUnit

__all__ = ["NetworkCimWriter"]

class NetworkCimWriter(BaseCimWriter):
    """
     A class for writing the :class:`NetworkService` tables to the database.
    
     :param database_tables: The tables available in the database.
    """

    def __init__(self, database_tables: NetworkDatabaseTables):
        super().__init__(database_tables)

    #######################
    # IEC61968 Asset Info #
    #######################

    def save_cable_info(self, cable_info: CableInfo) -> bool:
        """
        Save the :class:`CableInfo` fields to :class:`TableCableInfo`.

        :param cable_info: The :class:`CableInfo` instance to write to the database.
        :return: True if the :class:`CableInfo` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableCableInfo)
        insert = self._database_tables.get_insert(TableCableInfo)

        return self._save_wire_info(table, insert, cable_info, "cable info")

    def save_no_load_test(self, no_load_test: NoLoadTest) -> bool:
        """
        Save the :class:`NoLoadTest` fields to :class:`TableNoLoadTests`.

        :param no_load_test: The :class:`NoLoadTest` instance to write to the database.
        :return: True if the :class:`NoLoadTest` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableNoLoadTests)
        insert = self._database_tables.get_insert(TableNoLoadTests)

        insert.add_value(table.energised_end_voltage.query_index, no_load_test.energised_end_voltage)
        insert.add_value(table.exciting_current.query_index, no_load_test.exciting_current)
        insert.add_value(table.exciting_current_zero.query_index, no_load_test.exciting_current_zero)
        insert.add_value(table.loss.query_index, no_load_test.loss)
        insert.add_value(table.loss_zero.query_index, no_load_test.loss_zero)

        return self._save_transformer_test(table, insert, no_load_test, "no load test")

    def save_open_circuit_test(self, open_circuit_test: OpenCircuitTest) -> bool:
        """
        Save the :class:`OpenCircuitTest` fields to :class:`TableOpenCircuitTests`.

        :param open_circuit_test: The :class:`OpenCircuitTest` instance to write to the database.
        :return: True if the :class:`OpenCircuitTest` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableOpenCircuitTests)
        insert = self._database_tables.get_insert(TableOpenCircuitTests)

        insert.add_value(table.energised_end_step.query_index, open_circuit_test.energised_end_step)
        insert.add_value(table.energised_end_voltage.query_index, open_circuit_test.energised_end_voltage)
        insert.add_value(table.open_end_step.query_index, open_circuit_test.open_end_step)
        insert.add_value(table.open_end_voltage.query_index, open_circuit_test.open_end_voltage)
        insert.add_value(table.phase_shift.query_index, open_circuit_test.phase_shift)

        return self._save_transformer_test(table, insert, open_circuit_test, "open circuit test")

    def save_overhead_wire_info(self, overhead_wire_info: OverheadWireInfo) -> bool:
        """
        Save the :class:`OverheadWireInfo` fields to :class:`TableOverheadWireInfo`.

        :param overhead_wire_info: The :class:`OverheadWireInfo` instance to write to the database.
        :return: True if the :class:`OverheadWireInfo` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableOverheadWireInfo)
        insert = self._database_tables.get_insert(TableOverheadWireInfo)

        return self._save_wire_info(table, insert, overhead_wire_info, "overhead wire info")

    def save_power_transformer_info(self, power_transformer_info: PowerTransformerInfo) -> bool:
        """
        Save the :class:`PowerTransformerInfo` fields to :class:`TablePowerTransformerInfo`.

        :param power_transformer_info: The :class:`PowerTransformerInfo` instance to write to the database.
        :return: True if the :class:`PowerTransformerInfo` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TablePowerTransformerInfo)
        insert = self._database_tables.get_insert(TablePowerTransformerInfo)

        return self._save_asset_info(table, insert, power_transformer_info, "power transformer info")

    def save_short_circuit_test(self, short_circuit_test: ShortCircuitTest) -> bool:
        """
        Save the :class:`ShortCircuitTest` fields to :class:`TableShortCircuitTests`.

        :param short_circuit_test: The :class:`ShortCircuitTest` instance to write to the database.
        :return: True if the :class:`ShortCircuitTest` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableShortCircuitTests)
        insert = self._database_tables.get_insert(TableShortCircuitTests)

        insert.add_value(table.current.query_index, short_circuit_test.current)
        insert.add_value(table.energised_end_step.query_index, short_circuit_test.energised_end_step)
        insert.add_value(table.grounded_end_step.query_index, short_circuit_test.grounded_end_step)
        insert.add_value(table.leakage_impedance.query_index, short_circuit_test.leakage_impedance)
        insert.add_value(table.leakage_impedance_zero.query_index, short_circuit_test.leakage_impedance_zero)
        insert.add_value(table.loss.query_index, short_circuit_test.loss)
        insert.add_value(table.loss_zero.query_index, short_circuit_test.loss_zero)
        insert.add_value(table.power.query_index, short_circuit_test.power)
        insert.add_value(table.voltage.query_index, short_circuit_test.voltage)
        insert.add_value(table.voltage_ohmic_part.query_index, short_circuit_test.voltage_ohmic_part)

        return self._save_transformer_test(table, insert, short_circuit_test, "short circuit test")

    def save_shunt_compensator_info(self, shunt_compensator_info: ShuntCompensatorInfo) -> bool:
        """
        Save the :class:`ShuntCompensatorInfo` fields to :class:`TableShuntCompensatorInfo`.

        :param shunt_compensator_info: The :class:`ShuntCompensatorInfo` instance to write to the database.
        :return: True if the :class:`ShuntCompensatorInfo` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableShuntCompensatorInfo)
        insert = self._database_tables.get_insert(TableShuntCompensatorInfo)

        insert.add_value(table.max_power_loss.query_index, shunt_compensator_info.max_power_loss)
        insert.add_value(table.rated_current.query_index, shunt_compensator_info.rated_current)
        insert.add_value(table.rated_reactive_power.query_index, shunt_compensator_info.rated_reactive_power)
        insert.add_value(table.rated_voltage.query_index, shunt_compensator_info.rated_voltage)

        return self._save_asset_info(table, insert, shunt_compensator_info, "shunt compensator info")

    def save_switch_info(self, switch_info: SwitchInfo) -> bool:
        """
        Save the :class:`SwitchInfo` fields to :class:`TableSwitchInfo`.

        :param switch_info: The :class:`SwitchInfo` instance to write to the database.
        :return: True if the :class:`SwitchInfo` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableSwitchInfo)
        insert = self._database_tables.get_insert(TableSwitchInfo)

        insert.add_value(table.rated_interrupting_time.query_index, switch_info.rated_interrupting_time)

        return self._save_asset_info(table, insert, switch_info, "switch info")

    def save_transformer_end_info(self, transformer_end_info: TransformerEndInfo) -> bool:
        """
        Save the :class:`TransformerEndInfo` fields to :class:`TableTransformerEndInfo`.

        :param transformer_end_info: The :class:`TransformerEndInfo` instance to write to the database.
        :return: True if the :class:`TransformerEndInfo` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableTransformerEndInfo)
        insert = self._database_tables.get_insert(TableTransformerEndInfo)

        insert.add_value(table.connection_kind.query_index, transformer_end_info.connection_kind.short_name)
        insert.add_value(table.emergency_s.query_index, transformer_end_info.emergency_s)
        insert.add_value(table.end_number.query_index, transformer_end_info.end_number)
        insert.add_value(table.insulation_u.query_index, transformer_end_info.insulation_u)
        insert.add_value(table.phase_angle_clock.query_index, transformer_end_info.phase_angle_clock)
        insert.add_value(table.r.query_index, transformer_end_info.r)
        insert.add_value(table.rated_s.query_index, transformer_end_info.rated_s)
        insert.add_value(table.rated_u.query_index, transformer_end_info.rated_u)
        insert.add_value(table.short_term_s.query_index, transformer_end_info.short_term_s)
        insert.add_value(table.transformer_tank_info_mrid.query_index, self._mrid_or_none(transformer_end_info.transformer_tank_info))
        insert.add_value(table.energised_end_no_load_tests.query_index, self._mrid_or_none(transformer_end_info.energised_end_no_load_tests))
        insert.add_value(table.energised_end_short_circuit_tests.query_index, self._mrid_or_none(transformer_end_info.energised_end_short_circuit_tests))
        insert.add_value(table.grounded_end_short_circuit_tests.query_index, self._mrid_or_none(transformer_end_info.grounded_end_short_circuit_tests))
        insert.add_value(table.open_end_open_circuit_tests.query_index, self._mrid_or_none(transformer_end_info.open_end_open_circuit_tests))
        insert.add_value(table.energised_end_open_circuit_tests.query_index, self._mrid_or_none(transformer_end_info.energised_end_open_circuit_tests))

        return self._save_asset_info(table, insert, transformer_end_info, "transformer end info")

    def save_transformer_tank_info(self, transformer_tank_info: TransformerTankInfo) -> bool:
        """
        Save the :class:`TransformerTankInfo` fields to :class:`TableTransformerTankInfo`.

        :param transformer_tank_info: The :class:`TransformerTankInfo` instance to write to the database.
        :return: True if the :class:`TransformerTankInfo` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableTransformerTankInfo)
        insert = self._database_tables.get_insert(TableTransformerTankInfo)

        insert.add_value(table.power_transformer_info_mrid.query_index, self._mrid_or_none(transformer_tank_info.power_transformer_info))

        return self._save_asset_info(table, insert, transformer_tank_info, "transformer tank info")

    def _save_transformer_test(self, table: TableTransformerTest, insert: PreparedStatement, transformer_test: TransformerTest, description: str) -> bool:
        insert.add_value(table.base_power.query_index, transformer_test.base_power)
        insert.add_value(table.temperature.query_index, transformer_test.temperature)

        return self._save_identified_object(table, insert, transformer_test, description)

    def _save_wire_info(self, table: TableWireInfo, insert: PreparedStatement, wire_info: WireInfo, description: str) -> bool:
        insert.add_value(table.rated_current.query_index, wire_info.rated_current)
        insert.add_value(table.material.query_index, wire_info.material.short_name)

        return self._save_asset_info(table, insert, wire_info, description)

    ###################
    # IEC61968 Assets #
    ###################

    def _save_asset(self, table: TableAssets, insert: PreparedStatement, asset: Asset, description: str) -> bool:
        status = True

        insert.add_value(table.location_mrid.query_index, self._mrid_or_none(asset.location))
        for it in asset.organisation_roles:
            status = status and self._save_asset_organisation_role_to_asset_association(it, asset)

        return status and self._save_identified_object(table, insert, asset, description)

    def _save_asset_container(self, table: TableAssetContainers, insert: PreparedStatement, asset_container: AssetContainer, description: str) -> bool:
        return self._save_asset(table, insert, asset_container, description)

    def _save_asset_info(self, table: TableAssetInfo, insert: PreparedStatement, asset_info: AssetInfo, description: str) -> bool:
        return self._save_identified_object(table, insert, asset_info, description)

    def _save_asset_organisation_role(
        self,
        table: TableAssetOrganisationRoles,
        insert: PreparedStatement,
        asset_organisation_role: AssetOrganisationRole,
        description: str
    ) -> bool:
        return self._save_organisation_role(table, insert, asset_organisation_role, description)

    def save_asset_owner(self, asset_owner: AssetOwner) -> bool:
        """
        Save the :class:`AssetOwner` fields to :class:`TableAssetOwners`.

        :param asset_owner: The :class:`AssetOwner` instance to write to the database.
        :return: True if the :class:`AssetOwner` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableAssetOwners)
        insert = self._database_tables.get_insert(TableAssetOwners)

        return self._save_asset_organisation_role(table, insert, asset_owner, "asset owner")

    def _save_structure(self, table: TableStructures, insert: PreparedStatement, structure: Structure, description: str) -> bool:
        return self._save_asset_container(table, insert, structure, description)

    def save_pole(self, pole: Pole) -> bool:
        """
        Save the :class:`Pole` fields to :class:`TablePoles`.

        :param pole: The :class:`Pole` instance to write to the database.
        :return: True if the :class:`Pole` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TablePoles)
        insert = self._database_tables.get_insert(TablePoles)

        insert.add_value(table.classification.query_index, pole.classification)

        return self._save_structure(table, insert, pole, "pole")

    def save_streetlight(self, streetlight: Streetlight) -> bool:
        """
        Save the :class:`Streetlight` fields to :class:`TableStreetlights`.

        :param streetlight: The :class:`Streetlight` instance to write to the database.
        :return: True if the :class:`Streetlight` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableStreetlights)
        insert = self._database_tables.get_insert(TableStreetlights)

        insert.add_value(table.pole_mrid.query_index, self._mrid_or_none(streetlight.pole))
        insert.add_value(table.light_rating.query_index, streetlight.light_rating)
        insert.add_value(table.lamp_kind.query_index, streetlight.lamp_kind.short_name)
        return self._save_asset(table, insert, streetlight, "streetlight")

    ###################
    # IEC61968 Common #
    ###################

    @staticmethod
    def _insert_street_detail(table: TableStreetAddresses, insert: PreparedStatement, street_detail: Optional[StreetDetail]):
        insert.add_value(table.building_name.query_index, street_detail.building_name if street_detail else None)
        insert.add_value(table.floor_identification.query_index, street_detail.floor_identification if street_detail else None)
        insert.add_value(table.street_name.query_index, street_detail.name if street_detail else None)
        insert.add_value(table.number.query_index, street_detail.number if street_detail else None)
        insert.add_value(table.suite_number.query_index, street_detail.suite_number if street_detail else None)
        insert.add_value(table.type.query_index, street_detail.type if street_detail else None)
        insert.add_value(table.display_address.query_index, street_detail.display_address if street_detail else None)

    @staticmethod
    def _insert_town_detail(table: TableTownDetails, insert: PreparedStatement, town_detail: Optional[TownDetail]):
        insert.add_value(table.town_name.query_index, town_detail.name if town_detail else None)
        insert.add_value(table.state_or_province.query_index, town_detail.state_or_province if town_detail else None)

    def save_location(self, location: Location) -> bool:
        """
        Save the :class:`Location` fields to :class:`TableLocations`.

        :param location: The :class:`Location` instance to write to the database.
        :return: True if the :class:`Location` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableLocations)
        insert = self._database_tables.get_insert(TableLocations)

        status = self._save_location_street_address(location, TableLocationStreetAddressField.mainAddress, location.main_address, "location main address")
        for sequence_number, point in enumerate(location.points):
            status = status and self._save_position_point(location, sequence_number, point)

        return status and self._save_identified_object(table, insert, location, "location")

    def _save_location_street_address(
        self,
        location: Location,
        field: TableLocationStreetAddressField,
        street_address: Optional[StreetAddress],
        description: str
    ) -> bool:
        if street_address is None:
            return True

        table = self._database_tables.get_table(TableLocationStreetAddresses)
        insert = self._database_tables.get_insert(TableLocationStreetAddresses)

        insert.add_value(table.location_mrid.query_index, location.mrid)
        insert.add_value(table.address_field.query_index, field.short_name)

        return self._save_street_address(table, insert, street_address, description)

    def _save_position_point(self, location: Location, sequence_number: int, position_point: PositionPoint) -> bool:
        table = self._database_tables.get_table(TablePositionPoints)
        insert = self._database_tables.get_insert(TablePositionPoints)

        insert.add_value(table.location_mrid.query_index, location.mrid)
        insert.add_value(table.sequence_number.query_index, sequence_number)
        insert.add_value(table.x_position.query_index, position_point.x_position)
        insert.add_value(table.y_position.query_index, position_point.y_position)

        return self._try_execute_single_update(insert, "position point")

    def _save_street_address(
        self,
        table: TableStreetAddresses,
        insert: PreparedStatement,
        street_address: StreetAddress,
        description: str
    ) -> bool:
        insert.add_value(table.postal_code.query_index, street_address.postal_code)
        insert.add_value(table.po_box.query_index, street_address.po_box)

        self._insert_town_detail(table, insert, street_address.town_detail)
        self._insert_street_detail(table, insert, street_address.street_detail)

        return self._try_execute_single_update(insert, description)

    #####################################
    # IEC61968 infIEC61968 InfAssetInfo #
    #####################################

    def save_relay_info(self, relay_info: RelayInfo) -> bool:
        """
        Save the :class:`RelayInfo` fields to :class:`TableRelayInfo`.

        :param relay_info: The :class:`RelayInfo` instance to write to the database.
        :return: True if the :class:`RelayInfo` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableRelayInfo)
        insert = self._database_tables.get_insert(TableRelayInfo)

        reclose_delay_table = self._database_tables.get_table(TableRecloseDelays)
        reclose_delay_insert = self._database_tables.get_insert(TableRecloseDelays)
        for idx, delay in enumerate(relay_info.reclose_delays):
            reclose_delay_insert.add_value(reclose_delay_table.relay_info_mrid.query_index, relay_info.mrid)
            reclose_delay_insert.add_value(reclose_delay_table.sequence_number.query_index, idx)
            reclose_delay_insert.add_value(reclose_delay_table.reclose_delay.query_index, delay)
            self._try_execute_single_update(reclose_delay_insert, "reclose delay")

        insert.add_value(table.curve_setting.query_index, relay_info.curve_setting)
        insert.add_value(table.reclose_fast.query_index, relay_info.reclose_fast)

        return self._save_asset_info(table, insert, relay_info, "relay info")

    def save_current_transformer_info(self, current_transformer_info: CurrentTransformerInfo) -> bool:
        """
        Save the :class:`CurrentTransformerInfo` fields to :class:`TableCurrentTransformerInfo`.

        :param current_transformer_info: The :class:`CurrentTransformerInfo` instance to write to the database.
        :return: True if the :class:`CurrentTransformerInfo` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableCurrentTransformerInfo)
        insert = self._database_tables.get_insert(TableCurrentTransformerInfo)

        insert.add_value(table.accuracy_class.query_index, current_transformer_info.accuracy_class)
        insert.add_value(table.accuracy_limit.query_index, current_transformer_info.accuracy_limit)
        insert.add_value(table.core_count.query_index, current_transformer_info.core_count)
        insert.add_value(table.ct_class.query_index, current_transformer_info.ct_class)
        insert.add_value(table.knee_point_voltage.query_index, current_transformer_info.knee_point_voltage)
        insert.add_ratio(table.max_ratio_numerator.query_index, table.max_ratio_denominator.query_index, current_transformer_info.max_ratio)
        insert.add_ratio(table.nominal_ratio_numerator.query_index, table.nominal_ratio_denominator.query_index, current_transformer_info.nominal_ratio)
        insert.add_value(table.primary_ratio.query_index, current_transformer_info.primary_ratio)
        insert.add_value(table.rated_current.query_index, current_transformer_info.rated_current)
        insert.add_value(table.secondary_fls_rating.query_index, current_transformer_info.secondary_fls_rating)
        insert.add_value(table.secondary_ratio.query_index, current_transformer_info.secondary_ratio)
        insert.add_value(table.usage.query_index, current_transformer_info.usage)

        return self._save_asset_info(table, insert, current_transformer_info, "current transformer info")

    def save_potential_transformer_info(self, potential_transformer_info: PotentialTransformerInfo) -> bool:
        """
        Save the :class:`PotentialTransformerInfo` fields to :class:`TablePotentialTransformerInfo`.

        :param potential_transformer_info: The :class:`PotentialTransformerInfo` instance to write to the database.
        :return: True if the :class:`PotentialTransformerInfo` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TablePotentialTransformerInfo)
        insert = self._database_tables.get_insert(TablePotentialTransformerInfo)

        insert.add_value(table.accuracy_class.query_index, potential_transformer_info.accuracy_class)
        insert.add_ratio(table.nominal_ratio_numerator.query_index, table.nominal_ratio_denominator.query_index, potential_transformer_info.nominal_ratio)
        insert.add_value(table.primary_ratio.query_index, potential_transformer_info.primary_ratio)
        insert.add_value(table.pt_class.query_index, potential_transformer_info.pt_class)
        insert.add_value(table.rated_voltage.query_index, potential_transformer_info.rated_voltage)
        insert.add_value(table.secondary_ratio.query_index, potential_transformer_info.secondary_ratio)

        return self._save_asset_info(table, insert, potential_transformer_info, "potential transformer info")

    #####################
    # IEC61968 Metering #
    #####################

    def _save_end_device(self, table: TableEndDevices, insert: PreparedStatement, end_device: EndDevice, description: str) -> bool:
        insert.add_value(table.customer_mrid.query_index, end_device.customer_mrid)
        insert.add_value(table.service_location_mrid.query_index, self._mrid_or_none(end_device.service_location))

        status = True
        for it in end_device.usage_points:
            status = status and self._save_usage_point_to_end_device_association(it, end_device)

        return status and self._save_asset_container(table, insert, end_device, description)

    def save_meter(self, meter: Meter) -> bool:
        """
        Save the :class:`Meter` fields to :class:`TableMeters`.

        :param meter: The :class:`Meter` instance to write to the database.
        :return: True if the :class:`Meter` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableMeters)
        insert = self._database_tables.get_insert(TableMeters)

        return self._save_end_device(table, insert, meter, "meter")

    def save_usage_point(self, usage_point: UsagePoint) -> bool:
        """
        Save the :class:`UsagePoint` fields to :class:`TableUsagePoints`.

        :param usage_point: The :class:`UsagePoint` instance to write to the database.
        :return: True if the :class:`UsagePoint` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableUsagePoints)
        insert = self._database_tables.get_insert(TableUsagePoints)

        insert.add_value(table.location_mrid.query_index, self._mrid_or_none(usage_point.usage_point_location))
        insert.add_value(table.is_virtual.query_index, usage_point.is_virtual)
        insert.add_value(table.connection_category.query_index, usage_point.connection_category)
        insert.add_value(table.rated_power.query_index, usage_point.rated_power)
        insert.add_value(table.approved_inverter_capacity.query_index, usage_point.approved_inverter_capacity)
        insert.add_value(table.phase_code.query_index, usage_point.phase_code.short_name)

        status = True
        for it in usage_point.equipment:
            status = status and self._save_equipment_to_usage_point_association(it, usage_point)

        return status and self._save_identified_object(table, insert, usage_point, "usage point")

    #######################
    # IEC61968 Operations #
    #######################

    def save_operational_restriction(self, operational_restriction: OperationalRestriction) -> bool:
        """
        Save the :class:`OperationalRestriction` fields to :class:`TableOperationalRestrictions`.

        :param operational_restriction: The :class:`OperationalRestriction` instance to write to the database.
        :return: True if the :class:`OperationalRestriction` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableOperationalRestrictions)
        insert = self._database_tables.get_insert(TableOperationalRestrictions)

        status = True
        for it in operational_restriction.equipment:
            status = status and self._save_equipment_to_operational_restriction_association(it, operational_restriction)

        return status and self._save_document(table, insert, operational_restriction, "operational restriction")

    #####################################
    # IEC61970 Base Auxiliary Equipment #
    #####################################

    def _save_auxiliary_equipment(
        self,
        table: TableAuxiliaryEquipment,
        insert: PreparedStatement,
        auxiliary_equipment: AuxiliaryEquipment,
        description: str
    ) -> bool:
        insert.add_value(table.terminal_mrid.query_index, self._mrid_or_none(auxiliary_equipment.terminal))

        return self._save_equipment(table, insert, auxiliary_equipment, description)

    def save_current_transformer(self, current_transformer: CurrentTransformer) -> bool:
        """
        Save the :class:`CurrentTransformer` fields to :class:`TableCurrentTransformers`.

        :param current_transformer: The :class:`CurrentTransformer` instance to write to the database.
        :return: True if the :class:`CurrentTransformer` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableCurrentTransformers)
        insert = self._database_tables.get_insert(TableCurrentTransformers)

        insert.add_value(table.current_transformer_info_mrid.query_index, self._mrid_or_none(current_transformer.current_transformer_info))
        insert.add_value(table.core_burden.query_index, current_transformer.core_burden)

        return self._save_sensor(table, insert, current_transformer, "current transformer")

    def save_fault_indicator(self, fault_indicator: FaultIndicator) -> bool:
        """
        Save the :class:`FaultIndicator` fields to :class:`TableFaultIndicators`.

        :param fault_indicator: The :class:`FaultIndicator` instance to write to the database.
        :return: True if the :class:`FaultIndicator` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableFaultIndicators)
        insert = self._database_tables.get_insert(TableFaultIndicators)

        return self._save_auxiliary_equipment(table, insert, fault_indicator, "fault indicator")

    def save_potential_transformer(self, potential_transformer: PotentialTransformer) -> bool:
        """
        Save the :class:`PotentialTransformer` fields to :class:`TablePotentialTransformers`.

        :param potential_transformer: The :class:`PotentialTransformer` instance to write to the database.
        :return: True if the :class:`PotentialTransformer` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TablePotentialTransformers)
        insert = self._database_tables.get_insert(TablePotentialTransformers)

        insert.add_value(table.potential_transformer_info_mrid.query_index, self._mrid_or_none(potential_transformer.potential_transformer_info))
        insert.add_value(table.type.query_index, potential_transformer.type.short_name)

        return self._save_sensor(table, insert, potential_transformer, "potential transformer")

    def _save_sensor(self, table: TableSensors, insert: PreparedStatement, sensor: Sensor, description: str) -> bool:
        return self._save_auxiliary_equipment(table, insert, sensor, description)

    ######################
    # IEC61970 Base Core #
    ######################

    def _save_ac_dc_terminal(self, table: TableAcDcTerminals, insert: PreparedStatement, ac_dc_terminal: AcDcTerminal, description: str) -> bool:
        return self._save_identified_object(table, insert, ac_dc_terminal, description)

    def save_base_voltage(self, base_voltage: BaseVoltage) -> bool:
        """
        Save the :class:`BaseVoltage` fields to :class:`TableBaseVoltages`.

        :param base_voltage: The :class:`BaseVoltage` instance to write to the database.
        :return: True if the :class:`BaseVoltage` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableBaseVoltages)
        insert = self._database_tables.get_insert(TableBaseVoltages)

        insert.add_value(table.nominal_voltage.query_index, base_voltage.nominal_voltage)

        return self._save_identified_object(table, insert, base_voltage, "base voltage")

    def _save_conducting_equipment(
        self,
        table: TableConductingEquipment,
        insert: PreparedStatement,
        conducting_equipment: ConductingEquipment,
        description: str
    ) -> bool:
        insert.add_value(table.base_voltage_mrid.query_index, self._mrid_or_none(conducting_equipment.base_voltage))

        return self._save_equipment(table, insert, conducting_equipment, description)

    def save_connectivity_node(self, connectivity_node: ConnectivityNode) -> bool:
        """
        Save the :class:`ConnectivityNode` fields to :class:`TableConnectivityNodes`.

        :param connectivity_node: The :class:`ConnectivityNode` instance to write to the database.
        :return: True if the :class:`ConnectivityNode` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableConnectivityNodes)
        insert = self._database_tables.get_insert(TableConnectivityNodes)

        return self._save_identified_object(table, insert, connectivity_node, "connectivity node")

    def _save_connectivity_node_container(
        self,
        table: TableConnectivityNodeContainers,
        insert: PreparedStatement,
        connectivity_node_container: ConnectivityNodeContainer,
        description: str
    ) -> bool:
        return self._save_power_system_resource(table, insert, connectivity_node_container, description)

    def _save_curve(self, table: TableCurves, insert: PreparedStatement, curve: Curve, description: str) -> bool:
        status = True
        for curve_data in curve.data:
            status = status and self._save_curve_data(curve, curve_data)

        return status and self._save_identified_object(table, insert, curve, description)

    def _save_curve_data(self, curve: Curve, curve_data: CurveData) -> bool:
        table = self._database_tables.get_table(TableCurveData)
        insert = self._database_tables.get_insert(TableCurveData)

        insert.add_value(table.curve_mrid.query_index, curve.mrid)
        insert.add_value(table.x_value.query_index, curve_data.x_value)
        insert.add_value(table.y1_value.query_index, curve_data.y1_value)
        insert.add_value(table.y2_value.query_index, curve_data.y2_value)
        insert.add_value(table.y3_value.query_index, curve_data.y3_value)

        return self._try_execute_single_update(insert, "curve data")

    def _save_equipment(self, table: TableEquipment, insert: PreparedStatement, equipment: Equipment, description: str) -> bool:
        insert.add_value(table.normally_in_service.query_index, equipment.normally_in_service)
        insert.add_value(table.in_service.query_index, equipment.in_service)
        insert.add_value(table.commissioned_date.query_index, f"{equipment.commissioned_date.isoformat()}Z" if equipment.commissioned_date else None)

        status = True
        for it in equipment.containers:
            if self._should_export_container_contents(it):
                status = status and self._save_equipment_to_equipment_container_association(equipment, it)

        return status and self._save_power_system_resource(table, insert, equipment, description)

    def _save_equipment_container(
        self,
        table: TableEquipmentContainers,
        insert: PreparedStatement,
        equipment_container: EquipmentContainer,
        description: str
    ) -> bool:
        return self._save_connectivity_node_container(table, insert, equipment_container, description)

    def save_feeder(self, feeder: Feeder) -> bool:
        """
        Save the :class:`Feeder` fields to :class:`TableFeeders`.

        :param feeder: The :class:`Feeder` instance to write to the database.
        :return: True if the :class:`Feeder` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableFeeders)
        insert = self._database_tables.get_insert(TableFeeders)

        insert.add_value(table.normal_head_terminal_mrid.query_index, self._mrid_or_none(feeder.normal_head_terminal))
        insert.add_value(
            table.normal_energizing_substation_mrid.query_index,
            self._mrid_or_none(feeder.normal_energizing_substation)
        )

        return self._save_equipment_container(table, insert, feeder, "feeder")

    def save_geographical_region(self, geographical_region: GeographicalRegion) -> bool:
        """
        Save the :class:`GeographicalRegion` fields to :class:`TableGeographicalRegions`.

        :param geographical_region: The :class:`GeographicalRegion` instance to write to the database.
        :return: True if the :class:`GeographicalRegion` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableGeographicalRegions)
        insert = self._database_tables.get_insert(TableGeographicalRegions)

        return self._save_identified_object(table, insert, geographical_region, "geographical region")

    def _save_power_system_resource(
        self,
        table: TablePowerSystemResources,
        insert: PreparedStatement,
        power_system_resource: PowerSystemResource,
        description: str
    ) -> bool:
        insert.add_value(table.location_mrid.query_index, self._mrid_or_none(power_system_resource.location))
        insert.add_value(table.num_controls.query_index, power_system_resource.num_controls)

        return self._save_identified_object(table, insert, power_system_resource, description)

    def save_site(self, site: Site) -> bool:
        """
        Save the :class:`Site` fields to :class:`TableSites`.

        :param site: The :class:`Site` instance to write to the database.
        :return: True if the :class:`Site` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableSites)
        insert = self._database_tables.get_insert(TableSites)

        return self._save_equipment_container(table, insert, site, "site")

    def save_sub_geographical_region(self, sub_geographical_region: SubGeographicalRegion) -> bool:
        """
        Save the :class:`SubGeographicalRegion` fields to :class:`TableSubGeographicalRegions`.

        :param sub_geographical_region: The :class:`SubGeographicalRegion` instance to write to the database.
        :return: True if the :class:`SubGeographicalRegion` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableSubGeographicalRegions)
        insert = self._database_tables.get_insert(TableSubGeographicalRegions)

        insert.add_value(
            table.geographical_region_mrid.query_index,
            self._mrid_or_none(sub_geographical_region.geographical_region)
        )

        return self._save_identified_object(table, insert, sub_geographical_region, "sub-geographical region")

    def save_substation(self, substation: Substation) -> bool:
        """
        Save the :class:`Substation` fields to :class:`TableSubstations`.

        :param substation: The :class:`Substation` instance to write to the database.
        :return: True if the :class:`Substation` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableSubstations)
        insert = self._database_tables.get_insert(TableSubstations)

        insert.add_value(table.sub_geographical_region_mrid.query_index, self._mrid_or_none(substation.sub_geographical_region))

        return self._save_equipment_container(table, insert, substation, "substation")

    def save_terminal(self, terminal: Terminal) -> bool:
        """
        Save the :class:`Terminal` fields to :class:`TableTerminals`.

        :param terminal: The :class:`Terminal` instance to write to the database.
        :return: True if the :class:`Terminal` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableTerminals)
        insert = self._database_tables.get_insert(TableTerminals)

        insert.add_value(table.conducting_equipment_mrid.query_index, self._mrid_or_none(terminal.conducting_equipment))
        insert.add_value(table.sequence_number.query_index, terminal.sequence_number)
        insert.add_value(table.connectivity_node_mrid.query_index, terminal.connectivity_node_id)
        insert.add_value(table.phases.query_index, terminal.phases.short_name)

        return self._save_ac_dc_terminal(table, insert, terminal, "terminal")

    #############################
    # IEC61970 Base Equivalents #
    #############################

    def save_equivalent_branch(self, equivalent_branch: EquivalentBranch) -> bool:
        """
        Save the :class:`EquivalentBranch` fields to :class:`TableEquivalentBranches`.

        :param equivalent_branch: The :class:`EquivalentBranch` instance to write to the database.
        :return: True if the :class:`EquivalentBranch` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableEquivalentBranches)
        insert = self._database_tables.get_insert(TableEquivalentBranches)

        insert.add_value(table.negative_r12.query_index, equivalent_branch.negative_r12)
        insert.add_value(table.negative_r21.query_index, equivalent_branch.negative_r21)
        insert.add_value(table.negative_x12.query_index, equivalent_branch.negative_x12)
        insert.add_value(table.negative_x21.query_index, equivalent_branch.negative_x21)
        insert.add_value(table.positive_r12.query_index, equivalent_branch.positive_r12)
        insert.add_value(table.positive_r21.query_index, equivalent_branch.positive_r21)
        insert.add_value(table.positive_x12.query_index, equivalent_branch.positive_x12)
        insert.add_value(table.positive_x21.query_index, equivalent_branch.positive_x21)
        insert.add_value(table.r.query_index, equivalent_branch.r)
        insert.add_value(table.r21.query_index, equivalent_branch.r21)
        insert.add_value(table.x.query_index, equivalent_branch.x)
        insert.add_value(table.x21.query_index, equivalent_branch.x21)
        insert.add_value(table.zero_r12.query_index, equivalent_branch.zero_r12)
        insert.add_value(table.zero_r21.query_index, equivalent_branch.zero_r21)
        insert.add_value(table.zero_x12.query_index, equivalent_branch.zero_x12)
        insert.add_value(table.zero_x21.query_index, equivalent_branch.zero_x21)

        return self._save_equivalent_equipment(table, insert, equivalent_branch, "equivalent branch")

    def _save_equivalent_equipment(
        self,
        table: TableEquivalentEquipment,
        insert: PreparedStatement,
        equivalent_equipment: EquivalentEquipment,
        description: str
    ) -> bool:
        return self._save_conducting_equipment(table, insert, equivalent_equipment, description)

    ######################
    # IEC61970 Base Meas #
    ######################

    def _save_measurement(
        self,
        table: TableMeasurements,
        insert: PreparedStatement,
        measurement: Measurement,
        description: str
    ) -> bool:
        insert.add_value(table.power_system_resource_mrid.query_index, measurement.power_system_resource_mrid)
        insert.add_value(table.remote_source_mrid.query_index, self._mrid_or_none(measurement.remote_source))
        insert.add_value(table.terminal_mrid.query_index, measurement.terminal_mrid)
        insert.add_value(table.phases.query_index, measurement.phases.short_name)
        insert.add_value(table.unit_symbol.query_index, measurement.unit_symbol.short_name)

        return self._save_identified_object(table, insert, measurement, description)

    def save_analog(self, analog: Analog) -> bool:
        """
        Save the :class:`Analog` fields to :class:`TableAnalogs`.

        :param analog: The :class:`Analog` instance to write to the database.
        :return: True if the :class:`Analog` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableAnalogs)
        insert = self._database_tables.get_insert(TableAnalogs)

        insert.add_value(table.positive_flow_in.query_index, analog.positive_flow_in)

        return self._save_measurement(table, insert, analog, "analog")

    def save_accumulator(self, accumulator: Accumulator) -> bool:
        """
        Save the :class:`Accumulator` fields to :class:`TableAccumulators`.

        :param accumulator: The :class:`Accumulator` instance to write to the database.
        :return: True if the :class:`Accumulator` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableAccumulators)
        insert = self._database_tables.get_insert(TableAccumulators)

        return self._save_measurement(table, insert, accumulator, "accumulator")

    def save_discrete(self, discrete: Discrete) -> bool:
        """
        Save the :class:`Discrete` fields to :class:`TableDiscretes`.

        :param discrete: The :class:`Discrete` instance to write to the database.
        :return: True if the :class:`Discrete` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableDiscretes)
        insert = self._database_tables.get_insert(TableDiscretes)

        return self._save_measurement(table, insert, discrete, "discrete")

    def save_control(self, control: Control) -> bool:
        """
        Save the :class:`Control` fields to :class:`TableControls`.

        :param control: The :class:`Control` instance to write to the database.
        :return: True if the :class:`Control` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableControls)
        insert = self._database_tables.get_insert(TableControls)

        insert.add_value(table.power_system_resource_mrid.query_index, control.power_system_resource_mrid)

        return self._save_io_point(table, insert, control, "control")

    def _save_io_point(self, table: TableIoPoints, insert: PreparedStatement, io_point: IoPoint, description: str) -> bool:
        return self._save_identified_object(table, insert, io_point, description)

    ############################
    # IEC61970 Base Protection #
    ############################

    def save_current_relay(self, current_relay: CurrentRelay) -> bool:
        """
        Save the :class:`CurrentRelay` fields to :class:`TableCurrentRelays`.

        :param current_relay: The :class:`CurrentRelay` instance to write to the database.
        :return: True if the :class:`CurrentRelay` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableCurrentRelays)
        insert = self._database_tables.get_insert(TableCurrentRelays)

        insert.add_value(table.current_limit_1.query_index, current_relay.current_limit_1)
        insert.add_value(table.inverse_time_flag.query_index, current_relay.inverse_time_flag)
        insert.add_value(table.time_delay_1.query_index, current_relay.time_delay_1)

        return self._save_protection_relay_function(table, insert, current_relay, "current relay")

    def save_distance_relay(self, distance_relay: DistanceRelay) -> bool:
        """
        Save the :class:`DistanceRelay` fields to :class:`TableDistanceRelays`.

        :param distance_relay: The :class:`DistanceRelay` instance to write to the database.
        :return: True if the :class:`DistanceRelay` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableDistanceRelays)
        insert = self._database_tables.get_insert(TableDistanceRelays)

        insert.add_value(table.backward_blind.query_index, distance_relay.backward_blind)
        insert.add_value(table.backward_reach.query_index, distance_relay.backward_reach)
        insert.add_value(table.backward_reactance.query_index, distance_relay.backward_reactance)
        insert.add_value(table.forward_blind.query_index, distance_relay.forward_blind)
        insert.add_value(table.forward_reach.query_index, distance_relay.forward_reach)
        insert.add_value(table.forward_reactance.query_index, distance_relay.forward_reactance)
        insert.add_value(table.operation_phase_angle1.query_index, distance_relay.operation_phase_angle1)
        insert.add_value(table.operation_phase_angle2.query_index, distance_relay.operation_phase_angle2)
        insert.add_value(table.operation_phase_angle3.query_index, distance_relay.operation_phase_angle3)

        return self._save_protection_relay_function(table, insert, distance_relay, "distance relay")

    def _save_protection_relay_function(
        self,
        table: TableProtectionRelayFunctions,
        insert: PreparedStatement,
        protection_relay_function: ProtectionRelayFunction,
        description: str
    ) -> bool:
        insert.add_value(table.model.query_index, protection_relay_function.model)
        insert.add_value(table.reclosing.query_index, protection_relay_function.reclosing)
        insert.add_value(table.relay_delay_time.query_index, protection_relay_function.relay_delay_time)
        insert.add_value(table.protection_kind.query_index, protection_relay_function.protection_kind.short_name)
        insert.add_value(table.directable.query_index, protection_relay_function.directable)
        insert.add_value(table.power_direction.query_index, protection_relay_function.power_direction.short_name)
        insert.add_value(table.relay_info_mrid.query_index, self._mrid_or_none(protection_relay_function.asset_info))

        status = True
        for it in protection_relay_function.protected_switches:
            status = status and self._save_protection_relay_function_to_protected_switch_association(protection_relay_function, it)
        for it in protection_relay_function.sensors:
            status = status and self._save_protection_relay_function_to_sensor_association(protection_relay_function, it)
        for sequence_number, threshold in enumerate(protection_relay_function.thresholds):
            status = status and self._save_protection_relay_function_threshold(protection_relay_function, sequence_number, threshold)
        for sequence_number, time_limit in enumerate(protection_relay_function.time_limits):
            status = status and self._save_protection_relay_function_time_limit(protection_relay_function, sequence_number, time_limit)

        return status and self._save_power_system_resource(table, insert, protection_relay_function, description)

    def _save_protection_relay_function_threshold(
        self,
        protection_relay_function: ProtectionRelayFunction,
        sequence_number: int,
        threshold: RelaySetting
    ) -> bool:
        table = self._database_tables.get_table(TableProtectionRelayFunctionThresholds)
        insert = self._database_tables.get_insert(TableProtectionRelayFunctionThresholds)

        insert.add_value(table.protection_relay_function_mrid.query_index, protection_relay_function.mrid)
        insert.add_value(table.sequence_number.query_index, sequence_number)
        insert.add_value(table.unit_symbol.query_index, threshold.unit_symbol.short_name)
        insert.add_value(table.value.query_index, threshold.value)
        insert.add_value(table.name_.query_index, threshold.name)

        return self._try_execute_single_update(insert, "protection relay function threshold")

    def _save_protection_relay_function_time_limit(self, protection_relay_function: ProtectionRelayFunction, sequence_number: int, time_limit: float) -> bool:
        table = self._database_tables.get_table(TableProtectionRelayFunctionTimeLimits)
        insert = self._database_tables.get_insert(TableProtectionRelayFunctionTimeLimits)

        insert.add_value(table.protection_relay_function_mrid.query_index, protection_relay_function.mrid)
        insert.add_value(table.sequence_number.query_index, sequence_number)
        insert.add_value(table.time_limit.query_index, time_limit)

        return self._try_execute_single_update(insert, "protection relay function time limit")

    def save_protection_relay_scheme(self, protection_relay_scheme: ProtectionRelayScheme) -> bool:
        """
        Save the :class:`ProtectionRelayScheme` fields to :class:`TableProtectionRelaySchemes`.

        :param protection_relay_scheme: The :class:`ProtectionRelayScheme` instance to write to the database.
        :return: True if the :class:`ProtectionRelayScheme` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableProtectionRelaySchemes)
        insert = self._database_tables.get_insert(TableProtectionRelaySchemes)

        insert.add_value(table.system_mrid.query_index, self._mrid_or_none(protection_relay_scheme.system))

        status = True
        for it in protection_relay_scheme.functions:
            status and self._save_protection_relay_scheme_to_protection_relay_function_association(protection_relay_scheme, it)

        return status and self._save_identified_object(table, insert, protection_relay_scheme, "protection relay scheme")

    def save_protection_relay_system(self, protection_relay_system: ProtectionRelaySystem) -> bool:
        """
        Save the :class:`ProtectionRelaySystem` fields to :class:`TableProtectionRelaySystems`.

        :param protection_relay_system: The :class:`ProtectionRelaySystem` instance to write to the database.
        :return: True if the :class:`ProtectionRelaySystem` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableProtectionRelaySystems)
        insert = self._database_tables.get_insert(TableProtectionRelaySystems)

        insert.add_value(table.protection_kind.query_index, protection_relay_system.protection_kind.short_name)

        return self._save_equipment(table, insert, protection_relay_system, "protection relay system")

    def save_voltage_relay(self, voltage_relay: VoltageRelay) -> bool:
        """
        Save the :class:`VoltageRelay` fields to :class:`TableVoltageRelays`.

        :param voltage_relay: The :class:`VoltageRelay` instance to write to the database.
        :return: True if the :class:`VoltageRelay` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableVoltageRelays)
        insert = self._database_tables.get_insert(TableVoltageRelays)

        return self._save_protection_relay_function(table, insert, voltage_relay, "voltage relay")

    ############################
    # IEC61970 Base SCADA #
    ############################

    def save_remote_control(self, remote_control: RemoteControl) -> bool:
        """
        Save the :class:`RemoteControl` fields to :class:`TableRemoteControls`.

        :param remote_control: The :class:`RemoteControl` instance to write to the database.
        :return: True if the :class:`RemoteControl` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableRemoteControls)
        insert = self._database_tables.get_insert(TableRemoteControls)

        insert.add_value(table.control_mrid.query_index, self._mrid_or_none(remote_control.control))

        return self._save_remote_point(table, insert, remote_control, "remote control")

    def _save_remote_point(self, table: TableRemotePoints, insert: PreparedStatement, remote_point: RemotePoint, description: str) -> bool:
        return self._save_identified_object(table, insert, remote_point, description)

    def save_remote_source(self, remote_source: RemoteSource) -> bool:
        """
        Save the :class:`RemoteSource` fields to :class:`TableRemoteSources`.

        :param remote_source: The :class:`RemoteSource` instance to write to the database.
        :return: True if the :class:`RemoteSource` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableRemoteSources)
        insert = self._database_tables.get_insert(TableRemoteSources)

        insert.add_value(table.measurement_mrid.query_index, self._mrid_or_none(remote_source.measurement))

        return self._save_remote_point(table, insert, remote_source, "remote source")

    #############################################
    # IEC61970 Base Wires Generation Production #
    #############################################

    def save_battery_unit(self, battery_unit: BatteryUnit) -> bool:
        """
        Save the :class:`BatteryUnit` fields to :class:`TableBatteryUnits`.

        :param battery_unit: The :class:`BatteryUnit` instance to write to the database.
        :return: True if the :class:`BatteryUnit` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableBatteryUnits)
        insert = self._database_tables.get_insert(TableBatteryUnits)

        insert.add_value(table.battery_state.query_index, battery_unit.battery_state.short_name)
        insert.add_value(table.rated_e.query_index, battery_unit.rated_e)
        insert.add_value(table.stored_e.query_index, battery_unit.stored_e)

        return self._save_power_electronics_unit(table, insert, battery_unit, "battery unit")

    def save_photo_voltaic_unit(self, photo_voltaic_unit: PhotoVoltaicUnit) -> bool:
        """
        Save the :class:`PhotoVoltaicUnit` fields to :class:`TablePhotoVoltaicUnits`.

        :param photo_voltaic_unit: The :class:`PhotoVoltaicUnit` instance to write to the database.
        :return: True if the :class:`PhotoVoltaicUnit` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TablePhotoVoltaicUnits)
        insert = self._database_tables.get_insert(TablePhotoVoltaicUnits)

        return self._save_power_electronics_unit(table, insert, photo_voltaic_unit, "photo voltaic unit")

    def _save_power_electronics_unit(
        self,
        table: TablePowerElectronicsUnits,
        insert: PreparedStatement,
        power_electronics_unit: PowerElectronicsUnit,
        description: str
    ) -> bool:
        insert.add_value(table.power_electronics_connection_mrid.query_index, self._mrid_or_none(power_electronics_unit.power_electronics_connection))
        insert.add_value(table.max_p.query_index, power_electronics_unit.max_p)
        insert.add_value(table.min_p.query_index, power_electronics_unit.min_p)

        return self._save_equipment(table, insert, power_electronics_unit, description)

    def save_power_electronics_wind_unit(self, power_electronics_wind_unit: PowerElectronicsWindUnit) -> bool:
        """
        Save the :class:`PowerElectronicsWindUnit` fields to :class:`TablePowerElectronicsWindUnits`.

        :param power_electronics_wind_unit: The :class:`PowerElectronicsWindUnit` instance to write to the database.
        :return: True if the :class:`PowerElectronicsWindUnit` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TablePowerElectronicsWindUnits)
        insert = self._database_tables.get_insert(TablePowerElectronicsWindUnits)

        return self._save_power_electronics_unit(table, insert, power_electronics_wind_unit, "power electronics wind unit")

    #######################
    # IEC61970 Base Wires #
    #######################

    def save_ac_line_segment(self, ac_line_segment: AcLineSegment) -> bool:
        """
        Save the :class:`AcLineSegment` fields to :class:`TableAcLineSegments`.

        :param ac_line_segment: The :class:`AcLineSegment` instance to write to the database.
        :return: True if the :class:`AcLineSegment` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableAcLineSegments)
        insert = self._database_tables.get_insert(TableAcLineSegments)

        insert.add_value(
            table.per_length_sequence_impedance_mrid.query_index,
            self._mrid_or_none(ac_line_segment.per_length_sequence_impedance)
        )

        return self._save_conductor(table, insert, ac_line_segment, "AC line segment")

    def save_breaker(self, breaker: Breaker) -> bool:
        """
        Save the :class:`Breaker` fields to :class:`TableBreakers`.

        :param breaker: The :class:`Breaker` instance to write to the database.
        :return: True if the :class:`Breaker` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableBreakers)
        insert = self._database_tables.get_insert(TableBreakers)

        insert.add_value(table.in_transit_time.query_index, breaker.in_transit_time)

        return self._save_protected_switch(table, insert, breaker, "breaker")

    def save_busbar_section(self, busbar_section: BusbarSection) -> bool:
        """
        Save the :class:`BusbarSection` fields to :class:`TableBusbarSections`.

        :param busbar_section: The :class:`BusbarSection` instance to write to the database.
        :return: True if the :class:`BusbarSection` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableBusbarSections)
        insert = self._database_tables.get_insert(TableBusbarSections)

        return self._save_connector(table, insert, busbar_section, "busbar section")

    def _save_conductor(self, table: TableConductors, insert: PreparedStatement, conductor: Conductor, description: str) -> bool:
        insert.add_value(table.length.query_index, conductor.length)
        insert.add_value(table.design_temperature.query_index, conductor.design_temperature)
        insert.add_value(table.design_rating.query_index, conductor.design_rating)
        insert.add_value(table.wire_info_mrid.query_index, self._mrid_or_none(conductor.wire_info))

        return self._save_conducting_equipment(table, insert, conductor, description)

    def _save_connector(self, table: TableConnectors, insert: PreparedStatement, connector: Connector, description: str) -> bool:
        return self._save_conducting_equipment(table, insert, connector, description)

    def save_disconnector(self, disconnector: Disconnector) -> bool:
        """
        Save the :class:`Disconnector` fields to :class:`TableDisconnectors`.

        :param disconnector: The :class:`Disconnector` instance to write to the database.
        :return: True if the :class:`Disconnector` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableDisconnectors)
        insert = self._database_tables.get_insert(TableDisconnectors)

        return self._save_switch(table, insert, disconnector, "disconnector")

    def _save_earth_fault_compensator(
        self,
        table: TableEarthFaultCompensators,
        insert: PreparedStatement,
        earth_fault_compensator: EarthFaultCompensator,
        description: str
    ) -> bool:
        insert.add_value(table.r.query_index, earth_fault_compensator.r)

        return self._save_conducting_equipment(table, insert, earth_fault_compensator, description)

    def _save_energy_connection(
        self,
        table: TableEnergyConnections,
        insert: PreparedStatement,
        energy_connection: EnergyConnection,
        description: str
    ) -> bool:
        return self._save_conducting_equipment(table, insert, energy_connection, description)

    def save_energy_consumer(self, energy_consumer: EnergyConsumer) -> bool:
        """
        Save the :class:`EnergyConsumer` fields to :class:`TableEnergyConsumers`.

        :param energy_consumer: The :class:`EnergyConsumer` instance to write to the database.
        :return: True if the :class:`EnergyConsumer` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableEnergyConsumers)
        insert = self._database_tables.get_insert(TableEnergyConsumers)

        insert.add_value(table.customer_count.query_index, energy_consumer.customer_count)
        insert.add_value(table.grounded.query_index, energy_consumer.grounded)
        insert.add_value(table.p.query_index, energy_consumer.p)
        insert.add_value(table.q.query_index, energy_consumer.q)
        insert.add_value(table.p_fixed.query_index, energy_consumer.p_fixed)
        insert.add_value(table.q_fixed.query_index, energy_consumer.q_fixed)
        insert.add_value(table.phase_connection.query_index, energy_consumer.phase_connection.short_name)

        return self._save_energy_connection(table, insert, energy_consumer, "energy consumer")

    def save_energy_consumer_phase(self, energy_consumer_phase: EnergyConsumerPhase) -> bool:
        """
        Save the :class:`EnergyConsumerPhase` fields to :class:`TableEnergyConsumerPhases`.

        :param energy_consumer_phase: The :class:`EnergyConsumerPhase` instance to write to the database.
        :return: True if the :class:`EnergyConsumerPhase` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableEnergyConsumerPhases)
        insert = self._database_tables.get_insert(TableEnergyConsumerPhases)

        insert.add_value(table.energy_consumer_mrid.query_index, self._mrid_or_none(energy_consumer_phase.energy_consumer))
        insert.add_value(table.phase.query_index, energy_consumer_phase.phase.short_name)
        insert.add_value(table.p.query_index, energy_consumer_phase.p)
        insert.add_value(table.q.query_index, energy_consumer_phase.q)
        insert.add_value(table.p_fixed.query_index, energy_consumer_phase.p_fixed)
        insert.add_value(table.q_fixed.query_index, energy_consumer_phase.q_fixed)

        return self._save_power_system_resource(table, insert, energy_consumer_phase, "energy consumer phase")

    def save_energy_source(self, energy_source: EnergySource) -> bool:
        """
        Save the :class:`EnergySource` fields to :class:`TableEnergySources`.

        :param energy_source: The :class:`EnergySource` instance to write to the database.
        :return: True if the :class:`EnergySource` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableEnergySources)
        insert = self._database_tables.get_insert(TableEnergySources)

        insert.add_value(table.active_power.query_index, energy_source.active_power)
        insert.add_value(table.reactive_power.query_index, energy_source.reactive_power)
        insert.add_value(table.voltage_angle.query_index, energy_source.voltage_angle)
        insert.add_value(table.voltage_magnitude.query_index, energy_source.voltage_magnitude)
        insert.add_value(table.p_max.query_index, energy_source.p_max)
        insert.add_value(table.p_min.query_index, energy_source.p_min)
        insert.add_value(table.r.query_index, energy_source.r)
        insert.add_value(table.r0.query_index, energy_source.r0)
        insert.add_value(table.rn.query_index, energy_source.rn)
        insert.add_value(table.x.query_index, energy_source.x)
        insert.add_value(table.x0.query_index, energy_source.x0)
        insert.add_value(table.xn.query_index, energy_source.xn)
        insert.add_value(table.is_external_grid.query_index, energy_source.is_external_grid)
        insert.add_value(table.r_min.query_index, energy_source.r_min)
        insert.add_value(table.rn_min.query_index, energy_source.rn_min)
        insert.add_value(table.r0_min.query_index, energy_source.r0_min)
        insert.add_value(table.x_min.query_index, energy_source.x_min)
        insert.add_value(table.xn_min.query_index, energy_source.xn_min)
        insert.add_value(table.x0_min.query_index, energy_source.x0_min)
        insert.add_value(table.r_max.query_index, energy_source.r_max)
        insert.add_value(table.rn_max.query_index, energy_source.rn_max)
        insert.add_value(table.r0_max.query_index, energy_source.r0_max)
        insert.add_value(table.x_max.query_index, energy_source.x_max)
        insert.add_value(table.xn_max.query_index, energy_source.xn_max)
        insert.add_value(table.x0_max.query_index, energy_source.x0_max)

        return self._save_energy_connection(table, insert, energy_source, "energy source")

    def save_energy_source_phase(self, energy_source_phase: EnergySourcePhase) -> bool:
        """
        Save the :class:`EnergySourcePhase` fields to :class:`TableEnergySourcePhases`.

        :param energy_source_phase: The :class:`EnergySourcePhase` instance to write to the database.
        :return: True if the :class:`EnergySourcePhase` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableEnergySourcePhases)
        insert = self._database_tables.get_insert(TableEnergySourcePhases)

        insert.add_value(table.energy_source_mrid.query_index, self._mrid_or_none(energy_source_phase.energy_source))
        insert.add_value(table.phase.query_index, energy_source_phase.phase.short_name)

        return self._save_power_system_resource(table, insert, energy_source_phase, "energy source phase")

    def save_fuse(self, fuse: Fuse) -> bool:
        """
        Save the :class:`Fuse` fields to :class:`TableFuses`.

        :param fuse: The :class:`Fuse` instance to write to the database.
        :return: True if the :class:`Fuse` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableFuses)
        insert = self._database_tables.get_insert(TableFuses)

        insert.add_value(table.function_mrid.query_index, self._mrid_or_none(fuse.function))

        return self._save_switch(table, insert, fuse, "fuse")

    def save_ground(self, ground: Ground) -> bool:
        """
        Save the :class:`Ground` fields to :class:`TableGrounds`.

        :param ground: The :class:`Ground` instance to write to the database.
        :return: True if the :class:`Ground` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableGrounds)
        insert = self._database_tables.get_insert(TableGrounds)

        return self._save_conducting_equipment(table, insert, ground, "ground")

    def save_ground_disconnector(self, ground_disconnector: GroundDisconnector) -> bool:
        """
        Save the :class:`GroundDisconnector` fields to :class:`TableGroundDisconnectors`.

        :param ground_disconnector: The :class:`GroundDisconnector` instance to write to the database.
        :return: True if the :class:`GroundDisconnector` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableGroundDisconnectors)
        insert = self._database_tables.get_insert(TableGroundDisconnectors)

        return self._save_switch(table, insert, ground_disconnector, "ground disconnector")

    def save_grounding_impedance(self, grounding_impedance: GroundingImpedance) -> bool:
        """
        Save the :class:`GroundingImpedance` fields to :class:`TableGroundingImpedances`.

        :param grounding_impedance: The :class:`GroundingImpedance` instance to write to the database.

        :return: True if the :class:`GroundingImpedance` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableGroundingImpedances)
        insert = self._database_tables.get_insert(TableGroundingImpedances)

        insert.add_value(table.x.query_index, grounding_impedance.x)

        return self._save_earth_fault_compensator(table, insert, grounding_impedance, "ground disconnector")

    def save_jumper(self, jumper: Jumper) -> bool:
        """
        Save the :class:`Jumper` fields to :class:`TableJumpers`.

        :param jumper: The :class:`Jumper` instance to write to the database.
        :return: True if the :class:`Jumper` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableJumpers)
        insert = self._database_tables.get_insert(TableJumpers)

        return self._save_switch(table, insert, jumper, "jumper")

    def save_junction(self, junction: Junction) -> bool:
        """
        Save the :class:`Junction` fields to :class:`TableJunctions`.

        :param junction: The :class:`Junction` instance to write to the database.
        :return: True if the :class:`Junction` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableJunctions)
        insert = self._database_tables.get_insert(TableJunctions)

        return self._save_connector(table, insert, junction, "junction")

    def _save_line(self, table: TableLines, insert: PreparedStatement, line: Line, description: str) -> bool:
        return self._save_equipment_container(table, insert, line, description)

    def save_linear_shunt_compensator(self, linear_shunt_compensator: LinearShuntCompensator) -> bool:
        """
        Save the :class:`LinearShuntCompensator` fields to :class:`TableLinearShuntCompensators`.

        :param linear_shunt_compensator: The :class:`LinearShuntCompensator` instance to write to the database.
        :return: True if the :class:`LinearShuntCompensator` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableLinearShuntCompensators)
        insert = self._database_tables.get_insert(TableLinearShuntCompensators)

        insert.add_value(table.b0_per_section.query_index, linear_shunt_compensator.b0_per_section)
        insert.add_value(table.b_per_section.query_index, linear_shunt_compensator.b_per_section)
        insert.add_value(table.g0_per_section.query_index, linear_shunt_compensator.g0_per_section)
        insert.add_value(table.g_per_section.query_index, linear_shunt_compensator.g_per_section)

        return self._save_shunt_compensator(table, insert, linear_shunt_compensator, "linear shunt compensator")

    def save_load_break_switch(self, load_break_switch: LoadBreakSwitch) -> bool:
        """
        Save the :class:`LoadBreakSwitch` fields to :class:`TableLoadBreakSwitches`.

        :param load_break_switch: The :class:`LoadBreakSwitch` instance to write to the database.
        :return: True if the :class:`LoadBreakSwitch` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableLoadBreakSwitches)
        insert = self._database_tables.get_insert(TableLoadBreakSwitches)

        return self._save_protected_switch(table, insert, load_break_switch, "load break switch")

    def _save_per_length_impedance(
        self,
        table: TablePerLengthImpedances,
        insert: PreparedStatement,
        per_length_impedance: PerLengthImpedance,
        description: str
    ) -> bool:
        return self._save_per_length_line_parameter(table, insert, per_length_impedance, description)

    def _save_per_length_line_parameter(
        self,
        table: TablePerLengthLineParameters,
        insert: PreparedStatement,
        per_length_line_parameter: PerLengthLineParameter,
        description: str
    ) -> bool:
        return self._save_identified_object(table, insert, per_length_line_parameter, description)

    def save_per_length_sequence_impedance(self, per_length_sequence_impedance: PerLengthSequenceImpedance) -> bool:
        """
        Save the :class:`PerLengthSequenceImpedance` fields to :class:`TablePerLengthSequenceImpedances`.

        :param per_length_sequence_impedance: The :class:`PerLengthSequenceImpedance` instance to write to the database.
        :return: True if the :class:`PerLengthSequenceImpedance` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TablePerLengthSequenceImpedances)
        insert = self._database_tables.get_insert(TablePerLengthSequenceImpedances)

        insert.add_value(table.r.query_index, per_length_sequence_impedance.r)
        insert.add_value(table.x.query_index, per_length_sequence_impedance.x)
        insert.add_value(table.r0.query_index, per_length_sequence_impedance.r0)
        insert.add_value(table.x0.query_index, per_length_sequence_impedance.x0)
        insert.add_value(table.bch.query_index, per_length_sequence_impedance.bch)
        insert.add_value(table.gch.query_index, per_length_sequence_impedance.gch)
        insert.add_value(table.b0ch.query_index, per_length_sequence_impedance.b0ch)
        insert.add_value(table.g0ch.query_index, per_length_sequence_impedance.g0ch)

        return self._save_per_length_impedance(table, insert, per_length_sequence_impedance, "per length sequence impedance")

    def save_petersen_coil(self, petersen_coil: PetersenCoil) -> bool:
        """
        Save the :class:`PetersenCoil` fields to :class:`TablePetersenCoils`.

        :param petersen_coil: The :class:`PetersenCoil` instance to write to the database.

        :return: True if the :class:`PetersenCoil` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TablePetersenCoils)
        insert = self._database_tables.get_insert(TablePetersenCoils)

        insert.add_value(table.x_ground_nominal.query_index, petersen_coil.x_ground_nominal)

        return self._save_earth_fault_compensator(table, insert, petersen_coil, "petersen coil")

    def save_power_electronics_connection(self, power_electronics_connection: PowerElectronicsConnection) -> bool:
        """
        Save the :class:`PowerElectronicsConnection` fields to :class:`TablePowerElectronicsConnections`.

        :param power_electronics_connection: The :class:`PowerElectronicsConnection` instance to write to the database.
        :return: True if the :class:`PowerElectronicsConnection` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TablePowerElectronicsConnections)
        insert = self._database_tables.get_insert(TablePowerElectronicsConnections)

        insert.add_value(table.max_i_fault.query_index, power_electronics_connection.max_i_fault)
        insert.add_value(table.max_q.query_index, power_electronics_connection.max_q)
        insert.add_value(table.min_q.query_index, power_electronics_connection.min_q)
        insert.add_value(table.p.query_index, power_electronics_connection.p)
        insert.add_value(table.q.query_index, power_electronics_connection.q)
        insert.add_value(table.rated_s.query_index, power_electronics_connection.rated_s)
        insert.add_value(table.rated_u.query_index, power_electronics_connection.rated_u)
        insert.add_value(table.inverter_standard.query_index, power_electronics_connection.inverter_standard)
        insert.add_value(table.sustain_op_overvolt_limit.query_index, power_electronics_connection.sustain_op_overvolt_limit)
        insert.add_value(table.stop_at_over_freq.query_index, power_electronics_connection.stop_at_over_freq)
        insert.add_value(table.stop_at_under_freq.query_index, power_electronics_connection.stop_at_under_freq)
        insert.add_value(table.inv_volt_watt_resp_mode.query_index, power_electronics_connection.inv_volt_watt_resp_mode)
        insert.add_value(table.inv_watt_resp_v1.query_index, power_electronics_connection.inv_watt_resp_v1)
        insert.add_value(table.inv_watt_resp_v2.query_index, power_electronics_connection.inv_watt_resp_v2)
        insert.add_value(table.inv_watt_resp_v3.query_index, power_electronics_connection.inv_watt_resp_v3)
        insert.add_value(table.inv_watt_resp_v4.query_index, power_electronics_connection.inv_watt_resp_v4)
        insert.add_value(table.inv_watt_resp_p_at_v1.query_index, power_electronics_connection.inv_watt_resp_p_at_v1)
        insert.add_value(table.inv_watt_resp_p_at_v2.query_index, power_electronics_connection.inv_watt_resp_p_at_v2)
        insert.add_value(table.inv_watt_resp_p_at_v3.query_index, power_electronics_connection.inv_watt_resp_p_at_v3)
        insert.add_value(table.inv_watt_resp_p_at_v4.query_index, power_electronics_connection.inv_watt_resp_p_at_v4)
        insert.add_value(table.inv_volt_var_resp_mode.query_index, power_electronics_connection.inv_volt_var_resp_mode)
        insert.add_value(table.inv_var_resp_v1.query_index, power_electronics_connection.inv_var_resp_v1)
        insert.add_value(table.inv_var_resp_v2.query_index, power_electronics_connection.inv_var_resp_v2)
        insert.add_value(table.inv_var_resp_v3.query_index, power_electronics_connection.inv_var_resp_v3)
        insert.add_value(table.inv_var_resp_v4.query_index, power_electronics_connection.inv_var_resp_v4)
        insert.add_value(table.inv_var_resp_q_at_v1.query_index, power_electronics_connection.inv_var_resp_q_at_v1)
        insert.add_value(table.inv_var_resp_q_at_v2.query_index, power_electronics_connection.inv_var_resp_q_at_v2)
        insert.add_value(table.inv_var_resp_q_at_v3.query_index, power_electronics_connection.inv_var_resp_q_at_v3)
        insert.add_value(table.inv_var_resp_q_at_v4.query_index, power_electronics_connection.inv_var_resp_q_at_v4)
        insert.add_value(table.inv_reactive_power_mode.query_index, power_electronics_connection.inv_reactive_power_mode)
        insert.add_value(table.inv_fix_reactive_power.query_index, power_electronics_connection.inv_fix_reactive_power)

        return self._save_regulating_cond_eq(table, insert, power_electronics_connection, "power electronics connection")

    def save_power_electronics_connection_phase(self, power_electronics_connection_phase: PowerElectronicsConnectionPhase) -> bool:
        """
        Save the :class:`PowerElectronicsConnectionPhase` fields to :class:`TablePowerElectronicsConnectionPhases`.

        :param power_electronics_connection_phase: The :class:`PowerElectronicsConnectionPhase` instance to write to the database.
        :return: True if the :class:`PowerElectronicsConnectionPhase` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TablePowerElectronicsConnectionPhases)
        insert = self._database_tables.get_insert(TablePowerElectronicsConnectionPhases)

        insert.add_value(
            table.power_electronics_connection_mrid.query_index,
            self._mrid_or_none(power_electronics_connection_phase.power_electronics_connection)
        )
        insert.add_value(table.p.query_index, power_electronics_connection_phase.p)
        insert.add_value(table.phase.query_index, power_electronics_connection_phase.phase.short_name)
        insert.add_value(table.q.query_index, power_electronics_connection_phase.q)

        return self._save_power_system_resource(table, insert, power_electronics_connection_phase, "power electronics connection phase")

    def save_power_transformer(self, power_transformer: PowerTransformer) -> bool:
        """
        Save the :class:`PowerTransformer` fields to :class:`TablePowerTransformers`.

        :param power_transformer: The :class:`PowerTransformer` instance to write to the database.
        :return: True if the :class:`PowerTransformer` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TablePowerTransformers)
        insert = self._database_tables.get_insert(TablePowerTransformers)

        insert.add_value(table.vector_group.query_index, power_transformer.vector_group.short_name)
        insert.add_value(table.transformer_utilisation.query_index, power_transformer.transformer_utilisation)
        insert.add_value(table.construction_kind.query_index, power_transformer.construction_kind.short_name)
        insert.add_value(table.function.query_index, power_transformer.function.short_name)
        insert.add_value(table.power_transformer_info_mrid.query_index, self._mrid_or_none(power_transformer.power_transformer_info))

        return self._save_conducting_equipment(table, insert, power_transformer, "power transformer")

    def save_power_transformer_end(self, power_transformer_end: PowerTransformerEnd) -> bool:
        """
        Save the :class:`PowerTransformerEnd` fields to :class:`TablePowerTransformerEnds`.

        :param power_transformer_end: The :class:`PowerTransformerEnd` instance to write to the database.
        :return: True if the :class:`PowerTransformerEnd` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TablePowerTransformerEnds)
        insert = self._database_tables.get_insert(TablePowerTransformerEnds)

        insert.add_value(table.power_transformer_mrid.query_index, self._mrid_or_none(power_transformer_end.power_transformer))
        insert.add_value(table.connection_kind.query_index, power_transformer_end.connection_kind.short_name)
        insert.add_value(table.phase_angle_clock.query_index, power_transformer_end.phase_angle_clock)
        insert.add_value(table.b.query_index, power_transformer_end.b)
        insert.add_value(table.b0.query_index, power_transformer_end.b0)
        insert.add_value(table.g.query_index, power_transformer_end.g)
        insert.add_value(table.g0.query_index, power_transformer_end.g0)
        insert.add_value(table.r.query_index, power_transformer_end.r)
        insert.add_value(table.r0.query_index, power_transformer_end.r0)
        insert.add_value(table.rated_u.query_index, power_transformer_end.rated_u)
        insert.add_value(table.x.query_index, power_transformer_end.x)
        insert.add_value(table.x0.query_index, power_transformer_end.x0)

        ratings_table = self._database_tables.get_table(TablePowerTransformerEndRatings)
        ratings_insert = self._database_tables.get_insert(TablePowerTransformerEndRatings)
        for it in power_transformer_end.s_ratings:
            ratings_insert.add_value(ratings_table.power_transformer_end_mrid.query_index, power_transformer_end.mrid)
            ratings_insert.add_value(ratings_table.cooling_type.query_index, it.cooling_type.short_name)
            ratings_insert.add_value(ratings_table.rated_s.query_index, it.rated_s)
            self._try_execute_single_update(ratings_insert, "transformer end ratedS")

        return self._save_transformer_end(table, insert, power_transformer_end, "power transformer end")

    def _save_protected_switch(self, table: TableProtectedSwitches, insert: PreparedStatement, protected_switch: ProtectedSwitch, description: str) -> bool:
        insert.add_value(table.breaking_capacity.query_index, protected_switch.breaking_capacity)

        return self._save_switch(table, insert, protected_switch, description)

    def save_ratio_tap_changer(self, ratio_tap_changer: RatioTapChanger) -> bool:
        """
        Save the :class:`RatioTapChanger` fields to :class:`TableRatioTapChangers`.

        :param ratio_tap_changer: The :class:`RatioTapChanger` instance to write to the database.
        :return: True if the :class:`RatioTapChanger` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableRatioTapChangers)
        insert = self._database_tables.get_insert(TableRatioTapChangers)

        insert.add_value(table.transformer_end_mrid.query_index, self._mrid_or_none(ratio_tap_changer.transformer_end))
        insert.add_value(table.step_voltage_increment.query_index, ratio_tap_changer.step_voltage_increment)

        return self._save_tap_changer(table, insert, ratio_tap_changer, "ratio tap changer")

    def save_reactive_capability_curve(self, reactive_capability_curve: ReactiveCapabilityCurve) -> bool:
        """
        Save the :class:`ReactiveCapabilityCurve` fields to :class:`TableReactiveCapabilityCurves`.

        :param reactive_capability_curve: The :class:`ReactiveCapabilityCurve` instance to write to the database.

        :return: True if the :class:`ReactiveCapabilityCurve` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableReactiveCapabilityCurves)
        insert = self._database_tables.get_insert(TableReactiveCapabilityCurves)

        return self._save_curve(table, insert, reactive_capability_curve, "reactive capability curve")

    def save_recloser(self, recloser: Recloser) -> bool:
        """
        Save the :class:`Recloser` fields to :class:`TableReclosers`.

        :param recloser: The :class:`Recloser` instance to write to the database.
        :return: True if the :class:`Recloser` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableReclosers)
        insert = self._database_tables.get_insert(TableReclosers)

        return self._save_protected_switch(table, insert, recloser, "recloser")

    def _save_regulating_cond_eq(
        self,
        table: TableRegulatingCondEq,
        insert: PreparedStatement,
        regulating_cond_eq: RegulatingCondEq,
        description: str
    ) -> bool:
        insert.add_value(table.control_enabled.query_index, regulating_cond_eq.control_enabled)
        insert.add_value(table.regulating_control_mrid.query_index, self._mrid_or_none(regulating_cond_eq.regulating_control))

        return self._save_energy_connection(table, insert, regulating_cond_eq, description)

    def _save_regulating_control(
        self,
        table: TableRegulatingControls,
        insert: PreparedStatement,
        regulating_control: RegulatingControl,
        description: str
    ) -> bool:
        insert.add_value(table.discrete.query_index, regulating_control.discrete)
        insert.add_value(table.mode.query_index, regulating_control.mode.short_name)
        insert.add_value(table.monitored_phase.query_index, regulating_control.monitored_phase.short_name)
        insert.add_value(table.target_deadband.query_index, regulating_control.target_deadband)
        insert.add_value(table.target_value.query_index, regulating_control.target_value)
        insert.add_value(table.enabled.query_index, regulating_control.enabled)
        insert.add_value(table.max_allowed_target_value.query_index, regulating_control.max_allowed_target_value)
        insert.add_value(table.min_allowed_target_value.query_index, regulating_control.min_allowed_target_value)
        insert.add_value(table.rated_current.query_index, regulating_control.rated_current)
        insert.add_value(table.terminal_mrid.query_index, self._mrid_or_none(regulating_control.terminal))

        return self._save_power_system_resource(table, insert, regulating_control, description)

    def _save_rotating_machine(
        self,
        table: TableRotatingMachines,
        insert: PreparedStatement,
        rotating_machine: RotatingMachine,
        description: str
    ) -> bool:
        insert.add_value(table.rated_power_factor.query_index, rotating_machine.rated_power_factor)
        insert.add_value(table.rated_s.query_index, rotating_machine.rated_s)
        insert.add_value(table.rated_u.query_index, rotating_machine.rated_u)
        insert.add_value(table.p.query_index, rotating_machine.p)
        insert.add_value(table.q.query_index, rotating_machine.q)

        return self._save_regulating_cond_eq(table, insert, rotating_machine, description)

    def save_series_compensator(self, series_compensator: SeriesCompensator) -> bool:
        """
        Save the :class:`SeriesCompensator` fields to :class:`TableSeriesCompensators`.

        :param series_compensator: The :class:`SeriesCompensator` instance to write to the database.
        :return: True if the :class:`SeriesCompensator` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableSeriesCompensators)
        insert = self._database_tables.get_insert(TableSeriesCompensators)

        insert.add_value(table.r.query_index, series_compensator.r)
        insert.add_value(table.r0.query_index, series_compensator.r0)
        insert.add_value(table.x.query_index, series_compensator.x)
        insert.add_value(table.x0.query_index, series_compensator.x0)
        insert.add_value(table.varistor_rated_current.query_index, series_compensator.varistor_rated_current)
        insert.add_value(table.varistor_voltage_threshold.query_index, series_compensator.varistor_voltage_threshold)

        return self._save_conducting_equipment(table, insert, series_compensator, "series compensator")

    def _save_shunt_compensator(
        self,
        table: TableShuntCompensators,
        insert: PreparedStatement,
        shunt_compensator: ShuntCompensator,
        description: str
    ) -> bool:
        insert.add_value(table.shunt_compensator_info_mrid.query_index, self._mrid_or_none(shunt_compensator.asset_info))
        insert.add_value(table.grounded.query_index, shunt_compensator.grounded)
        insert.add_value(table.nom_u.query_index, shunt_compensator.nom_u)
        insert.add_value(table.phase_connection.query_index, shunt_compensator.phase_connection.short_name)
        insert.add_value(table.sections.query_index, shunt_compensator.sections)

        return self._save_regulating_cond_eq(table, insert, shunt_compensator, description)

    def _save_switch(self, table: TableSwitches, insert: PreparedStatement, switch: Switch, description: str) -> bool:
        # noinspection PyProtectedMember
        insert.add_value(table.normal_open.query_index, switch._normally_open)
        # noinspection PyProtectedMember
        insert.add_value(table.open.query_index, switch._open)
        insert.add_value(table.rated_current.query_index, switch.rated_current)
        insert.add_value(table.switch_info_mrid.query_index, self._mrid_or_none(switch.switch_info))

        return self._save_conducting_equipment(table, insert, switch, description)

    def save_synchronous_machine(self, synchronous_machine: SynchronousMachine) -> bool:
        """
        Save the :class:`SynchronousMachine` fields to :class:`TableSynchronousMachines`.

        :param synchronous_machine: The :class:`SynchronousMachine` instance to write to the database.

        @return true if the :class:`SynchronousMachine` was successfully written to the database, otherwise false.
        @throws SQLException For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableSynchronousMachines)
        insert = self._database_tables.get_insert(TableSynchronousMachines)

        insert.add_value(table.base_q.query_index, synchronous_machine.base_q)
        insert.add_value(table.condenser_p.query_index, synchronous_machine.condenser_p)
        insert.add_value(table.earthing.query_index, synchronous_machine.earthing)
        insert.add_value(table.earthing_star_point_r.query_index, synchronous_machine.earthing_star_point_r)
        insert.add_value(table.earthing_star_point_x.query_index, synchronous_machine.earthing_star_point_x)
        insert.add_value(table.ikk.query_index, synchronous_machine.ikk)
        insert.add_value(table.max_q.query_index, synchronous_machine.max_q)
        insert.add_value(table.max_u.query_index, synchronous_machine.max_u)
        insert.add_value(table.min_q.query_index, synchronous_machine.min_q)
        insert.add_value(table.min_u.query_index, synchronous_machine.min_u)
        insert.add_value(table.mu.query_index, synchronous_machine.mu)
        insert.add_value(table.r.query_index, synchronous_machine.r)
        insert.add_value(table.r0.query_index, synchronous_machine.r0)
        insert.add_value(table.r2.query_index, synchronous_machine.r2)
        insert.add_value(table.sat_direct_subtrans_x.query_index, synchronous_machine.sat_direct_subtrans_x)
        insert.add_value(table.sat_direct_sync_x.query_index, synchronous_machine.sat_direct_sync_x)
        insert.add_value(table.sat_direct_trans_x.query_index, synchronous_machine.sat_direct_trans_x)
        insert.add_value(table.x0.query_index, synchronous_machine.x0)
        insert.add_value(table.x2.query_index, synchronous_machine.x2)
        insert.add_value(table.type.query_index, synchronous_machine.type.short_name)
        insert.add_value(table.operating_mode.query_index, synchronous_machine.operating_mode.short_name)

        status = True
        for rcc in synchronous_machine.curves:
            status = status and self._save_synchronous_machine_to_reactive_capability_curve_association(synchronous_machine, rcc)

        return status and self._save_rotating_machine(table, insert, synchronous_machine, "synchronous machine")

    def _save_tap_changer(self, table: TableTapChangers, insert: PreparedStatement, tap_changer: TapChanger, description: str) -> bool:
        insert.add_value(table.control_enabled.query_index, tap_changer.control_enabled)
        insert.add_value(table.high_step.query_index, tap_changer.high_step)
        insert.add_value(table.low_step.query_index, tap_changer.low_step)
        insert.add_value(table.neutral_step.query_index, tap_changer.neutral_step)
        insert.add_value(table.neutral_u.query_index, tap_changer.neutral_u)
        insert.add_value(table.normal_step.query_index, tap_changer.normal_step)
        insert.add_value(table.step.query_index, tap_changer.step)
        insert.add_value(table.tap_changer_control_mrid.query_index, self._mrid_or_none(tap_changer.tap_changer_control))

        return self._save_power_system_resource(table, insert, tap_changer, description)

    def save_tap_changer_control(self, tap_changer_control: TapChangerControl) -> bool:
        """
        Save the :class:`TapChangerControl` fields to :class:`TableTapChangerControls`.

        :param tap_changer_control: The :class:`TapChangerControl` instance to write to the database.
        :return: True if the :class:`TapChangerControl` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableTapChangerControls)
        insert = self._database_tables.get_insert(TableTapChangerControls)

        insert.add_value(table.limit_voltage.query_index, tap_changer_control.limit_voltage)
        insert.add_value(table.line_drop_compensation.query_index, tap_changer_control.line_drop_compensation)
        insert.add_value(table.line_drop_r.query_index, tap_changer_control.line_drop_r)
        insert.add_value(table.line_drop_x.query_index, tap_changer_control.line_drop_x)
        insert.add_value(table.reverse_line_drop_r.query_index, tap_changer_control.reverse_line_drop_r)
        insert.add_value(table.reverse_line_drop_x.query_index, tap_changer_control.reverse_line_drop_x)
        insert.add_value(table.forward_ldc_blocking.query_index, tap_changer_control.forward_ldc_blocking)
        insert.add_value(table.time_delay.query_index, tap_changer_control.time_delay)
        insert.add_value(table.co_generation_enabled.query_index, tap_changer_control.co_generation_enabled)

        return self._save_regulating_control(table, insert, tap_changer_control, "tap changer control")

    def _save_transformer_end(
        self,
        table: TableTransformerEnds,
        insert: PreparedStatement,
        transformer_end: TransformerEnd,
        description: str
    ) -> bool:
        insert.add_value(table.end_number.query_index, transformer_end.end_number)
        insert.add_value(table.terminal_mrid.query_index, self._mrid_or_none(transformer_end.terminal))
        insert.add_value(table.base_voltage_mrid.query_index, self._mrid_or_none(transformer_end.base_voltage))
        insert.add_value(table.grounded.query_index, transformer_end.grounded)
        insert.add_value(table.r_ground.query_index, transformer_end.r_ground)
        insert.add_value(table.x_ground.query_index, transformer_end.x_ground)
        insert.add_value(table.star_impedance_mrid.query_index, self._mrid_or_none(transformer_end.star_impedance))

        return self._save_identified_object(table, insert, transformer_end, description)

    def save_transformer_star_impedance(self, transformer_star_impedance: TransformerStarImpedance) -> bool:
        """
        Save the :class:`TransformerStarImpedance` fields to :class:`TableTransformerStarImpedances`.

        :param transformer_star_impedance: The :class:`TransformerStarImpedance` instance to write to the database.
        :return: True if the :class:`TransformerStarImpedance` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableTransformerStarImpedances)
        insert = self._database_tables.get_insert(TableTransformerStarImpedances)

        insert.add_value(table.r.query_index, transformer_star_impedance.r)
        insert.add_value(table.r0.query_index, transformer_star_impedance.r0)
        insert.add_value(table.x.query_index, transformer_star_impedance.x)
        insert.add_value(table.x0.query_index, transformer_star_impedance.x0)
        insert.add_value(table.transformer_end_info_mrid.query_index, self._mrid_or_none(transformer_star_impedance.transformer_end_info))

        return self._save_identified_object(table, insert, transformer_star_impedance, "transformer star impedance")

    ###############################
    # IEC61970 InfIEC61970 Feeder #
    ###############################

    def save_circuit(self, circuit: Circuit) -> bool:
        """
        Save the :class:`Circuit` fields to :class:`TableCircuits`.

        :param circuit: The :class:`Circuit` instance to write to the database.
        :return: True if the :class:`Circuit` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableCircuits)
        insert = self._database_tables.get_insert(TableCircuits)

        insert.add_value(table.loop_mrid.query_index, self._mrid_or_none(circuit.loop))

        status = True
        for it in circuit.end_substations:
            status = status and self._save_circuit_to_substation_association(circuit, it)
        for it in circuit.end_terminals:
            status = status and self._save_circuit_to_terminal_association(circuit, it)

        return status and self._save_line(table, insert, circuit, "circuit")

    def save_loop(self, loop: Loop) -> bool:
        """
        Save the :class:`Loop` fields to :class:`TableLoops`.

        :param loop: The :class:`Loop` instance to write to the database.
        :return: True if the :class:`Loop` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableLoops)
        insert = self._database_tables.get_insert(TableLoops)

        status = True
        for it in loop.energizing_substations:
            status = status and self._save_loop_to_substation_association(loop, it, LoopSubstationRelationship.SUBSTATION_ENERGIZES_LOOP)
        for it in loop.substations:
            status = status and self._save_loop_to_substation_association(loop, it, LoopSubstationRelationship.LOOP_ENERGIZES_SUBSTATION)

        return status and self._save_identified_object(table, insert, loop, "loop")

    def save_lv_feeder(self, lv_feeder: LvFeeder) -> bool:
        """
        Save the :class:`LvFeeder` fields to :class:`TableLvFeeders`.

        :param lv_feeder: The :class:`LvFeeder` instance to write to the database.
        :return: True if the :class:`LvFeeder` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableLvFeeders)
        insert = self._database_tables.get_insert(TableLvFeeders)

        insert.add_value(table.normal_head_terminal_mrid.query_index, self._mrid_or_none(lv_feeder.normal_head_terminal))

        return self._save_equipment_container(table, insert, lv_feeder, "lv feeder")

    ####################################################
    # IEC61970 infIEC61970 Wires Generation Production #
    ####################################################

    def save_ev_charging_unit(self, ev_charging_unit: EvChargingUnit) -> bool:
        """
        Save the :class:`EvChargingUnit` fields to :class:`TableEvChargingUnits`.

        :param ev_charging_unit: The :class:`EvChargingUnit` instance to write to the database.
        :return: True if the :class:`EvChargingUnit` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableEvChargingUnits)
        insert = self._database_tables.get_insert(TableEvChargingUnits)

        return self._save_power_electronics_unit(table, insert, ev_charging_unit, "ev charging unit")

    ################
    # ASSOCIATIONS #
    ################

    def _save_asset_organisation_role_to_asset_association(self, asset_organisation_role: AssetOrganisationRole, asset: Asset) -> bool:
        table = self._database_tables.get_table(TableAssetOrganisationRolesAssets)
        insert = self._database_tables.get_insert(TableAssetOrganisationRolesAssets)

        insert.add_value(table.asset_organisation_role_mrid.query_index, asset_organisation_role.mrid)
        insert.add_value(table.asset_mrid.query_index, asset.mrid)

        return self._try_execute_single_update(insert, "asset organisation role to asset association")

    def _save_circuit_to_substation_association(self, circuit: Circuit, substation: Substation) -> bool:
        table = self._database_tables.get_table(TableCircuitsSubstations)
        insert = self._database_tables.get_insert(TableCircuitsSubstations)

        insert.add_value(table.circuit_mrid.query_index, circuit.mrid)
        insert.add_value(table.substation_mrid.query_index, substation.mrid)

        return self._try_execute_single_update(insert, "circuit to substation association")

    def _save_circuit_to_terminal_association(self, circuit: Circuit, terminal: Terminal) -> bool:
        table = self._database_tables.get_table(TableCircuitsTerminals)
        insert = self._database_tables.get_insert(TableCircuitsTerminals)

        insert.add_value(table.circuit_mrid.query_index, circuit.mrid)
        insert.add_value(table.terminal_mrid.query_index, terminal.mrid)

        return self._try_execute_single_update(insert, "circuit to terminal association")

    def _save_equipment_to_equipment_container_association(self, equipment: Equipment, equipment_container: EquipmentContainer) -> bool:
        table = self._database_tables.get_table(TableEquipmentEquipmentContainers)
        insert = self._database_tables.get_insert(TableEquipmentEquipmentContainers)

        insert.add_value(table.equipment_mrid.query_index, equipment.mrid)
        insert.add_value(table.equipment_container_mrid.query_index, equipment_container.mrid)

        return self._try_execute_single_update(insert, "equipment to equipment container association")

    def _save_equipment_to_operational_restriction_association(self, equipment: Equipment, operational_restriction: OperationalRestriction) -> bool:
        table = self._database_tables.get_table(TableEquipmentOperationalRestrictions)
        insert = self._database_tables.get_insert(TableEquipmentOperationalRestrictions)

        insert.add_value(table.equipment_mrid.query_index, equipment.mrid)
        insert.add_value(table.operational_restriction_mrid.query_index, operational_restriction.mrid)

        return self._try_execute_single_update(insert, "equipment to operational restriction association")

    def _save_equipment_to_usage_point_association(self, equipment: Equipment, usage_point: UsagePoint) -> bool:
        table = self._database_tables.get_table(TableEquipmentUsagePoints)
        insert = self._database_tables.get_insert(TableEquipmentUsagePoints)

        insert.add_value(table.equipment_mrid.query_index, equipment.mrid)
        insert.add_value(table.usage_point_mrid.query_index, usage_point.mrid)

        return self._try_execute_single_update(insert, "equipment to usage point association")

    def _save_loop_to_substation_association(self, loop: Loop, substation: Substation, relationship: LoopSubstationRelationship) -> bool:
        table = self._database_tables.get_table(TableLoopsSubstations)
        insert = self._database_tables.get_insert(TableLoopsSubstations)

        insert.add_value(table.loop_mrid.query_index, loop.mrid)
        insert.add_value(table.substation_mrid.query_index, substation.mrid)
        insert.add_value(table.relationship.query_index, relationship.short_name)

        return self._try_execute_single_update(insert, "loop to substation association")

    def _save_protection_relay_function_to_protected_switch_association(
        self,
        protection_relay_function: ProtectionRelayFunction,
        protected_switch: ProtectedSwitch
    ) -> bool:
        table = self._database_tables.get_table(TableProtectionRelayFunctionsProtectedSwitches)
        insert = self._database_tables.get_insert(TableProtectionRelayFunctionsProtectedSwitches)

        insert.add_value(table.protection_relay_function_mrid.query_index, protection_relay_function.mrid)
        insert.add_value(table.protected_switch_mrid.query_index, protected_switch.mrid)

        return self._try_execute_single_update(insert, "protection relay function to protected switch association")

    def _save_protection_relay_function_to_sensor_association(self, protection_relay_function: ProtectionRelayFunction, sensor: Sensor) -> bool:
        table = self._database_tables.get_table(TableProtectionRelayFunctionsSensors)
        insert = self._database_tables.get_insert(TableProtectionRelayFunctionsSensors)

        insert.add_value(table.protection_relay_function_mrid.query_index, protection_relay_function.mrid)
        insert.add_value(table.sensor_mrid.query_index, sensor.mrid)

        return self._try_execute_single_update(insert, "protection relay function to sensor association")

    def _save_protection_relay_scheme_to_protection_relay_function_association(
        self,
        protection_relay_scheme: ProtectionRelayScheme,
        protection_relay_function: ProtectionRelayFunction
    ) -> bool:
        table = self._database_tables.get_table(TableProtectionRelaySchemesProtectionRelayFunctions)
        insert = self._database_tables.get_insert(TableProtectionRelaySchemesProtectionRelayFunctions)

        insert.add_value(table.protection_relay_scheme_mrid.query_index, protection_relay_scheme.mrid)
        insert.add_value(table.protection_relay_function_mrid.query_index, protection_relay_function.mrid)

        return self._try_execute_single_update(insert, "protection relay function to protection relay function association")

    def _save_synchronous_machine_to_reactive_capability_curve_association(
        self,
        synchronous_machine: SynchronousMachine,
        reactive_capability_curve: ReactiveCapabilityCurve
    ) -> bool:
        table = self._database_tables.get_table(TableSynchronousMachinesReactiveCapabilityCurves)
        insert = self._database_tables.get_insert(TableSynchronousMachinesReactiveCapabilityCurves)

        insert.add_value(table.synchronous_machine_mrid.query_index, synchronous_machine.mrid)
        insert.add_value(table.reactive_capability_curve_mrid.query_index, reactive_capability_curve.mrid)

        return self._try_execute_single_update(insert, "usage point to end device association")

    def _save_usage_point_to_end_device_association(self, usage_point: UsagePoint, end_device: EndDevice) -> bool:
        table = self._database_tables.get_table(TableUsagePointsEndDevices)
        insert = self._database_tables.get_insert(TableUsagePointsEndDevices)

        insert.add_value(table.usage_point_mrid.query_index, usage_point.mrid)
        insert.add_value(table.end_device_mrid.query_index, end_device.mrid)

        return self._try_execute_single_update(insert, "usage point to end device association")

    @staticmethod
    def _should_export_container_contents(ec: EquipmentContainer) -> bool:
        return isinstance(ec, Site) or isinstance(ec, Substation) or isinstance(ec, Circuit)
