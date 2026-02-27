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
    create_pan_demand_response_function, create_battery_control, create_static_var_compensator, create_clamp, create_cut, create_directional_current_relay
from database.sqlite.common.cim_database_schema_common_tests import CimDatabaseSchemaCommonTests, TComparator, TService, TReader, TWriter
from database.sqlite.schema_utils import SchemaNetworks
from zepben.ewb import IdentifiedObject, AcLineSegment, NoLoadTest, OpenCircuitTest, PowerTransformerInfo, \
    ShortCircuitTest, ShuntCompensatorInfo, TransformerEndInfo, TransformerTankInfo, Pole, Streetlight, Location, Organisation, \
    OperationalRestriction, BaseVoltage, ConnectivityNode, Feeder, Site, Substation, Terminal, \
    EquivalentBranch, Control, RemoteControl, RemoteSource, BatteryUnit, PhotoVoltaicUnit, \
    PowerElectronicsConnection, PowerElectronicsWindUnit, Breaker, BusbarSection, Disconnector, EnergyConsumer, \
    EnergySource, EnergySourcePhase, Fuse, Jumper, Junction, LoadBreakSwitch, PowerTransformer, PowerTransformerEnd, Recloser, TransformerStarImpedance, \
    Circuit, Loop, NetworkDatabaseWriter, \
    NetworkDatabaseReader, NetworkServiceComparator, LvFeeder, CurrentTransformerInfo, PotentialTransformerInfo, CurrentTransformer, \
    PotentialTransformer, SwitchInfo, RelayInfo, CurrentRelay, EvChargingUnit, TapChangerControl, DistanceRelay, VoltageRelay, ProtectionRelayScheme, \
    ProtectionRelaySystem, Ground, GroundDisconnector, SeriesCompensator, NetworkService, GroundingImpedance, \
    PetersenCoil, ReactiveCapabilityCurve, SynchronousMachine, PanDemandResponseFunction, BatteryControl, StaticVarCompensator, Tracing, NetworkStateOperators, \
    NetworkTraceStep, DirectionalCurrentRelay, TestNetworkBuilder
from zepben.ewb.model.cim.iec61968.assetinfo.cable_info import CableInfo
from zepben.ewb.model.cim.iec61968.assetinfo.overhead_wire_info import OverheadWireInfo
from zepben.ewb.model.cim.iec61968.assets.asset_owner import AssetOwner
from zepben.ewb.model.cim.iec61968.common.street_address import StreetAddress
from zepben.ewb.model.cim.iec61968.common.street_detail import StreetDetail
from zepben.ewb.model.cim.iec61968.common.town_detail import TownDetail
from zepben.ewb.model.cim.iec61968.metering.meter import Meter
from zepben.ewb.model.cim.iec61968.metering.usage_point import UsagePoint
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.fault_indicator import FaultIndicator
from zepben.ewb.model.cim.iec61970.base.core.geographical_region import GeographicalRegion
from zepben.ewb.model.cim.iec61970.base.core.sub_geographical_region import SubGeographicalRegion
from zepben.ewb.model.cim.iec61970.base.meas.accumulator import Accumulator
from zepben.ewb.model.cim.iec61970.base.meas.analog import Analog
from zepben.ewb.model.cim.iec61970.base.meas.discrete import Discrete
from zepben.ewb.model.cim.iec61970.base.wires.clamp import Clamp
from zepben.ewb.model.cim.iec61970.base.wires.cut import Cut
from zepben.ewb.model.cim.iec61970.base.wires.energy_consumer_phase import EnergyConsumerPhase
from zepben.ewb.model.cim.iec61970.base.wires.linear_shunt_compensator import LinearShuntCompensator
from zepben.ewb.model.cim.iec61970.base.wires.per_length_phase_impedance import PerLengthPhaseImpedance
from zepben.ewb.model.cim.iec61970.base.wires.per_length_sequence_impedance import PerLengthSequenceImpedance
from zepben.ewb.model.cim.iec61970.base.wires.power_electronics_connection_phase import PowerElectronicsConnectionPhase
from zepben.ewb.model.cim.iec61970.base.wires.ratio_tap_changer import RatioTapChanger
from zepben.ewb.services.common import resolver

PYTEST_TIMEOUT_SEC = 1

hypothesis_settings = dict(
    deadline=2000,
    suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow],
    max_examples=4
)


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
        return Junction(mrid="test")

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

    ##################################
    # Extensions IEC61968 Asset Info #
    ##################################

    @settings(**hypothesis_settings)
    @given(relay_info=create_relay_info(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_relay_info(self, relay_info: RelayInfo):
        await self._validate_schema(SchemaNetworks().network_services_of(RelayInfo, relay_info))

    ################################
    # Extensions IEC61968 Metering #
    ################################

    @settings(**hypothesis_settings)
    @given(pan_demand_response_function=create_pan_demand_response_function(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_pan_demand_response_function(self, pan_demand_response_function: PanDemandResponseFunction):
        await self._validate_schema(SchemaNetworks().network_services_of(PanDemandResponseFunction, pan_demand_response_function))

    #################################
    # Extensions IEC61970 Base Core #
    #################################

    @settings(**hypothesis_settings)
    @given(site=create_site(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_site(self, site: Site):
        await self._validate_schema(SchemaNetworks().network_services_of(Site, site))

    ###################################
    # Extensions IEC61970 Base Feeder #
    ###################################

    @settings(**hypothesis_settings)
    @given(loop=create_loop(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_loop(self, loop: Loop):
        await self._validate_schema(SchemaNetworks().network_services_of(Loop, loop))

    @settings(**hypothesis_settings)
    @given(lv_feeder=create_lv_feeder(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_lv_feeder(self, lv_feeder: LvFeeder):
        network = SchemaNetworks().network_services_of(LvFeeder, lv_feeder)
        await Tracing().assign_equipment_to_lv_feeders().run(network, network_state_operators=NetworkStateOperators.NORMAL)
        await Tracing().assign_equipment_to_lv_feeders().run(network, network_state_operators=NetworkStateOperators.CURRENT)
        await self._validate_schema(network)

    ##################################################
    # Extensions IEC61970 Base Generation Production #
    ##################################################

    @settings(**hypothesis_settings)
    @given(ev_charging_unit=create_ev_charging_unit(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_ev_charging_unit(self, ev_charging_unit: EvChargingUnit):
        await self._validate_schema(SchemaNetworks().network_services_of(EvChargingUnit, ev_charging_unit))

    #######################################
    # Extensions IEC61970 Base Protection #
    #######################################

    @settings(**hypothesis_settings)
    @given(directional_current_relay=create_directional_current_relay(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_directional_current_relay(self, directional_current_relay: DirectionalCurrentRelay):
        await self._validate_schema(SchemaNetworks().network_services_of(DirectionalCurrentRelay, directional_current_relay))

    @settings(**hypothesis_settings)
    @given(distance_relay=create_distance_relay(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_distance_relay(self, distance_relay: DistanceRelay):
        await self._validate_schema(SchemaNetworks().network_services_of(DistanceRelay, distance_relay))

    @settings(**hypothesis_settings)
    @given(protection_relay_scheme=create_protection_relay_scheme(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_protection_relay_scheme(self, protection_relay_scheme: ProtectionRelayScheme):
        await self._validate_schema(SchemaNetworks().network_services_of(ProtectionRelayScheme, protection_relay_scheme))

    @settings(**hypothesis_settings)
    @given(protection_relay_system=create_protection_relay_system(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_protection_relay_system(self, protection_relay_system: ProtectionRelaySystem):
        await self._validate_schema(SchemaNetworks().network_services_of(ProtectionRelaySystem, protection_relay_system))

    @settings(**hypothesis_settings)
    @given(voltage_relay=create_voltage_relay(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_voltage_relay(self, voltage_relay: VoltageRelay):
        await self._validate_schema(SchemaNetworks().network_services_of(VoltageRelay, voltage_relay))

    ##################################
    # Extensions IEC61970 Base Wires #
    ##################################

    @settings(**hypothesis_settings)
    @given(battery_control=create_battery_control(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_battery_control(self, battery_control: BatteryControl):
        await self._validate_schema(SchemaNetworks().network_services_of(BatteryControl, battery_control))

    #######################
    # IEC61968 Asset Info #
    #######################

    @settings(**hypothesis_settings)
    @given(cable_info=create_cable_info(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_cable_info(self, cable_info: CableInfo):
        await self._validate_schema(SchemaNetworks().network_services_of(CableInfo, cable_info))

    @settings(**hypothesis_settings)
    @given(no_load_test=create_no_load_test(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_no_load_test(self, no_load_test: NoLoadTest):
        await self._validate_schema(SchemaNetworks().network_services_of(NoLoadTest, no_load_test))

    @settings(**hypothesis_settings)
    @given(open_circuit_test=create_open_circuit_test(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_open_circuit_test(self, open_circuit_test: OpenCircuitTest):
        await self._validate_schema(SchemaNetworks().network_services_of(OpenCircuitTest, open_circuit_test))

    @settings(**hypothesis_settings)
    @given(overhead_wire_info=create_overhead_wire_info(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_overhead_wire_info(self, overhead_wire_info: OverheadWireInfo):
        await self._validate_schema(SchemaNetworks().network_services_of(OverheadWireInfo, overhead_wire_info))

    @settings(**hypothesis_settings)
    @given(power_transformer_info=create_power_transformer_info(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_power_transformer_info(self, power_transformer_info: PowerTransformerInfo):
        await self._validate_schema(SchemaNetworks().network_services_of(PowerTransformerInfo, power_transformer_info))

    @settings(**hypothesis_settings)
    @given(short_circuit_test=create_short_circuit_test(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_short_circuit_test(self, short_circuit_test: ShortCircuitTest):
        await self._validate_schema(SchemaNetworks().network_services_of(ShortCircuitTest, short_circuit_test))

    @settings(**hypothesis_settings)
    @given(shunt_compensator_info=create_shunt_compensator_info(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_shunt_compensator_info(self, shunt_compensator_info: ShuntCompensatorInfo):
        await self._validate_schema(SchemaNetworks().network_services_of(ShuntCompensatorInfo, shunt_compensator_info))

    @settings(**hypothesis_settings)
    @given(switch_info=create_switch_info(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_switch_info(self, switch_info: SwitchInfo):
        await self._validate_schema(SchemaNetworks().network_services_of(SwitchInfo, switch_info))

    @settings(**hypothesis_settings)
    @given(transformer_end_info=create_transformer_end_info(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_transformer_end_info(self, transformer_end_info: TransformerEndInfo):
        await self._validate_schema(SchemaNetworks().network_services_of(TransformerEndInfo, transformer_end_info))

    @settings(**hypothesis_settings)
    @given(transformer_tank_info=create_transformer_tank_info(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_transformer_tank_info(self, transformer_tank_info: TransformerTankInfo):
        await self._validate_schema(SchemaNetworks().network_services_of(TransformerTankInfo, transformer_tank_info))

    ###################
    # IEC61968 Assets #
    ###################

    @settings(**hypothesis_settings)
    @given(asset_owner=create_asset_owner(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_asset_owner(self, asset_owner: AssetOwner):
        await self._validate_schema(SchemaNetworks().network_services_of(AssetOwner, asset_owner))

    @settings(**hypothesis_settings)
    @given(streetlight=create_streetlight(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_streetlight(self, streetlight: Streetlight):
        await self._validate_schema(SchemaNetworks().network_services_of(Streetlight, streetlight))

    ###################
    # IEC61968 Common #
    ###################

    @settings(**hypothesis_settings)
    @given(location=create_location(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_location(self, location: Location):
        await self._validate_schema(SchemaNetworks().network_services_of(Location, location))

    @settings(**hypothesis_settings)
    @given(organisation=create_organisation(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_organisation(self, organisation: Organisation):
        await self._validate_schema(SchemaNetworks().network_services_of(Organisation, organisation))

    #####################################
    # IEC61968 InfIEC61968 InfAssetInfo #
    #####################################

    @settings(**hypothesis_settings)
    @given(current_transformer_info=create_current_transformer_info(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_current_transformer_info(self, current_transformer_info: CurrentTransformerInfo):
        await self._validate_schema(SchemaNetworks().network_services_of(CurrentTransformerInfo, current_transformer_info))

    @settings(**hypothesis_settings)
    @given(potential_transformer_info=create_potential_transformer_info(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_potential_transformer_info(self, potential_transformer_info: PotentialTransformerInfo):
        await self._validate_schema(SchemaNetworks().network_services_of(PotentialTransformerInfo, potential_transformer_info))

    ##################################
    # IEC61968 InfIEC61968 InfAssets #
    ##################################

    @settings(**hypothesis_settings)
    @given(pole=create_pole(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_pole(self, pole: Pole):
        await self._validate_schema(SchemaNetworks().network_services_of(Pole, pole))

    #####################
    # IEC61968 Metering #
    #####################

    @settings(**hypothesis_settings)
    @given(meter=create_meter(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_meter(self, meter: Meter):
        await self._validate_schema(SchemaNetworks().network_services_of(Meter, meter))

    @settings(**hypothesis_settings)
    @given(usage_point=create_usage_point(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_usage_point(self, usage_point: UsagePoint):
        await self._validate_schema(SchemaNetworks().network_services_of(UsagePoint, usage_point))

    #######################
    # IEC61968 Operations #
    #######################

    @settings(**hypothesis_settings)
    @given(operational_restriction=create_operational_restriction(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_operational_restriction(self, operational_restriction: OperationalRestriction):
        await self._validate_schema(SchemaNetworks().network_services_of(OperationalRestriction, operational_restriction))

    #####################################
    # IEC61970 Base Auxiliary Equipment #
    #####################################

    @settings(**hypothesis_settings)
    @given(current_transformer=create_current_transformer(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_current_transformer(self, current_transformer: CurrentTransformer):
        await self._validate_schema(SchemaNetworks().network_services_of(CurrentTransformer, current_transformer))

    @settings(**hypothesis_settings)
    @given(fault_indicator=create_fault_indicator(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_fault_indicator(self, fault_indicator: FaultIndicator):
        await self._validate_schema(SchemaNetworks().network_services_of(FaultIndicator, fault_indicator))

    @settings(**hypothesis_settings)
    @given(potential_transformer=create_potential_transformer(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_potential_transformer(self, potential_transformer: PotentialTransformer):
        await self._validate_schema(SchemaNetworks().network_services_of(PotentialTransformer, potential_transformer))

    ######################
    # IEC61970 Base Core #
    ######################

    @settings(**hypothesis_settings)
    @given(base_voltage=create_base_voltage(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_base_voltage(self, base_voltage: BaseVoltage):
        await self._validate_schema(SchemaNetworks().network_services_of(BaseVoltage, base_voltage))

    @settings(**hypothesis_settings)
    @given(connectivity_node=create_connectivity_node(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_connectivity_node(self, connectivity_node: ConnectivityNode):
        await self._validate_schema(SchemaNetworks().network_services_of(ConnectivityNode, connectivity_node))

    @settings(**hypothesis_settings)
    @given(feeder=create_feeder(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_feeder(self, feeder: Feeder):
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

    @settings(**hypothesis_settings)
    @given(geographical_region=create_geographical_region(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_geographical_region(self, geographical_region: GeographicalRegion):
        await self._validate_schema(SchemaNetworks().network_services_of(GeographicalRegion, geographical_region))

    @settings(**hypothesis_settings)
    @given(sub_geographical_region=create_sub_geographical_region(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_sub_geographical_region(self, sub_geographical_region: SubGeographicalRegion):
        await self._validate_schema(SchemaNetworks().network_services_of(SubGeographicalRegion, sub_geographical_region))

    @settings(**hypothesis_settings)
    @given(substation=create_substation(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_substation(self, substation: Substation):
        await self._validate_schema(SchemaNetworks().network_services_of(Substation, substation))

    @settings(**hypothesis_settings)
    @given(terminal=create_terminal(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_terminal(self, terminal: Terminal):
        await self._validate_schema(SchemaNetworks().network_services_of(Terminal, terminal))

    #############################
    # IEC61970 Base Equivalents #
    #############################

    @settings(**hypothesis_settings)
    @given(equivalent_branch=create_equivalent_branch(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_equivalent_branch(self, equivalent_branch: EquivalentBranch):
        await self._validate_schema(SchemaNetworks().network_services_of(EquivalentBranch, equivalent_branch))

    #######################################
    # IEC61970 Base Generation Production #
    #######################################

    @settings(**hypothesis_settings)
    @given(battery_unit=create_battery_unit(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_battery_unit(self, battery_unit: BatteryUnit):
        await self._validate_schema(SchemaNetworks().network_services_of(BatteryUnit, battery_unit))

    @settings(**hypothesis_settings)
    @given(photo_voltaic_unit=create_photo_voltaic_unit(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_photo_voltaic_unit(self, photo_voltaic_unit: PhotoVoltaicUnit):
        await self._validate_schema(SchemaNetworks().network_services_of(PhotoVoltaicUnit, photo_voltaic_unit))

    @settings(**hypothesis_settings)
    @given(power_electronics_wind_unit=create_power_electronics_wind_unit(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_power_electronics_wind_unit(self, power_electronics_wind_unit: PowerElectronicsWindUnit):
        await self._validate_schema(SchemaNetworks().network_services_of(PowerElectronicsWindUnit, power_electronics_wind_unit))

    ######################
    # IEC61970 Base Meas #
    ######################

    @settings(**hypothesis_settings)
    @given(accumulator=create_accumulator(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_accumulator(self, accumulator: Accumulator):
        await self._validate_schema(SchemaNetworks().network_services_of(Accumulator, accumulator))

    @settings(**hypothesis_settings)
    @given(analog=create_analog(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_analog(self, analog: Analog):
        await self._validate_schema(SchemaNetworks().network_services_of(Analog, analog))

    @settings(**hypothesis_settings)
    @given(control=create_control(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_control(self, control: Control):
        await self._validate_schema(SchemaNetworks().network_services_of(Control, control))

    @settings(**hypothesis_settings)
    @given(discrete=create_discrete(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_discrete(self, discrete: Discrete):
        await self._validate_schema(SchemaNetworks().network_services_of(Discrete, discrete))

    ############################
    # IEC61970 Base Protection #
    ############################

    @settings(**hypothesis_settings)
    @given(current_relay=create_current_relay(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_current_relay(self, current_relay: CurrentRelay):
        await self._validate_schema(SchemaNetworks().network_services_of(CurrentRelay, current_relay))

    #######################
    # IEC61970 Base Scada #
    #######################

    @settings(**hypothesis_settings)
    @given(remote_control=create_remote_control(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_remote_control(self, remote_control: RemoteControl):
        await self._validate_schema(SchemaNetworks().network_services_of(RemoteControl, remote_control))

    @settings(**hypothesis_settings)
    @given(remote_source=create_remote_source(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_remote_source(self, remote_source: RemoteSource):
        await self._validate_schema(SchemaNetworks().network_services_of(RemoteSource, remote_source))

    #######################
    # IEC61970 Base Wires #
    #######################

    @settings(**hypothesis_settings)
    @given(ac_line_segment=create_ac_line_segment(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_ac_line_segment(self, ac_line_segment: AcLineSegment):
        await self._validate_schema(SchemaNetworks().network_services_of(AcLineSegment, ac_line_segment))

    @settings(**hypothesis_settings)
    @given(breaker=create_breaker(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_breaker(self, breaker: Breaker):
        await self._validate_schema(SchemaNetworks().network_services_of(Breaker, breaker))

    @settings(**hypothesis_settings)
    @given(busbar_section=create_busbar_section(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_busbar_section(self, busbar_section: BusbarSection):
        await self._validate_schema(SchemaNetworks().network_services_of(BusbarSection, busbar_section))

    @settings(**hypothesis_settings)
    @given(clamp=create_clamp(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_clamp(self, clamp: Clamp):
        await self._validate_schema(SchemaNetworks().network_services_of(Clamp, clamp))

    @settings(**hypothesis_settings)
    @given(cut=create_cut(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_cut(self, cut: Cut):
        await self._validate_schema(SchemaNetworks().network_services_of(Cut, cut))

    @settings(**hypothesis_settings)
    @given(disconnector=create_disconnector(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_disconnector(self, disconnector: Disconnector):
        await self._validate_schema(SchemaNetworks().network_services_of(Disconnector, disconnector))

    @settings(**hypothesis_settings)
    @given(energy_consumer=create_energy_consumer(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_energy_consumer(self, energy_consumer: EnergyConsumer):
        # Need to assure the correct number of phases to prevent errors.
        assume(len(Counter(map(lambda it: it.phase, energy_consumer.phases))) == len(list(energy_consumer.phases)))
        await self._validate_schema(SchemaNetworks().network_services_of(EnergyConsumer, energy_consumer))

    @settings(**hypothesis_settings)
    @given(energy_consumer_phase=create_energy_consumer_phase(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_energy_consumer_phase(self, energy_consumer_phase: EnergyConsumerPhase):
        await self._validate_schema(SchemaNetworks().network_services_of(EnergyConsumerPhase, energy_consumer_phase))

    @settings(**hypothesis_settings)
    @given(energy_source=create_energy_source(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_energy_source(self, energy_source: EnergySource):
        # Need to assure the correct number of phases to prevent errors.
        assume(len(Counter(map(lambda it: it.phase, energy_source.phases))) == len(list(energy_source.phases)))

        # Need to apply phases to match after the database load.
        network_service = SchemaNetworks().network_services_of(EnergySource, energy_source)
        await Tracing.set_phases().run(network_service)

        await self._validate_schema(network_service)

    @settings(**hypothesis_settings)
    @given(energy_source_phase=create_energy_source_phase(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_energy_source_phase(self, energy_source_phase: EnergyConsumerPhase):
        await self._validate_schema(SchemaNetworks().network_services_of(EnergySourcePhase, energy_source_phase))

    @settings(**hypothesis_settings)
    @given(fuse=create_fuse(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_fuse(self, fuse: Fuse):
        await self._validate_schema(SchemaNetworks().network_services_of(Fuse, fuse))

    @settings(**hypothesis_settings)
    @given(ground=create_ground(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_ground(self, ground: Ground):
        await self._validate_schema(SchemaNetworks().network_services_of(Ground, ground))

    @settings(**hypothesis_settings)
    @given(ground_disconnector=create_ground_disconnector(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_ground_disconnector(self, ground_disconnector: GroundDisconnector):
        await self._validate_schema(SchemaNetworks().network_services_of(GroundDisconnector, ground_disconnector))

    @settings(**hypothesis_settings)
    @given(grounding_impedance=create_grounding_impedance(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_grounding_impedance(self, grounding_impedance: GroundingImpedance):
        await self._validate_schema(SchemaNetworks().network_services_of(GroundingImpedance, grounding_impedance))

    @settings(**hypothesis_settings)
    @given(jumper=create_jumper(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_jumper(self, jumper: Jumper):
        await self._validate_schema(SchemaNetworks().network_services_of(Jumper, jumper))

    @settings(**hypothesis_settings)
    @given(junction=create_junction(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_junction(self, junction: Junction):
        await self._validate_schema(SchemaNetworks().network_services_of(Junction, junction))

    @settings(**hypothesis_settings)
    @given(linear_shunt_compensator=create_linear_shunt_compensator(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_linear_shunt_compensator(self, linear_shunt_compensator: LinearShuntCompensator):
        await self._validate_schema(SchemaNetworks().network_services_of(LinearShuntCompensator, linear_shunt_compensator))

    @settings(**hypothesis_settings)
    @given(load_break_switch=create_load_break_switch(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_load_break_switch(self, load_break_switch: LoadBreakSwitch):
        await self._validate_schema(SchemaNetworks().network_services_of(LoadBreakSwitch, load_break_switch))

    @settings(**hypothesis_settings)
    @given(per_length_phase_impedance=create_per_length_phase_impedance(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_per_length_phase_impedance(self, per_length_phase_impedance: PerLengthPhaseImpedance):
        await self._validate_schema(SchemaNetworks().network_services_of(PerLengthPhaseImpedance, per_length_phase_impedance))

    @settings(**hypothesis_settings)
    @given(per_length_sequence_impedance=create_per_length_sequence_impedance(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_per_length_sequence_impedance(self, per_length_sequence_impedance: PerLengthSequenceImpedance):
        await self._validate_schema(SchemaNetworks().network_services_of(PerLengthSequenceImpedance, per_length_sequence_impedance))

    @settings(**hypothesis_settings)
    @given(petersen_coil=create_petersen_coil(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_petersen_coil(self, petersen_coil: PetersenCoil):
        await self._validate_schema(SchemaNetworks().network_services_of(PetersenCoil, petersen_coil))

    @settings(**hypothesis_settings)
    @given(power_electronics_connection=create_power_electronics_connection(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_power_electronics_connection(self, power_electronics_connection: PowerElectronicsConnection):
        await self._validate_schema(SchemaNetworks().network_services_of(PowerElectronicsConnection, power_electronics_connection))

    @settings(**hypothesis_settings)
    @given(power_electronics_connection_phase=create_power_electronics_connection_phase(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_power_electronics_connection_phase(self, power_electronics_connection_phase: PowerElectronicsConnectionPhase):
        await self._validate_schema(SchemaNetworks().network_services_of(PowerElectronicsConnectionPhase, power_electronics_connection_phase))

    @settings(**hypothesis_settings)
    @given(power_transformer=create_power_transformer(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_power_transformer(self, power_transformer: PowerTransformer):
        await self._validate_schema(SchemaNetworks().network_services_of(PowerTransformer, power_transformer))

    @settings(**hypothesis_settings)
    @given(power_transformer_end=create_power_transformer_end(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_power_transformer_end(self, power_transformer_end: PowerTransformerEnd):
        await self._validate_schema(SchemaNetworks().network_services_of(PowerTransformerEnd, power_transformer_end))

    @settings(**hypothesis_settings)
    @given(ratio_tap_changer=create_ratio_tap_changer(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_ratio_tap_changer(self, ratio_tap_changer: RatioTapChanger):
        await self._validate_schema(SchemaNetworks().network_services_of(RatioTapChanger, ratio_tap_changer))

    @settings(**hypothesis_settings)
    @given(reactive_capability_curve=create_reactive_capability_curve(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_reactive_capability_curve(self, reactive_capability_curve: ReactiveCapabilityCurve):
        await self._validate_schema(SchemaNetworks().network_services_of(ReactiveCapabilityCurve, reactive_capability_curve))

    @settings(**hypothesis_settings)
    @given(recloser=create_recloser(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_recloser(self, recloser: Recloser):
        await self._validate_schema(SchemaNetworks().network_services_of(Recloser, recloser))

    @settings(**hypothesis_settings)
    @given(series_compensator=create_series_compensator(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_series_compensator(self, series_compensator: SeriesCompensator):
        await self._validate_schema(SchemaNetworks().network_services_of(SeriesCompensator, series_compensator))

    @settings(**hypothesis_settings)
    @given(static_var_compensator=create_static_var_compensator(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_static_var_compensator(self, static_var_compensator: StaticVarCompensator):
        await self._validate_schema(SchemaNetworks().network_services_of(StaticVarCompensator, static_var_compensator))

    @settings(**hypothesis_settings)
    @given(synchronous_machine=create_synchronous_machine(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_synchronous_machine(self, synchronous_machine: SynchronousMachine):
        await self._validate_schema(SchemaNetworks().network_services_of(SynchronousMachine, synchronous_machine))

    @settings(**hypothesis_settings)
    @given(tap_changer_control=create_tap_changer_control(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_tap_changer_control(self, tap_changer_control: TapChangerControl):
        await self._validate_schema(SchemaNetworks().network_services_of(TapChangerControl, tap_changer_control))

    @settings(**hypothesis_settings)
    @given(transformer_star_impedance=create_transformer_star_impedance(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_transformer_star_impedance(self, transformer_star_impedance: TransformerStarImpedance):
        await self._validate_schema(SchemaNetworks().network_services_of(TransformerStarImpedance, transformer_star_impedance))

    ###############################
    # IEC61970 InfIEC61970 Feeder #
    ###############################

    @settings(**hypothesis_settings)
    @given(circuit=create_circuit(False))
    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_schema_circuit(self, circuit: Circuit):
        await self._validate_schema(SchemaNetworks().network_services_of(Circuit, circuit))

    # ************ Services ************

    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_name_and_name_type_schema(self):
        await self._validate_schema(SchemaNetworks().create_name_test_services(NetworkService, Junction))

    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_post_process_fails_with_unresolved_references(self):
        pec = PowerElectronicsConnection(mrid="pec1")

        def add_deferred_reference(service: NetworkService):
            service.resolve_or_defer_reference(resolver.rce_regulating_control(pec), "tcc")

        await self._validate_unresolved_failure(str(pec), "RegulatingControl tcc", add_deferred_reference)

    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_assigns_feeders_in_parallel_correctly(self):
        # This test is to ensure parallel feeders don't assign directions back through the feeder heads. This was seen in the wild when
        # the feeder directions were set before the equipment was assigned, meaning no feeder heads were detected in the tracing.
        ns = await (
            TestNetworkBuilder()
            .from_source()  # s0
            .to_breaker()  # b1
            .to_acls()  # c2
            .to_breaker()  # b3
            .to_source()  # s4
            .add_feeder("b1", 2)
            .add_feeder("b3", 1)
            .build(apply_directions_from_sources=False)
        )

        # If the read from the database matches the test network we built, then the equipment is correctly assigned.
        await self._validate_schema(ns)

    @pytest.mark.timeout(PYTEST_TIMEOUT_SEC)
    async def test_only_loads_street_address_fields_if_required(self):
        # This test is here to make sure the database reading correctly removes the parts of loaded street addresses that are not filled out.
        write_service = NetworkService()
        write_service.add(Location(mrid="loc1", main_address=StreetAddress(town_detail=TownDetail(), street_detail=StreetDetail())))

        def validate(service: NetworkService):
            assert service.get("loc1", Location).main_address == StreetAddress(), \
                "Expected a default street address as blank parts should have been removed during teh database read"

        await self._validate_write_read(write_service, validate_read=validate)
