#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Generator

from zepben.evolve.database.sqlite.common.base_database_tables import BaseDatabaseTables
from zepben.evolve.database.sqlite.tables.associations.table_asset_organisation_roles_assets import *
from zepben.evolve.database.sqlite.tables.associations.table_assets_power_system_resources import TableAssetsPowerSystemResources
from zepben.evolve.database.sqlite.tables.associations.table_battery_units_battery_controls import *
from zepben.evolve.database.sqlite.tables.associations.table_circuits_substations import *
from zepben.evolve.database.sqlite.tables.associations.table_circuits_terminals import *
from zepben.evolve.database.sqlite.tables.associations.table_end_devices_end_device_functions import *
from zepben.evolve.database.sqlite.tables.associations.table_equipment_equipment_containers import *
from zepben.evolve.database.sqlite.tables.associations.table_equipment_operational_restrictions import *
from zepben.evolve.database.sqlite.tables.associations.table_equipment_usage_points import *
from zepben.evolve.database.sqlite.tables.associations.table_loops_substations import *
from zepben.evolve.database.sqlite.tables.associations.table_protection_relay_functions_protected_switches import *
from zepben.evolve.database.sqlite.tables.associations.table_protection_relay_functions_sensors import *
from zepben.evolve.database.sqlite.tables.associations.table_protection_relay_schemes_protection_relay_functions import *
from zepben.evolve.database.sqlite.tables.associations.table_synchronous_machines_reactive_capability_curves import \
    TableSynchronousMachinesReactiveCapabilityCurves
from zepben.evolve.database.sqlite.tables.associations.table_usage_points_end_devices import *
from zepben.evolve.database.sqlite.tables.extensions.iec61968.table_pan_demand_response_functions import TablePanDemandResponseFunctions
from zepben.evolve.database.sqlite.tables.extensions.iec61970.table_battery_controls import TableBatteryControls
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_cable_info import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_no_load_tests import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_open_circuit_tests import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_overhead_wire_info import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_power_transformer_info import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_short_circuit_tests import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_shunt_compensator_info import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_switch_info import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_transformer_end_info import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_transformer_tank_info import *
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_owners import *
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_poles import *
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_streetlights import *
from zepben.evolve.database.sqlite.tables.iec61968.common.table_location_street_addresses import *
from zepben.evolve.database.sqlite.tables.iec61968.common.table_locations import *
from zepben.evolve.database.sqlite.tables.iec61968.common.table_organisations import *
from zepben.evolve.database.sqlite.tables.iec61968.common.table_position_points import *
from zepben.evolve.database.sqlite.tables.iec61968.infiec61968.infassetinfo.table_current_transformer_info import *
from zepben.evolve.database.sqlite.tables.iec61968.infiec61968.infassetinfo.table_potential_transformer_info import *
from zepben.evolve.database.sqlite.tables.iec61968.infiec61968.infassetinfo.table_reclose_delays import *
from zepben.evolve.database.sqlite.tables.iec61968.infiec61968.infassetinfo.table_relay_info import *
from zepben.evolve.database.sqlite.tables.iec61968.metering.table_meters import *
from zepben.evolve.database.sqlite.tables.iec61968.metering.table_usage_points import *
from zepben.evolve.database.sqlite.tables.iec61968.operations.table_operational_restrictions import *
from zepben.evolve.database.sqlite.tables.iec61970.base.auxiliaryequipment.table_current_transformers import *
from zepben.evolve.database.sqlite.tables.iec61970.base.auxiliaryequipment.table_fault_indicators import *
from zepben.evolve.database.sqlite.tables.iec61970.base.auxiliaryequipment.table_potential_transformers import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_base_voltages import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_connectivity_nodes import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_curve_data import TableCurveData
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_feeders import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_geographical_regions import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_sites import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_sub_geographical_regions import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_substations import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_terminals import *
from zepben.evolve.database.sqlite.tables.iec61970.base.equivalents.table_equivalent_branches import *
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_accumulators import *
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_analogs import *
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_controls import *
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_discretes import *
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_current_relays import *
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_distance_relays import *
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_protection_relay_function_thresholds import *
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_protection_relay_function_time_limits import *
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_protection_relay_schemes import *
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_protection_relay_systems import *
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_voltage_relays import *
from zepben.evolve.database.sqlite.tables.iec61970.base.scada.table_remote_controls import *
from zepben.evolve.database.sqlite.tables.iec61970.base.scada.table_remote_sources import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.generation.production.table_battery_units import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.generation.production.table_photo_voltaic_units import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.generation.production.table_power_electronics_wind_units import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_ac_line_segments import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_breakers import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_busbar_sections import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_clamps import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_cuts import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_disconnectors import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_consumer_phases import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_consumers import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_source_phases import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_sources import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_fuses import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_ground_disconnectors import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_grounding_impedances import TableGroundingImpedances
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_grounds import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_jumpers import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_junctions import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_linear_shunt_compensators import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_load_break_switches import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_per_length_phase_impedances import TablePerLengthPhaseImpedances
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_per_length_sequence_impedances import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_petersen_coils import TablePetersenCoils
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_phase_impedance_data import TablePhaseImpedanceData
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_electronics_connection_phases import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_electronics_connections import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_transformer_end_ratings import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_transformer_ends import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_transformers import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_ratio_tap_changers import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_reactive_capability_curves import TableReactiveCapabilityCurves
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_reclosers import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_series_compensators import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_static_var_compensator import TableStaticVarCompensators
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_synchronous_machines import TableSynchronousMachines
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_tap_changer_controls import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_transformer_star_impedances import *
from zepben.evolve.database.sqlite.tables.iec61970.infiec61970.feeder.table_circuits import *
from zepben.evolve.database.sqlite.tables.iec61970.infiec61970.feeder.table_loops import *
from zepben.evolve.database.sqlite.tables.iec61970.infiec61970.feeder.table_lv_feeders import *
from zepben.evolve.database.sqlite.tables.iec61970.infiec61970.wires.generation.production.table_ev_charging_units import *
from zepben.evolve.database.sqlite.tables.sqlite_table import *

__all__ = ["NetworkDatabaseTables"]


class NetworkDatabaseTables(BaseDatabaseTables):
    """
    The collection of tables for our customer databases.
    """

    @property
    def _included_tables(self) -> Generator[SqliteTable, None, None]:
        for table in super()._included_tables:
            yield table

        yield TableAcLineSegments()
        yield TableAccumulators()
        yield TableAnalogs()
        yield TableAssetOrganisationRolesAssets()
        yield TableAssetsPowerSystemResources()
        yield TableAssetOwners()
        yield TableBaseVoltages()
        yield TableBatteryControls()
        yield TableBatteryUnits()
        yield TableBatteryUnitsBatteryControls()
        yield TableBreakers()
        yield TableBusbarSections()
        yield TableCableInfo()
        yield TableCircuits()
        yield TableCircuitsSubstations()
        yield TableCircuitsTerminals()
        yield TableClamps()
        yield TableConnectivityNodes()
        yield TableControls()
        yield TableCurrentRelays()
        yield TableCurrentTransformerInfo()
        yield TableCurrentTransformers()
        yield TableCurveData()
        yield TableCuts()
        yield TableDisconnectors()
        yield TableDiscretes()
        yield TableDistanceRelays()
        yield TableEndDevicesEndDeviceFunctions()
        yield TableEnergyConsumerPhases()
        yield TableEnergyConsumers()
        yield TableEnergySourcePhases()
        yield TableEnergySources()
        yield TableEquipmentEquipmentContainers()
        yield TableEquipmentOperationalRestrictions()
        yield TableEquipmentUsagePoints()
        yield TableEquivalentBranches()
        yield TableEvChargingUnits()
        yield TableFaultIndicators()
        yield TableFeeders()
        yield TableFuses()
        yield TableGeographicalRegions()
        yield TableGrounds()
        yield TableGroundDisconnectors()
        yield TableGroundingImpedances()
        yield TableJumpers()
        yield TableJunctions()
        yield TableLinearShuntCompensators()
        yield TableLoadBreakSwitches()
        yield TableLocationStreetAddresses()
        yield TableLocations()
        yield TableLoops()
        yield TableLoopsSubstations()
        yield TableLvFeeders()
        yield TableMeters()
        yield TableNoLoadTests()
        yield TableOpenCircuitTests()
        yield TableOperationalRestrictions()
        yield TableOrganisations()
        yield TableOverheadWireInfo()
        yield TablePanDemandResponseFunctions()
        yield TablePerLengthPhaseImpedances()
        yield TablePerLengthSequenceImpedances()
        yield TablePhaseImpedanceData()
        yield TablePetersenCoils()
        yield TablePhotoVoltaicUnits()
        yield TablePoles()
        yield TablePositionPoints()
        yield TablePotentialTransformerInfo()
        yield TablePotentialTransformers()
        yield TablePowerElectronicsConnections()
        yield TablePowerElectronicsConnectionPhases()
        yield TablePowerElectronicsWindUnits()
        yield TablePowerTransformerEnds()
        yield TablePowerTransformerEndRatings()
        yield TablePowerTransformerInfo()
        yield TablePowerTransformers()
        yield TableProtectionRelayFunctionThresholds()
        yield TableProtectionRelayFunctionTimeLimits()
        yield TableProtectionRelayFunctionsProtectedSwitches()
        yield TableProtectionRelayFunctionsSensors()
        yield TableProtectionRelaySchemes()
        yield TableProtectionRelaySchemesProtectionRelayFunctions()
        yield TableProtectionRelaySystems()
        yield TableRatioTapChangers()
        yield TableReactiveCapabilityCurves()
        yield TableReclosers()
        yield TableRecloseDelays()
        yield TableRelayInfo()
        yield TableRemoteControls()
        yield TableRemoteSources()
        yield TableSeriesCompensators()
        yield TableShortCircuitTests()
        yield TableShuntCompensatorInfo()
        yield TableSites()
        yield TableStaticVarCompensators()
        yield TableStreetlights()
        yield TableSubGeographicalRegions()
        yield TableSubstations()
        yield TableSwitchInfo()
        yield TableSynchronousMachines()
        yield TableSynchronousMachinesReactiveCapabilityCurves()
        yield TableTapChangerControls()
        yield TableTerminals()
        yield TableTransformerEndInfo()
        yield TableTransformerStarImpedances()
        yield TableTransformerTankInfo()
        yield TableUsagePoints()
        yield TableUsagePointsEndDevices()
        yield TableVoltageRelays()
