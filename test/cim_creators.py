#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime
from random import choice

from hypothesis.strategies import builds, text, integers, sampled_from, lists, floats, booleans, uuids, datetimes

from zepben.evolve import *
# WARNING!! # THIS IS A WORK IN PROGRESS AND MANY FUNCTIONS ARE LIKELY BROKEN
from zepben.evolve.model.cim.iec61970.base.core.name import Name
from zepben.evolve.model.cim.iec61970.base.core.name_type import NameType
from zepben.evolve.model.cim.iec61970.base.wires.generation.production.battery_state_kind import BatteryStateKind
from zepben.evolve.model.cim.iec61970.base.wires.generation.production.power_electronics_unit import BatteryUnit, PhotoVoltaicUnit, PowerElectronicsWindUnit
from zepben.evolve.model.cim.iec61970.base.wires.power_electronics_connection import PowerElectronicsConnection, PowerElectronicsConnectionPhase

MIN_32_BIT_INTEGER = -2147483648
MAX_32_BIT_INTEGER = 2147483647
MAX_64_BIT_INTEGER = 9223372036854775807
MIN_64_BIT_INTEGER = -9223372036854775808
TEXT_MAX_SIZE = 6
FLOAT_MIN = -100.0
FLOAT_MAX = 1000.0
MAX_END_NUMBER = 3
MAX_SEQUENCE_NUMBER = 40
MIN_SEQUENCE_NUMBER = 1
ALPHANUM = "abcdefghijbklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"


#######################
# IEC61968 ASSET INFO #
#######################


def create_cable_info():
    return builds(CableInfo, **create_wire_info())


def create_no_load_test():
    return builds(
        NoLoadTest,
        **create_transformer_test(),
        energised_end_voltage=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        exciting_current=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        exciting_current_zero=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        loss=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        loss_zero=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
    )


def create_open_circuit_test():
    return builds(
        OpenCircuitTest,
        **create_transformer_test(),
        energised_end_step=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        energised_end_voltage=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        open_end_step=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        open_end_voltage=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        phase_shift=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def create_overhead_wire_info():
    return builds(OverheadWireInfo, **create_wire_info())


def create_power_transformer_info():
    return builds(
        PowerTransformerInfo,
        **create_asset_info(),
        transformer_tank_infos=lists(builds(TransformerTankInfo, **create_identified_object()), min_size=1, max_size=2)
    )


def create_short_circuit_test():
    return builds(
        ShortCircuitTest,
        **create_transformer_test(),
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


def create_transformer_end_info():
    return builds(
        TransformerEndInfo,
        **create_asset_info(),
        connection_kind=sampled_winding_connection_kind(),
        emergency_s=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        end_number=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        insulation_u=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        phase_angle_clock=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        r=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        rated_s=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        rated_u=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        short_term_s=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        transformer_tank_info=builds(TransformerStarImpedance, **create_identified_object()),
        transformer_star_impedance=builds(TransformerStarImpedance, **create_identified_object()),
        energised_end_no_load_tests=builds(NoLoadTest, **create_identified_object()),
        energised_end_short_circuit_tests=builds(ShortCircuitTest, **create_identified_object()),
        grounded_end_short_circuit_tests=builds(ShortCircuitTest, **create_identified_object()),
        open_end_open_circuit_tests=builds(OpenCircuitTest, **create_identified_object()),
        energised_end_open_circuit_tests=builds(OpenCircuitTest, **create_identified_object()),
    )


def create_transformer_tank_info():
    return builds(
        TransformerTankInfo,
        **create_asset_info(),
        transformer_end_infos=lists(builds(TransformerEndInfo, **create_identified_object()), min_size=1, max_size=2)
    )


def create_transformer_test():
    return {
        **create_identified_object(),
        "base_power": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "temperature": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    }


def create_wire_info():
    return {
        **create_asset_info(),
        "rated_current": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "material": sampled_wire_material_kind()
    }


def sampled_wire_material_kind():
    return sampled_from(WireMaterialKind)


###################
# IEC61968 ASSETS #
###################


def create_asset():
    return {
        **create_identified_object(),
        "location": builds(Location, **create_identified_object()),
        "organisation_roles": lists(builds(AssetOwner, **create_identified_object()), min_size=1, max_size=2)
    }


def create_asset_info():
    return {**create_identified_object()}


def create_asset_container():
    return {**create_asset()}


def create_asset_organisation_role():
    return {**create_organisation_role()}


def create_asset_owner():
    return builds(AssetOwner, **create_asset_organisation_role())


def create_pole():
    return builds(
        Pole,
        **create_structure(),
        streetlights=lists(builds(Streetlight, **create_identified_object()), min_size=1, max_size=2),
        classification=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
    )


def create_streetlight():
    return builds(
        Streetlight,
        **create_asset(),
        pole=builds(Pole, **create_identified_object()),
        light_rating=integers(min_value=0, max_value=MAX_32_BIT_INTEGER * 2),
        lamp_kind=sampled_streetlight_lamp_kind()
    )


def sampled_streetlight_lamp_kind():
    return sampled_from(StreetlightLampKind)


def create_structure():
    return {**create_asset_container()}


###################
# IEC61968 COMMON #
###################


def create_agreement():
    return {**create_document()}


def create_document():
    return {
        **create_identified_object(),
        "title": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        "created_date_time": datetimes(min_value=datetime(1970, 1, 2)),
        "author_name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        "type": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        "status": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        "comment": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
    }


def create_location():
    return builds(Location, **create_identified_object(), main_address=builds(StreetAddress), position_points=lists(create_position_point(), max_size=4))


def create_organisation():
    return builds(Organisation, **create_identified_object())


def create_organisation_role():
    return {**create_identified_object(), "organisation": builds(Organisation, **create_identified_object())}


def create_position_point():
    return builds(PositionPoint, x_position=floats(min_value=-180.0, max_value=180.0), y_position=floats(min_value=-90.0, max_value=90.0))


def create_street_address():
    return builds(StreetAddress, postal_code=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), town_detail=builds(TownDetail))


def create_town_detail():
    return builds(TownDetail, name=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), state_or_province=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


######################
# IEC61968 CUSTOMERS #
######################


def create_customer():
    return builds(
        Customer,
        **create_organisation_role(),
        kind=sampled_customer_kind(),
        customer_agreements=lists(builds(CustomerAgreement, **create_identified_object()), min_size=1, max_size=2)
    )


def create_customer_agreement():
    return builds(
        CustomerAgreement,
        **create_agreement(),
        customer=builds(Customer, **create_identified_object()),
        pricing_structures=lists(builds(PricingStructure, **create_identified_object()), min_size=1, max_size=2)
    )


def sampled_customer_kind():
    return sampled_from(CustomerKind)


def create_pricing_structure():
    return builds(PricingStructure, **create_document(), tariffs=lists(builds(Tariff, **create_identified_object()), min_size=1, max_size=2))


def create_tariffs():
    return builds(Tariff, **create_document())


#####################
# IEC61968 METERING #
#####################


def create_end_device():
    return {
        **create_asset_container(),
        "usage_points": lists(builds(UsagePoint, **create_identified_object()), min_size=1, max_size=2),
        "customer_mrid": text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        "service_location": builds(Location, **create_identified_object())
    }


def create_meter():
    return builds(Meter, **create_end_device())


def create_usage_point():
    return builds(
        UsagePoint,
        **create_identified_object(),
        usage_point_location=builds(Location, **create_identified_object()),
        equipment=lists(builds(EnergyConsumer, **create_identified_object()), min_size=1, max_size=2),
        end_devices=lists(builds(Meter, **create_identified_object()), min_size=1, max_size=2)
    )


#######################
# IEC61968 OPERATIONS #
#######################


def create_operational_restriction():
    return builds(OperationalRestriction, **create_document(), equipment=lists(builds(PowerTransformer, **create_identified_object()), min_size=1, max_size=2))


#####################################
# IEC61970 BASE AUXILIARY EQUIPMENT #
#####################################


def create_auxiliary_equipment():
    return {**create_equipment(), "terminal": builds(Terminal, **create_identified_object())}


def create_fault_indicator():
    return builds(FaultIndicator, **create_auxiliary_equipment())


######################
# IEC61970 BASE CORE #
######################


def create_ac_dc_terminal():
    return {**create_identified_object()}


def create_base_voltage():
    return builds(BaseVoltage, **create_identified_object(), nominal_voltage=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER))


def create_conducting_equipment():
    return {
        **create_equipment(),
        "base_voltage": builds(BaseVoltage, **create_identified_object()),
        "terminals": lists(builds(Terminal, phases=sampled_from(PhaseCode)), min_size=1, max_size=2)
    }


def create_connectivity_node():
    return builds(ConnectivityNode, **create_identified_object(), terminals=lists(builds(Terminal, **create_identified_object()), max_size=10))


def create_connectivity_node_container():
    return {**create_power_system_resource()}


def create_equipment():
    return {
        **create_power_system_resource(),
        "in_service": booleans(),
        "normally_in_service": booleans(),
        "equipment_containers": lists(sampled_equipment_container(), min_size=1, max_size=2),
        "usage_points": lists(builds(UsagePoint, **create_identified_object()), min_size=1, max_size=2),
        "operational_restrictions": lists(builds(OperationalRestriction, **create_identified_object()), min_size=1, max_size=2),
        "current_feeders": lists(builds(Feeder, **create_identified_object()), min_size=1, max_size=2)
    }


def create_equipment_container():
    return {**create_connectivity_node_container(), "equipment": lists(sampled_equipment(), min_size=1, max_size=2)}


def create_feeder():
    return builds(
        Feeder,
        **create_equipment_container(),
        normal_head_terminal=builds(Terminal, **create_identified_object()),
        normal_energizing_substation=builds(Substation, **create_identified_object())
    )


def create_geographical_region():
    return builds(
        GeographicalRegion,
        **create_identified_object(),
        sub_geographical_regions=lists(builds(SubGeographicalRegion, **create_identified_object()), min_size=1, max_size=2)
    )


def create_identified_object():
    return {
        "mrid": uuids(version=4).map(lambda x: str(x)),
        "name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        "description": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
    }


def create_name():
    return builds(
        Name,
        name=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        type=create_name_type(),
        identified_object=sampled_equipment()
    )


def create_name_type():
    return builds(
        NameType,
        name=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        description=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
    )


def sampled_phase_code():
    return sampled_from(PhaseCode)


def create_power_system_resource():
    #
    # NOTE: We do not create the asset_info here, create it where it is actually used.
    #
    return {**create_identified_object(), "location": create_location()}


def create_site():
    return builds(Site, **create_equipment_container())


def create_sub_geographical_region():
    return builds(
        SubGeographicalRegion,
        **create_identified_object(),
        geographical_region=builds(GeographicalRegion, **create_identified_object()),
        substations=lists(builds(Substation, **create_identified_object()), min_size=1, max_size=2)
    )


def create_substation():
    return builds(
        Substation,
        **create_equipment_container(),
        sub_geographical_region=builds(SubGeographicalRegion, **create_identified_object()),
        normal_energized_feeders=lists(builds(Feeder, **create_identified_object()), min_size=1, max_size=2),
        loops=lists(builds(Loop, **create_identified_object()), min_size=1, max_size=2),
        energized_loops=lists(builds(Loop, **create_identified_object()), min_size=1, max_size=2),
        circuits=lists(builds(Circuit, **create_identified_object()), min_size=1, max_size=2)
    )


def create_terminal():
    return builds(
        Terminal,
        **create_ac_dc_terminal(),
        conducting_equipment=sampled_conducting_equipment(),
        connectivity_node=builds(ConnectivityNode, **create_identified_object()),
        traced_phases=builds(TracedPhases), phases=sampled_phase_code(),
        sequence_number=integers(min_value=MIN_SEQUENCE_NUMBER, max_value=MAX_SEQUENCE_NUMBER)
    )


#############################
# IEC61970 BASE EQUIVALENTS #
#############################


def create_equivalent_branch():
    return builds(
        EquivalentBranch,
        **create_equivalent_equipment(),
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


def create_equivalent_equipment():
    return {**create_conducting_equipment()}


################################
# IEC61970 BASE DIAGRAM LAYOUT #
################################


def create_diagram():
    return builds(
        Diagram,
        **create_identified_object(),
        diagram_style=sampled_from(DiagramStyle),
        orientation_kind=sampled_from(OrientationKind),
        diagram_objects=lists(builds(DiagramObject, **create_identified_object()), min_size=1, max_size=2)
    )


def create_diagram_object():
    return builds(
        DiagramObject,
        **create_identified_object(),
        diagram=builds(Diagram, **create_identified_object()),
        identified_object_mrid=text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        style=text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        rotation=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        diagram_object_points=lists(create_diagram_object_point(), min_size=1, max_size=2)
    )


def create_diagram_object_point():
    return builds(DiagramObjectPoint, x_position=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), y_position=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))


######################
# IEC61970 BASE MEAS #
######################


def create_accumulator():
    return builds(Accumulator, **create_measurement())


def create_accumulator_value():
    return builds(AccumulatorValue, **create_measurement())


def create_analog():
    return builds(Analog, **create_measurement(), positive_flow_in=booleans())


def create_analog_value():
    return builds(AnalogValue, **create_measurement())


def create_control():
    return builds(
        Control,
        **create_io_point(),
        power_system_resource_mrid=text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        remote_control=builds(RemoteControl, **create_identified_object())
    )


def create_discrete():
    return builds(Discrete, **create_measurement())


def create_discrete_value():
    return builds(DiscreteValue, **create_measurement())


def create_io_point():
    return {**create_identified_object()}


def create_measurement():
    return {
        **create_identified_object(),
        "remote_source": builds(RemoteSource, **create_identified_object()),
        "power_system_resource_mrid": uuids(version=4).map(lambda x: str(x)),
        "terminal_mrid": uuids(version=4).map(lambda x: str(x)),
        "phases": sampled_phase_code(),
        "unit_symbol": sampled_unit_symbol()
    }


def sampled_unit_symbol():
    return sampled_from(UnitSymbol)


#######################
# IEC61970 BASE SCADA #
#######################

def create_remote_control():
    return builds(RemoteControl, **create_remote_point(), control=builds(Control, **create_identified_object()))


def create_remote_point():
    return {**create_identified_object()}


def create_remote_source():
    return builds(RemoteSource, **create_remote_point(), measurement=sampled_measurement())


#############################################
# IEC61970 BASE WIRES GENERATION PRODUCTION #
#############################################


def sampled_battery_state_kind():
    return sampled_from(BatteryStateKind)


def create_battery_unit():
    return builds(
        BatteryUnit,
        **create_power_electronics_unit(),
        battery_state=sampled_battery_state_kind(),
        rated_e=integers(min_value=MIN_64_BIT_INTEGER, max_value=MAX_64_BIT_INTEGER),
        stored_e=integers(min_value=MIN_64_BIT_INTEGER, max_value=MAX_64_BIT_INTEGER)
    )


def create_photovoltaic_unit():
    return builds(PhotoVoltaicUnit, **create_power_electronics_unit())


def create_power_electronics_unit():
    return {
        **create_equipment(),
        "power_electronics_connection": builds(PowerElectronicsConnection, **create_identified_object()),
        "max_p": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "min_p": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
    }


def create_power_electronics_wind_unit():
    return builds(PowerElectronicsWindUnit, **create_power_electronics_unit())


#######################
# IEC61970 BASE WIRES #
#######################


def create_ac_line_segment():
    return builds(AcLineSegment, **create_conductor(), per_length_sequence_impedance=builds(PerLengthSequenceImpedance, **create_identified_object()))


def create_breaker():
    return builds(Breaker, **create_protected_switch())


def create_busbar_section():
    return builds(BusbarSection, **create_connector())


def create_conductor():
    return {**create_conducting_equipment(), "asset_info": sampled_wire_info(), "length": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)}


def create_connector():
    return {**create_conducting_equipment()}


def create_disconnector():
    return builds(Disconnector, **create_switch())


def create_energy_connection():
    return {**create_conducting_equipment()}


def create_energy_consumer():
    return builds(
        EnergyConsumer,
        **create_energy_connection(),
        energy_consumer_phases=lists(builds(EnergyConsumerPhase, **create_identified_object()), min_size=1, max_size=2),
        customer_count=integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
        grounded=booleans(),
        p=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        p_fixed=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        phase_connection=sampled_phase_shunt_connection_kind(),
        q=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        q_fixed=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def create_energy_consumer_phase():
    return builds(
        EnergyConsumerPhase,
        **create_power_system_resource(),
        energy_consumer=builds(EnergyConsumer, **create_identified_object()),
        phase=sampled_single_phase_kind(),
        p=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        p_fixed=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        q=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        q_fixed=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def create_energy_source():
    return builds(
        EnergySource,
        **create_energy_connection(),
        energy_source_phases=lists(builds(EnergySourcePhase, **create_identified_object()), min_size=1, max_size=2),
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
        xn=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def create_energy_source_phase():
    return builds(
        EnergySourcePhase,
        **create_power_system_resource(),
        energy_source=builds(EnergySource, **create_identified_object()),
        phase=sampled_single_phase_kind()
    )


def create_fuse():
    return builds(Fuse, **create_switch())


def create_jumper():
    return builds(Jumper, **create_switch())


def create_junction():
    return builds(Junction, **create_connector())


def create_line():
    return {**create_equipment_container()}


def create_linear_shunt_compensator():
    return builds(
        LinearShuntCompensator,
        **create_shunt_compensator(),
        b0_per_section=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        b_per_section=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        g0_per_section=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        g_per_section=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def create_load_break_switch():
    return builds(LoadBreakSwitch, **create_protected_switch())


def create_per_length_impedance():
    return {**create_per_length_line_parameter()}


def create_per_length_line_parameter():
    return {**create_identified_object()}


def create_per_length_sequence_impedance():
    return builds(
        PerLengthSequenceImpedance,
        **create_per_length_impedance(),
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


def create_power_electronics_connection():
    return builds(
        PowerElectronicsConnection,
        **create_power_system_resource(),
        power_electronics_units=lists(builds(BatteryUnit, **create_identified_object()), min_size=1, max_size=2),
        power_electronics_connection_phases=lists(builds(PowerElectronicsConnectionPhase, **create_identified_object()), min_size=1, max_size=2),
        max_i_fault=integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
        max_q=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        min_q=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        p=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        q=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        rated_s=integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
        rated_u=integers(min_value=0, max_value=MAX_32_BIT_INTEGER)
    )


def create_power_electronics_connection_phase():
    return builds(
        PowerElectronicsConnectionPhase,
        **create_power_system_resource(),
        power_electronics_connection=builds(PowerElectronicsConnection, **create_identified_object()),
        phase=sampled_single_phase_kind(),
        p=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        q=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def create_power_transformer():
    return builds(
        PowerTransformer,
        **create_conducting_equipment(),
        asset_info=builds(PowerTransformerInfo, **create_identified_object()),
        power_transformer_ends=lists(builds(PowerTransformerEnd, **create_identified_object()), min_size=1, max_size=2),
        vector_group=sampled_vector_group(),
        transformer_utilisation=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def create_power_transformer_end():
    return builds(
        PowerTransformerEnd,
        **create_transformer_end(),
        power_transformer=builds(PowerTransformer, **create_identified_object()),
        rated_s=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
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
        phase_angle_clock=integers(min_value=0, max_value=11)
    )


def create_protected_switch():
    return {**create_switch()}


def create_ratio_tap_changer():
    return builds(
        RatioTapChanger,
        **create_tap_changer(),
        transformer_end=builds(PowerTransformerEnd, **create_identified_object()),
        step_voltage_increment=floats(min_value=0.0, max_value=1.0)
    )


def create_recloser():
    return builds(Recloser, **create_protected_switch())


def create_regulating_cond_eq():
    return {**create_energy_connection(), "control_enabled": booleans()}


def create_shunt_compensator():
    return {
        **create_regulating_cond_eq(),
        "sections": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "grounded": booleans(),
        "nom_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "phase_connection": sampled_phase_shunt_connection_kind()
    }


def sampled_single_phase_kind():
    return sampled_from(SinglePhaseKind)


def create_switch():
    return {
        **create_conducting_equipment(),
        # NOTE: These are not currently encoded properly in protobuf so we can only use all or none.
        "_normally_open": sampled_from([0, 15]),
        "_open": sampled_from([0, 15])
        # "_normally_open": integers(min_value=0, max_value=15),
        # "_open": integers(min_value=0, max_value=15)
    }


def create_tap_changer():
    return {
        **create_power_system_resource(),
        "high_step": integers(min_value=10, max_value=15),
        "low_step": integers(min_value=0, max_value=2),
        "step": floats(min_value=2.0, max_value=10.0),
        "neutral_step": integers(min_value=2, max_value=10),
        "neutral_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        "normal_step": integers(min_value=2, max_value=10),
        "control_enabled": booleans()
    }


def create_transformer_end():
    return {
        **create_identified_object(),
        "terminal": builds(Terminal, **create_identified_object()),
        "base_voltage": builds(BaseVoltage, **create_identified_object()),
        "ratio_tap_changer": builds(RatioTapChanger, **create_identified_object()),
        "end_number": integers(min_value=MIN_SEQUENCE_NUMBER, max_value=MAX_END_NUMBER),
        "grounded": booleans(),
        "r_ground": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "x_ground": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        "star_impedance": builds(TransformerStarImpedance, **create_identified_object())
    }


def create_transformer_star_impedance():
    return builds(
        TransformerStarImpedance,
        **create_identified_object(),
        r=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        r0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        transformer_end_info=builds(TransformerEndInfo, **create_identified_object())
    )


def sampled_vector_group():
    return sampled_from(VectorGroup)


def sampled_winding_connection_kind():
    return sampled_from(WindingConnection)


#########################
# IEC61970 INF IEC61970 #
#########################


def create_circuit():
    return builds(
        Circuit,
        **create_line(),
        loop=builds(Loop, **create_identified_object()),
        end_terminals=lists(builds(Terminal, **create_identified_object()), min_size=1, max_size=2),
        end_substations=lists(builds(Substation, **create_identified_object()), min_size=1, max_size=2)
    )


def create_loop():
    return builds(
        Loop,
        **create_identified_object(),
        circuits=lists(builds(Circuit, **create_identified_object()), min_size=1, max_size=2),
        substations=lists(builds(Substation, **create_identified_object()), min_size=1, max_size=2),
        energizing_substations=lists(builds(Substation, **create_identified_object()), min_size=1, max_size=2)
    )


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


def sampled_wire_info():
    return choice([
        builds(OverheadWireInfo, **create_identified_object()),
        builds(CableInfo, **create_identified_object()),
    ])


def sampled_conducting_equipment():
    return choice([
        builds(AcLineSegment, **create_identified_object()),
        builds(PowerTransformer, **create_identified_object()),
        builds(Breaker, **create_identified_object()),
        builds(Disconnector, **create_identified_object()),
        builds(EnergyConsumer, **create_identified_object()),
        builds(EnergySource, **create_identified_object()),
    ])


def sampled_equipment():
    return choice([
        builds(AcLineSegment, **create_identified_object()),
        builds(PowerTransformer, **create_identified_object()),
        builds(Breaker, **create_identified_object()),
        builds(Disconnector, **create_identified_object()),
        builds(EnergyConsumer, **create_identified_object()),
        builds(EnergySource, **create_identified_object()),
        builds(FaultIndicator, **create_identified_object())
    ])


def sampled_equipment_container():
    return choice([
        builds(Feeder, **create_identified_object()),
        builds(Site, **create_identified_object()),
        builds(Circuit, **create_identified_object()),
        builds(Loop, **create_identified_object()),
        builds(Substation, **create_identified_object())
    ])


def sampled_measurement():
    return choice([
        builds(Accumulator),
        builds(Analog),
        builds(Discrete),
    ])
