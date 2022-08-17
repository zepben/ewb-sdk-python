#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import functools
import io
import os
import tempfile
from collections import Counter
from traceback import print_exc
from typing import TypeVar, Callable, Any

from hypothesis import given, settings, assume, HealthCheck

from test.cim.cim_creators import create_cable_info, create_no_load_test, create_open_circuit_test, create_overhead_wire_info, create_power_transformer_info, \
    create_short_circuit_test, create_shunt_compensator_info, create_transformer_end_info, create_transformer_tank_info, create_asset_owner, create_pole, \
    create_streetlight, create_location, create_organisation, create_customer, create_customer_agreement, create_pricing_structure, create_tariffs, \
    create_meter, create_usage_point, create_operational_restriction, create_fault_indicator, create_base_voltage, create_connectivity_node, create_feeder, \
    create_geographical_region, create_site, create_sub_geographical_region, create_substation, create_terminal, create_equivalent_branch, create_diagram, \
    create_diagram_object, create_accumulator, create_analog, create_control, create_discrete, create_remote_control, create_remote_source, \
    create_battery_unit, create_photovoltaic_unit, create_power_electronics_wind_unit, create_ac_line_segment, create_breaker, create_busbar_section, \
    create_disconnector, create_energy_consumer, create_energy_consumer_phase, create_energy_source, create_energy_source_phase, create_fuse, create_jumper, \
    create_junction, create_linear_shunt_compensator, create_load_break_switch, create_per_length_sequence_impedance, create_power_electronics_connection, \
    create_power_electronics_connection_phase, create_power_transformer, create_power_transformer_end, create_ratio_tap_changer, create_recloser, \
    create_transformer_star_impedance, create_circuit, create_loop
from test.database.sqlite.schema_utils import SchemaNetworks, Services, assume_non_blank_street_address_details
from zepben.evolve import MetadataCollection, IdentifiedObject, AcLineSegment, CableInfo, \
    NoLoadTest, OpenCircuitTest, OverheadWireInfo, PowerTransformerInfo, ShortCircuitTest, ShuntCompensatorInfo, TransformerEndInfo, TransformerTankInfo, \
    AssetOwner, Pole, Streetlight, Customer, CustomerAgreement, PricingStructure, Tariff, Meter, UsagePoint, Location, Organisation, OperationalRestriction, \
    FaultIndicator, BaseVoltage, ConnectivityNode, Feeder, GeographicalRegion, Site, SubGeographicalRegion, Substation, Terminal, Diagram, DiagramObject, \
    EquivalentBranch, Accumulator, Analog, Control, Discrete, RemoteControl, RemoteSource, BatteryUnit, \
    PhotoVoltaicUnit, PowerElectronicsConnection, PowerElectronicsConnectionPhase, PowerElectronicsWindUnit, Breaker, BusbarSection, Disconnector, \
    EnergyConsumer, EnergyConsumerPhase, EnergySource, EnergySourcePhase, Fuse, Jumper, Junction, LinearShuntCompensator, LoadBreakSwitch, \
    PerLengthSequenceImpedance, PowerTransformer, PowerTransformerEnd, RatioTapChanger, Recloser, TransformerStarImpedance, Circuit, Loop, BaseService, \
    DatabaseWriter, TableVersion, DatabaseReader, NetworkServiceComparator, BaseServiceComparator, StreetAddress, TownDetail, StreetDetail
from zepben.evolve.services.customer.customer_service_comparator import CustomerServiceComparator
from zepben.evolve.services.diagram.diagram_service_comparator import DiagramServiceComparator

T = TypeVar("T", bound=IdentifiedObject)

std_err = io.StringIO()


def log_on_failure_decorator(func):
    @functools.wraps(func)
    def log_on_failure(*args, **kwargs):
        try:
            # noinspection PyProtectedMember
            args[0]._caplog = kwargs["caplog"]
            func(*args, **kwargs)
        except Exception as e:
            print_exc()
            caplog = kwargs["caplog"]
            print(caplog.text)
            raise e

    return log_on_failure


class TestDatabaseSqlite(object):
    _caplog: Any

    # ************ IEC61968 ASSET INFO ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(cable_info=create_cable_info(False))
    def test_schema_cable_info(self, caplog, cable_info):
        self._validate_schema(SchemaNetworks().network_services_of(CableInfo, cable_info))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(no_load_test=create_no_load_test(False))
    def test_schema_no_load_test(self, caplog, no_load_test):
        self._validate_schema(SchemaNetworks().network_services_of(NoLoadTest, no_load_test))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(open_circuit_test=create_open_circuit_test(False))
    def test_schema_open_circuit_test(self, caplog, open_circuit_test):
        self._validate_schema(SchemaNetworks().network_services_of(OpenCircuitTest, open_circuit_test))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(overhead_wire_info=create_overhead_wire_info(False))
    def test_schema_overhead_wire_info(self, caplog, overhead_wire_info):
        self._validate_schema(SchemaNetworks().network_services_of(OverheadWireInfo, overhead_wire_info))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(power_transformer_info=create_power_transformer_info(False))
    def test_schema_power_transformer_info(self, caplog, power_transformer_info):
        self._validate_schema(SchemaNetworks().network_services_of(PowerTransformerInfo, power_transformer_info))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(short_circuit_test=create_short_circuit_test(False))
    def test_schema_short_circuit_test(self, caplog, short_circuit_test):
        self._validate_schema(SchemaNetworks().network_services_of(ShortCircuitTest, short_circuit_test))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(shunt_compensator_info=create_shunt_compensator_info(False))
    def test_schema_shunt_compensator_info(self, caplog, shunt_compensator_info):
        self._validate_schema(SchemaNetworks().network_services_of(ShuntCompensatorInfo, shunt_compensator_info))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(transformer_end_info=create_transformer_end_info(False))
    def test_schema_transformer_end_info(self, caplog, transformer_end_info):
        self._validate_schema(SchemaNetworks().network_services_of(TransformerEndInfo, transformer_end_info))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(transformer_tank_info=create_transformer_tank_info(False))
    def test_schema_transformer_tank_info(self, caplog, transformer_tank_info):
        self._validate_schema(SchemaNetworks().network_services_of(TransformerTankInfo, transformer_tank_info))

    # ************ IEC61968 ASSETS ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(asset_owner=create_asset_owner(False))
    def test_schema_asset_owner(self, caplog, asset_owner):
        self._validate_schema(SchemaNetworks().network_services_of(AssetOwner, asset_owner))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(pole=create_pole(False))
    def test_schema_pole(self, caplog, pole):
        self._validate_schema(SchemaNetworks().network_services_of(Pole, pole))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(streetlight=create_streetlight(False))
    def test_schema_streetlight(self, caplog, streetlight):
        self._validate_schema(SchemaNetworks().network_services_of(Streetlight, streetlight))

    # ************ IEC61968 CUSTOMERS ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(customer=create_customer(False))
    def test_schema_customer(self, caplog, customer):
        self._validate_schema(SchemaNetworks().customer_services_of(Customer, customer))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(customer_agreement=create_customer_agreement(False))
    def test_schema_customer_agreement(self, caplog, customer_agreement):
        self._validate_schema(SchemaNetworks().customer_services_of(CustomerAgreement, customer_agreement))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(pricing_structure=create_pricing_structure(False))
    def test_schema_pricing_structure(self, caplog, pricing_structure):
        self._validate_schema(SchemaNetworks().customer_services_of(PricingStructure, pricing_structure))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(tariffs=create_tariffs(False))
    def test_schema_tariffs(self, caplog, tariffs):
        self._validate_schema(SchemaNetworks().customer_services_of(Tariff, tariffs))

    # ************ IEC61968 METERING ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(meter=create_meter(False))
    def test_schema_meter(self, caplog, meter):
        self._validate_schema(SchemaNetworks().network_services_of(Meter, meter))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(usage_point=create_usage_point(False))
    def test_schema_usage_point(self, caplog, usage_point):
        self._validate_schema(SchemaNetworks().network_services_of(UsagePoint, usage_point))

    # ************ IEC61968 COMMON ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(location=create_location(False))
    def test_schema_location(self, caplog, location):
        self._validate_schema(SchemaNetworks().network_services_of(Location, location))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(organisation=create_organisation(False))
    def test_schema_organisation(self, caplog, organisation):
        self._validate_schema(SchemaNetworks().network_services_of(Organisation, organisation))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(organisation=create_organisation(False))
    def test_schema_organisation(self, caplog, organisation):
        self._validate_schema(SchemaNetworks().customer_services_of(Organisation, organisation))

    # ************ IEC61968 OPERATIONS ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(operational_restriction=create_operational_restriction(False))
    def test_schema_operational_restriction(self, caplog, operational_restriction):
        self._validate_schema(SchemaNetworks().network_services_of(OperationalRestriction, operational_restriction))

    # ************ IEC61970 BASE AUXILIARY EQUIPMENT ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(fault_indicator=create_fault_indicator(False))
    def test_schema_fault_indicator(self, caplog, fault_indicator):
        self._validate_schema(SchemaNetworks().network_services_of(FaultIndicator, fault_indicator))

    # ************ IEC61970 BASE CORE ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(base_voltage=create_base_voltage(False))
    def test_schema_base_voltage(self, caplog, base_voltage):
        self._validate_schema(SchemaNetworks().network_services_of(BaseVoltage, base_voltage))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(connectivity_node=create_connectivity_node(False))
    def test_schema_connectivity_node(self, caplog, connectivity_node):
        self._validate_schema(SchemaNetworks().network_services_of(ConnectivityNode, connectivity_node))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(feeder=create_feeder(False))
    def test_schema_feeder(self, caplog, feeder):
        self._validate_schema(SchemaNetworks().network_services_of(Feeder, feeder))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(geographical_region=create_geographical_region(False))
    def test_schema_geographical_region(self, caplog, geographical_region):
        self._validate_schema(SchemaNetworks().network_services_of(GeographicalRegion, geographical_region))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(site=create_site(False))
    def test_schema_site(self, caplog, site):
        self._validate_schema(SchemaNetworks().network_services_of(Site, site))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(sub_geographical_region=create_sub_geographical_region(False))
    def test_schema_sub_geographical_region(self, caplog, sub_geographical_region):
        self._validate_schema(SchemaNetworks().network_services_of(SubGeographicalRegion, sub_geographical_region))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(substation=create_substation(False))
    def test_schema_substation(self, caplog, substation):
        self._validate_schema(SchemaNetworks().network_services_of(Substation, substation))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(terminal=create_terminal(False))
    def test_schema_terminal(self, caplog, terminal):
        self._validate_schema(SchemaNetworks().network_services_of(Terminal, terminal))

    # ************ IEC61970 BASE DIAGRAM LAYOUT ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(diagram=create_diagram(False))
    def test_schema_diagram(self, caplog, diagram):
        self._validate_schema(SchemaNetworks().diagram_services_of(Diagram, diagram))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(diagram_object=create_diagram_object(False))
    def test_schema_diagram_object(self, caplog, diagram_object):
        self._validate_schema(SchemaNetworks().diagram_services_of(DiagramObject, diagram_object))

    # ************ IEC61970 BASE EQUIVALENTS ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(equivalent_branch=create_equivalent_branch(False))
    def test_schema_equivalent_branch(self, caplog, equivalent_branch):
        self._validate_schema(SchemaNetworks().network_services_of(EquivalentBranch, equivalent_branch))

    # ************ IEC61970 BASE MEAS ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(accumulator=create_accumulator(False))
    def test_schema_accumulator(self, caplog, accumulator):
        self._validate_schema(SchemaNetworks().network_services_of(Accumulator, accumulator))

        # self._validate_schema(SchemaNetworks().measurement_services_of(AccumulatorValue, data.draw(create_accumulator_value(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(analog=create_analog(False))
    def test_schema_analog(self, caplog, analog):
        self._validate_schema(SchemaNetworks().network_services_of(Analog, analog))

        # self._validate_schema(SchemaNetworks().measurement_services_of(AnalogValue, data.draw(create_analog_value(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(control=create_control(False))
    def test_schema_control(self, caplog, control):
        self._validate_schema(SchemaNetworks().network_services_of(Control, control))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(discrete=create_discrete(False))
    def test_schema_discrete(self, caplog, discrete):
        self._validate_schema(SchemaNetworks().network_services_of(Discrete, discrete))

        # self._validate_schema(SchemaNetworks().measurement_services_of(DiscreteValue, data.draw(create_discrete_value(False))))

    # ************ IEC61970 BASE SCADA ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(remote_control=create_remote_control(False))
    def test_schema_remote_control(self, caplog, remote_control):
        self._validate_schema(SchemaNetworks().network_services_of(RemoteControl, remote_control))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(remote_source=create_remote_source(False))
    def test_schema_remote_source(self, caplog, remote_source):
        self._validate_schema(SchemaNetworks().network_services_of(RemoteSource, remote_source))

    # ************ IEC61970 BASE WIRES GENERATION PRODUCTION ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(battery_unit=create_battery_unit(False))
    def test_schema_battery_unit(self, caplog, battery_unit):
        self._validate_schema(SchemaNetworks().network_services_of(BatteryUnit, battery_unit))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(photovoltaic_unit=create_photovoltaic_unit(False))
    def test_schema_photovoltaic_unit(self, caplog, photovoltaic_unit):
        self._validate_schema(SchemaNetworks().network_services_of(PhotoVoltaicUnit, photovoltaic_unit))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(power_electronics_connection=create_power_electronics_connection(False))
    def test_schema_power_electronics_connection(self, caplog, power_electronics_connection):
        self._validate_schema(SchemaNetworks().network_services_of(PowerElectronicsConnection, power_electronics_connection))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(power_electronics_connection_phase=create_power_electronics_connection_phase(False))
    def test_schema_power_electronics_connection_phase(self, caplog, power_electronics_connection_phase):
        self._validate_schema(SchemaNetworks().network_services_of(PowerElectronicsConnectionPhase, power_electronics_connection_phase))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(power_electronics_wind_unit=create_power_electronics_wind_unit(False))
    def test_schema_power_electronics_wind_unit(self, caplog, power_electronics_wind_unit):
        self._validate_schema(SchemaNetworks().network_services_of(PowerElectronicsWindUnit, power_electronics_wind_unit))

    # ************ IEC61970 BASE WIRES ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(ac_line_segment=create_ac_line_segment(False))
    def test_schema_ac_line_segment(self, caplog, ac_line_segment):
        self._validate_schema(SchemaNetworks().network_services_of(AcLineSegment, ac_line_segment))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(breaker=create_breaker(False))
    def test_schema_breaker(self, caplog, breaker):
        self._validate_schema(SchemaNetworks().network_services_of(Breaker, breaker))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(busbar_section=create_busbar_section(False))
    def test_schema_busbar_section(self, caplog, busbar_section):
        self._validate_schema(SchemaNetworks().network_services_of(BusbarSection, busbar_section))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(disconnector=create_disconnector(False))
    def test_schema_disconnector(self, caplog, disconnector):
        self._validate_schema(SchemaNetworks().network_services_of(Disconnector, disconnector))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(energy_consumer=create_energy_consumer(False))
    def test_schema_energy_consumer(self, caplog, energy_consumer):
        assume(len(Counter(map(lambda it: it.phase, energy_consumer.phases))) == len(list(energy_consumer.phases)))
        self._validate_schema(SchemaNetworks().network_services_of(EnergyConsumer, energy_consumer))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(energy_consumer_phase=create_energy_consumer_phase(False))
    def test_schema_energy_consumer_phase(self, caplog, energy_consumer_phase):
        self._validate_schema(SchemaNetworks().network_services_of(EnergyConsumerPhase, energy_consumer_phase))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(energy_source=create_energy_source(False))
    def test_schema_energy_source(self, caplog, energy_source):
        assume(len(Counter(map(lambda it: it.phase, energy_source.phases))) == len(list(energy_source.phases)))
        self._validate_schema(SchemaNetworks().network_services_of(EnergySource, energy_source))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(energy_source_phase=create_energy_source_phase(False))
    def test_schema_energy_source_phase(self, caplog, energy_source_phase):
        self._validate_schema(SchemaNetworks().network_services_of(EnergySourcePhase, energy_source_phase))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(fuse=create_fuse(False))
    def test_schema_fuse(self, caplog, fuse):
        self._validate_schema(SchemaNetworks().network_services_of(Fuse, fuse))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(jumper=create_jumper(False))
    def test_schema_jumper(self, caplog, jumper):
        self._validate_schema(SchemaNetworks().network_services_of(Jumper, jumper))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(junction=create_junction(False))
    def test_schema_junction(self, caplog, junction):
        self._validate_schema(SchemaNetworks().network_services_of(Junction, junction))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(linear_shunt_compensator=create_linear_shunt_compensator(False))
    def test_schema_linear_shunt_compensator(self, caplog, linear_shunt_compensator):
        self._validate_schema(SchemaNetworks().network_services_of(LinearShuntCompensator, linear_shunt_compensator))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(load_break_switch=create_load_break_switch(False))
    def test_schema_load_break_switch(self, caplog, load_break_switch):
        self._validate_schema(SchemaNetworks().network_services_of(LoadBreakSwitch, load_break_switch))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(per_length_sequence_impedance=create_per_length_sequence_impedance(False))
    def test_schema_per_length_sequence_impedance(self, caplog, per_length_sequence_impedance):
        self._validate_schema(SchemaNetworks().network_services_of(PerLengthSequenceImpedance, per_length_sequence_impedance))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(power_transformer=create_power_transformer(False))
    def test_schema_power_transformer(self, caplog, power_transformer):
        self._validate_schema(SchemaNetworks().network_services_of(PowerTransformer, power_transformer))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(power_transformer_end=create_power_transformer_end(False))
    def test_schema_power_transformer_end(self, caplog, power_transformer_end):
        self._validate_schema(SchemaNetworks().network_services_of(PowerTransformerEnd, power_transformer_end))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(ratio_tap_changer=create_ratio_tap_changer(False))
    def test_schema_ratio_tap_changer(self, caplog, ratio_tap_changer):
        self._validate_schema(SchemaNetworks().network_services_of(RatioTapChanger, ratio_tap_changer))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(recloser=create_recloser(False))
    def test_schema_recloser(self, caplog, recloser):
        self._validate_schema(SchemaNetworks().network_services_of(Recloser, recloser))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(transformer_star_impedance=create_transformer_star_impedance(False))
    def test_schema_transformer_star_impedance(self, caplog, transformer_star_impedance):
        self._validate_schema(SchemaNetworks().network_services_of(TransformerStarImpedance, transformer_star_impedance))

    # ************ IEC61970 InfIEC61970 ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(circuit=create_circuit(False))
    def test_schema_circuit(self, caplog, circuit):
        self._validate_schema(SchemaNetworks().network_services_of(Circuit, circuit))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(loop=create_loop(False))
    def test_schema_loop(self, caplog, loop):
        self._validate_schema(SchemaNetworks().network_services_of(Loop, loop))

    # ************ Services ************

    @log_on_failure_decorator
    def test_metadata_data_source_schema(self, caplog):
        self._validate_schema(SchemaNetworks().create_data_source_test_services())

    @log_on_failure_decorator
    def test_name_and_name_type_schema(self, caplog):
        self._validate_schema(SchemaNetworks().create_name_test_services())

    @log_on_failure_decorator
    def test_error_on_duplicate_id_added_to_customer_service(self, caplog):
        write_services = Services()
        read_services = Services()

        customer = Customer(mrid="customer1")
        write_services.customer_service.add(customer)
        read_services.customer_service.add(customer)

        self._test_duplicate_mrid_error(write_services, read_services, read_services.customer_service, customer)

    @log_on_failure_decorator
    def test_error_on_duplicate_id_added_to_diagram_service(self, caplog):
        write_services = Services()
        read_services = Services()

        diagram = Diagram(mrid="diagram1")
        write_services.diagram_service.add(diagram)
        read_services.diagram_service.add(diagram)

        self._test_duplicate_mrid_error(write_services, read_services, read_services.diagram_service, diagram)

    @log_on_failure_decorator
    def test_error_on_duplicate_id_added_to_network_service(self, caplog):
        write_services = Services()
        read_services = Services()

        junction = Junction(mrid="junction1")
        write_services.network_service.add(junction)
        read_services.network_service.add(junction)

        self._test_duplicate_mrid_error(write_services, read_services, read_services.network_service, junction)

    @log_on_failure_decorator
    def test_only_loads_street_address_fields_if_required(self, caplog):
        write_services = Services()
        read_services = Services()

        # noinspection PyArgumentList
        location = Location(mrid="loc1", main_address=StreetAddress(town_detail=TownDetail(), street_detail=StreetDetail()))
        write_services.network_service.add(location)

        read_services = Services()

        def validate_read(success):
            assert success
            loc = read_services.network_service.get("loc1", Location)
            assert loc.main_address == StreetAddress()

        self._test_write_read(
            write_services,
            read_services,
            validate_read
        )

    def _test_duplicate_mrid_error(
        self,
        write_services: Services,
        read_services: Services,
        service_with_duplicate: BaseService,
        duplicate: IdentifiedObject
    ):
        expected_error = f"Failed to load {duplicate}. Unable to add to service '{service_with_duplicate.name}': duplicate MRID"

        def validate_read(success):
            assert not success
            assert expected_error in self._caplog.text

        self._test_write_read(
            write_services,
            read_services,
            validate_read
        )

    def _validate_schema(self, expected: Services):
        for location in expected.network_service.objects(Location):
            assume_non_blank_street_address_details(location.main_address)

        read_services = Services()

        def validate_read(success):
            assert success
            self._validate_metadata(read_services.metadata_collection, expected.metadata_collection)
            self._validate_service(read_services.network_service, expected.network_service, NetworkServiceComparator())
            self._validate_service(read_services.diagram_service, expected.diagram_service, DiagramServiceComparator())
            self._validate_service(read_services.customer_service, expected.customer_service, CustomerServiceComparator())
            for d_obj in filter(lambda it: it.identified_object_mrid is not None, expected.diagram_service.objects(DiagramObject)):
                assert read_services.diagram_service.get_diagram_objects(d_obj.identified_object_mrid)

        self._test_write_read(
            expected,
            read_services,
            validate_read
        )

    def _test_write_read(
        self,
        write: Services,
        read: Services,
        validate_read: Callable[[bool], None]
    ):
        self._caplog.clear()
        global std_err
        std_err = io.StringIO()
        with contextlib.redirect_stderr(std_err):
            schema_test_file_temp = tempfile.NamedTemporaryFile()
            schema_test_file = schema_test_file_temp.name
            # noinspection PyArgumentList
            assert DatabaseWriter(schema_test_file).save(
                write.metadata_collection,
                [
                    write.network_service,
                    write.diagram_service,
                    write.customer_service
                ]
            )

            assert f"Creating database schema v{TableVersion.SUPPORTED_VERSION}" in self._caplog.text
            assert os.path.isfile(schema_test_file)

            validate_read(
                DatabaseReader(schema_test_file).load(
                    read.metadata_collection,
                    read.network_service,
                    read.diagram_service,
                    read.customer_service
                )
            )

    @staticmethod
    def _validate_metadata(metadata_collection: MetadataCollection, expected_metadata_collection: MetadataCollection):
        assert Counter(metadata_collection.data_sources) == Counter(expected_metadata_collection.data_sources)

    @staticmethod
    def _validate_service(
        service: BaseService,
        expected_service: BaseService,
        comparator: BaseServiceComparator
    ):
        differences = comparator.compare_services(service, expected_service, False)

        if list(differences.modifications()):
            print(str(differences))

        assert not list(differences.missing_from_target()), "unexpected objects found in loaded network"
        assert not list(differences.modifications()), "unexpected modifications"
        assert not list(differences.missing_from_source()), "objects missing from loaded network"
