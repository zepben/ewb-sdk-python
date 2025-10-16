#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import TypeVar

import pytest

from services.common.translator.base_test_translator import validate_service_translations
from test.cim.cim_creators import *
from zepben.ewb import IdentifiedObject, PowerTransformerEnd, PowerTransformer, NetworkService, NetworkServiceComparator, NameType, \
    NetworkDatabaseTables, TableAssetOrganisationRolesAssets, TableCircuitsSubstations, TableCircuitsTerminals, \
    TableEquipmentEquipmentContainers, TableEquipmentOperationalRestrictions, TableEquipmentUsagePoints, TableLoopsSubstations, \
    TableProtectionRelayFunctionsProtectedSwitches, TableProtectionRelaySchemesProtectionRelayFunctions, TableUsagePointsEndDevices, \
    TableLocationStreetAddresses, TablePositionPoints, TablePowerTransformerEndRatings, TableProtectionRelayFunctionThresholds, \
    TableProtectionRelayFunctionTimeLimits, TableProtectionRelayFunctionsSensors, TableRecloseDelays, TablePhaseImpedanceData, TableBatteryUnitsBatteryControls, \
    TableEndDevicesEndDeviceFunctions, TableAssetsPowerSystemResources, TableSynchronousMachinesReactiveCapabilityCurves, TableCurveData
from zepben.ewb.services.common.translator.base_proto2cim import get_nullable

T = TypeVar("T", bound=IdentifiedObject)

types_to_test = {
    ##################################
    # Extensions IEC61968 Asset Info #
    ##################################

    "create_relay_info": create_relay_info(),

    ################################
    # Extensions IEC61968 Metering #
    ################################

    "create_pan_demand_response_function": create_pan_demand_response_function(),

    #################################
    # Extensions IEC61970 Base Core #
    #################################

    "create_site": create_site(),

    ###################################
    # Extensions IEC61970 Base Feeder #
    ###################################

    "create_loop": create_loop(),
    "create_lv_feeder": create_lv_feeder(),

    ##################################################
    # Extensions IEC61970 Base Generation Production #
    ##################################################

    "create_ev_charging_unit": create_ev_charging_unit(),

    #######################################
    # Extensions IEC61970 Base Protection #
    #######################################

    "create_distance_relay": create_distance_relay(),
    "create_protection_relay_scheme": create_protection_relay_scheme(),
    "create_protection_relay_system": create_protection_relay_system(),
    "create_voltage_relay": create_voltage_relay(),

    ##################################
    # Extensions IEC61970 Base Wires #
    ##################################

    "create_battery_control": create_battery_control(),

    #######################
    # IEC61968 Asset Info #
    #######################

    "create_cable_info": create_cable_info(),
    "create_no_load_test": create_no_load_test(),
    "create_open_circuit_test": create_open_circuit_test(),
    "create_overhead_wire_info": create_overhead_wire_info(),
    "create_power_transformer_info": create_power_transformer_info(),
    "create_short_circuit_test": create_short_circuit_test(),
    "create_shunt_compensator_info": create_shunt_compensator_info(),
    "create_switch_info": create_switch_info(),
    "create_transformer_end_info": create_transformer_end_info(),
    "create_transformer_tank_info": create_transformer_tank_info(),

    ###################
    # IEC61968 Assets #
    ###################

    "create_asset_owner": create_asset_owner(),
    "create_streetlight": create_streetlight(),

    ###################
    # IEC61968 Common #
    ###################

    "create_location": create_location(),
    "create_organisation": create_organisation(),

    #####################################
    # IEC61968 InfIEC61968 InfAssetInfo #
    #####################################

    "create_current_transformer_info": create_current_transformer_info(),
    "create_potential_transformer_info": create_potential_transformer_info(),

    ##################################
    # IEC61968 InfIEC61968 InfAssets #
    ##################################

    "create_pole": create_pole(),

    #####################
    # IEC61968 Metering #
    #####################

    "create_meter": create_meter(),
    "create_usage_point": create_usage_point(),

    #######################
    # IEC61968 Operations #
    #######################

    "create_operational_restriction": create_operational_restriction(),

    #####################################
    # IEC61970 Base Auxiliary Equipment #
    #####################################

    "create_current_transformer": create_current_transformer(),
    "create_fault_indicator": create_fault_indicator(),
    "create_potential_transformer": create_potential_transformer(),

    ######################
    # IEC61970 Base Core #
    ######################

    "create_base_voltage": create_base_voltage(),
    "create_connectivity_node": create_connectivity_node(),
    "create_feeder": create_feeder(),
    "create_geographical_region": create_geographical_region(),
    "create_sub_geographical_region": create_sub_geographical_region(),
    "create_substation": create_substation(),
    "create_terminal": create_terminal(),

    #############################
    # IEC61970 Base Equivalents #
    #############################

    "create_equivalent_branch": create_equivalent_branch(),

    #######################################
    # IEC61970 Base Generation Production #
    #######################################

    "create_battery_unit": create_battery_unit(),
    "create_photo_voltaic_unit": create_photo_voltaic_unit(),
    "create_power_electronics_wind_unit": create_power_electronics_wind_unit(),

    ######################
    # IEC61970 Base Meas #
    ######################

    "create_accumulator": create_accumulator(),
    "create_analog": create_analog(),
    "create_control": create_control(),
    "create_discrete": create_discrete(),

    ############################
    # IEC61970 Base Protection #
    ############################

    "create_current_relay": create_current_relay(),

    #######################
    # IEC61970 Base Scada #
    #######################

    "create_remote_control": create_remote_control(),
    "create_remote_source": create_remote_source(),

    #######################
    # IEC61970 Base Wires #
    #######################

    "create_ac_line_segment": create_ac_line_segment(),
    "create_breaker": create_breaker(),
    "create_busbar_section": create_busbar_section(),
    "create_clamp": create_clamp(),
    "create_cut": create_cut(),
    "create_disconnector": create_disconnector(),
    "create_energy_consumer": create_energy_consumer(),
    "create_energy_consumer_phase": create_energy_consumer_phase(),
    "create_energy_source": create_energy_source(),
    "create_energy_source_phase": create_energy_source_phase(),
    "create_fuse": create_fuse(),
    "create_ground": create_ground(),
    "create_ground_disconnector": create_ground_disconnector(),
    "create_grounding_impedance": create_grounding_impedance(),
    "create_jumper": create_jumper(),
    "create_junction": create_junction(),
    "create_linear_shunt_compensator": create_linear_shunt_compensator(),
    "create_load_break_switch": create_load_break_switch(),
    "create_per_length_phase_impedance": create_per_length_phase_impedance(),
    "create_per_length_sequence_impedance": create_per_length_sequence_impedance(),
    "create_petersen_coil": create_petersen_coil(),
    "create_power_electronics_connection": create_power_electronics_connection(),
    "create_power_electronics_connection_phase": create_power_electronics_connection_phase(),
    "create_power_transformer": create_power_transformer(),
    "create_power_transformer_end": create_power_transformer_end(),
    "create_ratio_tap_changer": create_ratio_tap_changer(),
    "create_reactive_capability_curve": create_reactive_capability_curve(),
    "create_recloser": create_recloser(),
    "create_series_compensator": create_series_compensator(),
    "create_static_var_compensator": create_static_var_compensator(),
    "create_synchronous_machine": create_synchronous_machine(),
    "create_tap_changer_control": create_tap_changer_control(),
    "create_transformer_star_impedance": create_transformer_star_impedance(),

    ###############################
    # IEC61970 InfIEC61970 Feeder #
    ###############################

    "create_circuit": create_circuit(),
}

@pytest.mark.timeout(20000)
def test_network_service_translations():
    validate_service_translations(
        NetworkService,
        NetworkServiceComparator(),
        NetworkDatabaseTables(),
        excluded_tables={
            # Excluded associations.
            TableAssetOrganisationRolesAssets,
            TableAssetsPowerSystemResources,
            TableBatteryUnitsBatteryControls,
            TableCircuitsSubstations,
            TableCircuitsTerminals,
            TableEndDevicesEndDeviceFunctions,
            TableEquipmentEquipmentContainers,
            TableEquipmentOperationalRestrictions,
            TableEquipmentUsagePoints,
            TableLoopsSubstations,
            TableProtectionRelayFunctionsProtectedSwitches,
            TableProtectionRelaySchemesProtectionRelayFunctions,
            TableSynchronousMachinesReactiveCapabilityCurves,
            TableUsagePointsEndDevices,

            # Excluded array data.
            TableCurveData,
            TablePhaseImpedanceData,
            TableLocationStreetAddresses,
            TablePositionPoints,
            TablePowerTransformerEndRatings,
            TableProtectionRelayFunctionThresholds,
            TableProtectionRelayFunctionTimeLimits,
            TableProtectionRelayFunctionsSensors,
            TableRecloseDelays,

        },
        types_to_test=types_to_test,
    )

# NOTE: NameType is not sent via any grpc messages at this stage, so test it separately
def test_creates_new_name_type():
    # noinspection PyArgumentList, PyUnresolvedReferences
    pb = NameType("nt1 name", "nt1 desc").to_pb()

    # noinspection PyUnresolvedReferences
    cim = NetworkService().add_from_pb(pb)

    assert cim.name == pb.name
    assert cim.description == get_nullable(pb, 'description')


def test_updates_existing_name_type():
    # noinspection PyArgumentList, PyUnresolvedReferences
    pb = NameType("nt1 name", "nt1 desc").to_pb()

    # noinspection PyArgumentList
    nt = NameType("nt1 name")
    ns = NetworkService()
    ns.add_name_type(nt)
    # noinspection PyUnresolvedReferences
    cim = ns.add_from_pb(pb)

    assert cim is nt
    assert cim.description == get_nullable(pb, 'description')


def test_power_transformer_end_order():
    e1 = PowerTransformerEnd(mrid="e1", end_number=1)
    e2 = PowerTransformerEnd(mrid="e2", end_number=2)
    tx = PowerTransformer(mrid="tx", power_transformer_ends=[e1, e2])

    ns = NetworkService()
    # noinspection PyUnresolvedReferences
    ns.add_from_pb(tx.to_pb())
    # noinspection PyUnresolvedReferences
    ns.add_from_pb(e2.to_pb())
    # noinspection PyUnresolvedReferences
    ns.add_from_pb(e1.to_pb())

    assert [end.mrid for end in ns["tx"].ends] == ["e1", "e2"]
