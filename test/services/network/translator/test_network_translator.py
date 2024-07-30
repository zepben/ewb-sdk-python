#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import TypeVar

import pytest
from hypothesis import given, HealthCheck, settings

from database.sqlite.schema_utils import assume_non_blank_street_address_details
from cim.cim_creators import *
from services.common.translator.base_test_translator import validate_service_translations
from zepben.evolve import IdentifiedObject, PowerTransformerEnd, PowerTransformer, NetworkService, Location, NetworkServiceComparator, NameType

T = TypeVar("T", bound=IdentifiedObject)

types_to_test = {
    #######################
    # IEC61968 ASSET INFO #
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
    # IEC61968 ASSETS #
    ###################

    "create_asset_owner": create_asset_owner(),
    "create_pole": create_pole(),
    "create_streetlight": create_streetlight(),

    ###################
    # IEC61968 COMMON #
    ###################

    # NOTE: location is tested separately due to constraints on the translation.
    # "create_location": create_location(),
    "create_organisation": create_organisation(),

    #####################################
    # IEC61968 infIEC61968 InfAssetInfo #
    #####################################

    "create_relay_info": create_relay_info(),
    "create_current_transformer_info": create_current_transformer_info(),
    "create_potential_transformer_info": create_potential_transformer_info(),

    #####################
    # IEC61968 METERING #
    #####################

    "create_meter": create_meter(),
    "create_usage_point": create_usage_point(),

    #######################
    # IEC61968 OPERATIONS #
    #######################

    "create_operational_restriction": create_operational_restriction(),

    #####################################
    # IEC61970 BASE AUXILIARY EQUIPMENT #
    #####################################

    "create_current_transformer": create_current_transformer(),
    "create_fault_indicator": create_fault_indicator(),
    "create_potential_transformer": create_potential_transformer(),

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

    #############################
    # IEC61970 BASE EQUIVALENTS #
    #############################

    "create_equivalent_branch": create_equivalent_branch(),

    ######################
    # IEC61970 BASE MEAS #
    ######################

    "create_accumulator": create_accumulator(),
    "create_analog": create_analog(),
    "create_control": create_control(),
    "create_discrete": create_discrete(),

    ############################
    # IEC61970 Base Protection #
    ############################

    "create_current_relay": create_current_relay(),
    "create_distance_relay": create_distance_relay(),
    "create_voltage_relay": create_voltage_relay(),
    "create_protection_relay_scheme": create_protection_relay_scheme(),
    "create_protection_relay_system": create_protection_relay_system(),

    #######################
    # IEC61970 BASE SCADA #
    #######################

    "create_remote_control": create_remote_control(),
    "create_remote_source": create_remote_source(),

    ########################################
    # IEC61970 WIRES GENERATION PRODUCTION #
    ########################################

    "create_battery_unit": create_battery_unit(),
    "create_photovoltaic_unit": create_photovoltaic_unit(),
    "create_power_electronics_wind_unit": create_power_electronics_wind_unit(),

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
    "create_ground": create_ground(),
    "create_ground_disconnector": create_ground_disconnector(),
    "create_jumper": create_jumper(),
    "create_junction": create_junction(),

    "create_series_compensator": create_series_compensator(),
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
    "create_tap_changer_control": create_tap_changer_control(),

    #########################
    # IEC61970 INF IEC61970 #
    #########################

    "create_circuit": create_circuit(),
    "create_loop": create_loop(),
    "create_lv_feeder": create_lv_feeder(),

    ##########################################################
    # INFIEC61970 IEC61970 WIRES GENERATION PRODUCTION #
    ##########################################################

    "create_ev_charging_unit": create_ev_charging_unit(),
}

@given(**types_to_test)
@settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.large_base_example])
@pytest.mark.timeout(10000)
def test_network_service_translations(**kwargs):
    validate_service_translations(NetworkService, NetworkServiceComparator(), **kwargs)


@given(location=create_location())
@settings(suppress_health_check=[HealthCheck.too_slow])
@pytest.mark.timeout(10000)
def test_network_service_translations_location(location: Location):
    assume_non_blank_street_address_details(location.main_address)
    validate_service_translations(NetworkService, NetworkServiceComparator(), location=location)


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


def test_power_transformer_end_order():
    e1 = PowerTransformerEnd(mrid="e1", end_number=1)
    e2 = PowerTransformerEnd(mrid="e2", end_number=2)
    tx = PowerTransformer(mrid="tx", power_transformer_ends=[e1, e2])

    ns = NetworkService()
    ns.add_from_pb(tx.to_pb())
    ns.add_from_pb(e2.to_pb())
    ns.add_from_pb(e1.to_pb())

    assert [end.mrid for end in ns["tx"].ends] == ["e1", "e2"]
