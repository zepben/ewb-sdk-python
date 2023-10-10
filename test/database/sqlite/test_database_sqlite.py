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
from typing import TypeVar, Callable

import pytest
from _pytest.python_api import raises
from hypothesis import given, settings, assume, HealthCheck

from cim.cim_creators import create_cable_info, create_no_load_test, create_open_circuit_test, create_overhead_wire_info, create_power_transformer_info, \
    create_short_circuit_test, create_shunt_compensator_info, create_transformer_end_info, create_transformer_tank_info, create_asset_owner, create_pole, \
    create_streetlight, create_location, create_organisation, create_customer, create_customer_agreement, create_pricing_structure, create_tariffs, \
    create_meter, create_usage_point, create_operational_restriction, create_fault_indicator, create_base_voltage, create_connectivity_node, create_feeder, \
    create_geographical_region, create_site, create_sub_geographical_region, create_substation, create_terminal, create_equivalent_branch, create_diagram, \
    create_diagram_object, create_accumulator, create_analog, create_control, create_discrete, create_remote_control, create_remote_source, \
    create_battery_unit, create_photovoltaic_unit, create_power_electronics_wind_unit, create_ac_line_segment, create_breaker, create_busbar_section, \
    create_disconnector, create_energy_consumer, create_energy_consumer_phase, create_energy_source, create_energy_source_phase, create_fuse, create_jumper, \
    create_junction, create_linear_shunt_compensator, create_load_break_switch, create_per_length_sequence_impedance, create_power_electronics_connection, \
    create_power_electronics_connection_phase, create_power_transformer, create_power_transformer_end, create_ratio_tap_changer, create_recloser, \
    create_transformer_star_impedance, create_circuit, create_loop, create_lv_feeder, create_current_transformer_info, create_current_transformer, \
    create_potential_transformer, create_current_relay, create_current_relay_info, create_switch_info, create_ev_charging_unit, create_tap_changer_control
from database.sqlite.schema_utils import SchemaNetworks, Services, assume_non_blank_street_address_details
from zepben.evolve import MetadataCollection, IdentifiedObject, AcLineSegment, CableInfo, \
    NoLoadTest, OpenCircuitTest, OverheadWireInfo, PowerTransformerInfo, ShortCircuitTest, ShuntCompensatorInfo, TransformerEndInfo, TransformerTankInfo, \
    AssetOwner, Pole, Streetlight, Customer, CustomerAgreement, PricingStructure, Tariff, Meter, UsagePoint, Location, Organisation, OperationalRestriction, \
    FaultIndicator, BaseVoltage, ConnectivityNode, Feeder, GeographicalRegion, Site, SubGeographicalRegion, Substation, Terminal, Diagram, DiagramObject, \
    EquivalentBranch, Accumulator, Analog, Control, Discrete, RemoteControl, RemoteSource, BatteryUnit, \
    PhotoVoltaicUnit, PowerElectronicsConnection, PowerElectronicsConnectionPhase, PowerElectronicsWindUnit, Breaker, BusbarSection, Disconnector, \
    EnergyConsumer, EnergyConsumerPhase, EnergySource, EnergySourcePhase, Fuse, Jumper, Junction, LinearShuntCompensator, LoadBreakSwitch, \
    PerLengthSequenceImpedance, PowerTransformer, PowerTransformerEnd, RatioTapChanger, Recloser, TransformerStarImpedance, Circuit, Loop, BaseService, \
    DatabaseWriter, TableVersion, DatabaseReader, NetworkServiceComparator, BaseServiceComparator, StreetAddress, TownDetail, StreetDetail, LvFeeder, \
    CurrentTransformerInfo, PotentialTransformerInfo, CurrentTransformer, PotentialTransformer, SwitchInfo, CurrentRelayInfo, CurrentRelay, EvChargingUnit, \
    TapChangerControl, RegulatingControl
from zepben.evolve.services.customer.customer_service_comparator import CustomerServiceComparator
from zepben.evolve.services.diagram.diagram_service_comparator import DiagramServiceComparator
from zepben.evolve.services.network.tracing import tracing

T = TypeVar("T", bound=IdentifiedObject)


def log_on_failure_decorator(func):
    """
    A decorator that will print the captured log if an exception is thrown by the function. Should be used on test functions that use caplog.

    :param func: The test function to decorate
    :return: The decorated test function
    """

    @functools.wraps(func)
    def log_on_failure(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print_exc()
            print(kwargs["caplog"].text)
            raise e

    return log_on_failure


# pylint: disable=too-many-public-methods
class TestDatabaseSqlite:
    # ************ IEC61968 ASSET INFO ************

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(cable_info=create_cable_info(False))
    @pytest.mark.asyncio
    async def test_schema_cable_info(self, caplog, cable_info):
        await self._validate_schema(SchemaNetworks().network_services_of(CableInfo, cable_info), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(no_load_test=create_no_load_test(False))
    @pytest.mark.asyncio
    async def test_schema_no_load_test(self, caplog, no_load_test):
        await self._validate_schema(SchemaNetworks().network_services_of(NoLoadTest, no_load_test), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(open_circuit_test=create_open_circuit_test(False))
    @pytest.mark.asyncio
    async def test_schema_open_circuit_test(self, caplog, open_circuit_test):
        await self._validate_schema(SchemaNetworks().network_services_of(OpenCircuitTest, open_circuit_test), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(overhead_wire_info=create_overhead_wire_info(False))
    @pytest.mark.asyncio
    async def test_schema_overhead_wire_info(self, caplog, overhead_wire_info):
        await self._validate_schema(SchemaNetworks().network_services_of(OverheadWireInfo, overhead_wire_info), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(power_transformer_info=create_power_transformer_info(False))
    @pytest.mark.asyncio
    async def test_schema_power_transformer_info(self, caplog, power_transformer_info):
        await self._validate_schema(SchemaNetworks().network_services_of(PowerTransformerInfo, power_transformer_info), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(short_circuit_test=create_short_circuit_test(False))
    @pytest.mark.asyncio
    async def test_schema_short_circuit_test(self, caplog, short_circuit_test):
        await self._validate_schema(SchemaNetworks().network_services_of(ShortCircuitTest, short_circuit_test), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(shunt_compensator_info=create_shunt_compensator_info(False))
    @pytest.mark.asyncio
    async def test_schema_shunt_compensator_info(self, caplog, shunt_compensator_info):
        await self._validate_schema(SchemaNetworks().network_services_of(ShuntCompensatorInfo, shunt_compensator_info), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(switch_info=create_switch_info(False))
    async def test_schema_switch_info(self, caplog, switch_info):
        await self._validate_schema(SchemaNetworks().network_services_of(SwitchInfo, switch_info), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(transformer_end_info=create_transformer_end_info(False))
    @pytest.mark.asyncio
    async def test_schema_transformer_end_info(self, caplog, transformer_end_info):
        await self._validate_schema(SchemaNetworks().network_services_of(TransformerEndInfo, transformer_end_info), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(transformer_tank_info=create_transformer_tank_info(False))
    @pytest.mark.asyncio
    async def test_schema_transformer_tank_info(self, caplog, transformer_tank_info):
        await self._validate_schema(SchemaNetworks().network_services_of(TransformerTankInfo, transformer_tank_info), caplog)

    # ************ IEC61968 ASSETS ************

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(asset_owner=create_asset_owner(False))
    @pytest.mark.asyncio
    async def test_schema_asset_owner(self, caplog, asset_owner):
        await self._validate_schema(SchemaNetworks().network_services_of(AssetOwner, asset_owner), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(pole=create_pole(False))
    @pytest.mark.asyncio
    async def test_schema_pole(self, caplog, pole):
        await self._validate_schema(SchemaNetworks().network_services_of(Pole, pole), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(streetlight=create_streetlight(False))
    @pytest.mark.asyncio
    async def test_schema_streetlight(self, caplog, streetlight):
        await self._validate_schema(SchemaNetworks().network_services_of(Streetlight, streetlight), caplog)

    # ************ IEC61968 CUSTOMERS ************

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(customer=create_customer(False))
    @pytest.mark.asyncio
    async def test_schema_customer(self, caplog, customer):
        await self._validate_schema(SchemaNetworks().customer_services_of(Customer, customer), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(customer_agreement=create_customer_agreement(False))
    @pytest.mark.asyncio
    async def test_schema_customer_agreement(self, caplog, customer_agreement):
        await self._validate_schema(SchemaNetworks().customer_services_of(CustomerAgreement, customer_agreement), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(pricing_structure=create_pricing_structure(False))
    @pytest.mark.asyncio
    async def test_schema_pricing_structure(self, caplog, pricing_structure):
        await self._validate_schema(SchemaNetworks().customer_services_of(PricingStructure, pricing_structure), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(tariffs=create_tariffs(False))
    @pytest.mark.asyncio
    async def test_schema_tariffs(self, caplog, tariffs):
        await self._validate_schema(SchemaNetworks().customer_services_of(Tariff, tariffs), caplog)

    # ************ IEC61968 infIEC61968 InfAssetInfo ************

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(current_relay_info=create_current_relay_info(False))
    async def test_schema_current_relay_info(self, caplog, current_relay_info):
        await self._validate_schema(SchemaNetworks().network_services_of(CurrentRelayInfo, current_relay_info), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(current_transformer_info=create_current_transformer_info(False))
    @pytest.mark.asyncio
    async def test_schema_current_transformer_info(self, caplog, current_transformer_info):
        await self._validate_schema(SchemaNetworks().network_services_of(CurrentTransformerInfo, current_transformer_info), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(potential_transformer_info=create_current_transformer_info(False))
    @pytest.mark.asyncio
    async def test_schema_potential_transformer_info(self, caplog, potential_transformer_info):
        await self._validate_schema(SchemaNetworks().network_services_of(PotentialTransformerInfo, potential_transformer_info), caplog)

    # ************ IEC61968 METERING ************

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(meter=create_meter(False))
    @pytest.mark.asyncio
    async def test_schema_meter(self, caplog, meter):
        await self._validate_schema(SchemaNetworks().network_services_of(Meter, meter), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(usage_point=create_usage_point(False))
    @pytest.mark.asyncio
    async def test_schema_usage_point(self, caplog, usage_point):
        await self._validate_schema(SchemaNetworks().network_services_of(UsagePoint, usage_point), caplog)

    # ************ IEC61968 COMMON ************

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(location=create_location(False))
    @pytest.mark.asyncio
    async def test_schema_location(self, caplog, location):
        await self._validate_schema(SchemaNetworks().network_services_of(Location, location), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(organisation=create_organisation(False))
    @pytest.mark.asyncio
    async def test_schema_organisation(self, caplog, organisation):
        await self._validate_schema(SchemaNetworks().network_services_of(Organisation, organisation), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(organisation=create_organisation(False))
    @pytest.mark.asyncio
    async def test_schema_organisation_customer(self, caplog, organisation):
        await self._validate_schema(SchemaNetworks().customer_services_of(Organisation, organisation), caplog)

    # ************ IEC61968 OPERATIONS ************

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(operational_restriction=create_operational_restriction(False))
    @pytest.mark.asyncio
    async def test_schema_operational_restriction(self, caplog, operational_restriction):
        await self._validate_schema(SchemaNetworks().network_services_of(OperationalRestriction, operational_restriction), caplog)

    # ************ IEC61970 BASE AUXILIARY EQUIPMENT ************

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(current_transformer=create_current_transformer(False))
    @pytest.mark.asyncio
    async def test_schema_current_transformer(self, caplog, current_transformer):
        await self._validate_schema(SchemaNetworks().network_services_of(CurrentTransformer, current_transformer), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(fault_indicator=create_fault_indicator(False))
    @pytest.mark.asyncio
    async def test_schema_fault_indicator(self, caplog, fault_indicator):
        await self._validate_schema(SchemaNetworks().network_services_of(FaultIndicator, fault_indicator), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(potential_transformer=create_potential_transformer(False))
    @pytest.mark.asyncio
    async def test_schema_potential_transformer(self, caplog, potential_transformer):
        await self._validate_schema(SchemaNetworks().network_services_of(PotentialTransformer, potential_transformer), caplog)

    # ************ IEC61970 BASE CORE ************

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(base_voltage=create_base_voltage(False))
    @pytest.mark.asyncio
    async def test_schema_base_voltage(self, caplog, base_voltage):
        await self._validate_schema(SchemaNetworks().network_services_of(BaseVoltage, base_voltage), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(connectivity_node=create_connectivity_node(False))
    @pytest.mark.asyncio
    async def test_schema_connectivity_node(self, caplog, connectivity_node):
        await self._validate_schema(SchemaNetworks().network_services_of(ConnectivityNode, connectivity_node), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(feeder=create_feeder(False))
    @pytest.mark.asyncio
    async def test_schema_feeder(self, caplog, feeder):
        services = SchemaNetworks().network_services_of(Feeder, feeder)
        await tracing.set_direction().run(services.network_service)
        await self._validate_schema(services, caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(geographical_region=create_geographical_region(False))
    @pytest.mark.asyncio
    async def test_schema_geographical_region(self, caplog, geographical_region):
        await self._validate_schema(SchemaNetworks().network_services_of(GeographicalRegion, geographical_region), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(site=create_site(False))
    @pytest.mark.asyncio
    async def test_schema_site(self, caplog, site):
        await self._validate_schema(SchemaNetworks().network_services_of(Site, site), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(sub_geographical_region=create_sub_geographical_region(False))
    @pytest.mark.asyncio
    async def test_schema_sub_geographical_region(self, caplog, sub_geographical_region):
        await self._validate_schema(SchemaNetworks().network_services_of(SubGeographicalRegion, sub_geographical_region), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(substation=create_substation(False))
    @pytest.mark.asyncio
    async def test_schema_substation(self, caplog, substation):
        await self._validate_schema(SchemaNetworks().network_services_of(Substation, substation), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(terminal=create_terminal(False))
    @pytest.mark.asyncio
    async def test_schema_terminal(self, caplog, terminal):
        await self._validate_schema(SchemaNetworks().network_services_of(Terminal, terminal), caplog)

    # ************ IEC61970 BASE DIAGRAM LAYOUT ************

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(diagram=create_diagram(False))
    @pytest.mark.asyncio
    async def test_schema_diagram(self, caplog, diagram):
        await self._validate_schema(SchemaNetworks().diagram_services_of(Diagram, diagram), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(diagram_object=create_diagram_object(False))
    @pytest.mark.asyncio
    async def test_schema_diagram_object(self, caplog, diagram_object):
        await self._validate_schema(SchemaNetworks().diagram_services_of(DiagramObject, diagram_object), caplog)

    # ************ IEC61970 BASE EQUIVALENTS ************

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(equivalent_branch=create_equivalent_branch(False))
    @pytest.mark.asyncio
    async def test_schema_equivalent_branch(self, caplog, equivalent_branch):
        await self._validate_schema(SchemaNetworks().network_services_of(EquivalentBranch, equivalent_branch), caplog)

    # ************ IEC61970 BASE MEAS ************

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(accumulator=create_accumulator(False))
    @pytest.mark.asyncio
    async def test_schema_accumulator(self, caplog, accumulator):
        await self._validate_schema(SchemaNetworks().network_services_of(Accumulator, accumulator), caplog)

        # await self._validate_schema(SchemaNetworks().measurement_services_of(AccumulatorValue, data.draw(create_accumulator_value(False))), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(analog=create_analog(False))
    @pytest.mark.asyncio
    async def test_schema_analog(self, caplog, analog):
        await self._validate_schema(SchemaNetworks().network_services_of(Analog, analog), caplog)

        # await self._validate_schema(SchemaNetworks().measurement_services_of(AnalogValue, data.draw(create_analog_value(False))), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(control=create_control(False))
    @pytest.mark.asyncio
    async def test_schema_control(self, caplog, control):
        await self._validate_schema(SchemaNetworks().network_services_of(Control, control), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(discrete=create_discrete(False))
    @pytest.mark.asyncio
    async def test_schema_discrete(self, caplog, discrete):
        await self._validate_schema(SchemaNetworks().network_services_of(Discrete, discrete), caplog)

        # await self._validate_schema(SchemaNetworks().measurement_services_of(DiscreteValue, data.draw(create_discrete_value(False))), caplog)

    # ************ IEC61970 Base Protection ************

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(current_relay=create_current_relay(False))
    async def test_schema_current_relay(self, caplog, current_relay):
        await self._validate_schema(SchemaNetworks().network_services_of(CurrentRelay, current_relay), caplog)

    # ************ IEC61970 BASE SCADA ************

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(remote_control=create_remote_control(False))
    @pytest.mark.asyncio
    async def test_schema_remote_control(self, caplog, remote_control):
        await self._validate_schema(SchemaNetworks().network_services_of(RemoteControl, remote_control), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(remote_source=create_remote_source(False))
    @pytest.mark.asyncio
    async def test_schema_remote_source(self, caplog, remote_source):
        await self._validate_schema(SchemaNetworks().network_services_of(RemoteSource, remote_source), caplog)

    # ************ IEC61970 BASE WIRES GENERATION PRODUCTION ************

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(battery_unit=create_battery_unit(False))
    @pytest.mark.asyncio
    async def test_schema_battery_unit(self, caplog, battery_unit):
        await self._validate_schema(SchemaNetworks().network_services_of(BatteryUnit, battery_unit), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(photovoltaic_unit=create_photovoltaic_unit(False))
    @pytest.mark.asyncio
    async def test_schema_photovoltaic_unit(self, caplog, photovoltaic_unit):
        await self._validate_schema(SchemaNetworks().network_services_of(PhotoVoltaicUnit, photovoltaic_unit), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(power_electronics_connection=create_power_electronics_connection(False))
    @pytest.mark.asyncio
    async def test_schema_power_electronics_connection(self, caplog, power_electronics_connection):
        await self._validate_schema(SchemaNetworks().network_services_of(PowerElectronicsConnection, power_electronics_connection), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(pec_phase=create_power_electronics_connection_phase(False))
    @pytest.mark.asyncio
    async def test_schema_power_electronics_connection_phase(self, caplog, pec_phase):
        await self._validate_schema(SchemaNetworks().network_services_of(PowerElectronicsConnectionPhase, pec_phase), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(power_electronics_wind_unit=create_power_electronics_wind_unit(False))
    @pytest.mark.asyncio
    async def test_schema_power_electronics_wind_unit(self, caplog, power_electronics_wind_unit):
        await self._validate_schema(SchemaNetworks().network_services_of(PowerElectronicsWindUnit, power_electronics_wind_unit), caplog)

    # ************ IEC61970 BASE WIRES ************

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(ac_line_segment=create_ac_line_segment(False))
    @pytest.mark.asyncio
    async def test_schema_ac_line_segment(self, caplog, ac_line_segment):
        await self._validate_schema(SchemaNetworks().network_services_of(AcLineSegment, ac_line_segment), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(breaker=create_breaker(False))
    @pytest.mark.asyncio
    async def test_schema_breaker(self, caplog, breaker):
        await self._validate_schema(SchemaNetworks().network_services_of(Breaker, breaker), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(busbar_section=create_busbar_section(False))
    @pytest.mark.asyncio
    async def test_schema_busbar_section(self, caplog, busbar_section):
        await self._validate_schema(SchemaNetworks().network_services_of(BusbarSection, busbar_section), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(disconnector=create_disconnector(False))
    @pytest.mark.asyncio
    async def test_schema_disconnector(self, caplog, disconnector):
        await self._validate_schema(SchemaNetworks().network_services_of(Disconnector, disconnector), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(energy_consumer=create_energy_consumer(False))
    @pytest.mark.asyncio
    async def test_schema_energy_consumer(self, caplog, energy_consumer):
        assume(len(Counter(map(lambda it: it.phase, energy_consumer.phases))) == len(list(energy_consumer.phases)))
        await self._validate_schema(SchemaNetworks().network_services_of(EnergyConsumer, energy_consumer), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(energy_consumer_phase=create_energy_consumer_phase(False))
    @pytest.mark.asyncio
    async def test_schema_energy_consumer_phase(self, caplog, energy_consumer_phase):
        await self._validate_schema(SchemaNetworks().network_services_of(EnergyConsumerPhase, energy_consumer_phase), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(energy_source=create_energy_source(False))
    @pytest.mark.asyncio
    async def test_schema_energy_source(self, caplog, energy_source):
        assume(len(Counter(map(lambda it: it.phase, energy_source.phases))) == len(list(energy_source.phases)))
        services = SchemaNetworks().network_services_of(EnergySource, energy_source)
        await tracing.set_phases().run(services.network_service)
        await self._validate_schema(services, caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(energy_source_phase=create_energy_source_phase(False))
    @pytest.mark.asyncio
    async def test_schema_energy_source_phase(self, caplog, energy_source_phase):
        await self._validate_schema(SchemaNetworks().network_services_of(EnergySourcePhase, energy_source_phase), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(fuse=create_fuse(False))
    @pytest.mark.asyncio
    async def test_schema_fuse(self, caplog, fuse):
        await self._validate_schema(SchemaNetworks().network_services_of(Fuse, fuse), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(jumper=create_jumper(False))
    @pytest.mark.asyncio
    async def test_schema_jumper(self, caplog, jumper):
        await self._validate_schema(SchemaNetworks().network_services_of(Jumper, jumper), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(junction=create_junction(False))
    @pytest.mark.asyncio
    async def test_schema_junction(self, caplog, junction):
        await self._validate_schema(SchemaNetworks().network_services_of(Junction, junction), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(linear_shunt_compensator=create_linear_shunt_compensator(False))
    @pytest.mark.asyncio
    async def test_schema_linear_shunt_compensator(self, caplog, linear_shunt_compensator):
        await self._validate_schema(SchemaNetworks().network_services_of(LinearShuntCompensator, linear_shunt_compensator), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(load_break_switch=create_load_break_switch(False))
    @pytest.mark.asyncio
    async def test_schema_load_break_switch(self, caplog, load_break_switch):
        await self._validate_schema(SchemaNetworks().network_services_of(LoadBreakSwitch, load_break_switch), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(per_length_sequence_impedance=create_per_length_sequence_impedance(False))
    @pytest.mark.asyncio
    async def test_schema_per_length_sequence_impedance(self, caplog, per_length_sequence_impedance):
        await self._validate_schema(SchemaNetworks().network_services_of(PerLengthSequenceImpedance, per_length_sequence_impedance), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(power_transformer=create_power_transformer(False))
    @pytest.mark.asyncio
    async def test_schema_power_transformer(self, caplog, power_transformer):
        await self._validate_schema(SchemaNetworks().network_services_of(PowerTransformer, power_transformer), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(power_transformer_end=create_power_transformer_end(False))
    @pytest.mark.asyncio
    async def test_schema_power_transformer_end(self, caplog, power_transformer_end):
        await self._validate_schema(SchemaNetworks().network_services_of(PowerTransformerEnd, power_transformer_end), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(ratio_tap_changer=create_ratio_tap_changer(False))
    @pytest.mark.asyncio
    async def test_schema_ratio_tap_changer(self, caplog, ratio_tap_changer):
        await self._validate_schema(SchemaNetworks().network_services_of(RatioTapChanger, ratio_tap_changer), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(tap_changer_control=create_tap_changer_control(False))
    @pytest.mark.asyncio
    async def test_schema_tap_changer_control(self, caplog, tap_changer_control):
        await self._validate_schema(SchemaNetworks().network_services_of(TapChangerControl, tap_changer_control), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(recloser=create_recloser(False))
    @pytest.mark.asyncio
    async def test_schema_recloser(self, caplog, recloser):
        await self._validate_schema(SchemaNetworks().network_services_of(Recloser, recloser), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(transformer_star_impedance=create_transformer_star_impedance(False))
    @pytest.mark.asyncio
    async def test_schema_transformer_star_impedance(self, caplog, transformer_star_impedance):
        await self._validate_schema(SchemaNetworks().network_services_of(TransformerStarImpedance, transformer_star_impedance), caplog)

    # ************ IEC61970 InfIEC61970 ************

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(circuit=create_circuit(False))
    @pytest.mark.asyncio
    async def test_schema_circuit(self, caplog, circuit):
        await self._validate_schema(SchemaNetworks().network_services_of(Circuit, circuit), caplog)

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(loop=create_loop(False))
    @pytest.mark.asyncio
    async def test_schema_loop(self, caplog, loop):
        await self._validate_schema(SchemaNetworks().network_services_of(Loop, loop), caplog)

    # noinspection PyShadowingNames
    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(lv_feeder=create_lv_feeder(False))
    @pytest.mark.asyncio
    async def test_schema_lv_feeder(self, caplog, lv_feeder):
        await self._validate_schema(SchemaNetworks().network_services_of(LvFeeder, lv_feeder), caplog)

    # ************ IEC61970 InfIEC61970 WIRES GENERATION PRODUCTION ************

    @log_on_failure_decorator
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(ev_charging_unit=create_ev_charging_unit(False))
    @pytest.mark.asyncio
    async def test_schema_ev_charging_unit(self, caplog, ev_charging_unit):
        await self._validate_schema(SchemaNetworks().network_services_of(EvChargingUnit, ev_charging_unit), caplog)

    # ************ Services ************

    @log_on_failure_decorator
    async def test_metadata_data_source_schema(self, caplog):
        await self._validate_schema(SchemaNetworks().create_data_source_test_services(), caplog)

    @log_on_failure_decorator
    async def test_name_and_name_type_schema(self, caplog):
        await self._validate_schema(SchemaNetworks().create_name_test_services(), caplog)

    @log_on_failure_decorator
    async def test_post_process_fails_with_unresolved_regulating_control_references(self, caplog):
        write = Services()
        read = Services()
        pec = PowerElectronicsConnection()
        pec._regulating_control = RegulatingControl()
        write.network_service.add(pec)
        await self._test_unresolved_references_after_load(write,
                                                          read,
                                                          pec.mrid,
                                                          pec.regulating_control.__class__.__name__,
                                                          pec.regulating_control.mrid,
                                                          caplog)

    @staticmethod
    async def _test_unresolved_references_after_load(write: Services,
                                                     read: Services,
                                                     from_mrid: str,
                                                     to_clazz_name: str,
                                                     to_mrid,
                                                     caplog):
        expected_error = (f"Network still had unresolved references after load - this should not occur. Failing reference was from "
                          f"{from_mrid} resolving {to_clazz_name} {to_mrid}")
        caplog.clear()
        std_err = io.StringIO()
        with contextlib.redirect_stderr(std_err):
            with tempfile.NamedTemporaryFile() as schema_test_file_temp:
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

                assert f"Creating database schema v{TableVersion.SUPPORTED_VERSION}" in caplog.text
                assert os.path.isfile(schema_test_file)

                with raises(ValueError, match=expected_error):
                    await DatabaseReader(schema_test_file).load(
                        read.metadata_collection,
                        read.network_service,
                        read.diagram_service,
                        read.customer_service
                    )

    @log_on_failure_decorator
    @pytest.mark.asyncio
    async def test_error_on_duplicate_id_added_to_customer_service(self, caplog):
        write_services = Services()
        read_services = Services()

        customer = Customer(mrid="customer1")
        write_services.customer_service.add(customer)
        read_services.customer_service.add(customer)

        await self._test_duplicate_mrid_error(write_services, read_services, read_services.customer_service, customer, caplog)

    @log_on_failure_decorator
    @pytest.mark.asyncio
    async def test_error_on_duplicate_id_added_to_diagram_service(self, caplog):
        write_services = Services()
        read_services = Services()

        diagram = Diagram(mrid="diagram1")
        write_services.diagram_service.add(diagram)
        read_services.diagram_service.add(diagram)

        await self._test_duplicate_mrid_error(write_services, read_services, read_services.diagram_service, diagram, caplog)

    @log_on_failure_decorator
    @pytest.mark.asyncio
    async def test_error_on_duplicate_id_added_to_network_service(self, caplog):
        write_services = Services()
        read_services = Services()

        junction = Junction(mrid="junction1")
        write_services.network_service.add(junction)
        read_services.network_service.add(junction)

        await self._test_duplicate_mrid_error(write_services, read_services, read_services.network_service, junction, caplog)

    @log_on_failure_decorator
    @pytest.mark.asyncio
    async def test_only_loads_street_address_fields_if_required(self, caplog):
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

        await self._test_write_read(
            write_services,
            read_services,
            validate_read,
            caplog
        )

    async def _test_duplicate_mrid_error(
        self,
        write_services: Services,
        read_services: Services,
        service_with_duplicate: BaseService,
        duplicate: IdentifiedObject,
        caplog
    ):
        expected_error = f"Failed to load {duplicate}. Unable to add to service '{service_with_duplicate.name}': duplicate MRID"

        def validate_read(success):
            assert not success
            assert expected_error in caplog.text

        await self._test_write_read(
            write_services,
            read_services,
            validate_read,
            caplog
        )

    async def _validate_schema(self, expected: Services, caplog):
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

        await self._test_write_read(
            expected,
            read_services,
            validate_read,
            caplog
        )

    @staticmethod
    async def _test_write_read(
        write: Services,
        read: Services,
        validate_read: Callable[[bool], None],
        caplog
    ):
        caplog.clear()
        std_err = io.StringIO()
        with contextlib.redirect_stderr(std_err):
            with tempfile.NamedTemporaryFile() as schema_test_file_temp:
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

                assert f"Creating database schema v{TableVersion.SUPPORTED_VERSION}" in caplog.text
                assert os.path.isfile(schema_test_file)

                validate_read(
                    await DatabaseReader(schema_test_file).load(
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
