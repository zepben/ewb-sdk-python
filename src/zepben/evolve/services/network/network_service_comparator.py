#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass
from typing import Callable, Optional, Any

from zepben.evolve.model.cim.iec61968.assetinfo.no_load_test import NoLoadTest
from zepben.evolve.model.cim.iec61968.assetinfo.open_circuit_test import OpenCircuitTest
from zepben.evolve.model.cim.iec61968.assetinfo.power_transformer_info import PowerTransformerInfo
from zepben.evolve.model.cim.iec61968.assetinfo.short_circuit_test import ShortCircuitTest
from zepben.evolve.model.cim.iec61968.assetinfo.shunt_compensator_info import ShuntCompensatorInfo
from zepben.evolve.model.cim.iec61968.assetinfo.switch_info import SwitchInfo
from zepben.evolve.model.cim.iec61968.assetinfo.transformer_end_info import TransformerEndInfo
from zepben.evolve.model.cim.iec61968.assetinfo.transformer_tank_info import TransformerTankInfo
from zepben.evolve.model.cim.iec61968.assetinfo.transformer_test import TransformerTest
from zepben.evolve.model.cim.iec61968.assetinfo.wire_info import CableInfo, OverheadWireInfo, WireInfo
from zepben.evolve.model.cim.iec61968.assets.asset import Asset
from zepben.evolve.model.cim.iec61968.assets.asset_organisation_role import AssetOwner
from zepben.evolve.model.cim.iec61968.assets.pole import Pole
from zepben.evolve.model.cim.iec61968.assets.streetlight import Streetlight
from zepben.evolve.model.cim.iec61968.common.location import Location
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.current_transformer_info import CurrentTransformerInfo
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.potential_transformer_info import PotentialTransformerInfo
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.relay_info import RelayInfo
from zepben.evolve.model.cim.iec61968.metering.metering import EndDevice, Meter, UsagePoint
from zepben.evolve.model.cim.iec61968.operations.operational_restriction import OperationalRestriction
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.auxiliary_equipment import AuxiliaryEquipment, FaultIndicator
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.current_transformer import CurrentTransformer
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.potential_transformer import PotentialTransformer
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.sensor import Sensor
from zepben.evolve.model.cim.iec61970.base.core.base_voltage import BaseVoltage
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.connectivity_node import ConnectivityNode
from zepben.evolve.model.cim.iec61970.base.core.curve import Curve
from zepben.evolve.model.cim.iec61970.base.core.equipment import Equipment
from zepben.evolve.model.cim.iec61970.base.core.equipment_container import EquipmentContainer, Feeder, Site
from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.evolve.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.evolve.model.cim.iec61970.base.core.regions import GeographicalRegion, SubGeographicalRegion
from zepben.evolve.model.cim.iec61970.base.core.substation import Substation
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.equivalents.equivalent_branch import EquivalentBranch
from zepben.evolve.model.cim.iec61970.base.meas.control import Control
from zepben.evolve.model.cim.iec61970.base.meas.measurement import Accumulator, Analog, Discrete, Measurement
from zepben.evolve.model.cim.iec61970.base.protection.current_relay import CurrentRelay
from zepben.evolve.model.cim.iec61970.base.protection.distance_relay import DistanceRelay
from zepben.evolve.model.cim.iec61970.base.protection.protection_relay_function import ProtectionRelayFunction
from zepben.evolve.model.cim.iec61970.base.protection.protection_relay_scheme import ProtectionRelayScheme
from zepben.evolve.model.cim.iec61970.base.protection.protection_relay_system import ProtectionRelaySystem
from zepben.evolve.model.cim.iec61970.base.protection.voltage_relay import VoltageRelay
from zepben.evolve.model.cim.iec61970.base.scada.remote_control import RemoteControl
from zepben.evolve.model.cim.iec61970.base.scada.remote_source import RemoteSource
from zepben.evolve.model.cim.iec61970.base.wires.aclinesegment import AcLineSegment, Conductor
from zepben.evolve.model.cim.iec61970.base.wires.breaker import Breaker
from zepben.evolve.model.cim.iec61970.base.wires.connectors import BusbarSection, Junction
from zepben.evolve.model.cim.iec61970.base.wires.disconnector import Disconnector
from zepben.evolve.model.cim.iec61970.base.wires.earth_fault_compensator import EarthFaultCompensator
from zepben.evolve.model.cim.iec61970.base.wires.energy_connection import RegulatingCondEq
from zepben.evolve.model.cim.iec61970.base.wires.energy_consumer import EnergyConsumer, EnergyConsumerPhase
from zepben.evolve.model.cim.iec61970.base.wires.energy_source import EnergySource
from zepben.evolve.model.cim.iec61970.base.wires.energy_source_phase import EnergySourcePhase
from zepben.evolve.model.cim.iec61970.base.wires.fuse import Fuse
from zepben.evolve.model.cim.iec61970.base.wires.generation.production.power_electronics_unit import BatteryUnit, PhotoVoltaicUnit, PowerElectronicsUnit, \
    PowerElectronicsWindUnit
from zepben.evolve.model.cim.iec61970.base.wires.ground import Ground
from zepben.evolve.model.cim.iec61970.base.wires.ground_disconnector import GroundDisconnector
from zepben.evolve.model.cim.iec61970.base.wires.grounding_impedance import GroundingImpedance
from zepben.evolve.model.cim.iec61970.base.wires.jumper import Jumper
from zepben.evolve.model.cim.iec61970.base.wires.load_break_switch import LoadBreakSwitch
from zepben.evolve.model.cim.iec61970.base.wires.per_length import PerLengthSequenceImpedance
from zepben.evolve.model.cim.iec61970.base.wires.petersen_coil import PetersenCoil
from zepben.evolve.model.cim.iec61970.base.wires.power_electronics_connection import PowerElectronicsConnection, PowerElectronicsConnectionPhase
from zepben.evolve.model.cim.iec61970.base.wires.power_transformer import PowerTransformer, PowerTransformerEnd, RatioTapChanger, TapChanger, TransformerEnd
from zepben.evolve.model.cim.iec61970.base.wires.protected_switch import ProtectedSwitch
from zepben.evolve.model.cim.iec61970.base.wires.reactive_capability_curve import ReactiveCapabilityCurve
from zepben.evolve.model.cim.iec61970.base.wires.recloser import Recloser
from zepben.evolve.model.cim.iec61970.base.wires.regulating_control import RegulatingControl
from zepben.evolve.model.cim.iec61970.base.wires.rotating_machine import RotatingMachine
from zepben.evolve.model.cim.iec61970.base.wires.series_compensator import SeriesCompensator
from zepben.evolve.model.cim.iec61970.base.wires.shunt_compensator import LinearShuntCompensator, ShuntCompensator
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.model.cim.iec61970.base.wires.switch import Switch
from zepben.evolve.model.cim.iec61970.base.wires.synchronous_machine import SynchronousMachine
from zepben.evolve.model.cim.iec61970.base.wires.tap_changer_control import TapChangerControl
from zepben.evolve.model.cim.iec61970.base.wires.transformer_star_impedance import TransformerStarImpedance
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.circuit import Circuit
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.loop import Loop
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.lv_feeder import LvFeeder
from zepben.evolve.model.cim.iec61970.infiec61970.wires.generation.production.ev_charging_unit import EvChargingUnit
from zepben.evolve.services.common.base_service_comparator import BaseServiceComparator
from zepben.evolve.services.common.difference import ValueDifference
from zepben.evolve.services.common.translator.service_differences import ObjectDifference


@dataclass
class NetworkServiceComparatorOptions:
    compare_terminals: bool = True
    compare_traced_phases: bool = True
    compare_feeder_equipment: bool = True
    compare_equipment_containers: bool = True
    compare_lv_simplification: bool = True


#
# NOTE: The functions below are accessed by reflection rather than directly. Make sure you check the code coverage
#       to ensure they are covered correctly.
#

class NetworkServiceComparator(BaseServiceComparator):
    """
    Compare the objects supported by the network service.
    """

    def __init__(self, options: NetworkServiceComparatorOptions = NetworkServiceComparatorOptions()):
        """

        :param options: Indicates which optional checks to perform.
        """
        super().__init__()
        self._options = options

    #######################
    # IEC61968 ASSET INFO #
    #######################

    def _compare_cable_info(self, source: CableInfo, target: CableInfo) -> ObjectDifference:
        return self._compare_wire_info(ObjectDifference(source, target))

    def _compare_no_load_test(self, source: NoLoadTest, target: NoLoadTest) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(diff, NoLoadTest.energised_end_voltage, NoLoadTest.loss, NoLoadTest.loss_zero)
        self._compare_floats(diff, NoLoadTest.exciting_current, NoLoadTest.exciting_current_zero)

        return self._compare_transformer_test(diff)

    def _compare_open_circuit_test(self, source: OpenCircuitTest, target: OpenCircuitTest) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(
            diff,
            OpenCircuitTest.energised_end_step,
            OpenCircuitTest.energised_end_voltage,
            OpenCircuitTest.open_end_step,
            OpenCircuitTest.open_end_voltage
        )
        self._compare_floats(diff, OpenCircuitTest.phase_shift)

        return self._compare_transformer_test(diff)

    def _compare_overhead_wire_info(self, source: OverheadWireInfo, target: OverheadWireInfo) -> ObjectDifference:
        return self._compare_wire_info(ObjectDifference(source, target))

    def _compare_power_transformer_info(self, source: PowerTransformerInfo, target: PowerTransformerInfo) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_reference_collections(diff, PowerTransformerInfo.transformer_tank_infos)

        return self._compare_asset_info(diff)

    def _compare_short_circuit_test(self, source: ShortCircuitTest, target: ShortCircuitTest) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(
            diff,
            ShortCircuitTest.energised_end_step,
            ShortCircuitTest.grounded_end_step,
            ShortCircuitTest.loss,
            ShortCircuitTest.loss_zero,
            ShortCircuitTest.power
        )
        self._compare_floats(
            diff,
            ShortCircuitTest.current,
            ShortCircuitTest.leakage_impedance,
            ShortCircuitTest.leakage_impedance_zero,
            ShortCircuitTest.voltage,
            ShortCircuitTest.voltage_ohmic_part
        )
        return self._compare_transformer_test(diff)

    def _compare_shunt_compensator_info(self, source: ShuntCompensatorInfo, target: ShuntCompensatorInfo) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(
            diff,
            ShuntCompensatorInfo.max_power_loss,
            ShuntCompensatorInfo.rated_current,
            ShuntCompensatorInfo.rated_reactive_power,
            ShuntCompensatorInfo.rated_voltage,
        )

        return self._compare_asset_info(diff)

    def _compare_switch_info(self, source: SwitchInfo, target: SwitchInfo) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_floats(diff, SwitchInfo.rated_interrupting_time)

        return self._compare_asset_info(diff)

    def _compare_transformer_end_info(self, source: TransformerEndInfo, target: TransformerEndInfo) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_references(
            diff,
            TransformerEndInfo.transformer_star_impedance,
            TransformerEndInfo.energised_end_no_load_tests,
            TransformerEndInfo.energised_end_short_circuit_tests,
            TransformerEndInfo.grounded_end_short_circuit_tests,
            TransformerEndInfo.open_end_open_circuit_tests,
            TransformerEndInfo.energised_end_open_circuit_tests
        )
        self._compare_values(
            diff,
            TransformerEndInfo.connection_kind,
            TransformerEndInfo.emergency_s,
            TransformerEndInfo.end_number,
            TransformerEndInfo.insulation_u,
            TransformerEndInfo.phase_angle_clock,
            TransformerEndInfo.rated_s,
            TransformerEndInfo.rated_u,
            TransformerEndInfo.short_term_s
        )
        self._compare_floats(diff, TransformerEndInfo.r)

        return self._compare_asset_info(diff)

    def _compare_transformer_tank_info(self, source: TransformerTankInfo, target: TransformerTankInfo) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_reference_collections(diff, TransformerTankInfo.transformer_end_infos)

        return self._compare_asset_info(diff)

    def _compare_transformer_test(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_values(diff, TransformerTest.base_power)
        self._compare_floats(diff, TransformerTest.temperature)

        return self._compare_identified_object(diff)

    def _compare_wire_info(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_values(diff, WireInfo.rated_current, WireInfo.material)

        return self._compare_asset_info(diff)

    ###################
    # IEC61968 ASSETS #
    ###################

    def _compare_asset(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_id_references(diff, Asset.location)
        self._compare_id_reference_collections(diff, Asset.organisation_roles)

        return self._compare_identified_object(diff)

    def _compare_asset_container(self, diff: ObjectDifference) -> ObjectDifference:
        return self._compare_asset(diff)

    def _compare_asset_info(self, diff: ObjectDifference) -> ObjectDifference:
        return self._compare_identified_object(diff)

    def _compare_asset_organisation_role(self, diff: ObjectDifference) -> ObjectDifference:
        return self._compare_organisation_role(diff)

    def _compare_asset_owner(self, source: AssetOwner, target: AssetOwner) -> ObjectDifference:
        return self._compare_asset_organisation_role(ObjectDifference(source, target))

    def _compare_pole(self, source: Pole, target: Pole) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(diff, Pole.classification)
        self._compare_id_reference_collections(diff, Pole.streetlights)

        return self._compare_structure(diff)

    def _compare_streetlight(self, source: Streetlight, target: Streetlight) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(diff, Streetlight.light_rating, Streetlight.lamp_kind)
        self._compare_id_references(diff, Streetlight.pole)

        return self._compare_asset(diff)

    def _compare_structure(self, diff: ObjectDifference) -> ObjectDifference:
        return self._compare_asset_container(diff)

    ###################
    # IEC61968 COMMON #
    ###################

    def _compare_location(self, source: Location, target: Location) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(diff, Location.main_address)
        self._compare_indexed_value_collections(diff, Location.points)

        return self._compare_identified_object(diff)

    #####################################
    # IEC61968 infIEC61968 InfAssetInfo #
    #####################################

    def _compare_relay_info(self, source: RelayInfo, target: RelayInfo) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(diff, RelayInfo.curve_setting, RelayInfo.reclose_fast)
        self._compare_indexed_value_collections(diff, RelayInfo.reclose_delays)

        return self._compare_asset_info(diff)

    def _compare_current_transformer_info(self, source: CurrentTransformerInfo, target: CurrentTransformerInfo) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(
            diff,
            CurrentTransformerInfo.accuracy_class,
            CurrentTransformerInfo.core_count,
            CurrentTransformerInfo.ct_class,
            CurrentTransformerInfo.knee_point_voltage,
            CurrentTransformerInfo.max_ratio,
            CurrentTransformerInfo.nominal_ratio,
            CurrentTransformerInfo.rated_current,
            CurrentTransformerInfo.secondary_fls_rating,
            CurrentTransformerInfo.usage
        )
        self._compare_floats(
            diff,
            CurrentTransformerInfo.accuracy_limit,
            CurrentTransformerInfo.primary_ratio,
            CurrentTransformerInfo.secondary_ratio
        )

        return self._compare_asset_info(diff)

    def _compare_potential_transformer_info(self, source: PotentialTransformerInfo, target: PotentialTransformerInfo) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(
            diff,
            PotentialTransformerInfo.accuracy_class,
            PotentialTransformerInfo.nominal_ratio,
            PotentialTransformerInfo.pt_class,
            PotentialTransformerInfo.rated_voltage,
        )
        self._compare_floats(
            diff,
            PotentialTransformerInfo.primary_ratio,
            PotentialTransformerInfo.secondary_ratio
        )

        return self._compare_asset_info(diff)

    #####################
    # IEC61968 METERING #
    #####################

    def _compare_end_device(self, diff: ObjectDifference) -> ObjectDifference:
        if self._options.compare_lv_simplification:
            self._compare_id_reference_collections(diff, EndDevice.usage_points)

        self._compare_values(diff, EndDevice.customer_mrid)
        self._compare_id_references(diff, EndDevice.service_location)

        return self._compare_asset_container(diff)

    def _compare_meter(self, source: Meter, target: Meter) -> ObjectDifference:
        return self._compare_end_device(ObjectDifference(source, target))

    def _compare_usage_point(self, source: UsagePoint, target: UsagePoint) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_references(diff, UsagePoint.usage_point_location)
        self._compare_values(
            diff,
            UsagePoint.is_virtual,
            UsagePoint.connection_category,
            UsagePoint.rated_power,
            UsagePoint.approved_inverter_capacity,
            UsagePoint.phase_code
        )
        if self._options.compare_lv_simplification:
            self._compare_id_reference_collections(diff, UsagePoint.equipment)
            self._compare_id_reference_collections(diff, UsagePoint.end_devices)

        return self._compare_identified_object(diff)

    #######################
    # IEC61968 OPERATIONS #
    #######################

    def _compare_operational_restriction(self, source: OperationalRestriction, target: OperationalRestriction) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_reference_collections(diff, OperationalRestriction.equipment)

        return self._compare_document(diff)

    #####################################
    # IEC61970 BASE AUXILIARY EQUIPMENT #
    #####################################

    def _compare_auxiliary_equipment(self, diff: ObjectDifference) -> ObjectDifference:
        if self._options.compare_terminals:
            self._compare_id_references(diff, AuxiliaryEquipment.terminal)

        return self._compare_equipment(diff)

    def _compare_current_transformer(self, source: CurrentTransformer, target: CurrentTransformer) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(diff, CurrentTransformer.core_burden)
        self._compare_id_references(diff, CurrentTransformer.current_transformer_info)

        return self._compare_sensor(diff)

    def _compare_fault_indicator(self, source: FaultIndicator, target: FaultIndicator) -> ObjectDifference:
        return self._compare_auxiliary_equipment(ObjectDifference(source, target))

    def _compare_potential_transformer(self, source: PotentialTransformer, target: PotentialTransformer) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(diff, PotentialTransformer.type)
        self._compare_id_references(diff, PotentialTransformer.potential_transformer_info)

        return self._compare_sensor(diff)

    def _compare_sensor(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_id_reference_collections(diff, Sensor.relay_functions)

        return self._compare_auxiliary_equipment(diff)

    ######################
    # IEC61970 BASE CORE #
    ######################

    def _compare_ac_dc_terminal(self, diff: ObjectDifference) -> ObjectDifference:
        return self._compare_identified_object(diff)

    def _compare_base_voltage(self, source: BaseVoltage, target: BaseVoltage) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(diff, BaseVoltage.nominal_voltage)

        return self._compare_identified_object(diff)

    def _compare_conducting_equipment(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_id_references(diff, ConductingEquipment.base_voltage)

        if self._options.compare_terminals:
            self._compare_indexed_id_reference_collections(diff, ConductingEquipment.terminals)

        return self._compare_equipment(diff)

    def _compare_connectivity_node(self, source: ConnectivityNode, target: ConnectivityNode) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_reference_collections(diff, ConnectivityNode.terminals)

        return self._compare_identified_object(diff)

    def _compare_connectivity_node_container(self, diff: ObjectDifference) -> ObjectDifference:
        return self._compare_power_system_resource(diff)

    def _compare_curve(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_indexed_value_collections(diff, Curve.data)

        return self._compare_identified_object(diff)

    def _compare_equipment(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_values(diff, Equipment.in_service, Equipment.normally_in_service, Equipment.commissioned_date)

        if self._options.compare_equipment_containers:
            self._compare_id_reference_collections(diff, Equipment.containers, Equipment.current_containers)

        if self._options.compare_lv_simplification:
            self._compare_id_reference_collections(diff, Equipment.usage_points)

        self._compare_id_reference_collections(diff, Equipment.operational_restrictions)

        return self._compare_power_system_resource(diff)

    def _compare_equipment_container(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_id_reference_collections(diff, EquipmentContainer.equipment)

        return self._compare_connectivity_node_container(diff)

    def _compare_feeder(self, source: Feeder, target: Feeder) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_references(diff, Feeder.normal_head_terminal, Feeder.normal_energizing_substation)
        self._compare_id_reference_collections(diff, Feeder.normal_energized_lv_feeders)
        if self._options.compare_feeder_equipment:
            self._compare_id_reference_collections(diff, Feeder.current_equipment)

        return self._compare_equipment_container(diff)

    def _compare_geographical_region(self, source: GeographicalRegion, target: GeographicalRegion) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_reference_collections(diff, GeographicalRegion.sub_geographical_regions)

        return self._compare_identified_object(diff)

    def _compare_power_system_resource(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_id_references(diff, PowerSystemResource.asset_info, PowerSystemResource.location)

        return self._compare_identified_object(diff)

    def _compare_site(self, source: Site, target: Site) -> ObjectDifference:
        return self._compare_equipment_container(ObjectDifference(source, target))

    def _compare_sub_geographical_region(self, source: SubGeographicalRegion, target: SubGeographicalRegion) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_references(diff, SubGeographicalRegion.geographical_region)
        self._compare_id_reference_collections(diff, SubGeographicalRegion.substations)

        return self._compare_identified_object(diff)

    def _compare_substation(self, source: Substation, target: Substation) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_references(diff, Substation.sub_geographical_region)
        self._compare_id_reference_collections(diff, Substation.feeders)

        return self._compare_equipment_container(diff)

    def _compare_terminal(self, source: Terminal, target: Terminal) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_references(diff, Terminal.conducting_equipment, Terminal.connectivity_node)
        self._compare_values(
            diff,
            Terminal.phases,
            Terminal.sequence_number,
            Terminal.normal_feeder_direction,
            Terminal.current_feeder_direction,
            Terminal.traced_phases
        )

        return self._compare_ac_dc_terminal(diff)

    #############################
    # IEC61970 BASE EQUIVALENTS #
    #############################

    def _compare_equivalent_branch(self, source: EquivalentBranch, target: EquivalentBranch) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_floats(
            diff,
            EquivalentBranch.negative_r12,
            EquivalentBranch.negative_r21,
            EquivalentBranch.negative_x12,
            EquivalentBranch.negative_x21,
            EquivalentBranch.positive_r12,
            EquivalentBranch.positive_r21,
            EquivalentBranch.positive_x12,
            EquivalentBranch.positive_x21,
            EquivalentBranch.r,
            EquivalentBranch.r21,
            EquivalentBranch.x,
            EquivalentBranch.x21,
            EquivalentBranch.zero_r12,
            EquivalentBranch.zero_r21,
            EquivalentBranch.zero_x12,
            EquivalentBranch.zero_x21
        )

        return self._compare_equivalent_equipment(diff)

    def _compare_equivalent_equipment(self, diff: ObjectDifference) -> ObjectDifference:
        return self._compare_conducting_equipment(diff)

    ######################
    # IEC61970 BASE MEAS #
    ######################

    def _compare_accumulator(self, source: Accumulator, target: Accumulator) -> ObjectDifference:
        return self._compare_measurement(ObjectDifference(source, target))

    def _compare_analog(self, source: Analog, target: Analog) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(diff, Analog.positive_flow_in)

        return self._compare_measurement(diff)

    def _compare_control(self, source: Control, target: Control) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(diff, Control.power_system_resource_mrid)
        self._compare_id_references(diff, Control.remote_control)

        return self._compare_io_point(diff)

    def _compare_discrete(self, source: Discrete, target: Discrete) -> ObjectDifference:
        return self._compare_measurement(ObjectDifference(source, target))

    def _compare_io_point(self, diff: ObjectDifference) -> ObjectDifference:
        return self._compare_identified_object(diff)

    def _compare_measurement(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_values(diff, Measurement.power_system_resource_mrid, Measurement.unit_symbol, Measurement.phases, Measurement.terminal_mrid)
        self._compare_id_references(diff, Measurement.remote_source)

        return self._compare_identified_object(diff)

    ############################
    # IEC61970 Base Protection #
    ############################

    def _compare_current_relay(self, source: CurrentRelay, target: CurrentRelay) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(diff, CurrentRelay.inverse_time_flag)
        self._compare_floats(diff, CurrentRelay.current_limit_1, CurrentRelay.time_delay_1)

        return self._compare_protection_relay_function(diff)

    def _compare_distance_relay(self, source: DistanceRelay, target: DistanceRelay) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_floats(
            diff,
            DistanceRelay.backward_blind,
            DistanceRelay.backward_reach,
            DistanceRelay.backward_reactance,
            DistanceRelay.forward_blind,
            DistanceRelay.forward_reach,
            DistanceRelay.forward_reactance,
            DistanceRelay.operation_phase_angle1,
            DistanceRelay.operation_phase_angle2,
            DistanceRelay.operation_phase_angle3,
        )

        return self._compare_protection_relay_function(diff)

    def _compare_voltage_relay(self, source: VoltageRelay, target: VoltageRelay) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        return self._compare_protection_relay_function(diff)

    def _compare_protection_relay_function(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_values(
            diff,
            ProtectionRelayFunction.model,
            ProtectionRelayFunction.reclosing,
            ProtectionRelayFunction.protection_kind,
            ProtectionRelayFunction.directable,
            ProtectionRelayFunction.power_direction
        )
        self._compare_floats(diff, ProtectionRelayFunction.relay_delay_time)
        self._compare_indexed_value_collections(
            diff,
            ProtectionRelayFunction.time_limits,
            ProtectionRelayFunction.thresholds
        )
        self._compare_id_reference_collections(
            diff,
            ProtectionRelayFunction.protected_switches,
            ProtectionRelayFunction.sensors,
            ProtectionRelayFunction.schemes,
        )
        self._compare_id_references(diff, ProtectionRelayFunction.relay_info)

        return self._compare_power_system_resource(diff)

    def _compare_protection_relay_scheme(self, source: ProtectionRelayScheme, target: ProtectionRelayScheme) -> ObjectDifference:
        diff = ObjectDifference(source, target)
        self._compare_id_references(diff, ProtectionRelayScheme.system)
        self._compare_id_reference_collections(diff, ProtectionRelayScheme.functions)

        return self._compare_identified_object(diff)

    def _compare_protection_relay_system(self, source: ProtectionRelaySystem, target: ProtectionRelaySystem) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(diff, ProtectionRelaySystem.protection_kind)
        self._compare_id_reference_collections(diff, ProtectionRelaySystem.schemes)

        return self._compare_equipment(diff)

    #######################
    # IEC61970 BASE SCADA #
    #######################

    def _compare_remote_control(self, source: RemoteControl, target: RemoteControl) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_references(diff, RemoteControl.control)

        return self._compare_remote_point(diff)

    def _compare_remote_point(self, diff: ObjectDifference) -> ObjectDifference:
        return self._compare_identified_object(diff)

    def _compare_remote_source(self, source: RemoteSource, target: RemoteSource) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_references(diff, RemoteSource.measurement)

        return self._compare_remote_point(diff)

    #############################################
    # IEC61970 BASE WIRES GENERATION PRODUCTION #
    #############################################

    def _compare_battery_unit(self, source: BatteryUnit, target: BatteryUnit) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(diff, BatteryUnit.battery_state, BatteryUnit.rated_e, BatteryUnit.stored_e)

        return self._compare_power_electronics_unit(diff)

    def _compare_photo_voltaic_unit(self, source: PhotoVoltaicUnit, target: PhotoVoltaicUnit) -> ObjectDifference:
        return self._compare_power_electronics_unit(ObjectDifference(source, target))

    def _compare_power_electronics_unit(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_id_references(diff, PowerElectronicsUnit.power_electronics_connection)
        self._compare_values(diff, PowerElectronicsUnit.max_p, PowerElectronicsUnit.min_p)

        return self._compare_equipment(diff)

    def _compare_power_electronics_wind_unit(self, source: PowerElectronicsWindUnit, target: PowerElectronicsWindUnit) -> ObjectDifference:
        return self._compare_power_electronics_unit(ObjectDifference(source, target))

    #######################
    # IEC61970 BASE WIRES #
    #######################

    def _compare_ac_line_segment(self, source: AcLineSegment, target: AcLineSegment) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_references(diff, AcLineSegment.per_length_sequence_impedance)

        return self._compare_conductor(diff)

    def _compare_breaker(self, source: Breaker, target: Breaker) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_floats(diff, Breaker.in_transit_time)

        return self._compare_protected_switch(diff)

    def _compare_busbar_section(self, source: BusbarSection, target: BusbarSection) -> ObjectDifference:
        return self._compare_connector(ObjectDifference(source, target))

    def _compare_conductor(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_floats(diff, Conductor.length, Conductor.design_rating)
        self._compare_values(diff, Conductor.design_temperature)
        self._compare_id_references(diff, Conductor.wire_info)

        return self._compare_conducting_equipment(diff)

    def _compare_connector(self, diff: ObjectDifference) -> ObjectDifference:
        return self._compare_conducting_equipment(diff)

    def _compare_disconnector(self, source: Disconnector, target: Disconnector) -> ObjectDifference:
        return self._compare_switch(ObjectDifference(source, target))

    def _compare_earth_fault_compensator(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_floats(diff, EarthFaultCompensator.r)

        return self._compare_conducting_equipment(diff)

    def _compare_energy_connection(self, diff: ObjectDifference) -> ObjectDifference:
        return self._compare_conducting_equipment(diff)

    def _compare_energy_consumer(self, source: EnergyConsumer, target: EnergyConsumer) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_reference_collections(diff, EnergyConsumer.phases)
        self._compare_values(diff, EnergyConsumer.customer_count, EnergyConsumer.grounded, EnergyConsumer.phase_connection)
        self._compare_floats(diff, EnergyConsumer.p, EnergyConsumer.p_fixed, EnergyConsumer.q, EnergyConsumer.q_fixed)

        return self._compare_energy_connection(diff)

    def _compare_energy_consumer_phase(self, source: EnergyConsumerPhase, target: EnergyConsumerPhase) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_references(diff, EnergyConsumerPhase.energy_consumer)
        self._compare_values(diff, EnergyConsumerPhase.phase)
        self._compare_floats(diff, EnergyConsumerPhase.p, EnergyConsumerPhase.p_fixed, EnergyConsumerPhase.q, EnergyConsumerPhase.q_fixed)

        return self._compare_power_system_resource(diff)

    def _compare_energy_source(self, source: EnergySource, target: EnergySource) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_reference_collections(diff, EnergySource.phases)
        self._compare_floats(
            diff,
            EnergySource.active_power,
            EnergySource.reactive_power,
            EnergySource.voltage_angle,
            EnergySource.voltage_magnitude,
            EnergySource.p_max,
            EnergySource.p_min,
            EnergySource.r,
            EnergySource.r0,
            EnergySource.rn,
            EnergySource.x,
            EnergySource.x0,
            EnergySource.xn,
            EnergySource.r_min,
            EnergySource.rn_min,
            EnergySource.r0_min,
            EnergySource.x_min,
            EnergySource.xn_min,
            EnergySource.x0_min,
            EnergySource.r_max,
            EnergySource.rn_max,
            EnergySource.r0_max,
            EnergySource.x_max,
            EnergySource.xn_max,
            EnergySource.x0_max
        )
        self._compare_values(
            diff,
            EnergySource.is_external_grid
        )

        return self._compare_energy_connection(diff)

    def _compare_energy_source_phase(self, source: EnergySourcePhase, target: EnergySourcePhase) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_references(diff, EnergySourcePhase.energy_source)
        self._compare_values(diff, EnergySourcePhase.phase)

        return self._compare_power_system_resource(diff)

    def _compare_fuse(self, source: Fuse, target: Fuse) -> ObjectDifference:
        diff = ObjectDifference(source, target)
        self._compare_id_references(diff, Fuse.function)
        return self._compare_switch(diff)

    def _compare_ground(self, source: Ground, target: Ground) -> ObjectDifference:
        return self._compare_conducting_equipment(ObjectDifference(source, target))

    def _compare_compare_ground_disconnector(self, source: GroundDisconnector, target: GroundDisconnector) -> ObjectDifference:
        return self._compare_switch(ObjectDifference(source, target))

    def _compare_compare_grounding_impedance(self, source: GroundingImpedance, target: GroundingImpedance) -> ObjectDifference:
        diff = ObjectDifference(source, target)
        self._compare_floats(diff, GroundingImpedance.x)
        return self._compare_earth_fault_compensator(diff)

    def _compare_jumper(self, source: Jumper, target: Jumper) -> ObjectDifference:
        return self._compare_switch(ObjectDifference(source, target))

    def _compare_junction(self, source: Junction, target: Junction) -> ObjectDifference:
        return self._compare_connector(ObjectDifference(source, target))

    def _compare_line(self, diff: ObjectDifference) -> ObjectDifference:
        return self._compare_equipment_container(diff)

    def _compare_linear_shunt_compensator(self, source: LinearShuntCompensator, target: LinearShuntCompensator) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_floats(
            diff,
            LinearShuntCompensator.b0_per_section,
            LinearShuntCompensator.b_per_section,
            LinearShuntCompensator.g0_per_section,
            LinearShuntCompensator.g_per_section
        )

        return self._compare_shunt_compensator(diff)

    def _compare_load_break_switch(self, source: LoadBreakSwitch, target: LoadBreakSwitch) -> ObjectDifference:
        return self._compare_protected_switch(ObjectDifference(source, target))

    def _compare_per_length_impedance(self, diff: ObjectDifference) -> ObjectDifference:
        return self._compare_per_length_line_parameter(diff)

    def _compare_per_length_line_parameter(self, diff: ObjectDifference) -> ObjectDifference:
        return self._compare_identified_object(diff)

    def _compare_per_length_sequence_impedance(self, source: PerLengthSequenceImpedance, target: PerLengthSequenceImpedance) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_floats(
            diff,
            PerLengthSequenceImpedance.r,
            PerLengthSequenceImpedance.x,
            PerLengthSequenceImpedance.bch,
            PerLengthSequenceImpedance.gch,
            PerLengthSequenceImpedance.r0,
            PerLengthSequenceImpedance.x0,
            PerLengthSequenceImpedance.b0ch,
            PerLengthSequenceImpedance.g0ch
        )

        return self._compare_per_length_impedance(diff)

    def _compare_petersen_coil(self, source: PetersenCoil, target: PetersenCoil) -> ObjectDifference:
        diff = ObjectDifference(source, target)
        self._compare_floats(diff, PetersenCoil.x_ground_nominal)
        return self._compare_earth_fault_compensator(diff)

    def _compare_power_electronics_connection(self, source: PowerElectronicsConnection, target: PowerElectronicsConnection) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_reference_collections(diff, PowerElectronicsConnection.units, PowerElectronicsConnection.phases)
        self._compare_values(
            diff,
            PowerElectronicsConnection.max_i_fault,
            PowerElectronicsConnection.rated_s,
            PowerElectronicsConnection.rated_u,
            PowerElectronicsConnection.inverter_standard,
            PowerElectronicsConnection.sustain_op_overvolt_limit,
            PowerElectronicsConnection.inv_volt_watt_resp_mode,
            PowerElectronicsConnection.inv_watt_resp_v1,
            PowerElectronicsConnection.inv_watt_resp_v2,
            PowerElectronicsConnection.inv_watt_resp_v3,
            PowerElectronicsConnection.inv_watt_resp_v4,
            PowerElectronicsConnection.inv_volt_var_resp_mode,
            PowerElectronicsConnection.inv_var_resp_v1,
            PowerElectronicsConnection.inv_var_resp_v2,
            PowerElectronicsConnection.inv_var_resp_v3,
            PowerElectronicsConnection.inv_var_resp_v4,
            PowerElectronicsConnection.inv_reactive_power_mode
        )
        self._compare_floats(
            diff,
            PowerElectronicsConnection.max_q,
            PowerElectronicsConnection.min_q,
            PowerElectronicsConnection.p,
            PowerElectronicsConnection.q,
            PowerElectronicsConnection.stop_at_over_freq,
            PowerElectronicsConnection.stop_at_under_freq,
            PowerElectronicsConnection.inv_watt_resp_p_at_v1,
            PowerElectronicsConnection.inv_watt_resp_p_at_v2,
            PowerElectronicsConnection.inv_watt_resp_p_at_v3,
            PowerElectronicsConnection.inv_watt_resp_p_at_v4,
            PowerElectronicsConnection.inv_var_resp_q_at_v1,
            PowerElectronicsConnection.inv_var_resp_q_at_v2,
            PowerElectronicsConnection.inv_var_resp_q_at_v3,
            PowerElectronicsConnection.inv_var_resp_q_at_v4,
            PowerElectronicsConnection.inv_fix_reactive_power
        )

        return self._compare_regulating_cond_eq(diff)

    def _compare_power_electronics_connection_phase(self, source: PowerElectronicsConnectionPhase, target: PowerElectronicsConnectionPhase) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_references(diff, PowerElectronicsConnectionPhase.power_electronics_connection)
        self._compare_values(diff, PowerElectronicsConnectionPhase.phase)
        self._compare_floats(diff, PowerElectronicsConnectionPhase.p, PowerElectronicsConnectionPhase.q)

        return self._compare_power_system_resource(diff)

    def _compare_power_transformer(self, source: PowerTransformer, target: PowerTransformer) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_indexed_id_reference_collections(diff, PowerTransformer.ends)
        self._compare_values(diff, PowerTransformer.vector_group, PowerTransformer.construction_kind, PowerTransformer.function)
        self._compare_floats(diff, PowerTransformer.transformer_utilisation)
        self._compare_id_references(diff, PowerTransformer.power_transformer_info)

        return self._compare_conducting_equipment(diff)

    def _compare_power_transformer_end(self, source: PowerTransformerEnd, target: PowerTransformerEnd) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_references(diff, PowerTransformerEnd.power_transformer)
        self._compare_values(
            diff,
            PowerTransformerEnd.connection_kind,
            PowerTransformerEnd.phase_angle_clock,
            PowerTransformerEnd.rated_s,
            PowerTransformerEnd.rated_u
        )
        self._compare_floats(
            diff,
            PowerTransformerEnd.b,
            PowerTransformerEnd.b0,
            PowerTransformerEnd.g,
            PowerTransformerEnd.g0,
            PowerTransformerEnd.r,
            PowerTransformerEnd.r0,
            PowerTransformerEnd.x,
            PowerTransformerEnd.x0
        )
        self._compare_indexed_value_collections(diff, PowerTransformerEnd.s_ratings)

        return self._compare_transformer_end(diff)

    def _compare_protected_switch(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_values(diff, ProtectedSwitch.breaking_capacity)
        self._compare_id_reference_collections(diff, ProtectedSwitch.relay_functions)

        return self._compare_switch(diff)

    def _compare_ratio_tap_changer(self, source: RatioTapChanger, target: RatioTapChanger) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_references(diff, RatioTapChanger.transformer_end)
        self._compare_floats(diff, RatioTapChanger.step_voltage_increment)

        return self._compare_tap_changer(diff)

    def _compare_recloser(self, source: Recloser, target: Recloser) -> ObjectDifference:
        return self._compare_protected_switch(ObjectDifference(source, target))

    def _compare_regulating_cond_eq(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_values(diff, RegulatingCondEq.control_enabled)
        self._compare_id_references(diff, RegulatingCondEq.regulating_control)

        return self._compare_energy_connection(diff)

    def _compare_regulating_control(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_values(
            diff,
            RegulatingControl.discrete,
            RegulatingControl.mode,
            RegulatingControl.monitored_phase,
            RegulatingControl.enabled
        )
        self._compare_floats(
            diff,
            RegulatingControl.target_deadband,
            RegulatingControl.target_value,
            RegulatingControl.max_allowed_target_value,
            RegulatingControl.min_allowed_target_value,
            RegulatingControl.rated_current
        )
        self._compare_id_references(diff, RegulatingControl.terminal)
        self._compare_id_reference_collections(diff, RegulatingControl.regulating_conducting_equipment)

        return self._compare_power_system_resource(diff)

    def _compare_reactive_capability_curve(self, source: ReactiveCapabilityCurve, target: ReactiveCapabilityCurve) -> ObjectDifference:
        return self._compare_curve(ObjectDifference(source, target))

    def _compare_rotating_machine(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_values(diff, RotatingMachine.rated_u)
        self._compare_floats(diff, RotatingMachine.rated_power_factor, RotatingMachine.rated_s, RotatingMachine.p, RotatingMachine.q)

        return self._compare_regulating_cond_eq(diff)

    def _compare_series_compensator(self, source: SeriesCompensator, target: SeriesCompensator) -> ObjectDifference:
        diff = ObjectDifference(source, target)
        self._compare_values(diff, SeriesCompensator.varistor_rated_current, SeriesCompensator.varistor_voltage_threshold)
        self._compare_floats(diff, SeriesCompensator.r, SeriesCompensator.r0, SeriesCompensator.x, SeriesCompensator.x0)

        return self._compare_conducting_equipment(diff)

    def _compare_shunt_compensator(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_values(diff, ShuntCompensator.grounded, ShuntCompensator.nom_u, ShuntCompensator.phase_connection)
        self._compare_floats(diff, ShuntCompensator.sections)
        self._compare_id_references(diff, ShuntCompensator.shunt_compensator_info)

        return self._compare_regulating_cond_eq(diff)

    def _compare_switch(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_floats(diff, Switch.rated_current)
        self._add_if_different(diff, "isNormallyOpen", self._compare_open_status(diff, lambda it, phase: it.is_normally_open(phase)))
        self._add_if_different(diff, "isOpen", self._compare_open_status(diff, lambda it, phase: it.is_open(phase)))
        self._compare_id_references(diff, Switch.switch_info)

        return self._compare_conducting_equipment(diff)

    def _compare_synchronous_machine(self, source: SynchronousMachine, target: SynchronousMachine) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(
            diff,
            SynchronousMachine.condenser_p,
            SynchronousMachine.earthing,
            SynchronousMachine.max_u,
            SynchronousMachine.min_u,
            SynchronousMachine.type,
            SynchronousMachine.operating_mode
        )

        self._compare_floats(
            diff,
            SynchronousMachine.base_q,
            SynchronousMachine.earthing_star_point_r,
            SynchronousMachine.earthing_star_point_x,
            SynchronousMachine.ikk,
            SynchronousMachine.max_q,
            SynchronousMachine.min_q,
            SynchronousMachine.mu,
            SynchronousMachine.r,
            SynchronousMachine.r0,
            SynchronousMachine.r2,
            SynchronousMachine.sat_direct_subtrans_x,
            SynchronousMachine.sat_direct_sync_x,
            SynchronousMachine.sat_direct_trans_x,
            SynchronousMachine.x0,
            SynchronousMachine.x2,
        )
        self._compare_id_reference_collections(diff, SynchronousMachine.curves)

        return self._compare_rotating_machine(diff)

    def _compare_tap_changer(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_values(
            diff,
            TapChanger.control_enabled,
            TapChanger.neutral_u,
            TapChanger.high_step,
            TapChanger.low_step,
            TapChanger.neutral_step,
            TapChanger.normal_step
        )
        self._compare_floats(diff, TapChanger.step)

        self._compare_id_references(diff, TapChanger.tap_changer_control)
        return self._compare_power_system_resource(diff)

    def _compare_tap_changer_control(self, source: TapChangerControl, target: TapChangerControl) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(
            diff,
            TapChangerControl.limit_voltage,
            TapChangerControl.line_drop_compensation,
            TapChangerControl.forward_ldc_blocking,
            TapChangerControl.co_generation_enabled
        )
        self._compare_floats(
            diff,
            TapChangerControl.line_drop_r,
            TapChangerControl.line_drop_x,
            TapChangerControl.reverse_line_drop_r,
            TapChangerControl.reverse_line_drop_x,
            TapChangerControl.time_delay,
        )

        return self._compare_regulating_control(diff)

    def _compare_transformer_end(self, diff: ObjectDifference) -> ObjectDifference:
        self._compare_values(diff, TransformerEnd.grounded, TransformerEnd.end_number)
        self._compare_floats(diff, TransformerEnd.r_ground, TransformerEnd.x_ground)
        self._compare_id_references(diff, TransformerEnd.base_voltage, TransformerEnd.ratio_tap_changer, TransformerEnd.terminal, TransformerEnd.star_impedance)

        return self._compare_identified_object(diff)

    def _compare_transformer_star_impedance(self, source: TransformerStarImpedance, target: TransformerStarImpedance) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_floats(diff, TransformerStarImpedance.r, TransformerStarImpedance.r0, TransformerStarImpedance.x, TransformerStarImpedance.x0)
        self._compare_id_references(diff, TransformerStarImpedance.transformer_end_info)

        return self._compare_identified_object(diff)

    #########################
    # IEC61970 INF IEC61970 #
    #########################

    def _compare_circuit(self, source: Circuit, target: Circuit) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_references(diff, Circuit.loop)
        self._compare_id_reference_collections(diff, Circuit.end_terminals, Circuit.end_substations)

        return self._compare_line(diff)

    def _compare_loop(self, source: Loop, target: Loop) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_reference_collections(diff, Loop.circuits, Loop.substations, Loop.energizing_substations)

        return self._compare_identified_object(diff)

    def _compare_lv_feeder(self, source: LvFeeder, target: LvFeeder) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_references(diff, LvFeeder.normal_head_terminal)
        self._compare_id_reference_collections(diff, LvFeeder.normal_energizing_feeders)
        if self._options.compare_feeder_equipment:
            self._compare_id_reference_collections(diff, LvFeeder.current_equipment)

        return self._compare_equipment_container(diff)

    #####################################################
    # IEC61970 INF IEC61970 WIRES GENERATION PRODUCTION #
    #####################################################

    def _compare_ev_charging_unit(self, source: EvChargingUnit, target: EvChargingUnit) -> ObjectDifference:
        diff = ObjectDifference(source, target)
        return self._compare_power_electronics_unit(diff)

    @staticmethod
    # NOTE: Should be Callable[[Switch, SinglePhaseKind], bool], but type inference does not work correctly.
    def _compare_open_status(diff: ObjectDifference, open_test: Callable[[Any, SinglePhaseKind], bool]) -> Optional[ValueDifference]:
        source_status = {phase: open_test(diff.source, phase) for phase in PhaseCode.ABCN.single_phases}
        target_status = {phase: open_test(diff.target, phase) for phase in PhaseCode.ABCN.single_phases}

        return ValueDifference(source_status, target_status) if source_status != target_status else None
