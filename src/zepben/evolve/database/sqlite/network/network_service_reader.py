#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["NetworkServiceReader"]

from sqlite3 import Connection

from zepben.evolve.database.sqlite.common.base_service_reader import BaseServiceReader
from zepben.evolve.database.sqlite.network.network_cim_reader import NetworkCimReader
from zepben.evolve.database.sqlite.network.network_database_tables import NetworkDatabaseTables
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
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_owners import TableAssetOwners
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_poles import TablePoles
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_streetlights import TableStreetlights
from zepben.evolve.database.sqlite.tables.iec61968.common.table_location_street_addresses import TableLocationStreetAddresses
from zepben.evolve.database.sqlite.tables.iec61968.common.table_locations import TableLocations
from zepben.evolve.database.sqlite.tables.iec61968.common.table_organisations import TableOrganisations
from zepben.evolve.database.sqlite.tables.iec61968.common.table_position_points import TablePositionPoints
from zepben.evolve.database.sqlite.tables.iec61968.infiec61968.infassetinfo.table_current_transformer_info import TableCurrentTransformerInfo
from zepben.evolve.database.sqlite.tables.iec61968.infiec61968.infassetinfo.table_potential_transformer_info import TablePotentialTransformerInfo
from zepben.evolve.database.sqlite.tables.iec61968.infiec61968.infassetinfo.table_reclose_delays import TableRecloseDelays
from zepben.evolve.database.sqlite.tables.iec61968.infiec61968.infassetinfo.table_relay_info import TableRelayInfo
from zepben.evolve.database.sqlite.tables.iec61968.metering.table_meters import TableMeters
from zepben.evolve.database.sqlite.tables.iec61968.metering.table_usage_points import TableUsagePoints
from zepben.evolve.database.sqlite.tables.iec61968.operations.table_operational_restrictions import TableOperationalRestrictions
from zepben.evolve.database.sqlite.tables.iec61970.base.auxiliaryequipment.table_current_transformers import TableCurrentTransformers
from zepben.evolve.database.sqlite.tables.iec61970.base.auxiliaryequipment.table_fault_indicators import TableFaultIndicators
from zepben.evolve.database.sqlite.tables.iec61970.base.auxiliaryequipment.table_potential_transformers import TablePotentialTransformers
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_base_voltages import TableBaseVoltages
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_connectivity_nodes import TableConnectivityNodes
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_feeders import TableFeeders
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_geographical_regions import TableGeographicalRegions
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_sites import TableSites
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_sub_geographical_regions import TableSubGeographicalRegions
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_substations import TableSubstations
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_terminals import TableTerminals
from zepben.evolve.database.sqlite.tables.iec61970.base.equivalents.table_equivalent_branches import TableEquivalentBranches
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_accumulators import TableAccumulators
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_analogs import TableAnalogs
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_controls import TableControls
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_discretes import TableDiscretes
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_current_relays import TableCurrentRelays
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_distance_relays import TableDistanceRelays
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_protection_relay_function_thresholds import TableProtectionRelayFunctionThresholds
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_protection_relay_function_time_limits import TableProtectionRelayFunctionTimeLimits
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_protection_relay_schemes import TableProtectionRelaySchemes
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_protection_relay_systems import TableProtectionRelaySystems
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_voltage_relays import TableVoltageRelays
from zepben.evolve.database.sqlite.tables.iec61970.base.scada.table_remote_controls import TableRemoteControls
from zepben.evolve.database.sqlite.tables.iec61970.base.scada.table_remote_sources import TableRemoteSources
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.generation.production.table_battery_units import TableBatteryUnits
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.generation.production.table_photo_voltaic_units import TablePhotoVoltaicUnits
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.generation.production.table_power_electronics_wind_units import TablePowerElectronicsWindUnits
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_ac_line_segments import TableAcLineSegments
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_breakers import TableBreakers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_busbar_sections import TableBusbarSections
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_disconnectors import TableDisconnectors
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
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_load_break_switches import TableLoadBreakSwitches
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_per_length_sequence_impedances import TablePerLengthSequenceImpedances
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_electronics_connection_phases import TablePowerElectronicsConnectionPhases
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_electronics_connections import TablePowerElectronicsConnections
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_transformer_end_ratings import TablePowerTransformerEndRatings
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_transformer_ends import TablePowerTransformerEnds
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_transformers import TablePowerTransformers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_ratio_tap_changers import TableRatioTapChangers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_reclosers import TableReclosers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_series_compensators import TableSeriesCompensators
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_tap_changer_controls import TableTapChangerControls
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_transformer_star_impedances import TableTransformerStarImpedances
from zepben.evolve.database.sqlite.tables.iec61970.infiec61970.feeder.table_circuits import TableCircuits
from zepben.evolve.database.sqlite.tables.iec61970.infiec61970.feeder.table_loops import TableLoops
from zepben.evolve.database.sqlite.tables.iec61970.infiec61970.feeder.table_lv_feeders import TableLvFeeders
from zepben.evolve.database.sqlite.tables.iec61970.infiec61970.wires.generation.production.table_ev_charging_units import TableEvChargingUnits
from zepben.evolve.services.network.network_service import NetworkService


class NetworkServiceReader(BaseServiceReader):
    """
    A class for reading a `NetworkService` from the database.

    :param service: The `NetworkService` to populate from the database.
    :param database_tables: The tables available in the database.
    :param connection: A connection to the database.

    :param reader: The `NetworkCimReader` used to load the objects from the database.
    """

    def __init__(
        self,
        service: NetworkService,
        database_tables: NetworkDatabaseTables,
        connection: Connection,
        reader: NetworkCimReader = None
    ):
        reader = reader if reader else NetworkCimReader(service)
        super().__init__(database_tables, connection, reader)

        # This is not strictly necessary, it is just to update the type of the reader. It could be done with a generic
        # on the base class which looks like it works, but that actually silently breaks code insight and completion
        self._reader = reader

    def _do_load(self) -> bool:
        return all([
            self._load_each(TableCableInfo, self._reader.load_cable_info),
            self._load_each(TableOverheadWireInfo, self._reader.load_overhead_wire_info),
            self._load_each(TablePowerTransformerInfo, self._reader.load_power_transformer_info),
            self._load_each(TableTransformerTankInfo, self._reader.load_transformer_tank_info),
            self._load_each(TableNoLoadTests, self._reader.load_no_load_tests),
            self._load_each(TableOpenCircuitTests, self._reader.load_open_circuit_tests),
            self._load_each(TableShortCircuitTests, self._reader.load_short_circuit_tests),
            self._load_each(TableShuntCompensatorInfo, self._reader.load_shunt_compensator_info),
            self._load_each(TableSwitchInfo, self._reader.load_switch_info),
            self._load_each(TableTransformerEndInfo, self._reader.load_transformer_end_info),
            self._load_each(TableCurrentTransformerInfo, self._reader.load_current_transformer_info),
            self._load_each(TablePotentialTransformerInfo, self._reader.load_potential_transformer_info),
            self._load_each(TableRelayInfo, self._reader.load_relay_info),
            self._load_each(TableRecloseDelays, self._reader.load_reclose_delays),
            self._load_each(TableLocations, self._reader.load_locations),
            self._load_each(TableOrganisations, self._reader.load_organisations),
            self._load_each(TableAssetOwners, self._reader.load_asset_owners),
            self._load_each(TablePoles, self._reader.load_poles),
            self._load_each(TableStreetlights, self._reader.load_streetlights),
            self._load_each(TableMeters, self._reader.load_meters),
            self._load_each(TableUsagePoints, self._reader.load_usage_points),
            self._load_each(TableOperationalRestrictions, self._reader.load_operational_restrictions),
            self._load_each(TableBaseVoltages, self._reader.load_base_voltages),
            self._load_each(TableConnectivityNodes, self._reader.load_connectivity_nodes),
            self._load_each(TableGeographicalRegions, self._reader.load_geographical_regions),
            self._load_each(TableSubGeographicalRegions, self._reader.load_sub_geographical_regions),
            self._load_each(TableSubstations, self._reader.load_substations),
            self._load_each(TableSites, self._reader.load_sites),
            self._load_each(TablePerLengthSequenceImpedances, self._reader.load_per_length_sequence_impedances),
            self._load_each(TableEquivalentBranches, self._reader.load_equivalent_branches),
            self._load_each(TableAcLineSegments, self._reader.load_ac_line_segments),
            self._load_each(TableBreakers, self._reader.load_breakers),
            self._load_each(TableLoadBreakSwitches, self._reader.load_load_break_switches),
            self._load_each(TableBusbarSections, self._reader.load_busbar_sections),
            self._load_each(TableCurrentRelays, self._reader.load_current_relays),
            self._load_each(TableDistanceRelays, self._reader.load_distance_relays),
            self._load_each(TableVoltageRelays, self._reader.load_voltage_relays),
            self._load_each(TableProtectionRelayFunctionThresholds, self._reader.load_protection_relay_function_thresholds),
            self._load_each(TableProtectionRelayFunctionTimeLimits, self._reader.load_protection_relay_function_time_limits),
            self._load_each(TableProtectionRelaySystems, self._reader.load_protection_relay_systems),
            self._load_each(TableProtectionRelaySchemes, self._reader.load_protection_relay_schemes),
            self._load_each(TableDisconnectors, self._reader.load_disconnectors),
            self._load_each(TableEnergyConsumers, self._reader.load_energy_consumers),
            self._load_each(TableEnergyConsumerPhases, self._reader.load_energy_consumer_phases),
            self._load_each(TableEnergySources, self._reader.load_energy_sources),
            self._load_each(TableEnergySourcePhases, self._reader.load_energy_source_phases),
            self._load_each(TableFuses, self._reader.load_fuses),
            self._load_each(TableJumpers, self._reader.load_jumpers),
            self._load_each(TableJunctions, self._reader.load_junctions),
            self._load_each(TableGrounds, self._reader.load_grounds),
            self._load_each(TableGroundDisconnectors, self._reader.load_ground_disconnectors),
            self._load_each(TableSeriesCompensators, self._reader.load_series_compensators),
            self._load_each(TableLinearShuntCompensators, self._reader.load_linear_shunt_compensators),
            self._load_each(TablePowerTransformers, self._reader.load_power_transformers),
            self._load_each(TableReclosers, self._reader.load_reclosers),
            self._load_each(TablePowerElectronicsConnections, self._reader.load_power_electronics_connections),
            self._load_each(TableTerminals, self._reader.load_terminals),
            self._load_each(TableTapChangerControls, self._reader.load_tap_changer_controls),
            self._load_each(TablePowerElectronicsConnectionPhases, self._reader.load_power_electronics_connection_phases),
            self._load_each(TableBatteryUnits, self._reader.load_battery_units),
            self._load_each(TablePhotoVoltaicUnits, self._reader.load_photo_voltaic_units),
            self._load_each(TablePowerElectronicsWindUnits, self._reader.load_power_electronics_wind_units),
            self._load_each(TableEvChargingUnits, self._reader.load_ev_charging_units),
            self._load_each(TableTransformerStarImpedances, self._reader.load_transformer_star_impedances),
            self._load_each(TablePowerTransformerEnds, self._reader.load_power_transformer_ends),
            self._load_each(TablePowerTransformerEndRatings, self._reader.load_power_transformer_end_ratings),
            self._load_each(TableRatioTapChangers, self._reader.load_ratio_tap_changers),
            self._load_each(TableCurrentTransformers, self._reader.load_current_transformers),
            self._load_each(TableFaultIndicators, self._reader.load_fault_indicators),
            self._load_each(TablePotentialTransformers, self._reader.load_potential_transformers),
            self._load_each(TableFeeders, self._reader.load_feeders),
            self._load_each(TableLoops, self._reader.load_loops),
            self._load_each(TableLvFeeders, self._reader.load_lv_feeders),
            self._load_each(TableCircuits, self._reader.load_circuits),
            self._load_each(TablePositionPoints, self._reader.load_position_points),
            self._load_each(TableLocationStreetAddresses, self._reader.load_location_street_addresses),
            self._load_each(TableAssetOrganisationRolesAssets, self._reader.load_asset_organisation_roles_assets),
            self._load_each(TableUsagePointsEndDevices, self._reader.load_usage_points_end_devices),
            self._load_each(TableEquipmentUsagePoints, self._reader.load_equipment_usage_points),
            self._load_each(TableEquipmentOperationalRestrictions, self._reader.load_equipment_operational_restrictions),
            self._load_each(TableEquipmentEquipmentContainers, self._reader.load_equipment_equipment_containers),
            self._load_each(TableCircuitsSubstations, self._reader.load_circuits_substations),
            self._load_each(TableCircuitsTerminals, self._reader.load_circuits_terminals),
            self._load_each(TableLoopsSubstations, self._reader.load_loops_substations),
            self._load_each(TableProtectionRelayFunctionsProtectedSwitches, self._reader.load_protection_relay_functions_protected_switches),
            self._load_each(TableProtectionRelayFunctionsSensors, self._reader.load_protection_relay_functions_sensors),
            self._load_each(TableProtectionRelaySchemesProtectionRelayFunctions, self._reader.load_protection_relay_schemes_protection_relay_functions),
            self._load_each(TableControls, self._reader.load_controls),
            self._load_each(TableRemoteControls, self._reader.load_remote_controls),
            self._load_each(TableRemoteSources, self._reader.load_remote_sources),
            self._load_each(TableAnalogs, self._reader.load_analogs),
            self._load_each(TableAccumulators, self._reader.load_accumulators),
            self._load_each(TableDiscretes, self._reader.load_discretes),
        ])
