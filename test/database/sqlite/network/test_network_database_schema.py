#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import os
import sqlite3
import time
import unittest
from collections import Counter
from sqlite3 import Connection

import pytest
from hypothesis import given, settings, HealthCheck, assume
from zepben.evolve import IdentifiedObject, AcLineSegment, CableInfo, NoLoadTest, OpenCircuitTest, OverheadWireInfo, PowerTransformerInfo, \
    ShortCircuitTest, ShuntCompensatorInfo, TransformerEndInfo, TransformerTankInfo, AssetOwner, Pole, Streetlight, Meter, UsagePoint, Location, Organisation, \
    OperationalRestriction, FaultIndicator, BaseVoltage, ConnectivityNode, Feeder, GeographicalRegion, Site, SubGeographicalRegion, Substation, Terminal, \
    EquivalentBranch, Accumulator, Analog, Control, Discrete, RemoteControl, RemoteSource, BatteryUnit, PhotoVoltaicUnit, \
    PowerElectronicsConnection, PowerElectronicsConnectionPhase, PowerElectronicsWindUnit, Breaker, BusbarSection, Disconnector, EnergyConsumer, \
    EnergyConsumerPhase, EnergySource, EnergySourcePhase, Fuse, Jumper, Junction, LinearShuntCompensator, LoadBreakSwitch, PerLengthSequenceImpedance, \
    PowerTransformer, PowerTransformerEnd, RatioTapChanger, Recloser, TransformerStarImpedance, Circuit, Loop, NetworkDatabaseWriter, \
    NetworkDatabaseReader, NetworkServiceComparator, LvFeeder, CurrentTransformerInfo, PotentialTransformerInfo, CurrentTransformer, \
    PotentialTransformer, SwitchInfo, RelayInfo, CurrentRelay, EvChargingUnit, TapChangerControl, DistanceRelay, VoltageRelay, ProtectionRelayScheme, \
    ProtectionRelaySystem, Ground, GroundDisconnector, SeriesCompensator, NetworkService, StreetAddress, TownDetail, StreetDetail, GroundingImpedance, \
    PetersenCoil, ReactiveCapabilityCurve, SynchronousMachine, PanDemandResponseFunction, BatteryControl, StaticVarCompensator, Tracing, NetworkStateOperators, \
    NetworkTraceStep
from zepben.evolve.model.cim.iec61970.base.wires.clamp import Clamp
from zepben.evolve.model.cim.iec61970.base.wires.cut import Cut
from zepben.evolve.model.cim.iec61970.base.wires.per_length_phase_impedance import PerLengthPhaseImpedance
from zepben.evolve.services.common import resolver
from zepben.evolve.services.network.tracing.networktrace import tracing

from cim.cim_creators import create_cable_info, create_no_load_test, create_open_circuit_test, create_overhead_wire_info, create_power_transformer_info, \
    create_short_circuit_test, create_shunt_compensator_info, create_transformer_end_info, create_transformer_tank_info, create_asset_owner, create_pole, \
    create_streetlight, create_location, create_organisation, create_meter, create_usage_point, create_operational_restriction, create_fault_indicator, \
    create_base_voltage, create_connectivity_node, create_feeder, create_geographical_region, create_site, create_sub_geographical_region, create_substation, \
    create_terminal, create_equivalent_branch, create_accumulator, create_analog, create_control, create_discrete, create_remote_control, \
    create_remote_source, create_battery_unit, create_photo_voltaic_unit, create_power_electronics_wind_unit, create_ac_line_segment, create_breaker, \
    create_busbar_section, create_disconnector, create_energy_consumer, create_energy_consumer_phase, create_energy_source, create_energy_source_phase, \
    create_fuse, create_jumper, create_junction, create_linear_shunt_compensator, create_load_break_switch, create_per_length_sequence_impedance, \
    create_power_electronics_connection, create_power_electronics_connection_phase, create_power_transformer, create_power_transformer_end, \
    create_ratio_tap_changer, create_recloser, create_transformer_star_impedance, create_circuit, create_loop, create_lv_feeder, \
    create_current_transformer_info, create_current_transformer, create_potential_transformer, create_current_relay, create_relay_info, create_switch_info, \
    create_ev_charging_unit, create_tap_changer_control, create_distance_relay, create_voltage_relay, create_protection_relay_scheme, \
    create_protection_relay_system, create_ground, create_ground_disconnector, create_series_compensator, create_potential_transformer_info, \
    create_grounding_impedance, create_petersen_coil, create_reactive_capability_curve, create_synchronous_machine, create_per_length_phase_impedance, \
    create_pan_demand_response_function, create_battery_control, create_static_var_compensator, create_clamp, create_cut
from database.sqlite.common.cim_database_schema_common_tests import CimDatabaseSchemaCommonTests, TComparator, TService, TReader, TWriter
from database.sqlite.schema_utils import SchemaNetworks


# FIXME: see Line [305]

class PatchedNetworkTraceStepPath(NetworkTraceStep.Path):
    @property
    def from_equipment(self):
        try:
            return super().from_equipment
        except AttributeError:
            return

    @property
    def to_equipment(self):
        try:
            return super().to_equipment
        except AttributeError:
            return

NetworkTraceStep.Path = PatchedNetworkTraceStepPath

# pylint: disable=too-many-public-methods
class TestNetworkDatabaseSchema(CimDatabaseSchemaCommonTests[NetworkService, NetworkDatabaseWriter, NetworkDatabaseReader, NetworkServiceComparator]):

    def create_service(self) -> TService:
        return NetworkService()

    def create_writer(self, filename: str, service: TService) -> TWriter:
        return NetworkDatabaseWriter(filename, service)

    def create_reader(self, connection: Connection, service: TService, database_description: str) -> TReader:
        return NetworkDatabaseReader(connection, service, database_description)

    def create_comparator(self) -> TComparator:
        return NetworkServiceComparator()

    def create_identified_object(self) -> IdentifiedObject:
        return Junction()

    @unittest.skip("Only load real files on demand, not as part of the actual test suite")
    @pytest.mark.timeout(65536)
    async def test_load_real_file(self):
        #
        # NOTE: Comment out the @unittest.skip above to run this "test". Try not to commit the change as it will lock up all test runs.
        #
        #       Run the test with the `--log-cli-level=INFO` option to enable live logging.
        #

        # Put the name of the database you want to load in test/resources/test-network-database.txt
        with open(os.path.join("resources", "test-network-database.txt")) as file:
            database_file = file.read().strip().strip("\"")

        assert os.path.isfile(database_file), "database must exist"

        network_service = NetworkService()

        with contextlib.closing(sqlite3.connect(database_file)) as connection:
            assert await NetworkDatabaseReader(connection, network_service, database_file).load(), "Database should have loaded"

        print("Sleeping...")
        try:
            time.sleep(65536)
        except KeyboardInterrupt:
            pass

    #######################
    # EXTENSIONS IEC61968 METERING #
    #######################
    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(pan_demand_response_function=create_pan_demand_response_function(False))
    async def test_schema_pan_demand_response_function(self, pan_demand_response_function):
        await self._validate_schema(SchemaNetworks().network_services_of(PanDemandResponseFunction, pan_demand_response_function))

    #######################
    # EXTENSIONS IEC61968 METERING #
    #######################

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(battery_control=create_battery_control(False))
    async def test_schema_battery_control(self, battery_control):
        await self._validate_schema(SchemaNetworks().network_services_of(BatteryControl, battery_control))


    #######################
    # IEC61968 ASSET INFO #
    #######################

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(cable_info=create_cable_info(False))
    async def test_schema_cable_info(self, cable_info):
        await self._validate_schema(SchemaNetworks().network_services_of(CableInfo, cable_info))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(no_load_test=create_no_load_test(False))
    async def test_schema_no_load_test(self, no_load_test):
        await self._validate_schema(SchemaNetworks().network_services_of(NoLoadTest, no_load_test))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(open_circuit_test=create_open_circuit_test(False))
    async def test_schema_open_circuit_test(self, open_circuit_test):
        await self._validate_schema(SchemaNetworks().network_services_of(OpenCircuitTest, open_circuit_test))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(overhead_wire_info=create_overhead_wire_info(False))
    async def test_schema_overhead_wire_info(self, overhead_wire_info):
        await self._validate_schema(SchemaNetworks().network_services_of(OverheadWireInfo, overhead_wire_info))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(power_transformer_info=create_power_transformer_info(False))
    async def test_schema_power_transformer_info(self, power_transformer_info):
        await self._validate_schema(SchemaNetworks().network_services_of(PowerTransformerInfo, power_transformer_info))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(short_circuit_test=create_short_circuit_test(False))
    async def test_schema_short_circuit_test(self, short_circuit_test):
        await self._validate_schema(SchemaNetworks().network_services_of(ShortCircuitTest, short_circuit_test))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(shunt_compensator_info=create_shunt_compensator_info(False))
    async def test_schema_shunt_compensator_info(self, shunt_compensator_info):
        await self._validate_schema(SchemaNetworks().network_services_of(ShuntCompensatorInfo, shunt_compensator_info))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(switch_info=create_switch_info(False))
    async def test_schema_switch_info(self, switch_info):
        await self._validate_schema(SchemaNetworks().network_services_of(SwitchInfo, switch_info))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(transformer_end_info=create_transformer_end_info(False))
    async def test_schema_transformer_end_info(self, transformer_end_info):
        await self._validate_schema(SchemaNetworks().network_services_of(TransformerEndInfo, transformer_end_info))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(transformer_tank_info=create_transformer_tank_info(False))
    async def test_schema_transformer_tank_info(self, transformer_tank_info):
        await self._validate_schema(SchemaNetworks().network_services_of(TransformerTankInfo, transformer_tank_info))

    ###################
    # IEC61968 ASSETS #
    ###################

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(asset_owner=create_asset_owner(False))
    async def test_schema_asset_owner(self, asset_owner):
        await self._validate_schema(SchemaNetworks().network_services_of(AssetOwner, asset_owner))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(pole=create_pole(False))
    async def test_schema_pole(self, pole):
        await self._validate_schema(SchemaNetworks().network_services_of(Pole, pole))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(streetlight=create_streetlight(False))
    async def test_schema_streetlight(self, streetlight):
        await self._validate_schema(SchemaNetworks().network_services_of(Streetlight, streetlight))

    #####################################
    # IEC61968 infIEC61968 InfAssetInfo #
    #####################################

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(relay_info=create_relay_info(False))
    async def test_schema_relay_info(self, relay_info):
        await self._validate_schema(SchemaNetworks().network_services_of(RelayInfo, relay_info))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(current_transformer_info=create_current_transformer_info(False))
    async def test_schema_current_transformer_info(self, current_transformer_info):
        await self._validate_schema(SchemaNetworks().network_services_of(CurrentTransformerInfo, current_transformer_info))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(potential_transformer_info=create_potential_transformer_info(False))
    async def test_schema_potential_transformer_info(self, potential_transformer_info):
        await self._validate_schema(SchemaNetworks().network_services_of(PotentialTransformerInfo, potential_transformer_info))

    #####################
    # IEC61968 METERING #
    #####################

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(meter=create_meter(False))
    async def test_schema_meter(self, meter):
        await self._validate_schema(SchemaNetworks().network_services_of(Meter, meter))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(usage_point=create_usage_point(False))
    async def test_schema_usage_point(self, usage_point):
        await self._validate_schema(SchemaNetworks().network_services_of(UsagePoint, usage_point))

    ###################
    # IEC61968 COMMON #
    ###################

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(location=create_location(False))
    async def test_schema_location(self, location):
        await self._validate_schema(SchemaNetworks().network_services_of(Location, location))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(organisation=create_organisation(False))
    async def test_schema_organisation(self, organisation):
        await self._validate_schema(SchemaNetworks().network_services_of(Organisation, organisation))

    #######################
    # IEC61968 OPERATIONS #
    #######################

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(operational_restriction=create_operational_restriction(False))
    async def test_schema_operational_restriction(self, operational_restriction):
        await self._validate_schema(SchemaNetworks().network_services_of(OperationalRestriction, operational_restriction))

    #####################################
    # IEC61970 BASE AUXILIARY EQUIPMENT #
    #####################################

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(current_transformer=create_current_transformer(False))
    async def test_schema_current_transformer(self, current_transformer):
        await self._validate_schema(SchemaNetworks().network_services_of(CurrentTransformer, current_transformer))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(fault_indicator=create_fault_indicator(False))
    async def test_schema_fault_indicator(self, fault_indicator):
        await self._validate_schema(SchemaNetworks().network_services_of(FaultIndicator, fault_indicator))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(potential_transformer=create_potential_transformer(False))
    async def test_schema_potential_transformer(self, potential_transformer):
        await self._validate_schema(SchemaNetworks().network_services_of(PotentialTransformer, potential_transformer))

    ######################
    # IEC61970 BASE CORE #
    ######################

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(base_voltage=create_base_voltage(False))
    async def test_schema_base_voltage(self, base_voltage):
        await self._validate_schema(SchemaNetworks().network_services_of(BaseVoltage, base_voltage))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(connectivity_node=create_connectivity_node(False))
    async def test_schema_connectivity_node(self, connectivity_node):
        await self._validate_schema(SchemaNetworks().network_services_of(ConnectivityNode, connectivity_node))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(feeder=create_feeder(False))
    async def test_schema_feeder(self, feeder):
        # Need to set feeder directions to match database load.
        network_service = SchemaNetworks().network_services_of(Feeder, feeder)
        await Tracing().assign_equipment_to_feeders().run(network_service, network_state_operators=NetworkStateOperators.NORMAL)
        await Tracing().assign_equipment_to_feeders().run(network_service, network_state_operators=NetworkStateOperators.CURRENT)
        await Tracing().set_direction().run(network_service, network_state_operators=NetworkStateOperators.NORMAL)
        await Tracing().set_direction().run(network_service, network_state_operators=NetworkStateOperators.CURRENT)

        # TODO assign_to_feeders.py [62] line added to fix this, discuss
        """
        normal_head_terminal doesnt have conducting equipment?
        network has no feeder start points
        network has no connectivity nodes
        network has 2 feeders 1 terminal 1 substation 1 location 0 CN's
        1 feeder has no terminals (Feeder)
        other feeder (feeder) has a head terminal - the one with no conducting equipment... WT[actual]F?!
        """

        await self._validate_schema(network_service)

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(geographical_region=create_geographical_region(False))
    async def test_schema_geographical_region(self, geographical_region):
        await self._validate_schema(SchemaNetworks().network_services_of(GeographicalRegion, geographical_region))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(site=create_site(False))
    async def test_schema_site(self, site):
        await self._validate_schema(SchemaNetworks().network_services_of(Site, site))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(sub_geographical_region=create_sub_geographical_region(False))
    async def test_schema_sub_geographical_region(self, sub_geographical_region):
        await self._validate_schema(SchemaNetworks().network_services_of(SubGeographicalRegion, sub_geographical_region))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(substation=create_substation(False))
    async def test_schema_substation(self, substation):
        await self._validate_schema(SchemaNetworks().network_services_of(Substation, substation))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(terminal=create_terminal(False))
    async def test_schema_terminal(self, terminal):
        await self._validate_schema(SchemaNetworks().network_services_of(Terminal, terminal))

    #############################
    # IEC61970 BASE EQUIVALENTS #
    #############################

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(equivalent_branch=create_equivalent_branch(False))
    async def test_schema_equivalent_branch(self, equivalent_branch):
        await self._validate_schema(SchemaNetworks().network_services_of(EquivalentBranch, equivalent_branch))

    ######################
    # IEC61970 BASE MEAS #
    ######################

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(accumulator=create_accumulator(False))
    async def test_schema_accumulator(self, accumulator: Accumulator):
        await self._validate_schema(SchemaNetworks().network_services_of(Accumulator, accumulator))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(analog=create_analog(False))
    async def test_schema_analog(self, analog: Analog):
        await self._validate_schema(SchemaNetworks().network_services_of(Analog, analog))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(control=create_control(False))
    async def test_schema_control(self, control):
        await self._validate_schema(SchemaNetworks().network_services_of(Control, control))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(discrete=create_discrete(False))
    async def test_schema_discrete(self, discrete: Discrete):
        await self._validate_schema(SchemaNetworks().network_services_of(Discrete, discrete))

    ############################
    # IEC61970 Base Protection #
    ############################

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(current_relay=create_current_relay(False))
    async def test_schema_current_relay(self, current_relay):
        await self._validate_schema(SchemaNetworks().network_services_of(CurrentRelay, current_relay))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(distance_relay=create_distance_relay(False))
    async def test_schema_distance_relay(self, distance_relay):
        await self._validate_schema(SchemaNetworks().network_services_of(DistanceRelay, distance_relay))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(protection_relay_scheme=create_protection_relay_scheme(False))
    async def test_schema_protection_relay_scheme(self, protection_relay_scheme):
        await self._validate_schema(SchemaNetworks().network_services_of(ProtectionRelayScheme, protection_relay_scheme))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(protection_relay_system=create_protection_relay_system(False))
    async def test_schema_protection_relay_system(self, protection_relay_system):
        await self._validate_schema(SchemaNetworks().network_services_of(ProtectionRelaySystem, protection_relay_system))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(voltage_relay=create_voltage_relay(False))
    async def test_schema_voltage_relay(self, voltage_relay):
        await self._validate_schema(SchemaNetworks().network_services_of(VoltageRelay, voltage_relay))

    #######################
    # IEC61970 BASE SCADA #
    #######################

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(remote_control=create_remote_control(False))
    async def test_schema_remote_control(self, remote_control):
        await self._validate_schema(SchemaNetworks().network_services_of(RemoteControl, remote_control))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(remote_source=create_remote_source(False))
    async def test_schema_remote_source(self, remote_source: RemoteSource):
        await self._validate_schema(SchemaNetworks().network_services_of(RemoteSource, remote_source))

    #############################################
    # IEC61970 BASE WIRES GENERATION PRODUCTION #
    #############################################

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(battery_unit=create_battery_unit(False))
    async def test_schema_battery_unit(self, battery_unit):
        await self._validate_schema(SchemaNetworks().network_services_of(BatteryUnit, battery_unit))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(photo_voltaic_unit=create_photo_voltaic_unit(False))
    async def test_schema_photo_voltaic_unit(self, photo_voltaic_unit):
        await self._validate_schema(SchemaNetworks().network_services_of(PhotoVoltaicUnit, photo_voltaic_unit))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(power_electronics_connection=create_power_electronics_connection(False))
    async def test_schema_power_electronics_connection(self, power_electronics_connection):
        await self._validate_schema(SchemaNetworks().network_services_of(PowerElectronicsConnection, power_electronics_connection))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(power_electronics_connection_phase=create_power_electronics_connection_phase(False))
    async def test_schema_power_electronics_connection_phase(self, power_electronics_connection_phase):
        await self._validate_schema(SchemaNetworks().network_services_of(PowerElectronicsConnectionPhase, power_electronics_connection_phase))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(power_electronics_wind_unit=create_power_electronics_wind_unit(False))
    async def test_schema_power_electronics_wind_unit(self, power_electronics_wind_unit):
        await self._validate_schema(SchemaNetworks().network_services_of(PowerElectronicsWindUnit, power_electronics_wind_unit))

    #######################
    # IEC61970 BASE WIRES #
    #######################

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(ac_line_segment=create_ac_line_segment(False))
    async def test_schema_ac_line_segment(self, ac_line_segment):
        await self._validate_schema(SchemaNetworks().network_services_of(AcLineSegment, ac_line_segment))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(breaker=create_breaker(False))
    async def test_schema_breaker(self, breaker):
        await self._validate_schema(SchemaNetworks().network_services_of(Breaker, breaker))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(busbar_section=create_busbar_section(False))
    async def test_schema_busbar_section(self, busbar_section):
        await self._validate_schema(SchemaNetworks().network_services_of(BusbarSection, busbar_section))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(clamp=create_clamp(False))
    async def test_schema_clamp(self, clamp):
        await self._validate_schema(SchemaNetworks().network_services_of(Clamp, clamp))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(cut=create_cut(False))
    async def test_schema_cut(self, cut):
        await self._validate_schema(SchemaNetworks().network_services_of(Cut, cut))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(disconnector=create_disconnector(False))
    async def test_schema_disconnector(self, disconnector):
        await self._validate_schema(SchemaNetworks().network_services_of(Disconnector, disconnector))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(energy_consumer=create_energy_consumer(False))
    async def test_schema_energy_consumer(self, energy_consumer):
        # Need to assure the correct number of phases to prevent errors.
        assume(len(Counter(map(lambda it: it.phase, energy_consumer.phases))) == len(list(energy_consumer.phases)))
        await self._validate_schema(SchemaNetworks().network_services_of(EnergyConsumer, energy_consumer))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(energy_consumer_phase=create_energy_consumer_phase(False))
    async def test_schema_energy_consumer_phase(self, energy_consumer_phase):
        await self._validate_schema(SchemaNetworks().network_services_of(EnergyConsumerPhase, energy_consumer_phase))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(energy_source=create_energy_source(False))
    async def test_schema_energy_source(self, energy_source):
        # Need to assure the correct number of phases to prevent errors.
        assume(len(Counter(map(lambda it: it.phase, energy_source.phases))) == len(list(energy_source.phases)))

        # Need to apply phases to match after the database load.
        network_service = SchemaNetworks().network_services_of(EnergySource, energy_source)
        await Tracing.set_phases().run(network_service, NetworkStateOperators)

        await self._validate_schema(network_service)

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(energy_source_phase=create_energy_source_phase(False))
    async def test_schema_energy_source_phase(self, energy_source_phase):
        await self._validate_schema(SchemaNetworks().network_services_of(EnergySourcePhase, energy_source_phase))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(fuse=create_fuse(False))
    async def test_schema_fuse(self, fuse):
        await self._validate_schema(SchemaNetworks().network_services_of(Fuse, fuse))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(ground=create_ground(False))
    async def test_schema_ground(self, ground):
        await self._validate_schema(SchemaNetworks().network_services_of(Ground, ground))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(ground_disconnector=create_ground_disconnector(False))
    async def test_schema_ground_disconnector(self, ground_disconnector):
        await self._validate_schema(SchemaNetworks().network_services_of(GroundDisconnector, ground_disconnector))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(grounding_impedance=create_grounding_impedance(False))
    async def test_schema_grounding_impedance(self, grounding_impedance):
        await self._validate_schema(SchemaNetworks().network_services_of(GroundingImpedance, grounding_impedance))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(jumper=create_jumper(False))
    async def test_schema_jumper(self, jumper):
        await self._validate_schema(SchemaNetworks().network_services_of(Jumper, jumper))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(junction=create_junction(False))
    async def test_schema_junction(self, junction):
        await self._validate_schema(SchemaNetworks().network_services_of(Junction, junction))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(linear_shunt_compensator=create_linear_shunt_compensator(False))
    async def test_schema_linear_shunt_compensator(self, linear_shunt_compensator):
        await self._validate_schema(SchemaNetworks().network_services_of(LinearShuntCompensator, linear_shunt_compensator))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(load_break_switch=create_load_break_switch(False))
    async def test_schema_load_break_switch(self, load_break_switch):
        await self._validate_schema(SchemaNetworks().network_services_of(LoadBreakSwitch, load_break_switch))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(per_length_phase_impedance=create_per_length_phase_impedance(False))
    async def test_schema_per_length_phase_impedance(self, per_length_phase_impedance):
        await self._validate_schema(SchemaNetworks().network_services_of(PerLengthPhaseImpedance, per_length_phase_impedance))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(per_length_sequence_impedance=create_per_length_sequence_impedance(False))
    async def test_schema_per_length_sequence_impedance(self, per_length_sequence_impedance):
        await self._validate_schema(SchemaNetworks().network_services_of(PerLengthSequenceImpedance, per_length_sequence_impedance))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(petersen_coil=create_petersen_coil(False))
    async def test_schema_petersen_coil(self, petersen_coil):
        await self._validate_schema(SchemaNetworks().network_services_of(PetersenCoil, petersen_coil))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(power_transformer=create_power_transformer(False))
    async def test_schema_power_transformer(self, power_transformer):
        await self._validate_schema(SchemaNetworks().network_services_of(PowerTransformer, power_transformer))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(power_transformer_end=create_power_transformer_end(False))
    async def test_schema_power_transformer_end(self, power_transformer_end):
        await self._validate_schema(SchemaNetworks().network_services_of(PowerTransformerEnd, power_transformer_end))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(ratio_tap_changer=create_ratio_tap_changer(False))
    async def test_schema_ratio_tap_changer(self, ratio_tap_changer):
        await self._validate_schema(SchemaNetworks().network_services_of(RatioTapChanger, ratio_tap_changer))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(reactive_capability_curve=create_reactive_capability_curve(False))
    async def test_schema_reactive_capability_curve(self, reactive_capability_curve):
        await self._validate_schema(SchemaNetworks().network_services_of(ReactiveCapabilityCurve, reactive_capability_curve))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(recloser=create_recloser(False))
    async def test_schema_recloser(self, recloser):
        await self._validate_schema(SchemaNetworks().network_services_of(Recloser, recloser))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(series_compensator=create_series_compensator(False))
    async def test_schema_series_compensator(self, series_compensator):
        await self._validate_schema(SchemaNetworks().network_services_of(SeriesCompensator, series_compensator))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(static_var_compensator=create_static_var_compensator(False))
    async def test_schema_static_var_compensator(self, static_var_compensator):
        await self._validate_schema(SchemaNetworks().network_services_of(StaticVarCompensator, static_var_compensator))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(synchronous_machine=create_synchronous_machine(False))
    async def test_schema_synchronous_machine(self, synchronous_machine):
        await self._validate_schema(SchemaNetworks().network_services_of(SynchronousMachine, synchronous_machine))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(tap_changer_control=create_tap_changer_control(False))
    async def test_schema_tap_changer_control(self, tap_changer_control):
        await self._validate_schema(SchemaNetworks().network_services_of(TapChangerControl, tap_changer_control))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(transformer_star_impedance=create_transformer_star_impedance(False))
    async def test_schema_transformer_star_impedance(self, transformer_star_impedance):
        await self._validate_schema(SchemaNetworks().network_services_of(TransformerStarImpedance, transformer_star_impedance))

    #########################################################
    # IEC61970 InfIEC61970 BASE WIRES GENERATION PRODUCTION #
    #########################################################

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(ev_charging_unit=create_ev_charging_unit(False))
    async def test_schema_ev_charging_unit(self, ev_charging_unit):
        await self._validate_schema(SchemaNetworks().network_services_of(EvChargingUnit, ev_charging_unit))

    ###############################
    # IEC61970 InfIEC61970 Feeder #
    ###############################

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(circuit=create_circuit(False))
    async def test_schema_circuit(self, circuit):
        await self._validate_schema(SchemaNetworks().network_services_of(Circuit, circuit))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(loop=create_loop(False))
    async def test_schema_loop(self, loop):
        await self._validate_schema(SchemaNetworks().network_services_of(Loop, loop))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(lv_feeder=create_lv_feeder(False))
    async def test_schema_lv_feeder(self, lv_feeder):
        network = SchemaNetworks().network_services_of(LvFeeder, lv_feeder)
        await Tracing().assign_equipment_to_lv_feeders().run(network, network_state_operators=NetworkStateOperators.NORMAL)
        await Tracing().assign_equipment_to_lv_feeders().run(network, network_state_operators=NetworkStateOperators.CURRENT)
        await self._validate_schema(network)
        # TODO: NetworkDatabaseTestSchema 238

    # ************ Services ************

    async def test_name_and_name_type_schema(self):
        await self._validate_schema(SchemaNetworks().create_name_test_services(NetworkService, Junction))

    async def test_post_process_fails_with_unresolved_references(self):
        pec = PowerElectronicsConnection(mrid="pec1")

        def add_deferred_reference(service: NetworkService):
            service.resolve_or_defer_reference(resolver.rce_regulating_control(pec), "tcc")

        await self._validate_unresolved_failure(str(pec), "RegulatingControl tcc", add_deferred_reference)

    async def test_only_loads_street_address_fields_if_required(self):
        # This test is here to make sure the database reading correctly removes the parts of loaded street addresses that are not filled out.
        write_service = NetworkService()
        write_service.add(Location(mrid="loc1", main_address=StreetAddress(town_detail=TownDetail(), street_detail=StreetDetail())))

        def validate(service: NetworkService):
            assert service.get("loc1", Location).main_address == StreetAddress(), \
                "Expected a default street address as blank parts should have been removed during teh database read"

        await self._validate_write_read(write_service, validate_read=validate)
