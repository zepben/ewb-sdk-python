#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = [
    'MIN_32_BIT_INTEGER', 'MAX_32_BIT_INTEGER', 'MAX_32_BIT_UNSIGNED_INTEGER', 'MAX_64_BIT_INTEGER', 'MIN_64_BIT_INTEGER', 'TEXT_MAX_SIZE', 'FLOAT_MIN',
    'FLOAT_MAX', 'MAX_END_NUMBER', 'MAX_SEQUENCE_NUMBER', 'MIN_SEQUENCE_NUMBER', 'ALPHANUM', 'create_relay_info', 'relay_info_kwargs', 'create_contact_details',
    'contact_details_kwargs', 'create_pan_demand_response_function', 'pan_demand_response_function_kwargs', 'create_hv_customer', 'hv_customer_kwargs',
    'create_site', 'site_kwargs', 'create_loop', 'loop_kwargs', 'create_lv_feeder', 'lv_feeder_kwargs', 'create_lv_substation', 'lv_substation_kwargs',
    'create_ev_charging_unit', 'ev_charging_unit_kwargs', 'create_directional_current_relay', 'directional_current_relay_kwargs', 'create_distance_relay',
    'distance_relay_kwargs', 'sampled_power_direction_kind', 'sampled_protection_kind', 'protection_relay_function_kwargs', 'create_protection_relay_scheme',
    'protection_relay_scheme_kwargs', 'create_protection_relay_system', 'protection_relay_system_kwargs', 'create_relay_setting', 'relay_setting_kwargs',
    'create_voltage_relay', 'voltage_relay_kwargs', 'create_battery_control', 'battery_control_kwargs', 'sampled_battery_control_mode',
    'sampled_transformer_cooling_type', 'create_power_transformer_end_with_ratings', 'sampled_vector_group', 'create_cable_info', 'cable_info_kwargs',
    'create_no_load_test', 'no_load_test_kwargs', 'create_open_circuit_test', 'open_circuit_test_kwargs', 'create_overhead_wire_info',
    'overhead_wire_info_kwargs', 'create_power_transformer_info', 'power_transformer_info_kwargs', 'create_short_circuit_test', 'short_circuit_test_kwargs',
    'create_shunt_compensator_info', 'shunt_compensator_info_kwargs', 'create_switch_info', 'switch_info_kwargs', 'create_transformer_end_info',
    'transformer_end_info_kwargs', 'create_transformer_tank_info', 'transformer_tank_info_kwargs', 'transformer_test_kwargs', 'wire_info_kwargs',
    'sampled_wire_material_kind', 'sampled_wire_insulation_kind', 'asset_kwargs', 'asset_container_kwargs', 'asset_function_kwargs', 'asset_info_kwargs',
    'asset_organisation_role_kwargs', 'create_asset_owner', 'asset_owner_kwargs', 'create_streetlight', 'streetlight_kwargs', 'structure_kwargs',
    'agreement_kwargs', 'document_kwargs', 'create_electronic_address', 'electronic_address_kwargs', 'create_location', 'location_kwargs',
    'create_organisation', 'organisation_kwargs', 'organisation_role_kwargs', 'create_position_point', 'position_point_kwargs', 'create_street_address',
    'street_address_kwargs', 'create_street_detail', 'street_detail_kwargs', 'create_telephone_number', 'telephone_number_kwargs', 'create_town_detail',
    'town_detail_kwargs', 'create_customer', 'customer_kwargs', 'create_customer_agreement', 'customer_agreement_kwargs', 'sampled_customer_kind',
    'create_pricing_structure', 'pricing_structure_kwargs', 'create_tariffs', 'tariffs_kwargs', 'create_current_transformer_info',
    'current_transformer_info_kwargs', 'create_potential_transformer_info', 'potential_transformer_info_kwargs', 'sampled_transformer_construction_kind',
    'sampled_transformer_function_kind', 'create_pole', 'pole_kwargs', 'sampled_streetlight_lamp_kind', 'create_ratio', 'ratio_kwargs',
    'create_controlled_appliance', 'controlled_appliance_kwargs', 'end_device_kwargs', 'end_device_function_kwargs', 'sampled_end_device_function_kind',
    'create_meter', 'meter_kwargs', 'create_usage_point', 'usage_point_kwargs', 'create_operational_restriction', 'operational_restriction_kwargs',
    'auxiliary_equipment_kwargs', 'create_current_transformer', 'current_transformer_kwargs', 'create_fault_indicator', 'fault_indicator_kwargs',
    'create_potential_transformer', 'potential_transformer_kwargs', 'sampled_potential_transformer_kind', 'sensor_kwargs', 'ac_dc_terminal_kwargs',
    'create_base_voltage', 'base_voltage_kwargs', 'conducting_equipment_kwargs', 'create_connectivity_node', 'connectivity_node_kwargs',
    'connectivity_node_container_kwargs', 'curve_kwargs', 'create_curve_data', 'curve_data_kwargs', 'equipment_kwargs', 'equipment_container_kwargs',
    'create_feeder', 'feeder_kwargs', 'create_geographical_region', 'geographical_region_kwargs', 'identified_object_kwargs', 'create_name', 'name_kwargs',
    'create_name_type', 'name_type_kwargs', 'sampled_phase_code', 'power_system_resource_kwargs', 'create_sub_geographical_region',
    'sub_geographical_region_kwargs', 'create_substation', 'substation_kwargs', 'create_terminal', 'terminal_kwargs', 'create_diagram', 'diagram_kwargs',
    'create_diagram_object', 'diagram_object_kwargs', 'create_diagram_object_point', 'diagram_object_point_kwargs', 'sampled_diagram_style',
    'sampled_orientation_kind', 'sampled_unit_symbol', 'create_equivalent_branch', 'equivalent_branch_kwargs', 'equivalent_equipment_kwargs',
    'sampled_battery_state_kind', 'create_battery_unit', 'battery_unit_kwargs', 'create_photo_voltaic_unit', 'photo_voltaic_unit_kwargs',
    'power_electronics_unit_kwargs', 'create_power_electronics_wind_unit', 'power_electronics_wind_unit_kwargs', 'create_accumulator', 'accumulator_kwargs',
    'create_accumulator_value', 'accumulator_value_kwargs', 'create_analog', 'analog_kwargs', 'create_analog_value', 'analog_value_kwargs', 'create_control',
    'control_kwargs', 'create_discrete', 'discrete_kwargs', 'create_discrete_value', 'discrete_value_kwargs', 'io_point_kwargs', 'measurement_kwargs',
    'measurement_value_kwargs', 'create_current_relay', 'current_relay_kwargs', 'create_remote_control', 'remote_control_kwargs', 'remote_point_kwargs',
    'create_remote_source', 'remote_source_kwargs', 'create_ac_line_segment', 'ac_line_segment_kwargs', 'create_ac_line_segment_phase',
    'ac_line_segment_phase_kwargs', 'create_breaker', 'breaker_kwargs', 'create_busbar_section', 'busbar_section_kwargs', 'create_clamp', 'clamp_kwargs',
    'conductor_kwargs', 'connector_kwargs', 'create_cut', 'cut_kwargs', 'create_disconnector', 'disconnector_kwargs', 'earth_fault_compensator_kwargs',
    'energy_connection_kwargs', 'create_energy_consumer', 'energy_consumer_kwargs', 'create_energy_consumer_phase', 'energy_consumer_phase_kwargs',
    'create_energy_source', 'energy_source_kwargs', 'create_energy_source_phase', 'energy_source_phase_kwargs', 'create_fuse', 'fuse_kwargs', 'create_ground',
    'ground_kwargs', 'create_ground_disconnector', 'ground_disconnector_kwargs', 'create_grounding_impedance', 'grounding_impedance_kwargs', 'create_jumper',
    'jumper_kwargs', 'create_junction', 'junction_kwargs', 'line_kwargs', 'create_linear_shunt_compensator', 'linear_shunt_compensator_kwargs',
    'create_load_break_switch', 'load_break_switch_kwargs', 'per_length_impedance_kwargs', 'per_length_line_parameter_kwargs',
    'create_per_length_phase_impedance', 'per_length_phase_impedance_kwargs', 'create_per_length_sequence_impedance', 'per_length_sequence_impedance_kwargs',
    'create_petersen_coil', 'petersen_coil_kwargs', 'create_phase_impedance_data', 'phase_impedance_data_kwargs', 'sampled_phase_shunt_connection_kind',
    'create_power_electronics_connection', 'power_electronics_connection_kwargs', 'create_power_electronics_connection_phase',
    'power_electronics_connection_phase_kwargs', 'create_power_transformer', 'power_transformer_kwargs', 'create_power_transformer_end',
    'power_transformer_end_kwargs', 'protected_switch_kwargs', 'create_ratio_tap_changer', 'ratio_tap_changer_kwargs', 'create_reactive_capability_curve',
    'reactive_capability_curve_kwargs', 'create_recloser', 'recloser_kwargs', 'regulating_cond_eq_kwargs', 'regulating_control_kwargs',
    'sampled_regulating_control_mode_kind', 'rotating_machine_kwargs', 'create_series_compensator', 'series_compensator_kwargs', 'shunt_compensator_kwargs',
    'sampled_single_phase_kind', 'create_static_var_compensator', 'static_var_compensator_kwargs', 'sampled_svc_control_mode', 'switch_kwargs',
    'create_synchronous_machine', 'synchronous_machine_kwargs', 'sampled_synchronous_machine_kind', 'tap_changer_kwargs', 'create_tap_changer_control',
    'tap_changer_control_kwargs', 'transformer_end_kwargs', 'create_transformer_star_impedance', 'transformer_star_impedance_kwargs',
    'sampled_winding_connection', 'create_circuit', 'circuit_kwargs', 'sampled_wire_info', 'sampled_conducting_equipment', 'sampled_curves',
    'sampled_end_device_function', 'sampled_equipment', 'sampled_equipment_container', 'sampled_hvlv_feeder', 'sampled_measurement',
    'sampled_protected_switches'
]

from datetime import datetime
from random import choice

from streaming.get.pb_creators import lists, floats
from util import mrid_strategy
# @formatter:off

# This must be above hypothesis.strategies to avoid conflicting import with zepben.ewb.util.none
from zepben.ewb import *

from hypothesis.strategies import builds, text, integers, sampled_from, booleans, uuids, datetimes, one_of, none
from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_substation import LvSubstation
from zepben.ewb.model.cim.iec61968.assetinfo.wire_insulation_kind import WireInsulationKind
from zepben.ewb.model.cim.iec61970.base.wires.ac_line_segment_phase import AcLineSegmentPhase

# @formatter:on

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


##################################
# Extensions IEC61968 Asset Info #
##################################

def create_relay_info(include_runtime: bool = True):
    return builds(RelayInfo, **relay_info_kwargs(include_runtime))


def relay_info_kwargs(include_runtime: bool = True):
    return {
        **asset_info_kwargs(include_runtime),
        "curve_setting": text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        "reclose_delays": lists(floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "reclose_fast": one_of(none(), booleans()),
    }


##############################
# Extensions IEC61968 Common #
##############################

def create_contact_details():
    return builds(ContactDetails, **contact_details_kwargs())


def contact_details_kwargs():
    return {
        "id": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE, min_size=1),
        "contact_address": create_street_address(),
        "contact_type": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
        "first_name": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
        "last_name": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
        "preferred_contact_method": sampled_from(ContactMethodType),
        "is_primary": one_of(none(), booleans()),
        "business_name": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
        "phone_numbers": one_of(none(), lists(create_telephone_number())),
        "electronic_addresses": one_of(none(), lists(create_electronic_address())),
    }


################################
# Extensions IEC61968 Metering #
################################

def create_pan_demand_response_function(include_runtime: bool = True):
    return builds(PanDemandResponseFunction, **pan_demand_response_function_kwargs(include_runtime))


def pan_demand_response_function_kwargs(include_runtime: bool = True):
    return {
        **end_device_function_kwargs(include_runtime),
        "kind": sampled_from(EndDeviceFunctionKind),
        "appliances": integers(min_value=0, max_value=4095),
    }


#################################
# Extensions IEC61970 Base Core #
#################################

def create_hv_customer(include_runtime: bool = True):
    return builds(Site, **hv_customer_kwargs(include_runtime))


def hv_customer_kwargs(include_runtime: bool = True):
    return {
        **equipment_container_kwargs(include_runtime)
    }


def create_site(include_runtime: bool = True):
    return builds(Site, **site_kwargs(include_runtime))


def site_kwargs(include_runtime: bool = True):
    return {
        **equipment_container_kwargs(include_runtime)
    }


###################################
# Extensions IEC61970 Base Feeder #
###################################

def create_loop(include_runtime: bool = True):
    return builds(Loop, **loop_kwargs(include_runtime))


def loop_kwargs(include_runtime: bool = True):
    return {
        **identified_object_kwargs(include_runtime),
        "circuits": lists(builds(Circuit, **identified_object_kwargs(include_runtime)), max_size=2),
        "substations": lists(builds(Substation, **identified_object_kwargs(include_runtime)), max_size=2),
        "energizing_substations": lists(builds(Substation, **identified_object_kwargs(include_runtime)), max_size=2),
    }


def create_lv_feeder(include_runtime: bool = True):
    return builds(LvFeeder, **lv_feeder_kwargs(include_runtime))


def lv_feeder_kwargs(include_runtime: bool = True):
    runtime = {
        "normal_energizing_feeders": lists(builds(Feeder, **identified_object_kwargs(include_runtime)), max_size=2),
        "current_equipment": lists(sampled_equipment(include_runtime), max_size=2),
        "current_energizing_feeders": lists(builds(Feeder, **identified_object_kwargs(include_runtime)), max_size=2),
        "normal_energizing_lv_substation": builds(LvSubstation, **identified_object_kwargs(include_runtime)),
    } if include_runtime else {}

    return {
        # Only include equipment if we are processing runtime as we don't write equipment to the database for LvFeeder.
        **equipment_container_kwargs(include_runtime, add_equipment=include_runtime),
        "normal_head_terminal": builds(Terminal, **identified_object_kwargs(include_runtime)),
        **runtime,
    }


def create_lv_substation(include_runtime: bool = True):
    return builds(LvSubstation, **lv_substation_kwargs(include_runtime))


def lv_substation_kwargs(include_runtime: bool = True):
    runtime = {
        "normal_energizing_feeders": one_of(none(), lists(builds(Feeder, **identified_object_kwargs(include_runtime)), max_size=2)),
        "current_energizing_feeders": one_of(none(), lists(builds(Feeder, **identified_object_kwargs(include_runtime)), max_size=2)),
        "normal_energized_lv_feeders": one_of(none(), lists(builds(LvFeeder, **identified_object_kwargs(include_runtime)))),
    } if include_runtime else {}

    return {
        **equipment_container_kwargs(include_runtime, add_equipment=include_runtime),
        **runtime,
    }


##################################################
# Extensions IEC61970 Base Generation Production #
##################################################

def create_ev_charging_unit(include_runtime: bool = True):
    return builds(EvChargingUnit, **ev_charging_unit_kwargs(include_runtime))


def ev_charging_unit_kwargs(include_runtime: bool = True):
    return {
        **power_electronics_unit_kwargs(include_runtime)
    }


#######################################
# Extensions IEC61970 Base Protection #
#######################################

def create_directional_current_relay(include_runtime: bool = True):
    return builds(DirectionalCurrentRelay, **directional_current_relay_kwargs(include_runtime))


def directional_current_relay_kwargs(include_runtime: bool = True):
    return {
        **protection_relay_function_kwargs(include_runtime),
        "directional_characteristic_angle": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "polarizing_quantity_type": sampled_from(PolarizingQuantityType),
        "relay_element_phase": sampled_from(PhaseCode),
        "minimum_pickup_current": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "current_limit_1": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "inverse_time_flag": one_of(none(), booleans()),
        "time_delay_1": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
    }


def create_distance_relay(include_runtime: bool = True):
    return builds(DistanceRelay, **distance_relay_kwargs(include_runtime))


def distance_relay_kwargs(include_runtime: bool = True):
    return {
        **protection_relay_function_kwargs(include_runtime),
        "backward_blind": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "backward_reach": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "backward_reactance": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "forward_blind": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "forward_reach": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "forward_reactance": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "operation_phase_angle1": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "operation_phase_angle2": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "operation_phase_angle3": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
    }


def sampled_power_direction_kind():
    return sampled_from(PowerDirectionKind)


def sampled_protection_kind():
    return sampled_from(ProtectionKind)


def protection_relay_function_kwargs(include_runtime: bool = True):
    return {
        **power_system_resource_kwargs(include_runtime),
        "model": text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        "reclosing": one_of(none(), booleans()),
        "relay_delay_time": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "protection_kind": sampled_protection_kind(),
        "directable": one_of(none(), booleans()),
        "power_direction": sampled_power_direction_kind(),
        "sensors": lists(builds(CurrentTransformer, mrid=mrid_strategy), max_size=2),
        "protected_switches": lists(builds(Breaker, mrid=mrid_strategy), max_size=2),
        "schemes": lists(builds(ProtectionRelayScheme, mrid=mrid_strategy), max_size=2),
        "time_limits": lists(floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), min_size=4, max_size=4),
        "thresholds": lists(create_relay_setting(), min_size=4, max_size=4),
        "asset_info": builds(RelayInfo, mrid=mrid_strategy),
    }


def create_protection_relay_scheme(include_runtime: bool = True):
    return builds(ProtectionRelayScheme, **protection_relay_scheme_kwargs(include_runtime))


def protection_relay_scheme_kwargs(include_runtime: bool = True):
    return {
        **identified_object_kwargs(include_runtime),
        "system": builds(ProtectionRelaySystem, mrid=mrid_strategy),
        "functions": lists(builds(CurrentRelay, mrid=mrid_strategy)),
    }


def create_protection_relay_system(include_runtime: bool = True):
    return builds(ProtectionRelaySystem, **protection_relay_system_kwargs(include_runtime))


def protection_relay_system_kwargs(include_runtime: bool = True):
    return {
        **equipment_kwargs(include_runtime),
        "protection_kind": sampled_protection_kind(),
        "schemes": lists(builds(ProtectionRelayScheme, mrid=mrid_strategy)),
    }


def create_relay_setting():
    return builds(RelaySetting, **relay_setting_kwargs())


def relay_setting_kwargs():
    return {
        "unit_symbol": sampled_unit_symbol(),
        "value": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    }


def create_voltage_relay(include_runtime: bool = True):
    return builds(VoltageRelay, **voltage_relay_kwargs(include_runtime))


def voltage_relay_kwargs(include_runtime: bool = True):
    return {
        **protection_relay_function_kwargs(include_runtime),
    }


##################################
# Extensions IEC61970 Base Wires #
##################################

def create_battery_control(include_runtime: bool = True):
    return builds(BatteryControl, **battery_control_kwargs(include_runtime))


def battery_control_kwargs(include_runtime: bool = True):
    return {
        **regulating_control_kwargs(include_runtime),
        "charging_rate": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "discharging_rate": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "reserve_percent": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "control_mode": sampled_battery_control_mode(),
    }


def sampled_battery_control_mode():
    return sampled_from(BatteryControlMode)


def sampled_transformer_cooling_type():
    return sampled_from(TransformerCoolingType)


def create_power_transformer_end_with_ratings(ratings: List[TransformerEndRatedS], **kwargs):
    # This is needed as we purposely made it so you can't build a transformer end with multiple ratings through constructor
    pte = PowerTransformerEnd(**kwargs)
    if ratings:
        for rating in ratings:
            pte.add_transformer_end_rated_s(rating)
    return pte


def sampled_vector_group():
    return sampled_from(VectorGroup)


#######################
# IEC61968 Asset Info #
#######################


def create_cable_info(include_runtime: bool = True):
    return builds(CableInfo, **cable_info_kwargs(include_runtime))


def cable_info_kwargs(include_runtime: bool = True):
    return {
        **wire_info_kwargs(include_runtime)
    }


def create_no_load_test(include_runtime: bool = True):
    return builds(NoLoadTest, **no_load_test_kwargs(include_runtime))


def no_load_test_kwargs(include_runtime: bool = True):
    return {
        **transformer_test_kwargs(include_runtime),
        "energised_end_voltage": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "exciting_current": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "exciting_current_zero": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "loss": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "loss_zero": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    }


def create_open_circuit_test(include_runtime: bool = True):
    return builds(OpenCircuitTest, **open_circuit_test_kwargs(include_runtime))


def open_circuit_test_kwargs(include_runtime: bool = True):
    return {
        **transformer_test_kwargs(include_runtime),
        "energised_end_step": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "energised_end_voltage": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "open_end_step": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "open_end_voltage": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "phase_shift": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    }


def create_overhead_wire_info(include_runtime: bool = True):
    return builds(OverheadWireInfo, **overhead_wire_info_kwargs(include_runtime))


def overhead_wire_info_kwargs(include_runtime: bool = True):
    return {
        **wire_info_kwargs(include_runtime)
    }


def create_power_transformer_info(include_runtime: bool = True):
    return builds(PowerTransformerInfo, **power_transformer_info_kwargs(include_runtime))


def power_transformer_info_kwargs(include_runtime: bool = True):
    return {
        **asset_info_kwargs(include_runtime),
        "transformer_tank_infos": lists(builds(TransformerTankInfo, **identified_object_kwargs(include_runtime)), max_size=2),
    }


def create_short_circuit_test(include_runtime: bool = True):
    return builds(ShortCircuitTest, **short_circuit_test_kwargs(include_runtime))


def short_circuit_test_kwargs(include_runtime: bool = True):
    return {
        **transformer_test_kwargs(include_runtime),
        "current": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "energised_end_step": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "grounded_end_step": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "leakage_impedance": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "leakage_impedance_zero": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "loss": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "loss_zero": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "power": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "voltage": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "voltage_ohmic_part": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    }


def create_shunt_compensator_info(include_runtime: bool = True):
    return builds(ShuntCompensatorInfo, **shunt_compensator_info_kwargs(include_runtime))


def shunt_compensator_info_kwargs(include_runtime: bool = True):
    return {
        **asset_info_kwargs(include_runtime),
        "max_power_loss": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "rated_current": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "rated_reactive_power": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "rated_voltage": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    }


def create_switch_info(include_runtime: bool = True):
    return builds(SwitchInfo, **switch_info_kwargs(include_runtime))


def switch_info_kwargs(include_runtime: bool = True):
    return {
        **asset_info_kwargs(include_runtime),
        "rated_interrupting_time": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    }


def create_transformer_end_info(include_runtime: bool = True):
    return builds(TransformerEndInfo, **transformer_end_info_kwargs(include_runtime))


def transformer_end_info_kwargs(include_runtime: bool = True):
    return {
        **asset_info_kwargs(include_runtime),
        "connection_kind": sampled_winding_connection(),
        "emergency_s": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "end_number": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "insulation_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "phase_angle_clock": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "rated_s": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "rated_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "short_term_s": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "transformer_tank_info": builds(TransformerTankInfo, **identified_object_kwargs(include_runtime)),
        "transformer_star_impedance": builds(TransformerStarImpedance, **identified_object_kwargs(include_runtime)),
        "energised_end_no_load_tests": builds(NoLoadTest, **identified_object_kwargs(include_runtime)),
        "energised_end_short_circuit_tests": builds(ShortCircuitTest, **identified_object_kwargs(include_runtime)),
        "grounded_end_short_circuit_tests": builds(ShortCircuitTest, **identified_object_kwargs(include_runtime)),
        "open_end_open_circuit_tests": builds(OpenCircuitTest, **identified_object_kwargs(include_runtime)),
        "energised_end_open_circuit_tests": builds(OpenCircuitTest, **identified_object_kwargs(include_runtime)),
    }


def create_transformer_tank_info(include_runtime: bool = True):
    return builds(TransformerTankInfo, **transformer_tank_info_kwargs(include_runtime))


def transformer_tank_info_kwargs(include_runtime: bool = True):
    return {
        **asset_info_kwargs(include_runtime),
        "power_transformer_info": builds(PowerTransformerInfo, **identified_object_kwargs(include_runtime)),
        "transformer_end_infos": lists(builds(TransformerEndInfo, **identified_object_kwargs(include_runtime)), max_size=2),
    }


def transformer_test_kwargs(include_runtime: bool):
    return {
        **identified_object_kwargs(include_runtime),
        "base_power": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "temperature": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    }


def wire_info_kwargs(include_runtime: bool):
    return {
        **asset_info_kwargs(include_runtime),
        "rated_current": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "material": sampled_wire_material_kind(),
        "size_description": one_of(none(), text(alphabet=ALPHANUM)),
        "strand_count": one_of(none(), text(alphabet=ALPHANUM)),
        "core_strand_count": one_of(none(), text(alphabet=ALPHANUM)),
        "insulated": booleans(),
        "insulation_material": sampled_wire_insulation_kind(),
        "insulation_thickness": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
    }


def sampled_wire_material_kind():
    return sampled_from(WireMaterialKind)


def sampled_wire_insulation_kind():
    return sampled_from(WireInsulationKind)


###################
# IEC61968 Assets #
###################


def asset_kwargs(include_runtime: bool):
    return {
        **identified_object_kwargs(include_runtime),
        "location": builds(Location, **identified_object_kwargs(include_runtime)),
        "organisation_roles": lists(builds(AssetOwner, **identified_object_kwargs(include_runtime)), max_size=2),
        "power_system_resources": lists(builds(Junction, **identified_object_kwargs(include_runtime)), max_size=2),
    }


def asset_container_kwargs(include_runtime: bool):
    return {
        **asset_kwargs(include_runtime)
    }


def asset_function_kwargs(include_runtime: bool):
    return {
        **identified_object_kwargs(include_runtime)
    }


def asset_info_kwargs(include_runtime: bool):
    return {
        **identified_object_kwargs(include_runtime)
    }


def asset_organisation_role_kwargs(include_runtime: bool):
    return {
        **organisation_role_kwargs(include_runtime)
    }


def create_asset_owner(include_runtime: bool = True):
    return builds(AssetOwner, **asset_owner_kwargs(include_runtime))


def asset_owner_kwargs(include_runtime: bool = True):
    return {
        **asset_organisation_role_kwargs(include_runtime)
    }


def create_streetlight(include_runtime: bool = True):
    return builds(Streetlight, **streetlight_kwargs(include_runtime))


def streetlight_kwargs(include_runtime: bool = True):
    return {
        **asset_kwargs(include_runtime),
        "pole": builds(Pole, **identified_object_kwargs(include_runtime)),
        "light_rating": integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
        # Capping unsigned int to 32-bit int range to avoid issues with Python 3.7 testing.
        "lamp_kind": sampled_streetlight_lamp_kind(),
    }


def structure_kwargs(include_runtime: bool):
    return {
        **asset_container_kwargs(include_runtime)
    }


###################
# IEC61968 Common #
###################


def agreement_kwargs(include_runtime: bool):
    return {
        **document_kwargs(include_runtime)
    }


def document_kwargs(include_runtime: bool):
    return {
        **identified_object_kwargs(include_runtime),
        "title": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        "created_date_time": datetimes(min_value=datetime(1970, 1, 2)),
        "author_name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        "type": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        "status": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        "comment": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    }


def create_electronic_address():
    return builds(ElectronicAddress, **electronic_address_kwargs())


def electronic_address_kwargs():
    return {
        "email1": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
        "is_primary": one_of(none(), booleans()),
        "description": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
    }


def create_location(include_runtime: bool = True):
    return builds(Location, **location_kwargs(include_runtime))


def location_kwargs(include_runtime: bool = True):
    return {
        **identified_object_kwargs(include_runtime),
        "main_address": create_street_address(),
        "position_points": lists(create_position_point(), max_size=4),
    }


def create_organisation(include_runtime: bool = True):
    return builds(Organisation, **organisation_kwargs(include_runtime))


def organisation_kwargs(include_runtime: bool = True):
    return {
        **identified_object_kwargs(include_runtime)
    }


def organisation_role_kwargs(include_runtime: bool):
    return {
        **identified_object_kwargs(include_runtime),
        "organisation": builds(Organisation, **identified_object_kwargs(include_runtime)),
    }


def create_position_point():
    return builds(PositionPoint, **position_point_kwargs())


def position_point_kwargs():
    return {
        "x_position": floats(min_value=-180.0, max_value=180.0),
        "y_position": floats(min_value=-90.0, max_value=90.0),
    }


def create_street_address():
    return builds(StreetAddress, **street_address_kwargs())


def street_address_kwargs():
    return {
        "postal_code": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
        "town_detail": create_town_detail(),
        "po_box": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
        "street_detail": create_street_detail(),
    }


def create_street_detail():
    return builds(StreetDetail, **street_detail_kwargs())


def street_detail_kwargs():
    return {
        "building_name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        "floor_identification": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
        "name": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
        "number": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
        "suite_number": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
        "type": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
        "display_address": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
        "building_number": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
    }


def create_telephone_number():
    return builds(TelephoneNumber, **telephone_number_kwargs())


def telephone_number_kwargs():
    return {
        "area_code": text(alphabet=ALPHANUM, max_size=3),
        "city_code": one_of(none(), text(alphabet=ALPHANUM, max_size=2)),
        "dial_out": one_of(none(), text(alphabet=ALPHANUM, max_size=3)),
        "extension": one_of(none(), text(alphabet=ALPHANUM, max_size=4)),
        "international_prefix": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
        "local_number": one_of(none(), text(alphabet=ALPHANUM, max_size=8)),
        "is_primary": one_of(none(), booleans()),
        "description": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
    }


def create_town_detail():
    return builds(TownDetail, **town_detail_kwargs())


def town_detail_kwargs():
    return {
        "name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        "state_or_province": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
        "country": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
    }


######################
# IEC61968 Customers #
######################


def create_customer(include_runtime: bool = True):
    return builds(Customer, **customer_kwargs(include_runtime))


def customer_kwargs(include_runtime: bool = True):
    return {
        **organisation_role_kwargs(include_runtime),
        "kind": sampled_customer_kind(),
        # We can't use blank strings as it breaks some of the tests due to protobuf conversions dropping the blanks for None.
        "special_need": text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        "customer_agreements": lists(builds(CustomerAgreement, **identified_object_kwargs(include_runtime)), max_size=2),
    }


def create_customer_agreement(include_runtime: bool = True):
    return builds(CustomerAgreement, **customer_agreement_kwargs(include_runtime))


def customer_agreement_kwargs(include_runtime: bool = True):
    return {
        **agreement_kwargs(include_runtime),
        "customer": builds(Customer, **identified_object_kwargs(include_runtime)),
        "pricing_structures": lists(builds(PricingStructure, **identified_object_kwargs(include_runtime)), max_size=2),
    }


def sampled_customer_kind():
    return sampled_from(CustomerKind)


def create_pricing_structure(include_runtime: bool = True):
    return builds(PricingStructure, **pricing_structure_kwargs(include_runtime))


def pricing_structure_kwargs(include_runtime: bool = True):
    return {
        **document_kwargs(include_runtime),
        "tariffs": lists(builds(Tariff, **identified_object_kwargs(include_runtime)), max_size=2),
    }


def create_tariffs(include_runtime: bool = True):
    return builds(Tariff, **tariffs_kwargs(include_runtime))


def tariffs_kwargs(include_runtime: bool = True):
    return {
        **document_kwargs(include_runtime)
    }


#####################################
# IEC61968 InfIEC61968 InfAssetInfo #
#####################################

def create_current_transformer_info(include_runtime: bool = True):
    return builds(CurrentTransformerInfo, **current_transformer_info_kwargs(include_runtime))


def current_transformer_info_kwargs(include_runtime: bool = True):
    return {
        **asset_info_kwargs(include_runtime),
        "accuracy_class": text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        "accuracy_limit": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "core_count": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "ct_class": text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        "knee_point_voltage": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "max_ratio": create_ratio(),
        "nominal_ratio": create_ratio(),
        "primary_ratio": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "rated_current": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "secondary_fls_rating": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "secondary_ratio": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "usage": text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
    }


def create_potential_transformer_info(include_runtime: bool = True):
    return builds(PotentialTransformerInfo, **potential_transformer_info_kwargs(include_runtime))


def potential_transformer_info_kwargs(include_runtime: bool = True):
    return {
        **asset_info_kwargs(include_runtime),
        "accuracy_class": text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        "nominal_ratio": create_ratio(),
        "primary_ratio": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "pt_class": text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        "rated_voltage": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "secondary_ratio": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    }


def sampled_transformer_construction_kind():
    return sampled_from(TransformerConstructionKind)


def sampled_transformer_function_kind():
    return sampled_from(TransformerFunctionKind)


##################################
# IEC61968 InfIEC61968 InfAssets #
##################################


def create_pole(include_runtime: bool = True):
    return builds(Pole, **pole_kwargs(include_runtime))


def pole_kwargs(include_runtime: bool = True):
    return {
        **structure_kwargs(include_runtime),
        "streetlights": lists(builds(Streetlight, **identified_object_kwargs(include_runtime)), max_size=2),
        "classification": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    }


def sampled_streetlight_lamp_kind():
    return sampled_from(StreetlightLampKind)


##################################
# IEC61968 InfIEC61968 InfCommon #
##################################


def create_ratio():
    return builds(Ratio, **ratio_kwargs())


def ratio_kwargs():
    return {
        "numerator": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "denominator": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    }


#####################
# IEC61968 Metering #
#####################


def create_controlled_appliance():
    return builds(ControlledAppliance, **controlled_appliance_kwargs())


def controlled_appliance_kwargs():
    return {
        "appliances": sampled_from(Appliance),
    }


def end_device_kwargs(include_runtime: bool):
    return {
        **asset_container_kwargs(include_runtime),
        "usage_points": lists(builds(UsagePoint, **identified_object_kwargs(include_runtime)), max_size=2),
        "customer_mrid": text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        "service_location": builds(Location, **identified_object_kwargs(include_runtime)),
        "functions": lists(sampled_end_device_function(include_runtime), max_size=2),
    }


def end_device_function_kwargs(include_runtime: bool):
    return {
        **asset_function_kwargs(include_runtime),
        "enabled": booleans(),
    }


def sampled_end_device_function_kind():
    return sampled_from(EndDeviceFunctionKind)


def create_meter(include_runtime: bool = True):
    return builds(Meter, **meter_kwargs(include_runtime))


def meter_kwargs(include_runtime: bool = True):
    return {
        **end_device_kwargs(include_runtime)
    }


def create_usage_point(include_runtime: bool = True):
    return builds(UsagePoint, **usage_point_kwargs(include_runtime))


def usage_point_kwargs(include_runtime: bool = True):
    return {
        **identified_object_kwargs(include_runtime),
        "usage_point_location": builds(Location, **identified_object_kwargs(include_runtime)),
        "is_virtual": booleans(),
        "connection_category": text(alphabet=ALPHANUM, min_size=2, max_size=TEXT_MAX_SIZE),
        "rated_power": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "approved_inverter_capacity": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "equipment": lists(builds(EnergyConsumer, **identified_object_kwargs(include_runtime)), max_size=2),
        "end_devices": lists(builds(Meter, **identified_object_kwargs(include_runtime)), max_size=2),
        "contacts": lists(create_contact_details(), max_size=2),
    }


#######################
# IEC61968 Operations #
#######################


def create_operational_restriction(include_runtime: bool = True):
    return builds(OperationalRestriction, **operational_restriction_kwargs(include_runtime))


def operational_restriction_kwargs(include_runtime: bool = True):
    return {
        **document_kwargs(include_runtime),
        "equipment": lists(builds(PowerTransformer, **identified_object_kwargs(include_runtime)), max_size=2),
    }


#####################################
# IEC61970 Base Auxiliary Equipment #
#####################################

def auxiliary_equipment_kwargs(include_runtime: bool):
    return {
        **equipment_kwargs(include_runtime),
        "terminal": builds(Terminal, **identified_object_kwargs(include_runtime)),
    }


def create_current_transformer(include_runtime: bool = True):
    return builds(CurrentTransformer, **current_transformer_kwargs(include_runtime))


def current_transformer_kwargs(include_runtime: bool = True):
    return {
        **sensor_kwargs(include_runtime),
        "asset_info": builds(CurrentTransformerInfo, **identified_object_kwargs(include_runtime)),
        "core_burden": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    }


def create_fault_indicator(include_runtime: bool = True):
    return builds(FaultIndicator, **fault_indicator_kwargs(include_runtime))


def fault_indicator_kwargs(include_runtime: bool = True):
    return {
        **auxiliary_equipment_kwargs(include_runtime)
    }


def create_potential_transformer(include_runtime: bool = True):
    return builds(PotentialTransformer, **potential_transformer_kwargs(include_runtime))


def potential_transformer_kwargs(include_runtime: bool = True):
    return {
        **sensor_kwargs(include_runtime),
        "asset_info": builds(PotentialTransformerInfo, **identified_object_kwargs(include_runtime)),
        "type": sampled_from(PotentialTransformerKind),
    }


def sampled_potential_transformer_kind():
    return sampled_from(PotentialTransformerKind)


def sensor_kwargs(include_runtime: bool = True):
    return {
        **auxiliary_equipment_kwargs(include_runtime),
        "relay_functions": lists(builds(CurrentRelay, mrid=mrid_strategy), max_size=10),
    }


######################
# IEC61970 Base Core #
######################


def ac_dc_terminal_kwargs(include_runtime: bool):
    return {
        **identified_object_kwargs(include_runtime)
    }


def create_base_voltage(include_runtime: bool = True):
    return builds(BaseVoltage, **base_voltage_kwargs(include_runtime))


def base_voltage_kwargs(include_runtime: bool = True):
    return {
        **identified_object_kwargs(include_runtime),
        "nominal_voltage": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    }


def conducting_equipment_kwargs(include_runtime: bool):
    return {
        **equipment_kwargs(include_runtime),
        "base_voltage": builds(BaseVoltage, **identified_object_kwargs(include_runtime)),
        "terminals": lists(builds(Terminal, **identified_object_kwargs(include_runtime)), max_size=3),
    }


def create_connectivity_node(include_runtime: bool = True):
    return builds(ConnectivityNode, **connectivity_node_kwargs(include_runtime))


def connectivity_node_kwargs(include_runtime: bool = True):
    return {
        **identified_object_kwargs(include_runtime),
        "terminals": lists(builds(Terminal, **identified_object_kwargs(include_runtime)), max_size=10),
    }


def connectivity_node_container_kwargs(include_runtime: bool):
    return {
        **power_system_resource_kwargs(include_runtime)
    }


def curve_kwargs(include_runtime: bool):
    return {
        **identified_object_kwargs(include_runtime),
        "data": lists(create_curve_data(), max_size=4, unique_by=lambda it: it.x_value),
    }


def create_curve_data():
    return builds(CurveData, **curve_data_kwargs())


def curve_data_kwargs():
    return {
        "x_value": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "y1_value": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "y2_value": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "y3_value": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
    }


def equipment_kwargs(include_runtime: bool):
    runtime = {
        "current_containers": lists(sampled_hvlv_feeder(include_runtime), max_size=2),
    } if include_runtime else {}

    return {
        **power_system_resource_kwargs(include_runtime),
        "in_service": booleans(),
        "normally_in_service": booleans(),
        "equipment_containers": lists(sampled_equipment_container(include_runtime), max_size=2),
        "usage_points": lists(builds(UsagePoint, **identified_object_kwargs(include_runtime)), max_size=2),
        "operational_restrictions": lists(builds(OperationalRestriction, **identified_object_kwargs(include_runtime)), max_size=2),
        "commissioned_date": datetimes(min_value=datetime(1970, 1, 2)),
        **runtime,
    }


def equipment_container_kwargs(include_runtime: bool, add_equipment: bool = True):
    equipment = {
        "equipment": lists(sampled_equipment(include_runtime), max_size=30),
    } if add_equipment else {}

    return {
        **connectivity_node_container_kwargs(include_runtime),
        **equipment
    }


def create_feeder(include_runtime: bool = True):
    return builds(Feeder, **feeder_kwargs(include_runtime))


def feeder_kwargs(include_runtime: bool = True):
    runtime = {
        "normal_energized_lv_feeders": lists(builds(LvFeeder, **identified_object_kwargs(include_runtime)), max_size=2),
        "current_energized_lv_feeders": lists(builds(LvFeeder, **identified_object_kwargs(include_runtime)), max_size=2),
        "normal_energized_lv_substations": lists(builds(LvSubstation, **identified_object_kwargs(include_runtime)), max_size=2),
        "current_energized_lv_substations": lists(builds(LvSubstation, **identified_object_kwargs(include_runtime)), max_size=2),
        "current_equipment": lists(sampled_equipment(include_runtime), max_size=2),
    } if include_runtime else {}

    return {
        # Only include equipment if we are processing runtime as we don't write equipment to the database for Feeder.
        **equipment_container_kwargs(include_runtime, add_equipment=include_runtime),
        "normal_head_terminal": builds(Terminal, **identified_object_kwargs(include_runtime)),
        "normal_energizing_substation": builds(Substation, **identified_object_kwargs(include_runtime)),
        **runtime,
    }


def create_geographical_region(include_runtime: bool = True):
    return builds(GeographicalRegion, **geographical_region_kwargs(include_runtime))


def geographical_region_kwargs(include_runtime: bool = True):
    return {
        **identified_object_kwargs(include_runtime),
        "sub_geographical_regions": lists(builds(SubGeographicalRegion, **identified_object_kwargs(include_runtime)), max_size=2),
    }


# noinspection PyUnusedLocal
def identified_object_kwargs(include_runtime: bool):
    return {
        "mrid": uuids(version=4).map(lambda x: str(x)),
        "name": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
        "description": one_of(none(), text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
        "names": one_of(
            none(),
            lists(builds(Name, name=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), type=create_name_type()), max_size=2,
                  unique_by=lambda it: it.name)
        ),
    }


def create_name(include_runtime: bool = True):
    return builds(Name, **name_kwargs(include_runtime))


def name_kwargs(include_runtime: bool = True):
    return {
        "name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        "type": create_name_type(),
        "identified_object": sampled_equipment(include_runtime),
    }


def create_name_type():
    return builds(NameType, **name_type_kwargs())


def name_type_kwargs():
    return {
        "name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        "description": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    }


def sampled_phase_code():
    return sampled_from(PhaseCode)


def power_system_resource_kwargs(include_runtime: bool):
    #
    # NOTE: We do not create the asset_info here, create it where it is actually used.
    #
    return {
        **identified_object_kwargs(include_runtime),
        "location": create_location(),
        "num_controls": integers(min_value=0, max_value=MAX_64_BIT_INTEGER),
        "assets": lists(builds(Pole, **identified_object_kwargs(include_runtime)), max_size=2),
    }


def create_sub_geographical_region(include_runtime: bool = True):
    return builds(SubGeographicalRegion, **sub_geographical_region_kwargs(include_runtime))


def sub_geographical_region_kwargs(include_runtime: bool = True):
    return {
        **identified_object_kwargs(include_runtime),
        "geographical_region": builds(GeographicalRegion, **identified_object_kwargs(include_runtime)),
        "substations": lists(builds(Substation, **identified_object_kwargs(include_runtime)), max_size=2),
    }


def create_substation(include_runtime: bool = True):
    return builds(Substation, **substation_kwargs(include_runtime))


def substation_kwargs(include_runtime: bool = True):
    return {
        **equipment_container_kwargs(include_runtime),
        "sub_geographical_region": builds(SubGeographicalRegion, **identified_object_kwargs(include_runtime)),
        "normal_energized_feeders": lists(builds(Feeder, **identified_object_kwargs(include_runtime)), max_size=2),
        "loops": lists(builds(Loop, **identified_object_kwargs(include_runtime)), max_size=2),
        "energized_loops": lists(builds(Loop, **identified_object_kwargs(include_runtime)), max_size=2),
        "circuits": lists(builds(Circuit, **identified_object_kwargs(include_runtime)), max_size=2),
    }


def create_terminal(include_runtime: bool = True):
    return builds(Terminal, **terminal_kwargs(include_runtime))


def terminal_kwargs(include_runtime: bool = True):
    return {
        **ac_dc_terminal_kwargs(include_runtime),
        "conducting_equipment": sampled_conducting_equipment(include_runtime),
        "connectivity_node": builds(ConnectivityNode, **identified_object_kwargs(include_runtime)),
        "phases": sampled_phase_code(),
        "sequence_number": integers(min_value=MIN_SEQUENCE_NUMBER, max_value=MAX_SEQUENCE_NUMBER),
    }


################################
# IEC61970 Base Diagram Layout #
################################


def create_diagram(include_runtime: bool = True):
    return builds(Diagram, **diagram_kwargs(include_runtime))


def diagram_kwargs(include_runtime: bool = True):
    return {
        **identified_object_kwargs(include_runtime),
        "diagram_style": sampled_diagram_style(),
        "orientation_kind": sampled_orientation_kind(),
        "diagram_objects": lists(builds(DiagramObject, **identified_object_kwargs(include_runtime)), max_size=2),
    }


def create_diagram_object(include_runtime: bool = True):
    return builds(DiagramObject, **diagram_object_kwargs(include_runtime))


def diagram_object_kwargs(include_runtime: bool = True):
    return {
        **identified_object_kwargs(include_runtime),
        "diagram": builds(Diagram, **identified_object_kwargs(include_runtime)),
        "identified_object_mrid": text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        "style": text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        "rotation": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "diagram_object_points": lists(create_diagram_object_point(), max_size=2),
    }


def create_diagram_object_point():
    return builds(DiagramObjectPoint, **diagram_object_point_kwargs())


def diagram_object_point_kwargs():
    return {
        "x_position": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "y_position": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    }


def sampled_diagram_style():
    return sampled_from(DiagramStyle)


def sampled_orientation_kind():
    return sampled_from(OrientationKind)


########################
# IEC61970 Base Domain #
########################

def sampled_unit_symbol():
    return sampled_from(UnitSymbol)


#############################
# IEC61970 Base Equivalents #
#############################


def create_equivalent_branch(include_runtime: bool = True):
    return builds(EquivalentBranch, **equivalent_branch_kwargs(include_runtime))


def equivalent_branch_kwargs(include_runtime: bool = True):
    return {
        **equivalent_equipment_kwargs(include_runtime),
        "negative_r12": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "negative_r21": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "negative_x12": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "negative_x21": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "positive_r12": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "positive_r21": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "positive_x12": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "positive_x21": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "r21": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "x": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "x21": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "zero_r12": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "zero_r21": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "zero_x12": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "zero_x21": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    }


def equivalent_equipment_kwargs(include_runtime: bool):
    return {
        **conducting_equipment_kwargs(include_runtime)
    }


#######################################
# IEC61970 Base Generation Production #
#######################################

def sampled_battery_state_kind():
    return sampled_from(BatteryStateKind)


def create_battery_unit(include_runtime: bool = True):
    return builds(BatteryUnit, **battery_unit_kwargs(include_runtime))


def battery_unit_kwargs(include_runtime: bool = True):
    return {
        **power_electronics_unit_kwargs(include_runtime),
        "battery_state": sampled_battery_state_kind(),
        "rated_e": integers(min_value=MIN_64_BIT_INTEGER, max_value=MAX_64_BIT_INTEGER),
        "stored_e": integers(min_value=MIN_64_BIT_INTEGER, max_value=MAX_64_BIT_INTEGER),
        "controls": lists(builds(BatteryControl, **identified_object_kwargs(include_runtime)), max_size=2),
    }


def create_photo_voltaic_unit(include_runtime: bool = True):
    return builds(PhotoVoltaicUnit, **photo_voltaic_unit_kwargs(include_runtime))


def photo_voltaic_unit_kwargs(include_runtime: bool = True):
    return {
        **power_electronics_unit_kwargs(include_runtime)
    }


def power_electronics_unit_kwargs(include_runtime: bool):
    return {
        **equipment_kwargs(include_runtime),
        "power_electronics_connection": builds(PowerElectronicsConnection, **identified_object_kwargs(include_runtime)),
        "max_p": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "min_p": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    }


def create_power_electronics_wind_unit(include_runtime: bool = True):
    return builds(PowerElectronicsWindUnit, **power_electronics_wind_unit_kwargs(include_runtime))


def power_electronics_wind_unit_kwargs(include_runtime: bool = True):
    return {
        **power_electronics_unit_kwargs(include_runtime)
    }


######################
# IEC61970 Base Meas #
######################


def create_accumulator(include_runtime: bool = True):
    return builds(Accumulator, **accumulator_kwargs(include_runtime))


def accumulator_kwargs(include_runtime: bool = True):
    return {
        **measurement_kwargs(include_runtime)
    }


def create_accumulator_value():
    return builds(AccumulatorValue, **accumulator_value_kwargs())


def accumulator_value_kwargs():
    return {
        **measurement_value_kwargs(),
        "value": integers(min_value=MIN_64_BIT_INTEGER, max_value=MAX_64_BIT_INTEGER),
    }


def create_analog(include_runtime: bool = True):
    return builds(Analog, **analog_kwargs(include_runtime))


def analog_kwargs(include_runtime: bool = True):
    return {
        **measurement_kwargs(include_runtime),
        "positive_flow_in": booleans(),
    }


def create_analog_value():
    return builds(AnalogValue, **analog_value_kwargs())


def analog_value_kwargs():
    return {
        **measurement_value_kwargs(),
        "value": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    }


def create_control(include_runtime: bool = True):
    return builds(Control, **control_kwargs(include_runtime))


def control_kwargs(include_runtime: bool = True):
    return {
        **io_point_kwargs(include_runtime),
        "power_system_resource_mrid": text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        "remote_control": builds(RemoteControl, **identified_object_kwargs(include_runtime)),
    }


def create_discrete(include_runtime: bool = True):
    return builds(Discrete, **discrete_kwargs(include_runtime))


def discrete_kwargs(include_runtime: bool = True):
    return {
        **measurement_kwargs(include_runtime)
    }


def create_discrete_value():
    return builds(DiscreteValue, **discrete_value_kwargs())


def discrete_value_kwargs():
    return {
        **measurement_value_kwargs(),
        "value": integers(min_value=MIN_64_BIT_INTEGER, max_value=MAX_64_BIT_INTEGER),
    }


def io_point_kwargs(include_runtime: bool):
    return {
        **identified_object_kwargs(include_runtime)
    }


def measurement_kwargs(include_runtime: bool):
    return {
        **identified_object_kwargs(include_runtime),
        "remote_source": builds(RemoteSource, **identified_object_kwargs(include_runtime)),
        "power_system_resource_mrid": uuids(version=4).map(lambda x: str(x)),
        "terminal_mrid": uuids(version=4).map(lambda x: str(x)),
        "phases": sampled_phase_code(),
        "unit_symbol": sampled_unit_symbol(),
    }


# noinspection PyUnusedLocal
def measurement_value_kwargs():
    return {
        # "time_stamp": ...
    }


############################
# IEC61970 Base Protection #
############################


def create_current_relay(include_runtime: bool = True):
    return builds(CurrentRelay, **current_relay_kwargs(include_runtime))


def current_relay_kwargs(include_runtime: bool = True):
    return {
        **protection_relay_function_kwargs(include_runtime),
        "current_limit_1": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "inverse_time_flag": one_of(none(), booleans()),
        "time_delay_1": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    }


#######################
# IEC61970 Base Scada #
#######################

def create_remote_control(include_runtime: bool = True):
    return builds(RemoteControl, **remote_control_kwargs(include_runtime))


def remote_control_kwargs(include_runtime: bool = True):
    return {
        **remote_point_kwargs(include_runtime),
        "control": builds(Control, **identified_object_kwargs(include_runtime)),
    }


def remote_point_kwargs(include_runtime: bool):
    return {
        **identified_object_kwargs(include_runtime)
    }


def create_remote_source(include_runtime: bool = True):
    return builds(RemoteSource, **remote_source_kwargs(include_runtime))


def remote_source_kwargs(include_runtime: bool = True):
    return {
        **remote_point_kwargs(include_runtime),
        "measurement": sampled_measurement(include_runtime),
    }


#######################
# IEC61970 Base Wires #
#######################


def create_ac_line_segment(include_runtime: bool = True):
    return builds(AcLineSegment, **ac_line_segment_kwargs(include_runtime))


def ac_line_segment_kwargs(include_runtime: bool = True):
    args = conductor_kwargs(include_runtime)
    args["terminals"] = lists(builds(Terminal, **identified_object_kwargs(include_runtime)), max_size=2)

    return {
        **args,
        "per_length_impedance": builds(PerLengthSequenceImpedance, **identified_object_kwargs(include_runtime)),
    }


def create_ac_line_segment_phase(include_runtime: bool = True):
    return builds(AcLineSegmentPhase, **ac_line_segment_phase_kwargs(include_runtime))


def ac_line_segment_phase_kwargs(include_runtime: bool = True):
    return {
        **power_system_resource_kwargs(include_runtime),
        "ac_line_segment": builds(AcLineSegment, **identified_object_kwargs(include_runtime)),
        "phase": sampled_single_phase_kind(),
        "sequence_number": integers(min_value=MIN_SEQUENCE_NUMBER, max_value=MAX_SEQUENCE_NUMBER),
    }


def create_breaker(include_runtime: bool = True):
    return builds(Breaker, **breaker_kwargs(include_runtime))


def breaker_kwargs(include_runtime: bool = True):
    return {
        **protected_switch_kwargs(include_runtime),
        "in_transit_time": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    }


def create_busbar_section(include_runtime: bool = True):
    return builds(BusbarSection, **busbar_section_kwargs(include_runtime))


def busbar_section_kwargs(include_runtime: bool = True):
    #  Monkey patch the args to set terminals to 1, as busbars only have 1 terminal.
    args = connector_kwargs(include_runtime)
    args["terminals"] = lists(builds(Terminal, **identified_object_kwargs(include_runtime)), max_size=1)

    return {
        **args
    }


def create_clamp(include_runtime: bool = True):
    return builds(Clamp, **clamp_kwargs(include_runtime))


def clamp_kwargs(include_runtime: bool = True):
    args = conducting_equipment_kwargs(include_runtime)
    args["terminals"] = lists(builds(Terminal, **identified_object_kwargs(include_runtime)), max_size=1)

    return {
        **args,
        "length_from_terminal_1": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "ac_line_segment": builds(AcLineSegment, **identified_object_kwargs(include_runtime)),
    }


def conductor_kwargs(include_runtime: bool):
    return {
        **conducting_equipment_kwargs(include_runtime),
        "asset_info": sampled_wire_info(include_runtime),
        "length": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "design_temperature": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "design_rating": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    }


def connector_kwargs(include_runtime: bool):
    return {
        **conducting_equipment_kwargs(include_runtime)
    }


def create_cut(include_runtime: bool = True):
    return builds(Cut, **cut_kwargs(include_runtime))


def cut_kwargs(include_runtime: bool = True):
    args = switch_kwargs(include_runtime)
    args["terminals"] = lists(builds(Terminal, **identified_object_kwargs(include_runtime)), max_size=2)

    return {
        **args,
        "length_from_terminal_1": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "ac_line_segment": builds(AcLineSegment, **identified_object_kwargs(include_runtime)),
    }


def create_disconnector(include_runtime: bool = True):
    return builds(Disconnector, **disconnector_kwargs(include_runtime))


def disconnector_kwargs(include_runtime: bool = True):
    return {
        **switch_kwargs(include_runtime)
    }


def earth_fault_compensator_kwargs(include_runtime: bool):
    return {
        **conducting_equipment_kwargs(include_runtime),
        "r": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
    }


def energy_connection_kwargs(include_runtime: bool):
    return {
        **conducting_equipment_kwargs(include_runtime)
    }


def create_energy_consumer(include_runtime: bool = True):
    return builds(EnergyConsumer, **energy_consumer_kwargs(include_runtime))


def energy_consumer_kwargs(include_runtime: bool = True):
    return {
        **energy_connection_kwargs(include_runtime),
        "energy_consumer_phases": lists(
            builds(
                EnergyConsumerPhase,
                **identified_object_kwargs(include_runtime),
                phase=sampled_single_phase_kind()
            ),
            max_size=2
        ),
        "customer_count": integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
        "grounded": booleans(),
        "p": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "p_fixed": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "phase_connection": sampled_phase_shunt_connection_kind(),
        "q": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "q_fixed": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    }


def create_energy_consumer_phase(include_runtime: bool = True):
    return builds(EnergyConsumerPhase, **energy_consumer_phase_kwargs(include_runtime))


def energy_consumer_phase_kwargs(include_runtime: bool = True):
    return {
        **power_system_resource_kwargs(include_runtime),
        "energy_consumer": builds(EnergyConsumer, **identified_object_kwargs(include_runtime)),
        "phase": sampled_single_phase_kind(),
        "p": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "p_fixed": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "q": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "q_fixed": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    }


def create_energy_source(include_runtime: bool = True):
    return builds(EnergySource, **energy_source_kwargs(include_runtime))


def energy_source_kwargs(include_runtime: bool = True):
    return {
        **energy_connection_kwargs(include_runtime),
        "energy_source_phases": lists(
            builds(
                EnergySourcePhase,
                **identified_object_kwargs(include_runtime),
                phase=sampled_single_phase_kind()
            ),
            max_size=2),
        "active_power": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "reactive_power": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "voltage_angle": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "voltage_magnitude": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "x": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "p_max": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "p_min": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "r0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "rn": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "x0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "xn": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "is_external_grid": booleans(),
        "r_min": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "rn_min": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "r0_min": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "x_min": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "xn_min": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "x0_min": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "r_max": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "rn_max": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "r0_max": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "x_max": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "xn_max": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "x0_max": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    }


def create_energy_source_phase(include_runtime: bool = True):
    return builds(EnergySourcePhase, **energy_source_phase_kwargs(include_runtime))


def energy_source_phase_kwargs(include_runtime: bool = True):
    return {
        **power_system_resource_kwargs(include_runtime),
        "energy_source": builds(EnergySource, **identified_object_kwargs(include_runtime)),
        "phase": sampled_single_phase_kind(),
    }


def create_fuse(include_runtime: bool = True):
    return builds(Fuse, **fuse_kwargs(include_runtime))


def fuse_kwargs(include_runtime: bool = True):
    return {
        **switch_kwargs(include_runtime),
        "function": builds(DistanceRelay, mrid=mrid_strategy),
    }


def create_ground(include_runtime: bool = True):
    return builds(Ground, **ground_kwargs(include_runtime))


def ground_kwargs(include_runtime: bool = True):
    return {
        **conducting_equipment_kwargs(include_runtime),
    }


def create_ground_disconnector(include_runtime: bool = True):
    return builds(GroundDisconnector, **ground_disconnector_kwargs(include_runtime))


def ground_disconnector_kwargs(include_runtime: bool = True):
    return {
        **switch_kwargs(include_runtime),
    }


def create_grounding_impedance(include_runtime: bool = True):
    return builds(GroundingImpedance, **grounding_impedance_kwargs(include_runtime))


def grounding_impedance_kwargs(include_runtime: bool = True):
    return {
        **earth_fault_compensator_kwargs(include_runtime),
        "x": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
    }


def create_jumper(include_runtime: bool = True):
    return builds(Jumper, **jumper_kwargs(include_runtime))


def jumper_kwargs(include_runtime: bool = True):
    return {
        **switch_kwargs(include_runtime)
    }


def create_junction(include_runtime: bool = True):
    return builds(Junction, **junction_kwargs(include_runtime))


def junction_kwargs(include_runtime: bool = True):
    return {
        **connector_kwargs(include_runtime)
    }


def line_kwargs(include_runtime: bool):
    return {
        **equipment_container_kwargs(include_runtime)
    }


def create_linear_shunt_compensator(include_runtime: bool = True):
    return builds(LinearShuntCompensator, **linear_shunt_compensator_kwargs(include_runtime))


def linear_shunt_compensator_kwargs(include_runtime: bool = True):
    return {
        **shunt_compensator_kwargs(include_runtime),
        "b0_per_section": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "b_per_section": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "g0_per_section": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "g_per_section": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    }


def create_load_break_switch(include_runtime: bool = True):
    return builds(LoadBreakSwitch, **load_break_switch_kwargs(include_runtime))


def load_break_switch_kwargs(include_runtime: bool = True):
    return {
        **protected_switch_kwargs(include_runtime)
    }


def per_length_impedance_kwargs(include_runtime: bool):
    return {
        **per_length_line_parameter_kwargs(include_runtime)
    }


def per_length_line_parameter_kwargs(include_runtime: bool):
    return {
        **identified_object_kwargs(include_runtime)
    }


def create_per_length_phase_impedance(include_runtime: bool = True):
    return builds(PerLengthPhaseImpedance, **per_length_phase_impedance_kwargs(include_runtime))


def per_length_phase_impedance_kwargs(include_runtime: bool = True):
    return {
        **per_length_impedance_kwargs(include_runtime),
        "data": lists(create_phase_impedance_data(), max_size=4, unique_by=(lambda it: it.from_phase, lambda it: it.to_phase)),
    }


def create_per_length_sequence_impedance(include_runtime: bool = True):
    return builds(PerLengthSequenceImpedance, **per_length_sequence_impedance_kwargs(include_runtime))


def per_length_sequence_impedance_kwargs(include_runtime: bool = True):
    return {
        **per_length_impedance_kwargs(include_runtime),
        "r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "x": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "r0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "x0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "bch": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "gch": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "b0ch": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "g0ch": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    }


def create_petersen_coil(include_runtime: bool = True):
    return builds(PetersenCoil, **petersen_coil_kwargs(include_runtime))


def petersen_coil_kwargs(include_runtime: bool = True):
    return {
        **earth_fault_compensator_kwargs(include_runtime),
        "x_ground_nominal": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
    }


def create_phase_impedance_data():
    return builds(PhaseImpedanceData, **phase_impedance_data_kwargs())


def phase_impedance_data_kwargs():
    return {
        "from_phase": sampled_from(SinglePhaseKind),
        "to_phase": sampled_from(SinglePhaseKind),
        "b": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "g": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "r": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "x": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
    }


def sampled_phase_shunt_connection_kind():
    return sampled_from(PhaseShuntConnectionKind)


def create_power_electronics_connection(include_runtime: bool = True):
    return builds(PowerElectronicsConnection, **power_electronics_connection_kwargs(include_runtime))


def power_electronics_connection_kwargs(include_runtime: bool = True):
    return {
        **regulating_cond_eq_kwargs(include_runtime),
        "power_electronics_units": lists(builds(BatteryUnit, **identified_object_kwargs(include_runtime)), max_size=2),
        "power_electronics_connection_phases": lists(builds(PowerElectronicsConnectionPhase, **identified_object_kwargs(include_runtime)), max_size=2),
        "max_i_fault": integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
        "max_q": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "min_q": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "p": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "q": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "rated_s": integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
        "rated_u": integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
        "inverter_standard": text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        "sustain_op_overvolt_limit": integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
        "stop_at_over_freq": floats(min_value=51.0, max_value=52.0),
        "stop_at_under_freq": floats(min_value=47.0, max_value=49.0),
        "inv_volt_watt_resp_mode": one_of(none(), booleans()),
        "inv_watt_resp_v1": integers(min_value=200, max_value=300),
        "inv_watt_resp_v2": integers(min_value=216, max_value=230),
        "inv_watt_resp_v3": integers(min_value=235, max_value=255),
        "inv_watt_resp_v4": integers(min_value=244, max_value=265),
        "inv_watt_resp_p_at_v1": floats(min_value=0.0, max_value=1.0),
        "inv_watt_resp_p_at_v2": floats(min_value=0.0, max_value=1.0),
        "inv_watt_resp_p_at_v3": floats(min_value=0.0, max_value=1.0),
        "inv_watt_resp_p_at_v4": floats(min_value=0.0, max_value=0.12300000339746475),
        "inv_volt_var_resp_mode": one_of(none(), booleans()),
        "inv_var_resp_v1": integers(min_value=200, max_value=300),
        "inv_var_resp_v2": integers(min_value=200, max_value=300),
        "inv_var_resp_v3": integers(min_value=200, max_value=300),
        "inv_var_resp_v4": integers(min_value=200, max_value=300),
        "inv_var_resp_q_at_v1": floats(min_value=0.0, max_value=0.5120000243186951),
        "inv_var_resp_q_at_v2": floats(min_value=-1.0, max_value=1.0),
        "inv_var_resp_q_at_v3": floats(min_value=-1.0, max_value=1.0),
        "inv_var_resp_q_at_v4": floats(min_value=-0.5120000243186951, max_value=0.0),
        "inv_reactive_power_mode": one_of(none(), booleans()),
        "inv_fix_reactive_power": floats(min_value=-1.0, max_value=1.0),
    }


def create_power_electronics_connection_phase(include_runtime: bool = True):
    return builds(PowerElectronicsConnectionPhase, **power_electronics_connection_phase_kwargs(include_runtime))


def power_electronics_connection_phase_kwargs(include_runtime: bool = True):
    return {
        **power_system_resource_kwargs(include_runtime),
        "power_electronics_connection": builds(PowerElectronicsConnection, **identified_object_kwargs(include_runtime)),
        "phase": sampled_single_phase_kind(),
        "p": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "q": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    }


def create_power_transformer(include_runtime: bool = True):
    return builds(PowerTransformer, **power_transformer_kwargs(include_runtime))


def power_transformer_kwargs(include_runtime: bool = True):
    return {
        **conducting_equipment_kwargs(include_runtime),
        "asset_info": builds(PowerTransformerInfo, **identified_object_kwargs(include_runtime)),
        "power_transformer_ends": lists(builds(PowerTransformerEnd, **identified_object_kwargs(include_runtime)), max_size=2),
        "vector_group": sampled_vector_group(),
        "transformer_utilisation": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    }


def create_power_transformer_end(include_runtime: bool = True):
    return builds(create_power_transformer_end_with_ratings, **power_transformer_end_kwargs(include_runtime))


def power_transformer_end_kwargs(include_runtime: bool = True):
    return {
        **transformer_end_kwargs(include_runtime),
        "power_transformer": builds(PowerTransformer, **identified_object_kwargs(include_runtime)),
        # rated_s=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "rated_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "r0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "x": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "x0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "connection_kind": sampled_winding_connection(),
        "b": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "b0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "g": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "g0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "phase_angle_clock": integers(min_value=0, max_value=11),
        "ratings": lists(builds(
            TransformerEndRatedS,
            cooling_type=sampled_transformer_cooling_type(),
            rated_s=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
        ), max_size=11, unique_by=lambda it: it.cooling_type),
    }


def protected_switch_kwargs(include_runtime: bool):
    return {
        **switch_kwargs(include_runtime),
        "breaking_capacity": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "relay_functions": lists(builds(CurrentRelay, mrid=mrid_strategy), max_size=2),
    }


def create_ratio_tap_changer(include_runtime: bool = True):
    return builds(RatioTapChanger, **ratio_tap_changer_kwargs(include_runtime))


def ratio_tap_changer_kwargs(include_runtime: bool = True):
    return {
        **tap_changer_kwargs(include_runtime),
        "transformer_end": builds(PowerTransformerEnd, **identified_object_kwargs(include_runtime)),
        "step_voltage_increment": floats(min_value=0.0, max_value=1.0),
    }


def create_reactive_capability_curve(include_runtime: bool = True):
    return builds(ReactiveCapabilityCurve, **reactive_capability_curve_kwargs(include_runtime))


def reactive_capability_curve_kwargs(include_runtime: bool = True):
    return {
        **curve_kwargs(include_runtime),
    }


def create_recloser(include_runtime: bool = True):
    return builds(Recloser, **recloser_kwargs(include_runtime))


def recloser_kwargs(include_runtime: bool = True):
    return {
        **protected_switch_kwargs(include_runtime)
    }


def regulating_cond_eq_kwargs(include_runtime: bool):
    return {
        **energy_connection_kwargs(include_runtime),
        "control_enabled": one_of(none(), booleans()),
        "regulating_control": builds(TapChangerControl, **identified_object_kwargs(include_runtime)),
    }


def regulating_control_kwargs(include_runtime: bool):
    return {
        **power_system_resource_kwargs(include_runtime),
        "discrete": one_of(none(), booleans()),
        "mode": sampled_from(RegulatingControlModeKind),
        "monitored_phase": sampled_phase_code(),
        "target_deadband": floats(min_value=0.0, max_value=FLOAT_MAX),
        "target_value": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "enabled": one_of(none(), booleans()),
        "max_allowed_target_value": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "min_allowed_target_value": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "rated_current": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "terminal": builds(Terminal, **identified_object_kwargs(include_runtime)),
        "ct_primary": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "min_target_deadband": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "regulating_conducting_equipment": lists(builds(PowerElectronicsConnection, **identified_object_kwargs(include_runtime))),
    }


def sampled_regulating_control_mode_kind():
    return sampled_from(RegulatingControlModeKind)


def rotating_machine_kwargs(include_runtime: bool):
    return {
        **regulating_cond_eq_kwargs(include_runtime),
        "rated_power_factor": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "rated_s": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "rated_u": one_of(none(), integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)),
        "p": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "q": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
    }


def create_series_compensator(include_runtime: bool = True):
    return builds(SeriesCompensator, **series_compensator_kwargs(include_runtime))


def series_compensator_kwargs(include_runtime: bool = True):
    return {
        **conducting_equipment_kwargs(include_runtime),
        "r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "r0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "x": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "x0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "varistor_rated_current": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "varistor_voltage_threshold": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    }


def shunt_compensator_kwargs(include_runtime: bool):
    return {
        **regulating_cond_eq_kwargs(include_runtime),
        "asset_info": builds(ShuntCompensatorInfo, **identified_object_kwargs(include_runtime)),
        "grounded": booleans(),
        "nom_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "phase_connection": sampled_phase_shunt_connection_kind(),
        "sections": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "grounding_terminal": builds(Terminal, **identified_object_kwargs(include_runtime)),
    }


def sampled_single_phase_kind():
    return sampled_from(SinglePhaseKind)


def create_static_var_compensator(include_runtime: bool = True):
    return builds(StaticVarCompensator, **static_var_compensator_kwargs(include_runtime))


def static_var_compensator_kwargs(include_runtime: bool = True):
    return {
        **regulating_cond_eq_kwargs(include_runtime),
        "capacitive_rating": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "inductive_rating": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "q": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "svc_control_mode": sampled_svc_control_mode(),
        "voltage_set_point": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    }


def sampled_svc_control_mode():
    return sampled_from(SVCControlMode)


def switch_kwargs(include_runtime: bool):
    return {
        **conducting_equipment_kwargs(include_runtime),
        "rated_current": floats(min_value=1, max_value=FLOAT_MAX),
        # NOTE: These are not currently encoded properly in protobuf so we can only use all or none.
        "_normally_open": sampled_from([0, 15]),
        "_open": sampled_from([0, 15]),
        # "_normally_open": integers(min_value=0, max_value=15),
        # "_open": integers(min_value=0, max_value=15),
        "asset_info": builds(SwitchInfo, **identified_object_kwargs(include_runtime)),
    }


def create_synchronous_machine(include_runtime: bool = True):
    return builds(SynchronousMachine, **synchronous_machine_kwargs(include_runtime))


def synchronous_machine_kwargs(include_runtime: bool = True):
    return {
        **rotating_machine_kwargs(include_runtime),
        "curves": one_of(none(), lists(builds(ReactiveCapabilityCurve, **identified_object_kwargs(include_runtime)), max_size=2)),
        "base_q": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "condenser_p": one_of(none(), integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)),
        "earthing": one_of(none(), booleans()),
        "earthing_star_point_r": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "earthing_star_point_x": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "ikk": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "max_q": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "max_u": one_of(none(), integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)),
        "min_q": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "min_u": one_of(none(), integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)),
        "mu": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "r": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "r0": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "r2": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "sat_direct_subtrans_x": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "sat_direct_sync_x": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "sat_direct_trans_x": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "x0": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "x2": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        "type": sampled_synchronous_machine_kind(),
        "operating_mode": sampled_synchronous_machine_kind(),
    }


def sampled_synchronous_machine_kind():
    return sampled_from(SynchronousMachineKind)


def tap_changer_kwargs(include_runtime: bool):
    return {
        **power_system_resource_kwargs(include_runtime),
        "high_step": integers(min_value=10, max_value=15),
        "low_step": integers(min_value=0, max_value=2),
        "step": floats(min_value=2.0, max_value=10.0),
        "neutral_step": integers(min_value=2, max_value=10),
        "neutral_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "normal_step": integers(min_value=2, max_value=10),
        "control_enabled": booleans(),
        "tap_changer_control": builds(TapChangerControl, **identified_object_kwargs(include_runtime)),
    }


def create_tap_changer_control(include_runtime: bool = True):
    return builds(TapChangerControl, **tap_changer_control_kwargs(include_runtime))


def tap_changer_control_kwargs(include_runtime: bool = True):
    return {
        **regulating_control_kwargs(include_runtime),
        "limit_voltage": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "line_drop_compensation": one_of(none(), booleans()),
        "line_drop_r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "line_drop_x": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "reverse_line_drop_r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "reverse_line_drop_x": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "forward_ldc_blocking": one_of(none(), booleans()),
        "time_delay": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "co_generation_enabled": one_of(none(), booleans()),
    }


def transformer_end_kwargs(include_runtime: bool):
    return {
        **identified_object_kwargs(include_runtime),
        "terminal": builds(Terminal, **identified_object_kwargs(include_runtime)),
        "base_voltage": builds(BaseVoltage, **identified_object_kwargs(include_runtime)),
        "ratio_tap_changer": builds(RatioTapChanger, **identified_object_kwargs(include_runtime)),
        "end_number": integers(min_value=MIN_SEQUENCE_NUMBER, max_value=MAX_END_NUMBER),
        "grounded": booleans(),
        "r_ground": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "x_ground": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "star_impedance": builds(TransformerStarImpedance, **identified_object_kwargs(include_runtime)),
    }


def create_transformer_star_impedance(include_runtime: bool = True):
    return builds(TransformerStarImpedance, **transformer_star_impedance_kwargs(include_runtime))


def transformer_star_impedance_kwargs(include_runtime: bool = True):
    return {
        **identified_object_kwargs(include_runtime),
        "r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "r0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "x": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "x0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "transformer_end_info": builds(TransformerEndInfo, **identified_object_kwargs(include_runtime)),
    }


def sampled_winding_connection():
    return sampled_from(WindingConnection)


###############################
# IEC61970 InfIEC61970 Feeder #
###############################


def create_circuit(include_runtime: bool = True):
    return builds(Circuit, **circuit_kwargs(include_runtime))


def circuit_kwargs(include_runtime: bool = True):
    return {
        **line_kwargs(include_runtime),
        "loop": builds(Loop, **identified_object_kwargs(include_runtime)),
        "end_terminals": lists(builds(Terminal, **identified_object_kwargs(include_runtime)), max_size=2),
        "end_substations": lists(builds(Substation, **identified_object_kwargs(include_runtime)), max_size=2),
    }


###############
# SAMPLE SETS #
###############


def sampled_wire_info(include_runtime: bool):
    return choice([
        builds(OverheadWireInfo, **identified_object_kwargs(include_runtime)),
        builds(CableInfo, **identified_object_kwargs(include_runtime)),
    ])


def sampled_conducting_equipment(include_runtime: bool):
    return choice([
        # Don't add EnergySource to this list as it's used in SetPhases to start tracing, which will cause test_schema_terminal to fail.
        builds(AcLineSegment, **identified_object_kwargs(include_runtime)),
        builds(PowerTransformer, **identified_object_kwargs(include_runtime)),
        builds(Breaker, **identified_object_kwargs(include_runtime)),
        builds(Disconnector, **identified_object_kwargs(include_runtime)),
        builds(EnergyConsumer, **identified_object_kwargs(include_runtime)),
    ])


def sampled_curves(include_runtime: bool):
    return choice([
        builds(ReactiveCapabilityCurve, **identified_object_kwargs(include_runtime))
    ])


def sampled_end_device_function(include_runtime: bool):
    return choice([
        # Don't add EnergySource to this list as it's used in SetPhases to start tracing, which will cause test_schema_terminal to fail.
        builds(PanDemandResponseFunction, **identified_object_kwargs(include_runtime))
    ])


def sampled_equipment(include_runtime: bool):
    return choice([
        builds(AcLineSegment, **identified_object_kwargs(include_runtime)),
        builds(PowerTransformer, **identified_object_kwargs(include_runtime)),
        builds(Breaker, **identified_object_kwargs(include_runtime)),
        builds(Disconnector, **identified_object_kwargs(include_runtime)),
        builds(EnergyConsumer, **identified_object_kwargs(include_runtime)),
        builds(EnergySource, **identified_object_kwargs(include_runtime)),
        builds(FaultIndicator, **identified_object_kwargs(include_runtime))
    ])


def sampled_equipment_container(include_runtime: bool):
    available_containers = [
        builds(Site, **identified_object_kwargs(include_runtime)),
        builds(Circuit, **identified_object_kwargs(include_runtime)),
        builds(Substation, **identified_object_kwargs(include_runtime))
    ]

    if include_runtime:
        available_containers.append(builds(Feeder, **identified_object_kwargs(include_runtime)))

    return choice(available_containers)


def sampled_hvlv_feeder(include_runtime: bool):
    return choice([
        builds(Feeder, **identified_object_kwargs(include_runtime)),
        builds(LvFeeder, **identified_object_kwargs(include_runtime))
    ])


def sampled_measurement(include_runtime: bool):
    return choice([
        builds(Accumulator, **identified_object_kwargs(include_runtime)),
        builds(Analog, **identified_object_kwargs(include_runtime)),
        builds(Discrete, **identified_object_kwargs(include_runtime)),
    ])


def sampled_protected_switches(include_runtime: bool):
    return choice([
        builds(Breaker, **identified_object_kwargs(include_runtime)),
        builds(LoadBreakSwitch, **identified_object_kwargs(include_runtime)),
        builds(Recloser, **identified_object_kwargs(include_runtime))
    ])
