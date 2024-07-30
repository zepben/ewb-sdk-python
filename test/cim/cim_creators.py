#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime
from random import choice

from hypothesis.strategies import builds, text, integers, sampled_from, lists, floats, booleans, uuids, datetimes

from zepben.evolve import *
# WARNING!! # THIS IS A WORK IN PROGRESS AND MANY FUNCTIONS ARE LIKELY BROKEN

MIN_32_BIT_INTEGER = -2147483647  # _UNKNOWN_INT = -2147483648
MAX_32_BIT_INTEGER = 2147483647
MAX_32_BIT_UNSIGNED_INTEGER = 4294967294  # _UNKNOWN_UINT = 4294967295
MAX_64_BIT_INTEGER = 9223372036854775807
MIN_64_BIT_INTEGER = -9223372036854775807  # _UNKNOWN_LONG = -9223372036854775808
TEXT_MAX_SIZE = 6
FLOAT_MIN = -100.0
FLOAT_MAX = 1000.0
MAX_END_NUMBER = 3
MAX_SEQUENCE_NUMBER = 40
MIN_SEQUENCE_NUMBER = 1
ALPHANUM = "abcdefghijbklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"

__all__ = ['create_cable_info', 'create_no_load_test', 'create_open_circuit_test', 'create_overhead_wire_info', 'create_power_transformer_info',
           'create_short_circuit_test', 'create_series_compensator', 'create_shunt_compensator_info', 'create_switch_info', 'create_transformer_end_info',
           'create_transformer_tank_info',
           'create_transformer_test', 'create_wire_info', 'sampled_wire_material_kind', 'create_asset', 'create_asset_info', 'create_asset_container',
           'create_asset_organisation_role', 'create_asset_owner', 'create_pole', 'create_streetlight', 'sampled_streetlight_lamp_kind', 'create_structure',
           'create_agreement', 'create_document', 'create_location', 'create_organisation', 'create_organisation_role', 'create_position_point',
           'create_street_address', 'create_street_detail', 'create_town_detail', 'create_customer', 'create_customer_agreement', 'sampled_customer_kind',
           'create_pricing_structure', 'create_tariffs', 'create_relay_info', 'create_current_transformer_info', 'create_potential_transformer_info',
           'create_ratio', 'create_end_device', 'create_meter', 'create_usage_point', 'create_operational_restriction', 'create_auxiliary_equipment',
           'create_current_transformer', 'create_fault_indicator', 'create_potential_transformer', 'create_sensor', 'create_ac_dc_terminal',
           'create_base_voltage', 'create_conducting_equipment', 'create_connectivity_node', 'create_connectivity_node_container', 'create_equipment',
           'create_equipment_container', 'create_feeder', 'create_geographical_region', 'create_identified_object', 'create_name', 'create_name_type',
           'sampled_phase_code', 'create_power_system_resource', 'create_site', 'create_sub_geographical_region', 'create_substation', 'create_terminal',
           'create_equivalent_branch', 'create_equivalent_equipment', 'create_diagram', 'create_diagram_object', 'create_diagram_object_point',
           'create_accumulator', 'create_accumulator_value', 'create_analog', 'create_analog_value', 'create_control', 'create_discrete',
           'create_discrete_value', 'create_io_point', 'create_measurement', 'sampled_unit_symbol', 'create_current_relay', 'create_distance_relay',
           'create_protection_relay_function', 'create_protection_relay_scheme', 'create_voltage_relay', 'create_protection_relay_system',
           'create_remote_control', 'create_remote_point', 'create_remote_source', 'sampled_battery_state_kind', 'create_battery_unit',
           'create_photovoltaic_unit', 'create_power_electronics_unit', 'create_power_electronics_wind_unit', 'create_ac_line_segment', 'create_breaker',
           'create_busbar_section', 'create_conductor', 'create_connector', 'create_disconnector', 'create_energy_consumer', 'create_energy_connection',
           'create_energy_consumer_phase', 'create_energy_source', 'create_energy_source_phase', 'create_fuse', 'create_ground', 'create_ground_disconnector',
           'create_jumper', 'create_junction',
           'create_line', 'create_linear_shunt_compensator', 'create_load_break_switch', 'create_per_length_impedance', 'create_per_length_line_parameter',
           'create_per_length_sequence_impedance', 'sampled_phase_shunt_connection_kind', 'create_power_electronics_connection',
           'create_power_electronics_connection_phase', 'create_power_transformer', 'create_power_transformer_end', 'create_protected_switch',
           'create_ratio_tap_changer', 'create_recloser', 'create_regulating_cond_eq', 'create_shunt_compensator', 'sampled_single_phase_kind', 'create_switch',
           'create_tap_changer', 'create_transformer_end', 'create_transformer_star_impedance', 'sampled_vector_group', 'sampled_winding_connection_kind',
           'create_circuit', 'create_loop', 'create_lv_feeder', "create_ev_charging_unit", 'traced_phases', 'sampled_wire_info', 'sampled_conducting_equipment',
           'sampled_equipment', 'sampled_equipment_container', 'sampled_hvlv_feeder', 'sampled_measurement', 'sampled_protected_switches',
           'create_tap_changer_control']


#######################
# IEC61968 ASSET INFO #
#######################


def create_cable_info(include_runtime: bool = True):
    return builds(CableInfo, **create_wire_info(include_runtime))


def create_no_load_test(include_runtime: bool = True):
    return builds(
        NoLoadTest,
        **create_transformer_test(include_runtime),
        energised_end_voltage=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        exciting_current=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        exciting_current_zero=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        loss=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        loss_zero=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
    )


def create_open_circuit_test(include_runtime: bool = True):
    return builds(
        OpenCircuitTest,
        **create_transformer_test(include_runtime),
        energised_end_step=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        energised_end_voltage=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        open_end_step=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        open_end_voltage=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        phase_shift=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def create_overhead_wire_info(include_runtime: bool = True):
    return builds(OverheadWireInfo, **create_wire_info(include_runtime))


def create_power_transformer_info(include_runtime: bool = True):
    return builds(
        PowerTransformerInfo,
        **create_asset_info(include_runtime),
        transformer_tank_infos=lists(builds(TransformerTankInfo, **create_identified_object(include_runtime)), min_size=1, max_size=2)
    )


def create_short_circuit_test(include_runtime: bool = True):
    return builds(
        ShortCircuitTest,
        **create_transformer_test(include_runtime),
        current=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        energised_end_step=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        grounded_end_step=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        leakage_impedance=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        leakage_impedance_zero=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        loss=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        loss_zero=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        power=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        voltage=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        voltage_ohmic_part=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def create_shunt_compensator_info(include_runtime: bool = True):
    return builds(
        ShuntCompensatorInfo,
        **create_asset_info(include_runtime),
        max_power_loss=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        rated_current=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        rated_reactive_power=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        rated_voltage=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    )


def create_switch_info(include_runtime: bool = True):
    return builds(
        SwitchInfo,
        **create_asset_info(include_runtime),
        rated_interrupting_time=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def create_transformer_end_info(include_runtime: bool = True):
    return builds(
        TransformerEndInfo,
        **create_asset_info(include_runtime),
        connection_kind=sampled_winding_connection_kind(),
        emergency_s=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        end_number=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        insulation_u=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        phase_angle_clock=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        r=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        rated_s=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        rated_u=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        short_term_s=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        transformer_tank_info=builds(TransformerTankInfo, **create_identified_object(include_runtime)),
        transformer_star_impedance=builds(TransformerStarImpedance, **create_identified_object(include_runtime)),
        energised_end_no_load_tests=builds(NoLoadTest, **create_identified_object(include_runtime)),
        energised_end_short_circuit_tests=builds(ShortCircuitTest, **create_identified_object(include_runtime)),
        grounded_end_short_circuit_tests=builds(ShortCircuitTest, **create_identified_object(include_runtime)),
        open_end_open_circuit_tests=builds(OpenCircuitTest, **create_identified_object(include_runtime)),
        energised_end_open_circuit_tests=builds(OpenCircuitTest, **create_identified_object(include_runtime)),
    )


def create_transformer_tank_info(include_runtime: bool = True):
    return builds(
        TransformerTankInfo,
        **create_asset_info(include_runtime),
        power_transformer_info=builds(PowerTransformerInfo, **create_identified_object(include_runtime)),
        transformer_end_infos=lists(builds(TransformerEndInfo, **create_identified_object(include_runtime)), min_size=1, max_size=2)
    )


def create_transformer_test(include_runtime: bool):
    return {
        **create_identified_object(include_runtime),
        "base_power": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "temperature": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    }


def create_wire_info(include_runtime: bool):
    return {
        **create_asset_info(include_runtime),
        "rated_current": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "material": sampled_wire_material_kind()
    }


def sampled_wire_material_kind():
    return sampled_from(WireMaterialKind)


###################
# IEC61968 ASSETS #
###################


def create_asset(include_runtime: bool):
    return {
        **create_identified_object(include_runtime),
        "location": builds(Location, **create_identified_object(include_runtime)),
        "organisation_roles": lists(builds(AssetOwner, **create_identified_object(include_runtime)), min_size=1, max_size=2)
    }


def create_asset_info(include_runtime: bool):
    return {**create_identified_object(include_runtime)}


def create_asset_container(include_runtime: bool):
    return {**create_asset(include_runtime)}


def create_asset_organisation_role(include_runtime: bool):
    return {**create_organisation_role(include_runtime)}


def create_asset_owner(include_runtime: bool = True):
    return builds(AssetOwner, **create_asset_organisation_role(include_runtime))


def create_pole(include_runtime: bool = True):
    return builds(
        Pole,
        **create_structure(include_runtime),
        streetlights=lists(builds(Streetlight, **create_identified_object(include_runtime)), min_size=1, max_size=2),
        classification=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
    )


def create_streetlight(include_runtime: bool = True):
    return builds(
        Streetlight,
        **create_asset(include_runtime),
        pole=builds(Pole, **create_identified_object(include_runtime)),
        light_rating=integers(min_value=0, max_value=MAX_32_BIT_INTEGER),  # Capping unsigned int to 32-bit int range to avoid issues with Python 3.7 testing.
        lamp_kind=sampled_streetlight_lamp_kind()
    )


def sampled_streetlight_lamp_kind():
    return sampled_from(StreetlightLampKind)


def create_structure(include_runtime: bool):
    return {**create_asset_container(include_runtime)}


###################
# IEC61968 COMMON #
###################


def create_agreement(include_runtime: bool):
    return {**create_document(include_runtime)}


def create_document(include_runtime: bool):
    return {
        **create_identified_object(include_runtime),
        "title": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        "created_date_time": datetimes(min_value=datetime(1970, 1, 2)),
        "author_name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        "type": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        "status": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        "comment": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
    }


def create_location(include_runtime: bool = True):
    return builds(
        Location,
        **create_identified_object(include_runtime),
        main_address=create_street_address(),
        position_points=lists(create_position_point(), max_size=4)
    )


def create_organisation(include_runtime: bool = True):
    return builds(Organisation, **create_identified_object(include_runtime))


def create_organisation_role(include_runtime: bool):
    return {
        **create_identified_object(include_runtime),
        "organisation": builds(Organisation, **create_identified_object(include_runtime))
    }


def create_position_point():
    return builds(
        PositionPoint,
        x_position=floats(min_value=-180.0, max_value=180.0),
        y_position=floats(min_value=-90.0, max_value=90.0)
    )


def create_street_address():
    return builds(
        StreetAddress,
        postal_code=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        town_detail=create_town_detail(),
        po_box=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        street_detail=create_street_detail()
    )


def create_street_detail():
    return builds(
        StreetDetail,
        building_name=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        floor_identification=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        name=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        number=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        suite_number=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        type=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        display_address=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
    )


def create_town_detail():
    return builds(
        TownDetail,
        name=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        state_or_province=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
    )


######################
# IEC61968 CUSTOMERS #
######################


def create_customer(include_runtime: bool = True):
    return builds(
        Customer,
        **create_organisation_role(include_runtime),
        kind=sampled_customer_kind(),
        customer_agreements=lists(builds(CustomerAgreement, **create_identified_object(include_runtime)), min_size=1, max_size=2)
    )


def create_customer_agreement(include_runtime: bool = True):
    return builds(
        CustomerAgreement,
        **create_agreement(include_runtime),
        customer=builds(Customer, **create_identified_object(include_runtime)),
        pricing_structures=lists(builds(PricingStructure, **create_identified_object(include_runtime)), min_size=1, max_size=2)
    )


def sampled_customer_kind():
    return sampled_from(CustomerKind)


def create_pricing_structure(include_runtime: bool = True):
    return builds(
        PricingStructure,
        **create_document(include_runtime),
        tariffs=lists(builds(Tariff, **create_identified_object(include_runtime)), min_size=1, max_size=2)
    )


def create_tariffs(include_runtime: bool = True):
    return builds(Tariff, **create_document(include_runtime))


#####################################
# IEC61968 infIEC61968 InfAssetInfo #
#####################################


def create_relay_info(include_runtime: bool = True):
    return builds(
        RelayInfo,
        **create_asset_info(include_runtime),
        curve_setting=text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        reclose_delays=lists(floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        reclose_fast=boolean_or_none()
    )


def create_current_transformer_info(include_runtime: bool = True):
    return builds(
        CurrentTransformerInfo,
        **create_asset_info(include_runtime),
        accuracy_class=text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        accuracy_limit=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        core_count=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        ct_class=text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        knee_point_voltage=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        max_ratio=create_ratio(),
        nominal_ratio=create_ratio(),
        primary_ratio=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        rated_current=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        secondary_fls_rating=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        secondary_ratio=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        usage=text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE)
    )


def create_potential_transformer_info(include_runtime: bool = True):
    return builds(
        PotentialTransformerInfo,
        **create_asset_info(include_runtime),
        accuracy_class=text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        nominal_ratio=create_ratio(),
        primary_ratio=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        pt_class=text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        rated_voltage=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        secondary_ratio=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


##################################
# IEC61968 infIEC61968 InfCommon #
##################################


def create_ratio():
    return builds(
        Ratio,
        numerator=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        denominator=floats(min_value=0.1, max_value=FLOAT_MAX)
    )


#####################
# IEC61968 METERING #
#####################


def create_end_device(include_runtime: bool):
    return {
        **create_asset_container(include_runtime),
        "usage_points": lists(builds(UsagePoint, **create_identified_object(include_runtime)), min_size=1, max_size=2),
        "customer_mrid": text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        "service_location": builds(Location, **create_identified_object(include_runtime))
    }


def create_meter(include_runtime: bool = True):
    return builds(Meter, **create_end_device(include_runtime))


def create_usage_point(include_runtime: bool = True):
    return builds(
        UsagePoint,
        **create_identified_object(include_runtime),
        usage_point_location=builds(Location, **create_identified_object(include_runtime)),
        is_virtual=booleans(),
        connection_category=text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        rated_power=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        approved_inverter_capacity=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        equipment=lists(builds(EnergyConsumer, **create_identified_object(include_runtime)), min_size=1, max_size=2),
        end_devices=lists(builds(Meter, **create_identified_object(include_runtime)), min_size=1, max_size=2)
    )


#######################
# IEC61968 OPERATIONS #
#######################


def create_operational_restriction(include_runtime: bool = True):
    return builds(
        OperationalRestriction,
        **create_document(include_runtime),
        equipment=lists(builds(PowerTransformer, **create_identified_object(include_runtime)), min_size=1, max_size=2)
    )


#####################################
# IEC61970 BASE AUXILIARY EQUIPMENT #
#####################################


def create_auxiliary_equipment(include_runtime: bool):
    return {
        **create_equipment(include_runtime),
        "terminal": builds(Terminal, **create_identified_object(include_runtime))
    }


def create_current_transformer(include_runtime: bool = True):
    return builds(
        CurrentTransformer,
        **create_sensor(include_runtime),
        asset_info=builds(CurrentTransformerInfo, **create_identified_object(include_runtime)),
        core_burden=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
    )


def create_fault_indicator(include_runtime: bool = True):
    return builds(FaultIndicator, **create_auxiliary_equipment(include_runtime))


def create_potential_transformer(include_runtime: bool = True):
    return builds(
        PotentialTransformer,
        **create_sensor(include_runtime),
        asset_info=builds(PotentialTransformerInfo, **create_identified_object(include_runtime)),
        type=sampled_from(PotentialTransformerKind)
    )


def create_sensor(include_runtime: bool = True):
    return {
        **create_auxiliary_equipment(include_runtime),
        "relay_functions": lists(builds(CurrentRelay), max_size=10)
    }


######################
# IEC61970 BASE CORE #
######################


def create_ac_dc_terminal(include_runtime: bool):
    return {**create_identified_object(include_runtime)}


def create_base_voltage(include_runtime: bool = True):
    return builds(
        BaseVoltage,
        **create_identified_object(include_runtime),
        nominal_voltage=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
    )


def create_conducting_equipment(include_runtime: bool):
    return {
        **create_equipment(include_runtime),
        "base_voltage": builds(BaseVoltage, **create_identified_object(include_runtime)),
        "terminals": lists(builds(Terminal, **create_identified_object(include_runtime)), min_size=1, max_size=3)
    }


def create_connectivity_node(include_runtime: bool = True):
    return builds(
        ConnectivityNode,
        **create_identified_object(include_runtime),
        terminals=lists(builds(Terminal, **create_identified_object(include_runtime)), max_size=10)
    )


def create_connectivity_node_container(include_runtime: bool):
    return {**create_power_system_resource(include_runtime)}


def create_equipment(include_runtime: bool):
    runtime = {
        "current_containers": lists(sampled_hvlv_feeder(include_runtime), min_size=1, max_size=2)
    } if include_runtime else {}

    return {
        **create_power_system_resource(include_runtime),
        "in_service": booleans(),
        "normally_in_service": booleans(),
        "equipment_containers": lists(sampled_equipment_container(include_runtime), min_size=1, max_size=2),
        "usage_points": lists(builds(UsagePoint, **create_identified_object(include_runtime)), min_size=1, max_size=2),
        "operational_restrictions": lists(builds(OperationalRestriction, **create_identified_object(include_runtime)), min_size=1, max_size=2),
        "commissioned_date": datetimes(min_value=datetime(1970, 1, 2)),
        **runtime
    }


def create_equipment_container(include_runtime: bool, add_equipment: bool = True):
    equipment = {
        "equipment": lists(sampled_equipment(include_runtime), min_size=1, max_size=2)
    } if add_equipment else {}

    return {
        **create_connectivity_node_container(include_runtime),
        **equipment
    }


def create_feeder(include_runtime: bool = True):
    runtime = {
        "normal_energized_lv_feeders": lists(builds(LvFeeder, **create_identified_object(include_runtime)), min_size=1, max_size=2),
        "current_equipment": lists(sampled_equipment(include_runtime), min_size=1, max_size=2)
    } if include_runtime else {}

    return builds(
        Feeder,
        **create_equipment_container(include_runtime, include_runtime),
        normal_head_terminal=builds(Terminal, **create_identified_object(include_runtime)),
        normal_energizing_substation=builds(Substation, **create_identified_object(include_runtime)),
        **runtime
    )


def create_geographical_region(include_runtime: bool = True):
    return builds(
        GeographicalRegion,
        **create_identified_object(include_runtime),
        sub_geographical_regions=lists(builds(SubGeographicalRegion, **create_identified_object(include_runtime)), min_size=1, max_size=2)
    )


# noinspection PyUnusedLocal
def create_identified_object(include_runtime: bool):
    return {
        "mrid": uuids(version=4).map(lambda x: str(x)),
        "name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        "description": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        "names": lists(builds(Name, text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), create_name_type()), max_size=2, unique_by=lambda it: it.name)
    }


def create_name(include_runtime: bool = True):
    return builds(
        Name,
        name=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        type=create_name_type(),
        identified_object=sampled_equipment(include_runtime)
    )


def create_name_type():
    return builds(
        NameType,
        name=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        description=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
    )


def sampled_phase_code():
    return sampled_from(PhaseCode)


def create_power_system_resource(include_runtime: bool):
    #
    # NOTE: We do not create the asset_info here, create it where it is actually used.
    #
    return {
        **create_identified_object(include_runtime),
        "location": create_location()
    }


def create_site(include_runtime: bool = True):
    return builds(Site, **create_equipment_container(include_runtime))


def create_sub_geographical_region(include_runtime: bool = True):
    return builds(
        SubGeographicalRegion,
        **create_identified_object(include_runtime),
        geographical_region=builds(GeographicalRegion, **create_identified_object(include_runtime)),
        substations=lists(builds(Substation, **create_identified_object(include_runtime)), min_size=1, max_size=2)
    )


def create_substation(include_runtime: bool = True):
    return builds(
        Substation,
        **create_equipment_container(include_runtime),
        sub_geographical_region=builds(SubGeographicalRegion, **create_identified_object(include_runtime)),
        normal_energized_feeders=lists(builds(Feeder, **create_identified_object(include_runtime)), min_size=1, max_size=2),
        loops=lists(builds(Loop, **create_identified_object(include_runtime)), min_size=1, max_size=2),
        energized_loops=lists(builds(Loop, **create_identified_object(include_runtime)), min_size=1, max_size=2),
        circuits=lists(builds(Circuit, **create_identified_object(include_runtime)), min_size=1, max_size=2)
    )


def create_terminal(include_runtime: bool = True):
    runtime = {
        "traced_phases": builds(TracedPhases)
    } if include_runtime else {}

    return builds(
        Terminal,
        **create_ac_dc_terminal(include_runtime),
        conducting_equipment=sampled_conducting_equipment(include_runtime),
        connectivity_node=builds(ConnectivityNode, **create_identified_object(include_runtime)),
        phases=sampled_phase_code(),
        sequence_number=integers(min_value=MIN_SEQUENCE_NUMBER, max_value=MAX_SEQUENCE_NUMBER),
        **runtime
    )


#############################
# IEC61970 BASE EQUIVALENTS #
#############################


def create_equivalent_branch(include_runtime: bool = True):
    return builds(
        EquivalentBranch,
        **create_equivalent_equipment(include_runtime),
        negative_r12=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        negative_r21=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        negative_x12=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        negative_x21=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        positive_r12=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        positive_r21=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        positive_x12=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        positive_x21=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        r=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        r21=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x21=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        zero_r12=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        zero_r21=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        zero_x12=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        zero_x21=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def create_equivalent_equipment(include_runtime: bool):
    return {**create_conducting_equipment(include_runtime)}


################################
# IEC61970 BASE DIAGRAM LAYOUT #
################################


def create_diagram(include_runtime: bool = True):
    return builds(
        Diagram,
        **create_identified_object(include_runtime),
        diagram_style=sampled_from(DiagramStyle),
        orientation_kind=sampled_from(OrientationKind),
        diagram_objects=lists(builds(DiagramObject, **create_identified_object(include_runtime)), min_size=1, max_size=2)
    )


def create_diagram_object(include_runtime: bool = True):
    return builds(
        DiagramObject,
        **create_identified_object(include_runtime),
        diagram=builds(Diagram, **create_identified_object(include_runtime)),
        identified_object_mrid=text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        style=text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        rotation=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        diagram_object_points=lists(create_diagram_object_point(), min_size=1, max_size=2)
    )


def create_diagram_object_point():
    return builds(
        DiagramObjectPoint,
        x_position=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        y_position=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


######################
# IEC61970 BASE MEAS #
######################


def create_accumulator(include_runtime: bool = True):
    return builds(Accumulator, **create_measurement(include_runtime))


def create_accumulator_value(include_runtime: bool = True):
    return builds(AccumulatorValue, **create_measurement(include_runtime))


def create_analog(include_runtime: bool = True):
    return builds(
        Analog,
        **create_measurement(include_runtime),
        positive_flow_in=booleans()
    )


def create_analog_value(include_runtime: bool = True):
    return builds(AnalogValue, **create_measurement(include_runtime))


def create_control(include_runtime: bool = True):
    return builds(
        Control,
        **create_io_point(include_runtime),
        power_system_resource_mrid=text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        remote_control=builds(RemoteControl, **create_identified_object(include_runtime))
    )


def create_discrete(include_runtime: bool = True):
    return builds(Discrete, **create_measurement(include_runtime))


def create_discrete_value(include_runtime: bool = True):
    return builds(DiscreteValue, **create_measurement(include_runtime))


def create_io_point(include_runtime: bool):
    return {**create_identified_object(include_runtime)}


def create_measurement(include_runtime: bool):
    return {
        **create_identified_object(include_runtime),
        "remote_source": builds(RemoteSource, **create_identified_object(include_runtime)),
        "power_system_resource_mrid": uuids(version=4).map(lambda x: str(x)),
        "terminal_mrid": uuids(version=4).map(lambda x: str(x)),
        "phases": sampled_phase_code(),
        "unit_symbol": sampled_unit_symbol()
    }


def sampled_unit_symbol():
    return sampled_from(UnitSymbol)


############################
# IEC61970 Base Protection #
############################


def create_current_relay(include_runtime: bool = True):
    return builds(
        CurrentRelay,
        **create_protection_relay_function(include_runtime),
        current_limit_1=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        inverse_time_flag=boolean_or_none(),
        time_delay_1=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def create_distance_relay(include_runtime: bool = True):
    return builds(
        DistanceRelay,
        **create_protection_relay_function(include_runtime),
        backward_blind=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        backward_reach=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        backward_reactance=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        forward_blind=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        forward_reach=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        forward_reactance=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        operation_phase_angle1=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        operation_phase_angle2=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        operation_phase_angle3=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def create_voltage_relay(include_runtime: bool = True):
    return builds(
        VoltageRelay,
        **create_protection_relay_function(include_runtime),
    )


def boolean_or_none():
    return sampled_from([False, True, None])


def create_protection_relay_function(include_runtime: bool = True):
    return {
        **create_power_system_resource(include_runtime),
        "model": text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        "reclosing": boolean_or_none(),
        "relay_delay_time": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "protection_kind": sampled_from(ProtectionKind),
        "directable": boolean_or_none(),
        "power_direction": sampled_from(PowerDirectionKind),
        "sensors": lists(builds(CurrentTransformer), max_size=2),
        "protected_switches": lists(builds(Breaker), max_size=2),
        "schemes": lists(builds(ProtectionRelayScheme), max_size=2),
        "time_limits": lists(floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), min_size=4, max_size=4),
        "thresholds": lists(builds(RelaySetting, unit_symbol=sampled_unit_symbol(), value=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                                   name=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)), min_size=4, max_size=4),
        "relay_info": builds(RelayInfo)
    }


def create_protection_relay_scheme(include_runtime: bool = True):
    return builds(
        ProtectionRelayScheme,
        **create_identified_object(include_runtime),
        system=builds(ProtectionRelaySystem),
        functions=lists(builds(CurrentRelay))
    )


def create_protection_relay_system(include_runtime: bool = True):
    return builds(
        ProtectionRelaySystem,
        **create_equipment(include_runtime),
        protection_kind=sampled_from(ProtectionKind),
        schemes=lists(builds(ProtectionRelayScheme))
    )


#######################
# IEC61970 BASE SCADA #
#######################

def create_remote_control(include_runtime: bool = True):
    return builds(
        RemoteControl,
        **create_remote_point(include_runtime),
        control=builds(Control, **create_identified_object(include_runtime))
    )


def create_remote_point(include_runtime: bool):
    return {**create_identified_object(include_runtime)}


def create_remote_source(include_runtime: bool = True):
    return builds(
        RemoteSource,
        **create_remote_point(include_runtime),
        measurement=sampled_measurement(include_runtime)
    )


#############################################
# IEC61970 BASE WIRES GENERATION PRODUCTION #
#############################################


def sampled_battery_state_kind():
    return sampled_from(BatteryStateKind)


def create_battery_unit(include_runtime: bool = True):
    return builds(
        BatteryUnit,
        **create_power_electronics_unit(include_runtime),
        battery_state=sampled_battery_state_kind(),
        rated_e=integers(min_value=MIN_64_BIT_INTEGER, max_value=MAX_64_BIT_INTEGER),
        stored_e=integers(min_value=MIN_64_BIT_INTEGER, max_value=MAX_64_BIT_INTEGER)
    )


def create_photovoltaic_unit(include_runtime: bool = True):
    return builds(PhotoVoltaicUnit, **create_power_electronics_unit(include_runtime))


def create_power_electronics_unit(include_runtime: bool):
    return {
        **create_equipment(include_runtime),
        "power_electronics_connection": builds(PowerElectronicsConnection, **create_identified_object(include_runtime)),
        "max_p": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "min_p": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
    }


def create_power_electronics_wind_unit(include_runtime: bool = True):
    return builds(PowerElectronicsWindUnit, **create_power_electronics_unit(include_runtime))


#######################
# IEC61970 BASE WIRES #
#######################


def create_ac_line_segment(include_runtime: bool = True):
    return builds(
        AcLineSegment,
        **create_conductor(include_runtime),
        per_length_sequence_impedance=builds(PerLengthSequenceImpedance, **create_identified_object(include_runtime))
    )


def create_breaker(include_runtime: bool = True):
    return builds(
        Breaker,
        **create_protected_switch(include_runtime),
        in_transit_time=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def create_busbar_section(include_runtime: bool = True):
    return builds(BusbarSection, **create_connector(include_runtime))


def create_conductor(include_runtime: bool):
    return {
        **create_conducting_equipment(include_runtime),
        "asset_info": sampled_wire_info(include_runtime),
        "length": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    }


def create_connector(include_runtime: bool):
    return {**create_conducting_equipment(include_runtime)}


def create_disconnector(include_runtime: bool = True):
    return builds(Disconnector, **create_switch(include_runtime))


def create_energy_connection(include_runtime: bool):
    return {**create_conducting_equipment(include_runtime)}


def create_energy_consumer(include_runtime: bool = True):
    return builds(
        EnergyConsumer,
        **create_energy_connection(include_runtime),
        energy_consumer_phases=lists(
            builds(
                EnergyConsumerPhase,
                **create_identified_object(include_runtime),
                phase=sampled_single_phase_kind()
            ),
            min_size=1,
            max_size=2
        ),
        customer_count=integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
        grounded=booleans(),
        p=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        p_fixed=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        phase_connection=sampled_phase_shunt_connection_kind(),
        q=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        q_fixed=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def create_energy_consumer_phase(include_runtime: bool = True):
    return builds(
        EnergyConsumerPhase,
        **create_power_system_resource(include_runtime),
        energy_consumer=builds(EnergyConsumer, **create_identified_object(include_runtime)),
        phase=sampled_single_phase_kind(),
        p=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        p_fixed=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        q=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        q_fixed=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def create_energy_source(include_runtime: bool = True):
    return builds(
        EnergySource,
        **create_energy_connection(include_runtime),
        energy_source_phases=lists(
            builds(
                EnergySourcePhase,
                **create_identified_object(include_runtime),
                phase=sampled_single_phase_kind()
            ),
            min_size=1,
            max_size=2),
        active_power=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        reactive_power=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        voltage_angle=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        voltage_magnitude=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        r=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        p_max=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        p_min=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        r0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        rn=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        xn=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        is_external_grid=booleans(),
        r_min=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        rn_min=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        r0_min=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x_min=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        xn_min=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x0_min=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        r_max=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        rn_max=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        r0_max=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x_max=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        xn_max=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x0_max=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def create_energy_source_phase(include_runtime: bool = True):
    return builds(
        EnergySourcePhase,
        **create_power_system_resource(include_runtime),
        energy_source=builds(EnergySource, **create_identified_object(include_runtime)),
        phase=sampled_single_phase_kind()
    )


def create_fuse(include_runtime: bool = True):
    return builds(
        Fuse,
        **create_switch(include_runtime),
        function=builds(DistanceRelay)
    )


def create_ground(include_runtime: bool = True):
    return builds(
        Ground,
        **create_equipment(include_runtime)
    )


def create_ground_disconnector(include_runtime: bool = True):
    return builds(
        GroundDisconnector,
        **create_switch(include_runtime)
    )


def create_jumper(include_runtime: bool = True):
    return builds(Jumper, **create_switch(include_runtime))


def create_junction(include_runtime: bool = True):
    return builds(Junction, **create_connector(include_runtime))


def create_line(include_runtime: bool):
    return {**create_equipment_container(include_runtime)}


def create_linear_shunt_compensator(include_runtime: bool = True):
    return builds(
        LinearShuntCompensator,
        **create_shunt_compensator(include_runtime),
        b0_per_section=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        b_per_section=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        g0_per_section=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        g_per_section=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def create_series_compensator(include_runtime: bool = True):
    return builds(
        SeriesCompensator,
        **create_conducting_equipment(include_runtime),
        r=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        r0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        varistor_rated_current=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        varistor_voltage_threshold=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    )


def create_load_break_switch(include_runtime: bool = True):
    return builds(LoadBreakSwitch, **create_protected_switch(include_runtime))


def create_per_length_impedance(include_runtime: bool):
    return {**create_per_length_line_parameter(include_runtime)}


def create_per_length_line_parameter(include_runtime: bool):
    return {**create_identified_object(include_runtime)}


def create_per_length_sequence_impedance(include_runtime: bool = True):
    return builds(
        PerLengthSequenceImpedance,
        **create_per_length_impedance(include_runtime),
        r=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        r0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        bch=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        gch=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        b0ch=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        g0ch=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def sampled_phase_shunt_connection_kind():
    return sampled_from(PhaseShuntConnectionKind)


def create_power_electronics_connection(include_runtime: bool = True):
    return builds(
        PowerElectronicsConnection,
        **create_regulating_cond_eq(include_runtime),
        power_electronics_units=lists(builds(BatteryUnit, **create_identified_object(include_runtime)), min_size=1, max_size=2),
        power_electronics_connection_phases=lists(builds(PowerElectronicsConnectionPhase, **create_identified_object(include_runtime)), min_size=1, max_size=2),
        max_i_fault=integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
        max_q=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        min_q=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        p=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        q=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        rated_s=integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
        rated_u=integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
        inverter_standard=text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        sustain_op_overvolt_limit=integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
        stop_at_over_freq=floats(min_value=51.0, max_value=52.0),
        stop_at_under_freq=floats(min_value=47.0, max_value=49.0),
        inv_volt_watt_resp_mode=boolean_or_none(),
        inv_watt_resp_v1=integers(min_value=200, max_value=300),
        inv_watt_resp_v2=integers(min_value=216, max_value=230),
        inv_watt_resp_v3=integers(min_value=235, max_value=255),
        inv_watt_resp_v4=integers(min_value=244, max_value=265),
        inv_watt_resp_p_at_v1=floats(min_value=0.0, max_value=1.0),
        inv_watt_resp_p_at_v2=floats(min_value=0.0, max_value=1.0),
        inv_watt_resp_p_at_v3=floats(min_value=0.0, max_value=1.0),
        inv_watt_resp_p_at_v4=floats(min_value=0.0, max_value=0.2),
        inv_volt_var_resp_mode=boolean_or_none(),
        inv_var_resp_v1=integers(min_value=200, max_value=300),
        inv_var_resp_v2=integers(min_value=200, max_value=300),
        inv_var_resp_v3=integers(min_value=200, max_value=300),
        inv_var_resp_v4=integers(min_value=200, max_value=300),
        inv_var_resp_q_at_v1=floats(min_value=0.0, max_value=0.6),
        inv_var_resp_q_at_v2=floats(min_value=-1.0, max_value=1.0),
        inv_var_resp_q_at_v3=floats(min_value=-1.0, max_value=1.0),
        inv_var_resp_q_at_v4=floats(min_value=-0.6, max_value=0.0),
        inv_reactive_power_mode=boolean_or_none(),
        inv_fix_reactive_power=floats(min_value=-1.0, max_value=1.0),
    )


def create_power_electronics_connection_phase(include_runtime: bool = True):
    return builds(
        PowerElectronicsConnectionPhase,
        **create_power_system_resource(include_runtime),
        power_electronics_connection=builds(PowerElectronicsConnection, **create_identified_object(include_runtime)),
        phase=sampled_single_phase_kind(),
        p=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        q=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def create_power_transformer(include_runtime: bool = True):
    return builds(
        PowerTransformer,
        **create_conducting_equipment(include_runtime),
        asset_info=builds(PowerTransformerInfo, **create_identified_object(include_runtime)),
        power_transformer_ends=lists(builds(PowerTransformerEnd, **create_identified_object(include_runtime)), min_size=1, max_size=2),
        vector_group=sampled_vector_group(),
        transformer_utilisation=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def create_power_transformer_end(include_runtime: bool = True):
    return builds(
        create_power_transformer_end_with_ratings,
        **create_transformer_end(include_runtime),
        power_transformer=builds(PowerTransformer, **create_identified_object(include_runtime)),
        # rated_s=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        rated_u=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        r=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        r0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        connection_kind=sampled_winding_connection_kind(),
        b=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        b0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        g=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        g0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        phase_angle_clock=integers(min_value=0, max_value=11),
        ratings=lists(builds(
            TransformerEndRatedS,
            cooling_type=sampled_from(TransformerCoolingType),
            rated_s=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
        ), min_size=0, max_size=11, unique_by=lambda it: it.cooling_type)
    )


def create_power_transformer_end_with_ratings(ratings: List[TransformerEndRatedS], **kwargs):
    # This is needed as we purposely made it so you can't build a transformer end with multiple ratings through constructor
    pte = PowerTransformerEnd(**kwargs)
    if ratings:
        for rating in ratings:
            pte.add_transformer_end_rated_s(rating)
    return pte


def create_protected_switch(include_runtime: bool):
    return {
        **create_switch(include_runtime),
        "breaking_capacity": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "relay_functions": lists(builds(CurrentRelay), min_size=1, max_size=2)
    }


def create_ratio_tap_changer(include_runtime: bool = True):
    return builds(
        RatioTapChanger,
        **create_tap_changer(include_runtime),
        transformer_end=builds(PowerTransformerEnd, **create_identified_object(include_runtime)),
        step_voltage_increment=floats(min_value=0.0, max_value=1.0)
    )


def create_recloser(include_runtime: bool = True):
    return builds(Recloser, **create_protected_switch(include_runtime))


def create_regulating_cond_eq(include_runtime: bool):
    return {
        **create_energy_connection(include_runtime),
        "control_enabled": booleans(),
        "regulating_control": builds(TapChangerControl, **create_identified_object(include_runtime)),
    }


def create_regulating_control(include_runtime: bool):
    return {
        **create_power_system_resource(include_runtime),
        "discrete": boolean_or_none(),
        "mode": sampled_from(RegulatingControlModeKind),
        "monitored_phase": sampled_phase_code(),
        "target_deadband": floats(min_value=0.0, max_value=FLOAT_MAX),
        "target_value": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "enabled": boolean_or_none(),
        "max_allowed_target_value": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "min_allowed_target_value": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "rated_current": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "terminal": builds(Terminal, **create_identified_object(include_runtime)),
        "regulating_conducting_equipment": lists(builds(PowerElectronicsConnection, **create_identified_object(include_runtime)))
    }


def create_tap_changer_control(include_runtime: bool = True):
    return builds(
        TapChangerControl,
        **create_regulating_control(include_runtime),
        limit_voltage=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        line_drop_compensation=boolean_or_none(),
        line_drop_r=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        line_drop_x=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        reverse_line_drop_r=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        reverse_line_drop_x=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        forward_ldc_blocking=boolean_or_none(),
        time_delay=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        co_generation_enabled=boolean_or_none()
    )


def create_shunt_compensator(include_runtime: bool):
    return {
        **create_regulating_cond_eq(include_runtime),
        "asset_info": builds(ShuntCompensatorInfo, **create_identified_object(include_runtime)),
        "sections": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "grounded": booleans(),
        "nom_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "phase_connection": sampled_phase_shunt_connection_kind()
    }


def sampled_single_phase_kind():
    return sampled_from(SinglePhaseKind)


def create_switch(include_runtime: bool):
    return {
        **create_conducting_equipment(include_runtime),
        "rated_current": integers(min_value=1, max_value=MAX_32_BIT_INTEGER),
        # NOTE: These are not currently encoded properly in protobuf so we can only use all or none.
        "_normally_open": sampled_from([0, 15]),
        "_open": sampled_from([0, 15])
        # "_normally_open": integers(min_value=0, max_value=15),
        # "_open": integers(min_value=0, max_value=15)
    }


def create_tap_changer(include_runtime: bool):
    return {
        **create_power_system_resource(include_runtime),
        "high_step": integers(min_value=10, max_value=15),
        "low_step": integers(min_value=0, max_value=2),
        "step": floats(min_value=2.0, max_value=10.0),
        "neutral_step": integers(min_value=2, max_value=10),
        "neutral_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "normal_step": integers(min_value=2, max_value=10),
        "control_enabled": booleans(),
        "tap_changer_control": builds(TapChangerControl, **create_identified_object(include_runtime))
    }


def create_transformer_end(include_runtime: bool):
    return {
        **create_identified_object(include_runtime),
        "terminal": builds(Terminal, **create_identified_object(include_runtime)),
        "base_voltage": builds(BaseVoltage, **create_identified_object(include_runtime)),
        "ratio_tap_changer": builds(RatioTapChanger, **create_identified_object(include_runtime)),
        "end_number": integers(min_value=MIN_SEQUENCE_NUMBER, max_value=MAX_END_NUMBER),
        "grounded": booleans(),
        "r_ground": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "x_ground": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "star_impedance": builds(TransformerStarImpedance, **create_identified_object(include_runtime))
    }


def create_transformer_star_impedance(include_runtime: bool = True):
    return builds(
        TransformerStarImpedance,
        **create_identified_object(include_runtime),
        r=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        r0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        transformer_end_info=builds(TransformerEndInfo, **create_identified_object(include_runtime))
    )


def sampled_vector_group():
    return sampled_from(VectorGroup)


def sampled_winding_connection_kind():
    return sampled_from(WindingConnection)


#########################
# IEC61970 INF IEC61970 #
#########################


def create_circuit(include_runtime: bool = True):
    return builds(
        Circuit,
        **create_line(include_runtime),
        loop=builds(Loop, **create_identified_object(include_runtime)),
        end_terminals=lists(builds(Terminal, **create_identified_object(include_runtime)), min_size=1, max_size=2),
        end_substations=lists(builds(Substation, **create_identified_object(include_runtime)), min_size=1, max_size=2)
    )


def create_loop(include_runtime: bool = True):
    return builds(
        Loop,
        **create_identified_object(include_runtime),
        circuits=lists(builds(Circuit, **create_identified_object(include_runtime)), min_size=1, max_size=2),
        substations=lists(builds(Substation, **create_identified_object(include_runtime)), min_size=1, max_size=2),
        energizing_substations=lists(builds(Substation, **create_identified_object(include_runtime)), min_size=1, max_size=2)
    )


def create_lv_feeder(include_runtime: bool = True):
    runtime = {
        "normal_energizing_feeders": lists(builds(Feeder, **create_identified_object(include_runtime)), min_size=1, max_size=2),
        "current_equipment": lists(sampled_equipment(include_runtime), min_size=1, max_size=2)
    } if include_runtime else {}

    return builds(
        LvFeeder,
        **create_equipment_container(include_runtime),
        normal_head_terminal=builds(Terminal, **create_identified_object(include_runtime)),
        **runtime
    )


#####################################################
# IEC61970 INFIEC61970 WIRES GENERATION PRODUCTION #
#####################################################

def create_ev_charging_unit(include_runtime: bool = True):
    return builds(EvChargingUnit, **create_power_electronics_unit(include_runtime))


#########
# MODEL #
#########


def traced_phases():
    return builds(
        TracedPhases,
        normal_status=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        current_status=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
    )


###############
# SAMPLE SETS #
###############


def sampled_wire_info(include_runtime: bool):
    return choice([
        builds(OverheadWireInfo, **create_identified_object(include_runtime)),
        builds(CableInfo, **create_identified_object(include_runtime)),
    ])


def sampled_conducting_equipment(include_runtime: bool):
    return choice([
        # Don't add EnergySource to this list as it's used in SetPhases to start tracing, which will cause test_schema_terminal to fail.
        builds(AcLineSegment, **create_identified_object(include_runtime)),
        builds(PowerTransformer, **create_identified_object(include_runtime)),
        builds(Breaker, **create_identified_object(include_runtime)),
        builds(Disconnector, **create_identified_object(include_runtime)),
        builds(EnergyConsumer, **create_identified_object(include_runtime)),
    ])


def sampled_equipment(include_runtime: bool):
    return choice([
        builds(AcLineSegment, **create_identified_object(include_runtime)),
        builds(PowerTransformer, **create_identified_object(include_runtime)),
        builds(Breaker, **create_identified_object(include_runtime)),
        builds(Disconnector, **create_identified_object(include_runtime)),
        builds(EnergyConsumer, **create_identified_object(include_runtime)),
        builds(EnergySource, **create_identified_object(include_runtime)),
        builds(FaultIndicator, **create_identified_object(include_runtime))
    ])


def sampled_equipment_container(include_runtime: bool):
    available_containers = [
        builds(Site, **create_identified_object(include_runtime)),
        builds(Circuit, **create_identified_object(include_runtime)),
        builds(Substation, **create_identified_object(include_runtime))
    ]

    if include_runtime:
        available_containers.append(builds(Feeder, **create_identified_object(include_runtime)))

    return choice(available_containers)


def sampled_hvlv_feeder(include_runtime: bool):
    return choice([
        builds(Feeder, **create_identified_object(include_runtime)),
        builds(LvFeeder, **create_identified_object(include_runtime))
    ])


def sampled_measurement(include_runtime: bool):
    return choice([
        builds(Accumulator, **create_identified_object(include_runtime)),
        builds(Analog, **create_identified_object(include_runtime)),
        builds(Discrete, **create_identified_object(include_runtime)),
    ])


def sampled_protected_switches(include_runtime: bool):
    return choice([
        builds(Breaker, **create_identified_object(include_runtime)),
        builds(LoadBreakSwitch, **create_identified_object(include_runtime)),
        builds(Recloser, **create_identified_object(include_runtime))
    ])
