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

from hypothesis import given, settings, assume
from hypothesis.strategies import data

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
    @settings(deadline=1000)
    @given(data())
    def test_schema_cable_info(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(CableInfo, data.draw(create_cable_info(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_no_load_test(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(NoLoadTest, data.draw(create_no_load_test(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_open_circuit_test(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(OpenCircuitTest, data.draw(create_open_circuit_test(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_overhead_wire_info(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(OverheadWireInfo, data.draw(create_overhead_wire_info(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_power_transformer_info(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(PowerTransformerInfo, data.draw(create_power_transformer_info(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_short_circuit_test(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(ShortCircuitTest, data.draw(create_short_circuit_test(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_shunt_compensator_info(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(ShuntCompensatorInfo, data.draw(create_shunt_compensator_info(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_transformer_end_info(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(TransformerEndInfo, data.draw(create_transformer_end_info(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_transformer_tank_info(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(TransformerTankInfo, data.draw(create_transformer_tank_info(False))))

    # ************ IEC61968 ASSETS ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_asset_owner(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(AssetOwner, data.draw(create_asset_owner(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_pole(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Pole, data.draw(create_pole(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_streetlight(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Streetlight, data.draw(create_streetlight(False))))

    # ************ IEC61968 CUSTOMERS ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_customer(self, caplog, data):
        self._validate_schema(SchemaNetworks().customer_services_of(Customer, data.draw(create_customer(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_customer_agreement(self, caplog, data):
        self._validate_schema(SchemaNetworks().customer_services_of(CustomerAgreement, data.draw(create_customer_agreement(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_pricing_structure(self, caplog, data):
        self._validate_schema(SchemaNetworks().customer_services_of(PricingStructure, data.draw(create_pricing_structure(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_tariffs(self, caplog, data):
        self._validate_schema(SchemaNetworks().customer_services_of(Tariff, data.draw(create_tariffs(False))))

    # ************ IEC61968 METERING ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_meter(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Meter, data.draw(create_meter(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_usage_point(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(UsagePoint, data.draw(create_usage_point(False))))

    # ************ IEC61968 COMMON ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_location(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Location, data.draw(create_location(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_organisation(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Organisation, data.draw(create_organisation(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_organisation(self, caplog, data):
        self._validate_schema(SchemaNetworks().customer_services_of(Organisation, data.draw(create_organisation(False))))

    # ************ IEC61968 OPERATIONS ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_operational_restriction(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(OperationalRestriction, data.draw(create_operational_restriction(False))))

    # ************ IEC61970 BASE AUXILIARY EQUIPMENT ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_fault_indicator(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(FaultIndicator, data.draw(create_fault_indicator(False))))

    # ************ IEC61970 BASE CORE ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_base_voltage(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(BaseVoltage, data.draw(create_base_voltage(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_connectivity_node(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(ConnectivityNode, data.draw(create_connectivity_node(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_feeder(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Feeder, data.draw(create_feeder(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_geographical_region(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(GeographicalRegion, data.draw(create_geographical_region(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_site(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Site, data.draw(create_site(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_sub_geographical_region(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(SubGeographicalRegion, data.draw(create_sub_geographical_region(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_substation(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Substation, data.draw(create_substation(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_terminal(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Terminal, data.draw(create_terminal(False))))

    # ************ IEC61970 BASE DIAGRAM LAYOUT ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_diagram(self, caplog, data):
        self._validate_schema(SchemaNetworks().diagram_services_of(Diagram, data.draw(create_diagram(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_diagram_object(self, caplog, data):
        self._validate_schema(SchemaNetworks().diagram_services_of(DiagramObject, data.draw(create_diagram_object(False))))

    # ************ IEC61970 BASE EQUIVALENTS ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_equivalent_branch(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(EquivalentBranch, data.draw(create_equivalent_branch(False))))

    # ************ IEC61970 BASE MEAS ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_accumulator(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Accumulator, data.draw(create_accumulator(False))))

        # self._validate_schema(SchemaNetworks().measurement_services_of(AccumulatorValue, data.draw(create_accumulator_value(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_analog(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Analog, data.draw(create_analog(False))))

        # self._validate_schema(SchemaNetworks().measurement_services_of(AnalogValue, data.draw(create_analog_value(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_control(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Control, data.draw(create_control(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_discrete(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Discrete, data.draw(create_discrete(False))))

        # self._validate_schema(SchemaNetworks().measurement_services_of(DiscreteValue, data.draw(create_discrete_value(False))))

    # ************ IEC61970 BASE SCADA ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_remote_control(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(RemoteControl, data.draw(create_remote_control(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_remote_source(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(RemoteSource, data.draw(create_remote_source(False))))

    # ************ IEC61970 BASE WIRES GENERATION PRODUCTION ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_battery_unit(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(BatteryUnit, data.draw(create_battery_unit(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_photovoltaic_unit(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(PhotoVoltaicUnit, data.draw(create_photovoltaic_unit(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_power_electronics_connection(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(PowerElectronicsConnection, data.draw(create_power_electronics_connection(False))))
        pass

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_power_electronics_connection_phase(self, caplog, data):
        self._validate_schema(
            SchemaNetworks().network_services_of(PowerElectronicsConnectionPhase, data.draw(create_power_electronics_connection_phase(False)))
        )

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_power_electronics_wind_unit(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(PowerElectronicsWindUnit, data.draw(create_power_electronics_wind_unit(False))))

    # ************ IEC61970 BASE WIRES ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_ac_line_segment(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(AcLineSegment, data.draw(create_ac_line_segment(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_breaker(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Breaker, data.draw(create_breaker(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_busbar_section(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(BusbarSection, data.draw(create_busbar_section(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_disconnector(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Disconnector, data.draw(create_disconnector(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_energy_consumer(self, caplog, data):
        consumer: EnergyConsumer = data.draw(create_energy_consumer(False))
        assume(len(Counter(map(lambda it: it.phase, consumer.phases))) == len(list(consumer.phases)))
        self._validate_schema(SchemaNetworks().network_services_of(EnergyConsumer, consumer))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_energy_consumer_phase(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(EnergyConsumerPhase, data.draw(create_energy_consumer_phase(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_energy_source(self, caplog, data):
        source: EnergySource = data.draw(create_energy_source(False))
        assume(len(Counter(map(lambda it: it.phase, source.phases))) == len(list(source.phases)))
        self._validate_schema(SchemaNetworks().network_services_of(EnergySource, source))
        pass

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_energy_source_phase(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(EnergySourcePhase, data.draw(create_energy_source_phase(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_fuse(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Fuse, data.draw(create_fuse(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_jumper(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Jumper, data.draw(create_jumper(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_junction(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Junction, data.draw(create_junction(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_linear_shunt_compensator(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(LinearShuntCompensator, data.draw(create_linear_shunt_compensator(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_load_break_switch(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(LoadBreakSwitch, data.draw(create_load_break_switch(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_per_length_sequence_impedance(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(PerLengthSequenceImpedance, data.draw(create_per_length_sequence_impedance(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_power_transformer(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(PowerTransformer, data.draw(create_power_transformer(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_power_transformer_end(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(PowerTransformerEnd, data.draw(create_power_transformer_end(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_ratio_tap_changer(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(RatioTapChanger, data.draw(create_ratio_tap_changer(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_recloser(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Recloser, data.draw(create_recloser(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_transformer_star_impedance(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(TransformerStarImpedance, data.draw(create_transformer_star_impedance(False))))

    # ************ IEC61970 InfIEC61970 ************

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_circuit(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Circuit, data.draw(create_circuit(False))))

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=1000)
    @given(data())
    def test_schema_loop(self, caplog, data):
        self._validate_schema(SchemaNetworks().network_services_of(Loop, data.draw(create_loop(False))))

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
