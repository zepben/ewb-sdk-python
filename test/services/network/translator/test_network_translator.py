#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given

from test.cim_creators import *
from test.services.common.translator.base_test_translator import validate_service_translations
from zepben.evolve import NetworkService, NetworkServiceComparator

T = TypeVar("T", bound=IdentifiedObject)

#
# NOTE: The following have been split into multiple tests to avoid issues with hypothesis timeout warnings due to the amount of things we are generating
#
iec61968_types_to_test = {
    #######################
    # IEC61968 ASSET INFO #
    #######################

    "create_cable_info": create_cable_info(),
    "create_no_load_test": create_no_load_test(),
    "create_open_circuit_test": create_open_circuit_test(),
    "create_overhead_wire_info": create_overhead_wire_info(),
    "create_power_transformer_info": create_power_transformer_info(),
    "create_short_circuit_test": create_short_circuit_test(),
    "create_transformer_end_info": create_transformer_end_info(),
    "create_transformer_tank_info": create_transformer_tank_info(),

    ###################
    # IEC61968 ASSETS #
    ###################

    "create_asset_owner": create_asset_owner(),
    "create_pole": create_pole(),
    "create_streetlight": create_streetlight(),

    ###################
    # IEC61968 COMMON #
    ###################

    "create_location": create_location(),
    "create_organisation": create_organisation(),

    #####################
    # IEC61968 METERING #
    #####################

    "create_meter": create_meter(),
    "create_usage_point": create_usage_point(),

    #######################
    # IEC61968 OPERATIONS #
    #######################

    "create_operational_restriction": create_operational_restriction(),
}

iec61970_non_wires_types_to_test = {
    #####################################
    # IEC61970 BASE AUXILIARY EQUIPMENT #
    #####################################

    "create_fault_indicator": create_fault_indicator(),

    ######################
    # IEC61970 BASE CORE #
    ######################

    "create_base_voltage": create_base_voltage(),
    "create_connectivity_node": create_connectivity_node(),
    "create_feeder": create_feeder(),
    "create_geographical_region": create_geographical_region(),
    "create_site": create_site(),
    "create_sub_geographical_region": create_sub_geographical_region(),
    "create_substation": create_substation(),
    "create_terminal": create_terminal(),

    ######################
    # IEC61970 BASE MEAS #
    ######################

    "create_accumulator": create_accumulator(),
    "create_analog": create_analog(),
    "create_control": create_control(),
    "create_discrete": create_discrete(),

    #######################
    # IEC61970 BASE SCADA #
    #######################

    "create_remote_control": create_remote_control(),
    "create_remote_source": create_remote_source(),
}

iec61970_wires_gen_types_to_test = {
    ########################################
    # IEC61970 WIRES GENERATION PRODUCTION #
    ########################################

    "create_battery_unit": create_battery_unit(),
    "create_photovoltaic_unit": create_photovoltaic_unit(),
    "create_power_electronics_wind_unit": create_power_electronics_wind_unit(),
}

iec61970_wires_types_to_test = {
    #######################
    # IEC61970 BASE WIRES #
    #######################

    "create_ac_line_segment": create_ac_line_segment(),
    "create_breaker": create_breaker(),
    "create_busbar_section": create_busbar_section(),
    "create_disconnector": create_disconnector(),
    "create_energy_consumer": create_energy_consumer(),
    "create_energy_consumer_phase": create_energy_consumer_phase(),
    "create_energy_source": create_energy_source(),
    "create_energy_source_phase": create_energy_source_phase(),
    "create_fuse": create_fuse(),
    "create_jumper": create_jumper(),
    "create_junction": create_junction(),
}

iec61970_wires_cont_types_to_test = {
    "create_linear_shunt_compensator": create_linear_shunt_compensator(),
    "create_load_break_switch": create_load_break_switch(),
    "create_per_length_sequence_impedance": create_per_length_sequence_impedance(),
    "create_power_electronics_connection": create_power_electronics_connection(),
    "create_power_electronics_connection_phase": create_power_electronics_connection_phase(),
    "create_power_transformer": create_power_transformer(),
    "create_power_transformer_end": create_power_transformer_end(),
    "create_ratio_tap_changer": create_ratio_tap_changer(),
    "create_recloser": create_recloser(),
    "create_transformer_star_impedance": create_transformer_star_impedance(),
}

iec61970_inf_types_to_test = {
    #########################
    # IEC61970 INF IEC61970 #
    #########################

    "create_circuit": create_circuit(),
    "create_loop": create_loop(),
}


@given(**iec61968_types_to_test)
def test_network_service_iec61968_translations(**kwargs):
    validate_service_translations(NetworkService, NetworkServiceComparator(), **kwargs)


@given(**iec61970_non_wires_types_to_test)
def test_network_service_iec61970_non_wires_translations(**kwargs):
    validate_service_translations(NetworkService, NetworkServiceComparator(), **kwargs)


@given(**iec61970_wires_gen_types_to_test)
def test_network_service_iec61970_wires_gen_translations(**kwargs):
    validate_service_translations(NetworkService, NetworkServiceComparator(), **kwargs)


@given(**iec61970_wires_types_to_test)
def test_network_service_iec61970_wires_translations(**kwargs):
    validate_service_translations(NetworkService, NetworkServiceComparator(), **kwargs)


@given(**iec61970_wires_cont_types_to_test)
def test_network_service_iec61970_wires_cont_translations(**kwargs):
    validate_service_translations(NetworkService, NetworkServiceComparator(), **kwargs)


@given(**iec61970_inf_types_to_test)
def test_network_service_iec61970_inf_translations(**kwargs):
    validate_service_translations(NetworkService, NetworkServiceComparator(), **kwargs)


#
# NOTE: NameType is not sent via any grpc messages at this stage, so test it separately
#

def test_creates_new_name_type():
    # noinspection PyArgumentList, PyUnresolvedReferences
    pb = NameType("nt1 name", "nt1 desc").to_pb()

    # noinspection PyUnresolvedReferences
    cim = NetworkService().add_from_pb(pb)

    assert cim.name == pb.name
    assert cim.description == pb.description


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
    assert cim.description == pb.description
