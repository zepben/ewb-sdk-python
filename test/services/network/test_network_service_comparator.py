#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import datetime
from typing import Type

import pytest

from zepben.evolve import CableInfo, NoLoadTest, OpenCircuitTest, OverheadWireInfo, PowerTransformerInfo, TransformerTankInfo, ShortCircuitTest, \
    TransformerEndInfo, TransformerStarImpedance, TransformerTest, WireInfo, WireMaterialKind, Asset, AssetOwner, Location, AssetContainer, AssetInfo, \
    AssetOrganisationRole, Pole, Streetlight, WindingConnection, StreetlightLampKind, Structure, StreetAddress, TownDetail, PositionPoint, EndDevice, \
    UsagePoint, Meter, Junction, OperationalRestriction, AuxiliaryEquipment, Terminal, FaultIndicator, AcDcTerminal, BaseVoltage, ConductingEquipment, \
    ConnectivityNode, ConnectivityNodeContainer, Equipment, Site, EquipmentContainer, Feeder, Substation, GeographicalRegion, SubGeographicalRegion, \
    PowerSystemResource, EquivalentBranch, EquivalentEquipment, Accumulator, Analog, Discrete, Measurement, RemoteSource, PhaseCode, UnitSymbol, \
    RemoteControl, Control, RemotePoint, BatteryUnit, BatteryStateKind, PhotoVoltaicUnit, PowerElectronicsUnit, PowerElectronicsConnection, \
    PowerElectronicsWindUnit, AcLineSegment, PerLengthSequenceImpedance, Breaker, BusbarSection, Conductor, Connector, Disconnector, EnergyConnection, \
    EnergyConsumer, PhaseShuntConnectionKind, EnergyConsumerPhase, SinglePhaseKind, EnergySource, EnergySourcePhase, Fuse, Jumper, Line, \
    LinearShuntCompensator, PerLengthImpedance, PerLengthLineParameter, PowerElectronicsConnectionPhase, PowerTransformer, PowerTransformerEnd, VectorGroup, \
    ProtectedSwitch, RatioTapChanger, Recloser, RegulatingCondEq, ShuntCompensator, Switch, ObjectDifference, ValueDifference, TapChanger, TransformerEnd, \
    Circuit, Loop, NetworkService, TracedPhases, FeederDirection, ShuntCompensatorInfo, TransformerConstructionKind, TransformerFunctionKind, LvFeeder, Sensor, \
    CurrentTransformer, PotentialTransformer, CurrentTransformerInfo, PotentialTransformerInfo, PotentialTransformerKind, Ratio, SwitchInfo, RelayInfo, \
    CurrentRelay, EvChargingUnit, PowerDirectionKind, RegulatingControl, TapChangerControl, RegulatingControlModeKind, \
    TransformerEndRatedS, TransformerCoolingType, ProtectionRelayFunction, ProtectionRelayScheme, RelaySetting, DistanceRelay, VoltageRelay, ProtectionKind, \
    ProtectionRelaySystem, Ground, GroundDisconnector, SeriesCompensator
from zepben.evolve.services.network.network_service_comparator import NetworkServiceComparatorOptions, NetworkServiceComparator

from services.common.service_comparator_validator import ServiceComparatorValidator
from services.common.test_base_service_comparator import TestBaseServiceComparator


class TestNetworkServiceComparator(TestBaseServiceComparator):
    validator = ServiceComparatorValidator(lambda: NetworkService(), lambda options: NetworkServiceComparator(options))

    #######################
    # IEC61968 ASSET INFO #
    #######################

    def test_compare_cable_info(self):
        self._compare_wire_info(CableInfo)

    def test_compare_no_load_test(self):
        self._compare_transformer_test(NoLoadTest)

        self.validator.validate_property(NoLoadTest.energised_end_voltage, NoLoadTest, lambda _: 1, lambda _: 2)
        self.validator.validate_property(NoLoadTest.exciting_current, NoLoadTest, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(NoLoadTest.exciting_current_zero, NoLoadTest, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(NoLoadTest.loss, NoLoadTest, lambda _: 1, lambda _: 2)
        self.validator.validate_property(NoLoadTest.loss_zero, NoLoadTest, lambda _: 1, lambda _: 2)

    def test_compare_open_circuit_test(self):
        self._compare_transformer_test(OpenCircuitTest)

        self.validator.validate_property(OpenCircuitTest.energised_end_step, OpenCircuitTest, lambda _: 1, lambda _: 2)
        self.validator.validate_property(OpenCircuitTest.energised_end_voltage, OpenCircuitTest, lambda _: 1, lambda _: 2)
        self.validator.validate_property(OpenCircuitTest.open_end_step, OpenCircuitTest, lambda _: 1, lambda _: 2)
        self.validator.validate_property(OpenCircuitTest.open_end_voltage, OpenCircuitTest, lambda _: 1, lambda _: 2)
        self.validator.validate_property(OpenCircuitTest.phase_shift, OpenCircuitTest, lambda _: 1.0, lambda _: 2.0)

    def test_compare_overhead_wire_info(self):
        self._compare_wire_info(OverheadWireInfo)

    def test_compare_power_transformer_info(self):
        self._compare_asset_info(PowerTransformerInfo)

        self.validator.validate_collection(
            PowerTransformerInfo.transformer_tank_infos,
            PowerTransformerInfo.add_transformer_tank_info,
            PowerTransformerInfo,
            lambda _: TransformerTankInfo(mrid="tti1"),
            lambda _: TransformerTankInfo(mrid="tti2")
        )

    def test_compare_short_circuit_test(self):
        self._compare_transformer_test(ShortCircuitTest)

        self.validator.validate_property(ShortCircuitTest.current, ShortCircuitTest, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(ShortCircuitTest.energised_end_step, ShortCircuitTest, lambda _: 1, lambda _: 2)
        self.validator.validate_property(ShortCircuitTest.grounded_end_step, ShortCircuitTest, lambda _: 1, lambda _: 2)
        self.validator.validate_property(ShortCircuitTest.leakage_impedance, ShortCircuitTest, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(ShortCircuitTest.leakage_impedance_zero, ShortCircuitTest, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(ShortCircuitTest.loss, ShortCircuitTest, lambda _: 1, lambda _: 2)
        self.validator.validate_property(ShortCircuitTest.loss_zero, ShortCircuitTest, lambda _: 1, lambda _: 2)
        self.validator.validate_property(ShortCircuitTest.power, ShortCircuitTest, lambda _: 1, lambda _: 2)
        self.validator.validate_property(ShortCircuitTest.voltage, ShortCircuitTest, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(ShortCircuitTest.voltage_ohmic_part, ShortCircuitTest, lambda _: 1.0, lambda _: 2.0)

    def test_compare_shunt_compensator_info(self):
        self._compare_asset_info(ShuntCompensatorInfo)
        self.validator.validate_property(ShuntCompensatorInfo.max_power_loss, ShuntCompensatorInfo, lambda _: 1, lambda _: 2)
        self.validator.validate_property(ShuntCompensatorInfo.rated_current, ShuntCompensatorInfo, lambda _: 1, lambda _: 2)
        self.validator.validate_property(ShuntCompensatorInfo.rated_reactive_power, ShuntCompensatorInfo, lambda _: 1, lambda _: 2)
        self.validator.validate_property(ShuntCompensatorInfo.rated_voltage, ShuntCompensatorInfo, lambda _: 1, lambda _: 2)

    def test_compare_switch_info(self):
        self._compare_asset_info(SwitchInfo)
        self.validator.validate_property(SwitchInfo.rated_interrupting_time, SwitchInfo, lambda _: 1.1, lambda _: 2.2)

    def test_compare_transformer_end_info(self):
        self._compare_asset_info(TransformerEndInfo)

        self.validator.validate_property(TransformerEndInfo.connection_kind, TransformerEndInfo, lambda _: WindingConnection.D, lambda _: WindingConnection.Y)
        self.validator.validate_property(TransformerEndInfo.emergency_s, TransformerEndInfo, lambda _: 1, lambda _: 2)
        self.validator.validate_property(TransformerEndInfo.end_number, TransformerEndInfo, lambda _: 1, lambda _: 2)
        self.validator.validate_property(TransformerEndInfo.insulation_u, TransformerEndInfo, lambda _: 1, lambda _: 2)
        self.validator.validate_property(TransformerEndInfo.phase_angle_clock, TransformerEndInfo, lambda _: 1, lambda _: 2)
        self.validator.validate_property(TransformerEndInfo.r, TransformerEndInfo, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(TransformerEndInfo.rated_s, TransformerEndInfo, lambda _: 1, lambda _: 2)
        self.validator.validate_property(TransformerEndInfo.rated_u, TransformerEndInfo, lambda _: 1, lambda _: 2)
        self.validator.validate_property(TransformerEndInfo.short_term_s, TransformerEndInfo, lambda _: 1, lambda _: 2)

        self.validator.validate_property(
            TransformerEndInfo.transformer_star_impedance,
            TransformerEndInfo,
            lambda _: TransformerStarImpedance(mrid="tsi1"),
            lambda _: TransformerStarImpedance(mrid="tsi2")
        )

    def test_compare_transformer_tank_info(self):
        self._compare_asset_info(TransformerTankInfo)

        self.validator.validate_collection(
            TransformerTankInfo.transformer_end_infos,
            TransformerTankInfo.add_transformer_end_info,
            TransformerTankInfo,
            lambda _: TransformerEndInfo(mrid="tei1"),
            lambda _: TransformerEndInfo(mrid="tei2")
        )

    def _compare_transformer_test(self, creator: Type[TransformerTest]):
        self._compare_identified_object(creator)

        self.validator.validate_property(TransformerTest.base_power, creator, lambda _: 1, lambda _: 2)
        self.validator.validate_property(TransformerTest.temperature, creator, lambda _: 1.0, lambda _: 2.0)

    def _compare_wire_info(self, creator: Type[WireInfo]):
        self._compare_asset_info(creator)

        self.validator.validate_property(WireInfo.rated_current, creator, lambda _: 1, lambda _: 2)
        self.validator.validate_property(WireInfo.material, creator, lambda _: WireMaterialKind.aluminum, lambda _: WireMaterialKind.copperCadmium)

    ###################
    # IEC61968 ASSETS #
    ###################

    def _compare_asset(self, creator: Type[Asset]):
        self._compare_identified_object(creator)

        self.validator.validate_collection(
            Asset.organisation_roles,
            Asset.add_organisation_role,
            creator,
            lambda _: AssetOwner(mrid="a1"),
            lambda _: AssetOwner(mrid="a2")
        )
        self.validator.validate_property(Asset.location, creator, lambda _: Location(mrid="l1"), lambda _: Location(mrid="l2"))

    def _compare_asset_container(self, creator: Type[AssetContainer]):
        self._compare_asset(creator)

    def _compare_asset_info(self, creator: Type[AssetInfo]):
        self._compare_identified_object(creator)

    def _compare_asset_organisation_role(self, creator: Type[AssetOrganisationRole]):
        self._compare_organisation_role(creator)

    def test_compare_asset_owner(self):
        self._compare_asset_organisation_role(AssetOwner)

    def test_compare_pole(self):
        self._compare_structure(Pole)
        self.validator.validate_property(Pole.classification, Pole, lambda _: "c1", lambda _: "c2")
        self.validator.validate_collection(Pole.streetlights, Pole.add_streetlight, Pole, lambda _: Streetlight(mrid="sl1"), lambda _: Streetlight(mrid="sl2"))

    def test_compare_streetlight(self):
        self._compare_asset(Streetlight)

        self.validator.validate_property(
            Streetlight.lamp_kind,
            Streetlight,
            lambda _: StreetlightLampKind.HIGH_PRESSURE_SODIUM,
            lambda _: StreetlightLampKind.MERCURY_VAPOR
        )
        self.validator.validate_property(Streetlight.light_rating, Streetlight, lambda _: 1, lambda _: 2)
        self.validator.validate_property(Streetlight.pole, Streetlight, lambda _: Pole(mrid="x"), lambda _: Pole(mrid="y"))

    def _compare_structure(self, creator: Type[Structure]):
        self._compare_asset_container(creator)

    ###################
    # IEC61968 COMMON #
    ###################

    def test_compare_location(self):
        self._compare_identified_object(Location)

        # noinspection PyArgumentList
        self.validator.validate_property(
            Location.main_address,
            Location,
            lambda _: StreetAddress("1234", TownDetail("town", "state")),
            lambda _: StreetAddress("1234", TownDetail("other", "state"))
        )
        # noinspection PyArgumentList
        self.validator.validate_indexed_collection(
            Location.points,
            Location.add_point,
            Location,
            lambda _: PositionPoint(1.0, 2.0),
            lambda _: PositionPoint(3.0, 4.0)
        )

    #####################################
    # IEC61968 infIEC61968 InfAssetInfo #
    #####################################

    def test_compare_relay_info(self):
        self._compare_asset_info(RelayInfo)

        self.validator.validate_property(RelayInfo.curve_setting, RelayInfo, lambda _: "cs1", lambda _: "cs2")
        self.validator.validate_property(RelayInfo.reclose_fast, RelayInfo, lambda _: True, lambda _: False)
        self.validator.validate_indexed_collection(
            RelayInfo.reclose_delays,
            RelayInfo.add_delay,
            RelayInfo,
            lambda _: [0.1, 0.2],
            lambda _: [0.1, 0.3]
        )

    # noinspection PyArgumentList
    def test_compare_current_transformer_info(self):
        self._compare_asset_info(CurrentTransformerInfo)

        self.validator.validate_property(CurrentTransformerInfo.accuracy_class, CurrentTransformerInfo, lambda _: "acc1", lambda _: "acc2")
        self.validator.validate_property(CurrentTransformerInfo.accuracy_limit, CurrentTransformerInfo, lambda _: 1.1, lambda _: 2.2)
        self.validator.validate_property(CurrentTransformerInfo.core_count, CurrentTransformerInfo, lambda _: 1, lambda _: 2)
        self.validator.validate_property(CurrentTransformerInfo.ct_class, CurrentTransformerInfo, lambda _: "ctc1", lambda _: "ctc2")
        self.validator.validate_property(CurrentTransformerInfo.knee_point_voltage, CurrentTransformerInfo, lambda _: 1, lambda _: 2)
        self.validator.validate_property(CurrentTransformerInfo.max_ratio, CurrentTransformerInfo, lambda _: Ratio(1.1, 2.2), lambda _: Ratio(3.3, 4.4))
        self.validator.validate_property(CurrentTransformerInfo.nominal_ratio, CurrentTransformerInfo, lambda _: Ratio(1.1, 2.2), lambda _: Ratio(3.3, 4.4))
        self.validator.validate_property(CurrentTransformerInfo.primary_ratio, CurrentTransformerInfo, lambda _: 1.1, lambda _: 2.2)
        self.validator.validate_property(CurrentTransformerInfo.rated_current, CurrentTransformerInfo, lambda _: 1, lambda _: 2)
        self.validator.validate_property(CurrentTransformerInfo.secondary_fls_rating, CurrentTransformerInfo, lambda _: 1, lambda _: 2)
        self.validator.validate_property(CurrentTransformerInfo.secondary_ratio, CurrentTransformerInfo, lambda _: 1.1, lambda _: 2.2)
        self.validator.validate_property(CurrentTransformerInfo.usage, CurrentTransformerInfo, lambda _: "usage1", lambda _: "usage2")

    # noinspection PyArgumentList
    def test_compare_potential_transformer_info(self):
        self._compare_asset_info(PotentialTransformerInfo)

        self.validator.validate_property(PotentialTransformerInfo.accuracy_class, PotentialTransformerInfo, lambda _: "acc1", lambda _: "acc2")
        self.validator.validate_property(PotentialTransformerInfo.nominal_ratio, PotentialTransformerInfo, lambda _: Ratio(1.1, 2.2), lambda _: Ratio(3.3, 4.4))
        self.validator.validate_property(PotentialTransformerInfo.primary_ratio, PotentialTransformerInfo, lambda _: 1.1, lambda _: 2.2)
        self.validator.validate_property(PotentialTransformerInfo.pt_class, PotentialTransformerInfo, lambda _: "ptc1", lambda _: "ptc2")
        self.validator.validate_property(PotentialTransformerInfo.rated_voltage, PotentialTransformerInfo, lambda _: 1, lambda _: 2)
        self.validator.validate_property(PotentialTransformerInfo.secondary_ratio, PotentialTransformerInfo, lambda _: 1.1, lambda _: 2.2)

    #####################
    # IEC61968 METERING #
    #####################

    def _compare_end_device(self, creator: Type[EndDevice]):
        self._compare_asset_container(creator)

        self.validator.validate_property(EndDevice.customer_mrid, creator, lambda _: "customer1", lambda _: "customer2")
        self.validator.validate_property(EndDevice.service_location, creator, lambda _: Location(mrid="l1"), lambda _: Location(mrid="l2"))
        self.validator.validate_collection(
            EndDevice.usage_points,
            EndDevice.add_usage_point,
            creator,
            lambda _: UsagePoint(mrid="up1"),
            lambda _: UsagePoint(mrid="up2"),
            NetworkServiceComparatorOptions(compare_lv_simplification=False),
            options_stop_compare=True
        )

    def test_compare_meter(self):
        self._compare_end_device(Meter)

    def test_compare_usage_point(self):
        self._compare_identified_object(UsagePoint)

        self.validator.validate_property(UsagePoint.usage_point_location, UsagePoint, lambda _: Location(mrid="l1"), lambda _: Location(mrid="l2"))
        self.validator.validate_property(UsagePoint.is_virtual, UsagePoint, lambda _: False, lambda _: True)
        self.validator.validate_property(UsagePoint.connection_category, UsagePoint, lambda _: "first", lambda _: "second")
        self.validator.validate_property(UsagePoint.rated_power, UsagePoint, lambda _: 1, lambda _: 2)
        self.validator.validate_property(UsagePoint.approved_inverter_capacity, UsagePoint, lambda _: 1, lambda _: 2)
        self.validator.validate_collection(
            UsagePoint.end_devices,
            UsagePoint.add_end_device,
            UsagePoint,
            lambda _: Meter(mrid="m1"),
            lambda _: Meter(mrid="m2"),
            NetworkServiceComparatorOptions(compare_lv_simplification=False),
            options_stop_compare=True
        )
        self.validator.validate_collection(
            UsagePoint.equipment,
            UsagePoint.add_equipment,
            UsagePoint,
            lambda _: Junction(mrid="j1"),
            lambda _: Junction(mrid="j2"),
            NetworkServiceComparatorOptions(compare_lv_simplification=False),
            options_stop_compare=True
        )

    #######################
    # IEC61968 OPERATIONS #
    #######################

    def test_compare_operational_restriction(self):
        self._compare_document(OperationalRestriction)

        self.validator.validate_collection(
            OperationalRestriction.equipment,
            OperationalRestriction.add_equipment,
            OperationalRestriction,
            lambda _: Junction(mrid="j1"),
            lambda _: Junction(mrid="j2")
        )

    #####################################
    # IEC61970 BASE AUXILIARY EQUIPMENT #
    #####################################

    def _compare_auxiliary_equipment(self, creator: Type[AuxiliaryEquipment]):
        self._compare_equipment(creator)

        self.validator.validate_property(
            AuxiliaryEquipment.terminal,
            creator,
            lambda _: Terminal(mrid="t1"),
            lambda _: Terminal(mrid="t2"),
            NetworkServiceComparatorOptions(compare_terminals=False),
            options_stop_compare=True
        )

    def test_compare_current_transformer(self):
        self._compare_sensor(CurrentTransformer)

        self.validator.validate_property(CurrentTransformer.core_burden, CurrentTransformer, lambda _: 1, lambda _: 2)
        self.validator.validate_property(
            CurrentTransformer.asset_info,
            CurrentTransformer,
            lambda _: CurrentTransformerInfo(mrid="acti1"),
            lambda _: CurrentTransformerInfo(mrid="acti2"),
            expected_differences={"current_transformer_info"}
        )
        self.validator.validate_property(
            CurrentTransformer.current_transformer_info,
            CurrentTransformer,
            lambda _: CurrentTransformerInfo(mrid="acti1"),
            lambda _: CurrentTransformerInfo(mrid="acti2"),
            expected_differences={"asset_info"}
        )

    def test_compare_fault_indicator(self):
        self._compare_auxiliary_equipment(FaultIndicator)

    def test_compare_potential_transformer(self):
        self._compare_sensor(PotentialTransformer)

        self.validator.validate_property(
            PotentialTransformer.type,
            PotentialTransformer,
            lambda _: PotentialTransformerKind.capacitiveCoupling,
            lambda _: PotentialTransformerKind.inductive
        )
        self.validator.validate_property(
            PotentialTransformer.asset_info,
            PotentialTransformer,
            lambda _: PotentialTransformerInfo(mrid="avti1"),
            lambda _: PotentialTransformerInfo(mrid="avti2"),
            expected_differences={"potential_transformer_info"}
        )
        self.validator.validate_property(
            PotentialTransformer.potential_transformer_info,
            PotentialTransformer,
            lambda _: PotentialTransformerInfo(mrid="vti1"),
            lambda _: PotentialTransformerInfo(mrid="vti2"),
            expected_differences={"asset_info"}
        )

    def _compare_sensor(self, creator: Type[Sensor]):
        self.validator.validate_collection(
            Sensor.relay_functions,
            Sensor.add_relay_function,
            creator,
            lambda _: ProtectionRelayFunction(mrid="prf1"),
            lambda _: ProtectionRelayFunction(mrid="prf2")
        )
        self._compare_auxiliary_equipment(creator)

    ######################
    # IEC61970 BASE CORE #
    ######################

    def _compare_ac_dc_terminal(self, creator: Type[AcDcTerminal]):
        self._compare_identified_object(creator)

    def test_compare_base_voltage(self):
        self._compare_identified_object(BaseVoltage)

        self.validator.validate_property(BaseVoltage.nominal_voltage, BaseVoltage, lambda _: 1, lambda _: 2)

    def _compare_conducting_equipment(self, creator: Type[ConductingEquipment]):
        self._compare_equipment(creator)

        self.validator.validate_property(ConductingEquipment.base_voltage, creator, lambda _: BaseVoltage(mrid="b1"), lambda _: BaseVoltage(mrid="b2"))
        self.validator.validate_indexed_collection(
            ConductingEquipment.terminals,
            ConductingEquipment.add_terminal,
            creator,
            lambda _: Terminal(mrid="1"),
            lambda _: Terminal(mrid="2"),
            NetworkServiceComparatorOptions(compare_terminals=False),
            options_stop_compare=True
        )

    def test_compare_connectivity_node(self):
        self._compare_identified_object(ConnectivityNode)

        self.validator.validate_collection(
            ConnectivityNode.terminals,
            ConnectivityNode.add_terminal,
            ConnectivityNode,
            lambda _: Terminal(mrid="1"),
            lambda _: Terminal(mrid="2")
        )

    def _compare_connectivity_node_container(self, creator: Type[ConnectivityNodeContainer]):
        self._compare_power_system_resource(creator)

    def _compare_equipment(self, creator: Type[Equipment]):
        self._compare_power_system_resource(creator)

        self.validator.validate_property(Equipment.in_service, creator, lambda _: True, lambda _: False)
        self.validator.validate_property(Equipment.normally_in_service, creator, lambda _: True, lambda _: False)
        self.validator.validate_property(
            Equipment.commissioned_date,
            creator,
            lambda _: datetime.datetime.fromtimestamp(0),
            lambda _: datetime.datetime.fromtimestamp(1)
        )
        self.validator.validate_collection(Equipment.containers, Equipment.add_container, creator, lambda _: Site(mrid="s1"), lambda _: Site(mrid="s2"))
        self.validator.validate_collection(
            Equipment.usage_points,
            Equipment.add_usage_point,
            creator, lambda _: UsagePoint(mrid="u1"),
            lambda _: UsagePoint(mrid="u2")
        )
        self.validator.validate_collection(
            Equipment.operational_restrictions,
            Equipment.add_operational_restriction,
            creator,
            lambda _: OperationalRestriction(mrid="o1"),
            lambda _: OperationalRestriction(mrid="o2")
        )
        self.validator.validate_collection(
            Equipment.current_containers,
            Equipment.add_current_container,
            creator,
            lambda _: Feeder(mrid="f1"),
            lambda _: Feeder(mrid="f2")
        )

    def _compare_equipment_container(self, creator: Type[EquipmentContainer]):
        self._compare_connectivity_node_container(creator)

        self.validator.validate_collection(
            EquipmentContainer.equipment,
            EquipmentContainer.add_equipment,
            creator,
            lambda _: Junction(mrid="j1"),
            lambda _: Junction(mrid="j2")
        )

    def test_compare_feeder(self):
        self._compare_equipment_container(Feeder)

        self.validator.validate_property(Feeder.normal_head_terminal, Feeder, lambda _: Terminal(mrid="t1"), lambda _: Terminal(mrid="t2"))
        self.validator.validate_property(Feeder.normal_energizing_substation, Feeder, lambda _: Substation(mrid="s1"), lambda _: Substation(mrid="s2"))
        self.validator.validate_collection(
            Feeder.current_equipment,
            Feeder.add_current_equipment,
            Feeder,
            lambda _: Junction(mrid="j1"),
            lambda _: Junction(mrid="j2")
        )
        self.validator.validate_collection(
            Feeder.normal_energized_lv_feeders,
            Feeder.add_normal_energized_lv_feeder,
            Feeder,
            lambda _: LvFeeder(mrid="lvf1"),
            lambda _: LvFeeder(mrid="lvf2")
        )

    def test_compare_geographical_region(self):
        self._compare_identified_object(GeographicalRegion)

        self.validator.validate_collection(
            GeographicalRegion.sub_geographical_regions,
            GeographicalRegion.add_sub_geographical_region,
            GeographicalRegion,
            lambda _: SubGeographicalRegion(mrid="sg1"),
            lambda _: SubGeographicalRegion(mrid="sg2")
        )

    def _compare_power_system_resource(self, creator: Type[PowerSystemResource]):
        self._compare_identified_object(creator)

        self.validator.validate_property(PowerSystemResource.location, creator, lambda _: Location(mrid="l1"), lambda _: Location(mrid="l2"))

    def test_compare_site(self):
        self._compare_equipment_container(Site)

    def test_compare_sub_geographical_region(self):
        self._compare_identified_object(SubGeographicalRegion)

        self.validator.validate_property(
            SubGeographicalRegion.geographical_region,
            SubGeographicalRegion,
            lambda _: GeographicalRegion(mrid="g1"),
            lambda _: GeographicalRegion(mrid="g2")
        )
        self.validator.validate_collection(
            SubGeographicalRegion.substations,
            SubGeographicalRegion.add_substation,
            SubGeographicalRegion,
            lambda _: Substation(mrid="s1"),
            lambda _: Substation(mrid="s2")
        )

    def test_compare_substation(self):
        self._compare_equipment_container(Substation)

        self.validator.validate_property(
            Substation.sub_geographical_region,
            Substation,
            lambda _: SubGeographicalRegion(mrid="sg1"),
            lambda _: SubGeographicalRegion(mrid="sg2")
        )
        self.validator.validate_collection(Substation.feeders, Substation.add_feeder, Substation, lambda _: Feeder(mrid="f1"), lambda _: Feeder(mrid="f2"))

    def test_compare_terminal(self):
        self._compare_ac_dc_terminal(Terminal)

        #
        # NOTE: We need to have local variables for these otherwise they are garbage collected as they are only stored in weak references.
        #
        cn1 = ConnectivityNode(mrid="c1")
        cn2 = ConnectivityNode(mrid="c2")

        self.validator.validate_property(Terminal.phases, Terminal, lambda _: PhaseCode.ABC, lambda _: PhaseCode.ABCN)
        self.validator.validate_property(Terminal.sequence_number, Terminal, lambda _: 1, lambda _: 2)
        self.validator.validate_property(Terminal.normal_feeder_direction, Terminal, lambda _: FeederDirection.UPSTREAM, lambda _: FeederDirection.DOWNSTREAM)
        self.validator.validate_property(Terminal.current_feeder_direction, Terminal, lambda _: FeederDirection.UPSTREAM, lambda _: FeederDirection.DOWNSTREAM)

        for i in range(0, 32, 4):
            # noinspection PyArgumentList
            self.validator.validate_property(Terminal.traced_phases, Terminal, lambda _: TracedPhases(0x00000001 << i), lambda _: TracedPhases(0x00000002 << i))
            # noinspection PyArgumentList
            self.validator.validate_property(Terminal.traced_phases, Terminal, lambda _: TracedPhases(0x00000004 << i), lambda _: TracedPhases(0x00000008 << i))
            # noinspection PyArgumentList
            self.validator.validate_property(Terminal.traced_phases, Terminal, lambda _: TracedPhases(0x00000010 << i), lambda _: TracedPhases(0x00000020 << i))
            # noinspection PyArgumentList
            self.validator.validate_property(Terminal.traced_phases, Terminal, lambda _: TracedPhases(0x00000040 << i), lambda _: TracedPhases(0x00000080 << i))

        self.validator.validate_val_property(
            Terminal.connectivity_node,
            Terminal,
            lambda terminal, _: terminal.connect(cn1),
            lambda terminal, _: terminal.connect(cn2)
        )
        self.validator.validate_property(Terminal.conducting_equipment, Terminal, lambda _: Junction(mrid="j1"), lambda _: Junction(mrid="j2"))

    #############################
    # IEC61970 BASE EQUIVALENTS #
    #############################

    def test_compare_equivalent_branch(self):
        self._compare_equivalent_equipment(EquivalentBranch)

        self.validator.validate_property(EquivalentBranch.negative_r12, EquivalentBranch, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EquivalentBranch.negative_r21, EquivalentBranch, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EquivalentBranch.negative_x12, EquivalentBranch, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EquivalentBranch.negative_x21, EquivalentBranch, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EquivalentBranch.positive_r12, EquivalentBranch, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EquivalentBranch.positive_r21, EquivalentBranch, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EquivalentBranch.positive_x12, EquivalentBranch, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EquivalentBranch.positive_x21, EquivalentBranch, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EquivalentBranch.r, EquivalentBranch, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EquivalentBranch.r21, EquivalentBranch, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EquivalentBranch.x, EquivalentBranch, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EquivalentBranch.x21, EquivalentBranch, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EquivalentBranch.zero_r12, EquivalentBranch, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EquivalentBranch.zero_r21, EquivalentBranch, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EquivalentBranch.zero_x12, EquivalentBranch, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EquivalentBranch.zero_x21, EquivalentBranch, lambda _: 1.0, lambda _: 2.0)

    def _compare_equivalent_equipment(self, creator: Type[EquivalentEquipment]):
        self._compare_conducting_equipment(creator)

    ######################
    # IEC61970 BASE MEAS #
    ######################

    def test_compare_accumulator(self):
        self._compare_measurement(Accumulator)

    def test_compare_analog(self):
        self._compare_measurement(Analog)
        self.validator.validate_property(Analog.positive_flow_in, Analog, lambda _: True, lambda _: False)

    def test_compare_discrete(self):
        self._compare_measurement(Discrete)

    def _compare_measurement(self, creator: Type[Measurement]):
        self._compare_identified_object(creator)

        self.validator.validate_property(Measurement.power_system_resource_mrid, creator, lambda _: "psr1", lambda _: "psr2")
        self.validator.validate_property(Measurement.terminal_mrid, creator, lambda _: "terminal1", lambda _: "terminal2")
        self.validator.validate_property(Measurement.remote_source, creator, lambda _: RemoteSource(mrid="rs1"), lambda _: RemoteSource(mrid="rs2"))
        self.validator.validate_property(Measurement.phases, creator, lambda _: PhaseCode.ABCN, lambda _: PhaseCode.ABC)
        self.validator.validate_property(Measurement.unit_symbol, creator, lambda _: UnitSymbol.HENRYS, lambda _: UnitSymbol.HOURS)

    ############################
    # IEC61970 Base Protection #
    ############################
    def test_compare_current_relay(self):
        self._compare_protection_relay_function(CurrentRelay)

        self.validator.validate_property(CurrentRelay.current_limit_1, CurrentRelay, lambda _: 1.1, lambda _: 2.2)
        self.validator.validate_property(CurrentRelay.inverse_time_flag, CurrentRelay, lambda _: False, lambda _: True)
        self.validator.validate_property(CurrentRelay.time_delay_1, CurrentRelay, lambda _: 1.1, lambda _: 2.2)

    def test_compare_distance_relay(self):
        self._compare_protection_relay_function(DistanceRelay)

        self.validator.validate_property(DistanceRelay.backward_blind, DistanceRelay, lambda _: 1.1, lambda _: 2.2)
        self.validator.validate_property(DistanceRelay.backward_reach, DistanceRelay, lambda _: 1.1, lambda _: 2.2)
        self.validator.validate_property(DistanceRelay.backward_reactance, DistanceRelay, lambda _: 1.1, lambda _: 2.2)
        self.validator.validate_property(DistanceRelay.forward_blind, DistanceRelay, lambda _: 1.1, lambda _: 2.2)
        self.validator.validate_property(DistanceRelay.forward_reach, DistanceRelay, lambda _: 1.1, lambda _: 2.2)
        self.validator.validate_property(DistanceRelay.forward_reactance, DistanceRelay, lambda _: 1.1, lambda _: 2.2)
        self.validator.validate_property(DistanceRelay.operation_phase_angle1, DistanceRelay, lambda _: 1.1, lambda _: 2.2)
        self.validator.validate_property(DistanceRelay.operation_phase_angle2, DistanceRelay, lambda _: 1.1, lambda _: 2.2)
        self.validator.validate_property(DistanceRelay.operation_phase_angle3, DistanceRelay, lambda _: 1.1, lambda _: 2.2)

    def test_compare_voltage_relay(self):
        self._compare_protection_relay_function(VoltageRelay)

    def _compare_protection_relay_function(self, creator: Type[ProtectionRelayFunction]):
        self._compare_power_system_resource(creator)

        self.validator.validate_property(ProtectionRelayFunction.model, creator, lambda _: "model_1", lambda _: "model_2")
        self.validator.validate_property(ProtectionRelayFunction.reclosing, creator, lambda _: False, lambda _: True)
        self.validator.validate_property(
            ProtectionRelayFunction.protection_kind,
            creator,
            lambda _: ProtectionKind.JGGG,
            lambda _: ProtectionKind.NEGATIVE_OVERCURRENT
        )
        self.validator.validate_property(ProtectionRelayFunction.relay_delay_time, creator, lambda _: 1.1, lambda _: 2.2)
        self.validator.validate_property(ProtectionRelayFunction.directable, creator, lambda _: False, lambda _: True)
        self.validator.validate_property(
            ProtectionRelayFunction.power_direction,
            creator,
            lambda _: PowerDirectionKind.FORWARD,
            lambda _: PowerDirectionKind.REVERSE
        )

        self.validator.validate_collection(
            ProtectionRelayFunction.sensors,
            ProtectionRelayFunction.add_sensor,
            creator,
            lambda _: CurrentTransformer(mrid="ct1"),
            lambda _: CurrentTransformer(mrid="ct2")
        )

        self.validator.validate_collection(
            ProtectionRelayFunction.protected_switches,
            ProtectionRelayFunction.add_protected_switch,
            creator,
            lambda _: Breaker(mrid="b1"),
            lambda _: Breaker(mrid="b2")
        )

        self.validator.validate_collection(
            ProtectionRelayFunction.schemes,
            ProtectionRelayFunction.add_scheme,
            creator,
            lambda _: ProtectionRelayScheme(mrid="prs1"),
            lambda _: ProtectionRelayScheme(mrid="prs2")
        )

        self.validator.validate_indexed_collection(
            ProtectionRelayFunction.time_limits,
            ProtectionRelayFunction.add_time_limit,
            creator,
            lambda _: 1.11,
            lambda _: 2.12,
        )

        self.validator.validate_indexed_collection(
            ProtectionRelayFunction.thresholds,
            ProtectionRelayFunction.add_threshold,
            creator,
            lambda _: RelaySetting(UnitSymbol.HENRYS, 1.01, "name_rs1"),
            lambda _: RelaySetting(UnitSymbol.PAPERS, 2.02, "name_rs2"),
        )

        self.validator.validate_property(
            ProtectionRelayFunction.asset_info,
            creator,
            lambda _: RelayInfo(mrid="ari1"),
            lambda _: RelayInfo(mrid="ari2"),
            expected_differences={"relay_info"}
        )

        self.validator.validate_property(
            ProtectionRelayFunction.relay_info,
            creator,
            lambda _: RelayInfo(mrid="ri1"),
            lambda _: RelayInfo(mrid="ri2"),
            expected_differences={"asset_info"}
        )

    def test_compare_protection_relay_scheme(self):
        self._compare_identified_object(ProtectionRelayScheme)
        self.validator.validate_property(
            ProtectionRelayScheme.system,
            ProtectionRelayScheme,
            lambda _: ProtectionRelaySystem(mrid="prs1"),
            lambda _: ProtectionRelaySystem(mrid="prs2")
        )

        self.validator.validate_collection(
            ProtectionRelayScheme.functions,
            ProtectionRelayScheme.add_function,
            ProtectionRelayScheme,
            lambda _: ProtectionRelayFunction(mrid="prf1"),
            lambda _: ProtectionRelayFunction(mrid="prf2")
        )

    def test_compare_protection_relay_system(self):
        self._compare_equipment(ProtectionRelaySystem)
        self.validator.validate_property(
            ProtectionRelaySystem.protection_kind,
            ProtectionRelaySystem,
            lambda _: ProtectionKind.JDIFF,
            lambda _: ProtectionKind.SECTIONALIZER
        )

        self.validator.validate_collection(
            ProtectionRelaySystem.schemes,
            ProtectionRelaySystem.add_scheme,
            ProtectionRelaySystem,
            lambda _: ProtectionRelayScheme(mrid="prs1"),
            lambda _: ProtectionRelayScheme(mrid="prs2")
        )

    #######################
    # IEC61970 BASE SCADA #
    #######################

    def test_compare_remote_control(self):
        self._compare_remote_point(RemoteControl)

        self.validator.validate_property(RemoteControl.control, RemoteControl, lambda _: Control(mrid="c1"), lambda _: Control(mrid="c2"))

    def _compare_remote_point(self, creator: Type[RemotePoint]):
        self._compare_identified_object(creator)

    def test_compare_remote_source(self):
        self._compare_remote_point(RemoteSource)

        self.validator.validate_property(
            RemoteSource.measurement,
            RemoteSource,
            lambda _: Measurement(mrid="m1"),
            lambda _: Measurement(mrid="m2")
        )

    #############################################
    # IEC61970 BASE WIRES GENERATION PRODUCTION #
    #############################################

    def test_compare_battery_unit(self):
        self._compare_power_electronics_unit(BatteryUnit)

        self.validator.validate_property(BatteryUnit.battery_state, BatteryUnit, lambda _: BatteryStateKind.charging, lambda _: BatteryStateKind.discharging)
        self.validator.validate_property(BatteryUnit.rated_e, BatteryUnit, lambda _: 1, lambda _: 2)
        self.validator.validate_property(BatteryUnit.stored_e, BatteryUnit, lambda _: 1, lambda _: 2)

    def test_compare_photo_voltaic_unit(self):
        self._compare_power_electronics_unit(PhotoVoltaicUnit)

    def _compare_power_electronics_unit(self, creator: Type[PowerElectronicsUnit]):
        self._compare_equipment(creator)

        self.validator.validate_property(
            PowerElectronicsUnit.power_electronics_connection,
            creator,
            lambda _: PowerElectronicsConnection(mrid="pec1"),
            lambda _: PowerElectronicsConnection(mrid="pec2")
        )
        self.validator.validate_property(PowerElectronicsUnit.max_p, creator, lambda _: 1, lambda _: 2)
        self.validator.validate_property(PowerElectronicsUnit.min_p, creator, lambda _: 1, lambda _: 2)

    def test_compare_power_electronics_wind_unit(self):
        self._compare_power_electronics_unit(PowerElectronicsWindUnit)

    #######################
    # IEC61970 BASE WIRES #
    #######################

    def test_compare_ac_line_segment(self):
        self._compare_conductor(AcLineSegment)

        self.validator.validate_property(
            AcLineSegment.per_length_sequence_impedance,
            AcLineSegment,
            lambda _: PerLengthSequenceImpedance(mrid="p1"),
            lambda _: PerLengthSequenceImpedance(mrid="p2")
        )

    def test_compare_breaker(self):
        self._compare_protected_switch(Breaker)

        self.validator.validate_property(Breaker.in_transit_time, Breaker, lambda _: 1.1, lambda _: 2.2)

    def test_compare_busbar_section(self):
        self._compare_connector(BusbarSection)

    def _compare_conductor(self, creator: Type[Conductor]):
        self._compare_conducting_equipment(creator)

        self.validator.validate_property(Conductor.length, creator, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(Conductor.asset_info, creator, lambda _: CableInfo(mrid="c1"), lambda _: CableInfo(mrid="c2"),
                                         expected_differences={"wire_info"})
        self.validator.validate_property(Conductor.wire_info, creator, lambda _: OverheadWireInfo(mrid="owi1"), lambda _: CableInfo(mrid="c2"),
                                         expected_differences={"asset_info"})

    def _compare_connector(self, creator: Type[Connector]):
        self._compare_conducting_equipment(creator)

    def test_compare_disconnector(self):
        self._compare_switch(Disconnector)

    def _compare_energy_connection(self, creator: Type[EnergyConnection]):
        self._compare_conducting_equipment(creator)

    def test_compare_energy_consumer(self):
        self._compare_energy_connection(EnergyConsumer)

        self.validator.validate_property(EnergyConsumer.customer_count, EnergyConsumer, lambda _: 1, lambda _: 2)
        self.validator.validate_property(EnergyConsumer.grounded, EnergyConsumer, lambda _: True, lambda _: False)
        self.validator.validate_property(EnergyConsumer.p, EnergyConsumer, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergyConsumer.p_fixed, EnergyConsumer, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(
            EnergyConsumer.phase_connection,
            EnergyConsumer,
            lambda _: PhaseShuntConnectionKind.I,
            lambda _: PhaseShuntConnectionKind.D
        )
        self.validator.validate_property(EnergyConsumer.q, EnergyConsumer, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergyConsumer.q_fixed, EnergyConsumer, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_collection(
            EnergyConsumer.phases,
            EnergyConsumer.add_phase,
            EnergyConsumer,
            lambda _: EnergyConsumerPhase(mrid="ecp1"),
            lambda _: EnergyConsumerPhase(mrid="ecp2")
        )

    def test_compare_energy_consumer_phase(self):
        self._compare_power_system_resource(EnergyConsumerPhase)

        self.validator.validate_property(
            EnergyConsumerPhase.energy_consumer,
            EnergyConsumerPhase,
            lambda _: EnergyConsumer(mrid="ec1"),
            lambda _: EnergyConsumer(mrid="ec2")
        )
        self.validator.validate_property(EnergyConsumerPhase.phase, EnergyConsumerPhase, lambda _: SinglePhaseKind.A, lambda _: SinglePhaseKind.B)
        self.validator.validate_property(EnergyConsumerPhase.p, EnergyConsumerPhase, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergyConsumerPhase.p_fixed, EnergyConsumerPhase, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergyConsumerPhase.q, EnergyConsumerPhase, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergyConsumerPhase.q_fixed, EnergyConsumerPhase, lambda _: 1.0, lambda _: 2.0)

    def test_compare_energy_source(self):
        self._compare_energy_connection(EnergySource)

        self.validator.validate_property(EnergySource.active_power, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.reactive_power, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.voltage_angle, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.voltage_magnitude, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.p_max, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.p_min, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.r, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.r0, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.rn, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.x, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.x0, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.xn, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.is_external_grid, EnergySource, lambda _: False, lambda _: True)
        self.validator.validate_property(EnergySource.r_min, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.rn_min, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.r0_min, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.x_min, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.xn_min, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.x0_min, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.r_max, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.rn_max, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.r0_max, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.x_max, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.xn_max, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(EnergySource.x0_max, EnergySource, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_collection(
            EnergySource.phases,
            EnergySource.add_phase,
            EnergySource,
            lambda _: EnergySourcePhase(mrid="ecp1"),
            lambda _: EnergySourcePhase(mrid="ecp2")
        )

    def test_compare_energy_source_phase(self):
        self._compare_power_system_resource(EnergySourcePhase)

        self.validator.validate_property(EnergySourcePhase.phase, EnergySourcePhase, lambda _: SinglePhaseKind.A, lambda _: SinglePhaseKind.B)
        self.validator.validate_property(
            EnergySourcePhase.energy_source,
            EnergySourcePhase,
            lambda _: EnergySource(mrid="es1"),
            lambda _: EnergySource(mrid="es2")
        )

    def test_compare_fuse(self):
        self._compare_switch(Fuse)
        self.validator.validate_property(
            Fuse.function,
            Fuse,
            lambda _: ProtectionRelayFunction(mrid="prf1"),
            lambda _: ProtectionRelayFunction(mrid="prf2")
        )

    def test_compare_ground(self):
        self._compare_conducting_equipment(Ground)

    def test_compare_ground_disconnector(self):
        self._compare_switch(GroundDisconnector)

    def test_compare_jumper(self):
        self._compare_switch(Jumper)

    def test_compare_junction(self):
        self._compare_connector(Junction)

    def _compare_line(self, creator: Type[Line]):
        self._compare_equipment_container(creator)

    def test_compare_linear_shunt_compensator(self):
        self._compare_shunt_compensator(LinearShuntCompensator)

        self.validator.validate_property(LinearShuntCompensator.b0_per_section, LinearShuntCompensator, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(LinearShuntCompensator.b_per_section, LinearShuntCompensator, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(LinearShuntCompensator.g0_per_section, LinearShuntCompensator, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(LinearShuntCompensator.g_per_section, LinearShuntCompensator, lambda _: 1.0, lambda _: 2.0)

    def _compare_per_length_impedance(self, creator: Type[PerLengthImpedance]):
        self._compare_per_length_line_parameter(creator)

    def _compare_per_length_line_parameter(self, creator: Type[PerLengthLineParameter]):
        self._compare_identified_object(creator)

    def test_compare_per_length_sequence_impedance(self):
        self._compare_per_length_impedance(PerLengthSequenceImpedance)

        self.validator.validate_property(PerLengthSequenceImpedance.r, PerLengthSequenceImpedance, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(PerLengthSequenceImpedance.x, PerLengthSequenceImpedance, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(PerLengthSequenceImpedance.bch, PerLengthSequenceImpedance, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(PerLengthSequenceImpedance.gch, PerLengthSequenceImpedance, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(PerLengthSequenceImpedance.r0, PerLengthSequenceImpedance, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(PerLengthSequenceImpedance.x0, PerLengthSequenceImpedance, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(PerLengthSequenceImpedance.b0ch, PerLengthSequenceImpedance, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(PerLengthSequenceImpedance.g0ch, PerLengthSequenceImpedance, lambda _: 1.0, lambda _: 2.0)

    def test_compare_power_electronics_connection(self):
        self._compare_regulating_cond_eq(PowerElectronicsConnection)

        self.validator.validate_collection(
            PowerElectronicsConnection.phases,
            PowerElectronicsConnection.add_phase,
            PowerElectronicsConnection,
            lambda _: PowerElectronicsConnectionPhase(mrid="pecp1"),
            lambda _: PowerElectronicsConnectionPhase(mrid="pecp2")
        )
        self.validator.validate_collection(
            PowerElectronicsConnection.units,
            PowerElectronicsConnection.add_unit,
            PowerElectronicsConnection,
            lambda _: PowerElectronicsUnit(mrid="peu1"),
            lambda _: PowerElectronicsUnit(mrid="peu2")
        )
        self.validator.validate_property(PowerElectronicsConnection.max_i_fault, PowerElectronicsConnection, lambda _: 1, lambda _: 2)
        self.validator.validate_property(PowerElectronicsConnection.max_q, PowerElectronicsConnection, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(PowerElectronicsConnection.min_q, PowerElectronicsConnection, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(PowerElectronicsConnection.p, PowerElectronicsConnection, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(PowerElectronicsConnection.q, PowerElectronicsConnection, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(PowerElectronicsConnection.rated_s, PowerElectronicsConnection, lambda _: 1, lambda _: 2)
        self.validator.validate_property(PowerElectronicsConnection.rated_u, PowerElectronicsConnection, lambda _: 1, lambda _: 2)
        self.validator.validate_property(PowerElectronicsConnection.inverter_standard, PowerElectronicsConnection, lambda _: "first", lambda _: "second")
        self.validator.validate_property(PowerElectronicsConnection.sustain_op_overvolt_limit, PowerElectronicsConnection, lambda _: 1, lambda _: 2)
        self.validator.validate_property(PowerElectronicsConnection.stop_at_over_freq, PowerElectronicsConnection, lambda _: 51.1, lambda _: 51.2)
        self.validator.validate_property(PowerElectronicsConnection.stop_at_under_freq, PowerElectronicsConnection, lambda _: 47.1, lambda _: 47.2)
        self.validator.validate_property(PowerElectronicsConnection.inv_volt_watt_resp_mode, PowerElectronicsConnection, lambda _: False, lambda _: True)
        self.validator.validate_property(PowerElectronicsConnection.inv_watt_resp_v1, PowerElectronicsConnection, lambda _: 201, lambda _: 202)
        self.validator.validate_property(PowerElectronicsConnection.inv_watt_resp_v2, PowerElectronicsConnection, lambda _: 217, lambda _: 218)
        self.validator.validate_property(PowerElectronicsConnection.inv_watt_resp_v3, PowerElectronicsConnection, lambda _: 236, lambda _: 237)
        self.validator.validate_property(PowerElectronicsConnection.inv_watt_resp_v4, PowerElectronicsConnection, lambda _: 245, lambda _: 246)
        self.validator.validate_property(PowerElectronicsConnection.inv_watt_resp_p_at_v1, PowerElectronicsConnection, lambda _: 0.1, lambda _: 0.2)
        self.validator.validate_property(PowerElectronicsConnection.inv_watt_resp_p_at_v2, PowerElectronicsConnection, lambda _: 0.1, lambda _: 0.2)
        self.validator.validate_property(PowerElectronicsConnection.inv_watt_resp_p_at_v3, PowerElectronicsConnection, lambda _: 0.1, lambda _: 0.2)
        self.validator.validate_property(PowerElectronicsConnection.inv_watt_resp_p_at_v4, PowerElectronicsConnection, lambda _: 0.1, lambda _: 0.2)
        self.validator.validate_property(PowerElectronicsConnection.inv_volt_var_resp_mode, PowerElectronicsConnection, lambda _: False, lambda _: True)
        self.validator.validate_property(PowerElectronicsConnection.inv_var_resp_v1, PowerElectronicsConnection, lambda _: 201, lambda _: 202)
        self.validator.validate_property(PowerElectronicsConnection.inv_var_resp_v2, PowerElectronicsConnection, lambda _: 201, lambda _: 202)
        self.validator.validate_property(PowerElectronicsConnection.inv_var_resp_v3, PowerElectronicsConnection, lambda _: 201, lambda _: 202)
        self.validator.validate_property(PowerElectronicsConnection.inv_var_resp_v4, PowerElectronicsConnection, lambda _: 201, lambda _: 202)
        self.validator.validate_property(PowerElectronicsConnection.inv_var_resp_q_at_v1, PowerElectronicsConnection, lambda _: 0.1, lambda _: 0.2)
        self.validator.validate_property(PowerElectronicsConnection.inv_var_resp_q_at_v2, PowerElectronicsConnection, lambda _: 0.1, lambda _: 0.2)
        self.validator.validate_property(PowerElectronicsConnection.inv_var_resp_q_at_v3, PowerElectronicsConnection, lambda _: 0.1, lambda _: 0.2)
        self.validator.validate_property(PowerElectronicsConnection.inv_var_resp_q_at_v4, PowerElectronicsConnection, lambda _: -0.5, lambda _: -0.4)
        self.validator.validate_property(PowerElectronicsConnection.inv_reactive_power_mode, PowerElectronicsConnection, lambda _: False, lambda _: True)
        self.validator.validate_property(PowerElectronicsConnection.inv_fix_reactive_power, PowerElectronicsConnection, lambda _: 0.1, lambda _: 0.2)

    def test_compare_power_electronics_connection_phase(self):
        self._compare_power_system_resource(PowerElectronicsConnectionPhase)

        self.validator.validate_property(
            PowerElectronicsConnectionPhase.phase,
            PowerElectronicsConnectionPhase,
            lambda _: SinglePhaseKind.A,
            lambda _: SinglePhaseKind.B
        )
        self.validator.validate_property(
            PowerElectronicsConnectionPhase.power_electronics_connection,
            PowerElectronicsConnectionPhase,
            lambda _: PowerElectronicsConnection(mrid="pec1"),
            lambda _: PowerElectronicsConnection(mrid="pec2")
        )

    def test_compare_power_transformer(self):
        self._compare_conducting_equipment(PowerTransformer)

        self.validator.validate_property(PowerTransformer.vector_group, PowerTransformer, lambda _: VectorGroup.DYN11, lambda _: VectorGroup.D0)
        self.validator.validate_property(PowerTransformer.transformer_utilisation, PowerTransformer, lambda _: 0.1, lambda _: 0.9)
        self.validator.validate_property(PowerTransformer.construction_kind, PowerTransformer, lambda _: TransformerConstructionKind.subway,
                                         lambda _: TransformerConstructionKind.overhead)
        self.validator.validate_property(PowerTransformer.function, PowerTransformer, lambda _: TransformerFunctionKind.isolationTransformer,
                                         lambda _: TransformerFunctionKind.voltageRegulator)
        self.validator.validate_indexed_collection(
            PowerTransformer.ends,
            PowerTransformer.add_end,
            PowerTransformer,
            lambda _: PowerTransformerEnd(mrid="pte1"),
            lambda _: PowerTransformerEnd(mrid="pte2"),
        )

        self.validator.validate_property(
            PowerTransformer.asset_info,
            PowerTransformer,
            lambda _: PowerTransformerInfo(mrid="apti1"),
            lambda _: PowerTransformerInfo(mrid="apti2"),
            expected_differences={"power_transformer_info"}
        )

        self.validator.validate_property(
            PowerTransformer.power_transformer_info,
            PowerTransformer,
            lambda _: PowerTransformerInfo(mrid="pti1"),
            lambda _: PowerTransformerInfo(mrid="pti2"),
            expected_differences={"asset_info"}
        )

    def test_compare_power_transformer_end(self):
        self._compare_transformer_end(PowerTransformerEnd)

        self.validator.validate_property(
            PowerTransformerEnd.power_transformer,
            PowerTransformerEnd,
            lambda _: PowerTransformer(mrid="pt1"),
            lambda _: PowerTransformer(mrid="pt2")
        )
        self.validator.validate_property(PowerTransformerEnd.b, PowerTransformerEnd, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(PowerTransformerEnd.b0, PowerTransformerEnd, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(PowerTransformerEnd.connection_kind, PowerTransformerEnd, lambda _: WindingConnection.A, lambda _: WindingConnection.D)
        self.validator.validate_property(PowerTransformerEnd.g, PowerTransformerEnd, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(PowerTransformerEnd.g0, PowerTransformerEnd, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(PowerTransformerEnd.phase_angle_clock, PowerTransformerEnd, lambda _: 1, lambda _: 2)
        self.validator.validate_property(PowerTransformerEnd.r, PowerTransformerEnd, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(PowerTransformerEnd.r0, PowerTransformerEnd, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(PowerTransformerEnd.rated_s, PowerTransformerEnd, lambda _: 1, lambda _: 2, expected_differences={"s_ratings"})
        self.validator.validate_property(PowerTransformerEnd.rated_u, PowerTransformerEnd, lambda _: 1, lambda _: 2)
        self.validator.validate_property(PowerTransformerEnd.x, PowerTransformerEnd, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(PowerTransformerEnd.x0, PowerTransformerEnd, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(PowerTransformerEnd.r, PowerTransformerEnd, lambda _: 1.0, lambda _: float('nan'))
        self.validator.validate_property(PowerTransformerEnd.r0, PowerTransformerEnd, lambda _: 1.0, lambda _: float('nan'))
        self.validator.validate_property(PowerTransformerEnd.x, PowerTransformerEnd, lambda _: 1.0, lambda _: float('nan'))
        self.validator.validate_property(PowerTransformerEnd.x0, PowerTransformerEnd, lambda _: 1.0, lambda _: float('nan'))

        self.validator.validate_indexed_collection(
            PowerTransformerEnd.s_ratings,
            PowerTransformerEnd.add_transformer_end_rated_s,
            PowerTransformerEnd,
            lambda _: TransformerEndRatedS(TransformerCoolingType.UNKNOWN_COOLING_TYPE, 1),
            lambda _: TransformerEndRatedS(TransformerCoolingType.UNKNOWN_COOLING_TYPE, 2),
            expected_differences={"rated_s"}
        )

    def _compare_protected_switch(self, creator: Type[ProtectedSwitch]):
        self._compare_switch(creator)

        self.validator.validate_property(ProtectedSwitch.breaking_capacity, creator, lambda _: 1, lambda _: 2)
        self.validator.validate_collection(
            ProtectedSwitch.relay_functions,
            ProtectedSwitch.add_relay_function,
            creator,
            lambda _: CurrentRelay(mrid="cr1"),
            lambda _: CurrentRelay(mrid="cr2")
        )

    def test_compare_ratio_tap_changer(self):
        self._compare_tap_changer(RatioTapChanger)

        self.validator.validate_property(
            RatioTapChanger.transformer_end,
            RatioTapChanger,
            lambda _: PowerTransformerEnd(mrid="pte1"),
            lambda _: PowerTransformerEnd(mrid="pte2")
        )
        self.validator.validate_property(RatioTapChanger.step_voltage_increment, RatioTapChanger, lambda _: 1.0, lambda _: 2.0)

    def test_compare_recloser(self):
        self._compare_protected_switch(Recloser)

    def _compare_regulating_cond_eq(self, creator: Type[RegulatingCondEq]):
        self._compare_energy_connection(creator)

        self.validator.validate_property(RegulatingCondEq.control_enabled, creator, lambda _: False, lambda _: True)
        self.validator.validate_property(
            RegulatingCondEq.regulating_control,
            creator,
            lambda _: RegulatingControl(mrid="rc1"),
            lambda _: RegulatingControl(mrid="rc2")
        )

    def _compare_regulating_control(self, creator: Type[RegulatingControl]):
        self._compare_power_system_resource(creator)

        self.validator.validate_property(RegulatingControl.discrete, creator, lambda _: False, lambda _: True)
        self.validator.validate_property(
            RegulatingControl.mode, creator,
            lambda _: RegulatingControlModeKind.voltage,
            lambda _: RegulatingControlModeKind.currentFlow
        )
        self.validator.validate_property(RegulatingControl.monitored_phase, creator, lambda _: PhaseCode.ABC, lambda _: PhaseCode.ABCN)
        self.validator.validate_property(RegulatingControl.target_deadband, creator, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(RegulatingControl.target_value, creator, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(RegulatingControl.enabled, creator, lambda _: False, lambda _: True)
        self.validator.validate_property(RegulatingControl.max_allowed_target_value, creator, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(RegulatingControl.min_allowed_target_value, creator, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(RegulatingControl.rated_current, creator, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(RegulatingControl.terminal, creator, lambda _: Terminal(mrid="t1"), lambda _: Terminal(mrid="t2"))
        self.validator.validate_collection(
            RegulatingControl.regulating_conducting_equipment,
            RegulatingControl.add_regulating_cond_eq,
            creator,
            lambda _: RegulatingCondEq(mrid="rce1"),
            lambda _: RegulatingCondEq(mrid="rce2")
        )

    def test_compare_series_compensator(self):
        self._compare_conducting_equipment(SeriesCompensator)

        self.validator.validate_property(SeriesCompensator.r, SeriesCompensator, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(SeriesCompensator.r0, SeriesCompensator, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(SeriesCompensator.x, SeriesCompensator, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(SeriesCompensator.x0, SeriesCompensator, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(SeriesCompensator.varistor_rated_current, SeriesCompensator, lambda _: 1, lambda _: 2)
        self.validator.validate_property(SeriesCompensator.varistor_voltage_threshold, SeriesCompensator, lambda _: 1, lambda _: 2)

    def _compare_shunt_compensator(self, creator: Type[ShuntCompensator]):
        self._compare_regulating_cond_eq(creator)

        self.validator.validate_property(ShuntCompensator.grounded, creator, lambda _: False, lambda _: True)
        self.validator.validate_property(ShuntCompensator.nom_u, creator, lambda _: 1, lambda _: 2)
        self.validator.validate_property(
            ShuntCompensator.phase_connection,
            creator,
            lambda _: PhaseShuntConnectionKind.D,
            lambda _: PhaseShuntConnectionKind.G
        )
        self.validator.validate_property(ShuntCompensator.sections, creator, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(ShuntCompensator.asset_info, creator, lambda _: ShuntCompensatorInfo(mrid="asci1"),
                                         lambda _: ShuntCompensatorInfo(mrid="asci2"), expected_differences={"shunt_compensator_info"})
        self.validator.validate_property(ShuntCompensator.shunt_compensator_info, creator, lambda _: ShuntCompensatorInfo(mrid="sci1"),
                                         lambda _: ShuntCompensatorInfo(mrid="sci2"), expected_differences={"asset_info"})

    def _compare_switch(self, creator: Type[Switch]):
        self._compare_conducting_equipment(creator)

        self.validator.validate_property(Switch.rated_current, creator, lambda _: 1, lambda _: 2)
        self.validator.validate_property(Switch.asset_info, creator, lambda _: SwitchInfo(mrid="asi1"), lambda _: SwitchInfo(mrid="sai2"),
                                         expected_differences={"switch_info"})
        self.validator.validate_property(Switch.switch_info, creator, lambda _: SwitchInfo(mrid="si1"), lambda _: SwitchInfo(mrid="si2"),
                                         expected_differences={"asset_info"})

        closed_switch = Jumper(mrid="mRID")
        closed_switch.set_normally_open(False)
        closed_switch.set_open(True)

        open_switch = Jumper(mrid="mRID")
        open_switch.set_normally_open(True)
        open_switch.set_open(False)

        difference = ObjectDifference(closed_switch, open_switch)
        difference.differences["isNormallyOpen"] = ValueDifference(
            {p: False for p in PhaseCode.ABCN.single_phases},
            {p: True for p in PhaseCode.ABCN.single_phases}
        )

        difference.differences["isOpen"] = ValueDifference(
            {p: True for p in PhaseCode.ABCN.single_phases},
            {p: False for p in PhaseCode.ABCN.single_phases}
        )

        self.validator.validate_compare(closed_switch, open_switch, expect_modification=difference)

    def _compare_tap_changer(self, creator: Type[TapChanger]):
        self._compare_power_system_resource(creator)

        self.validator.validate_property(TapChanger.control_enabled, creator, lambda _: True, lambda _: False)
        self.validator.validate_property(TapChanger.high_step, creator, lambda _: 1, lambda _: 2)
        self.validator.validate_property(TapChanger.low_step, creator, lambda _: -1, lambda _: 0)
        self.validator.validate_property(TapChanger.neutral_step, creator, lambda _: 0, lambda _: 1)
        self.validator.validate_property(TapChanger.neutral_u, creator, lambda _: 0, lambda _: 1)
        self.validator.validate_property(TapChanger.normal_step, creator, lambda _: 0, lambda _: 1)
        self.validator.validate_property(TapChanger.step, creator, lambda _: 0, lambda _: 1)
        self.validator.validate_property(TapChanger.tap_changer_control, creator, lambda _: TapChangerControl(mrid="tcc1"), lambda _: TapChangerControl(mrid="tcc2"))

    def test_compare_tap_changer_control(self):
        self._compare_regulating_control(TapChangerControl)

        self.validator.validate_property(TapChangerControl.limit_voltage, TapChangerControl, lambda _: 1, lambda _: 2)
        self.validator.validate_property(TapChangerControl.line_drop_compensation, TapChangerControl, lambda _: False, lambda _: True)
        self.validator.validate_property(TapChangerControl.line_drop_r, TapChangerControl, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(TapChangerControl.line_drop_x, TapChangerControl, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(TapChangerControl.reverse_line_drop_r, TapChangerControl, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(TapChangerControl.reverse_line_drop_x, TapChangerControl, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(TapChangerControl.forward_ldc_blocking, TapChangerControl, lambda _: False, lambda _: True)
        self.validator.validate_property(TapChangerControl.time_delay, TapChangerControl, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(TapChangerControl.co_generation_enabled, TapChangerControl, lambda _: False, lambda _: True)

    def _compare_transformer_end(self, creator: Type[TransformerEnd]):
        self._compare_identified_object(creator)

        self.validator.validate_property(TransformerEnd.grounded, creator, lambda _: True, lambda _: False)
        self.validator.validate_property(TransformerEnd.r_ground, creator, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(TransformerEnd.x_ground, creator, lambda _: 1.0, lambda _: 2.0)
        self.validator.validate_property(TransformerEnd.base_voltage, creator, lambda _: BaseVoltage(mrid="bv1"), lambda _: BaseVoltage(mrid="b21"))
        self.validator.validate_property(
            TransformerEnd.ratio_tap_changer,
            creator,
            lambda _: RatioTapChanger(mrid="rtc1"),
            lambda _: RatioTapChanger(mrid="rtc2")
        )
        self.validator.validate_property(TransformerEnd.terminal, creator, lambda _: Terminal(mrid="t1", conducting_equipment=PowerTransformer(mrid="t1-pt1")),
                                         lambda _: Terminal(mrid="t2", conducting_equipment=PowerTransformer(mrid="t2-pt2")))
        self.validator.validate_property(
            TransformerEnd.star_impedance,
            creator,
            lambda _: TransformerStarImpedance(mrid="tsi1"),
            lambda _: TransformerStarImpedance(mrid="tsi2")
        )

    ####################################################
    # IEC61970 INFIEC61970 WIRES GENERATION PRODUCTION #
    ####################################################

    def test_compare_ev_charging_unit(self):
        self._compare_power_electronics_unit(EvChargingUnit)

    ###############################
    # IEC61970 INFIEC61970 FEEDER #
    ###############################

    def test_compare_circuit(self):
        self._compare_line(Circuit)

        self.validator.validate_property(Circuit.loop, Circuit, lambda _: Loop(mrid="l1"), lambda _: Loop(mrid="l2"))
        self.validator.validate_collection(
            Circuit.end_terminals,
            Circuit.add_end_terminal,
            Circuit,
            lambda _: Terminal(mrid="t1"),
            lambda _: Terminal(mrid="t2")
        )
        self.validator.validate_collection(
            Circuit.end_substations,
            Circuit.add_end_substation,
            Circuit,
            lambda _: Substation(mrid="s1"),
            lambda _: Substation(mrid="s2")
        )

    def test_compare_loop(self):
        self._compare_identified_object(Loop)

        self.validator.validate_collection(Loop.circuits, Loop.add_circuit, Loop, lambda _: Circuit(mrid="c1"), lambda _: Circuit(mrid="c2"))
        self.validator.validate_collection(Loop.substations, Loop.add_substation, Loop, lambda _: Substation(mrid="s1"), lambda _: Substation(mrid="s2"))
        self.validator.validate_collection(
            Loop.energizing_substations,
            Loop.add_energizing_substation,
            Loop,
            lambda _: Substation(mrid="s1"),
            lambda _: Substation(mrid="s2")
        )

    def test_compare_lv_feeder(self):
        self._compare_equipment_container(LvFeeder)

        self.validator.validate_property(LvFeeder.normal_head_terminal, LvFeeder, lambda _: Terminal(mrid="t1"), lambda _: Terminal(mrid="t2"))
        self.validator.validate_collection(
            LvFeeder.normal_energizing_feeders,
            LvFeeder.add_normal_energizing_feeder,
            LvFeeder,
            lambda _: Feeder(mrid="f1"),
            lambda _: Feeder(mrid="f2")
        )
        self.validator.validate_collection(
            LvFeeder.current_equipment,
            LvFeeder.add_current_equipment,
            LvFeeder,
            lambda _: Junction(mrid="j1"),
            lambda _: Junction(mrid="j2")
        )
