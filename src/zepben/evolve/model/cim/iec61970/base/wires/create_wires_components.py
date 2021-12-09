#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import *


def create_ac_line_segment(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                           asset_info: AssetInfo = None, in_service: bool = True, normally_in_service: bool = True, usage_points: List[UsagePoint] = None,
                           equipment_containers: List[EquipmentContainer] = None, operational_restrictions: List[OperationalRestriction] = None,
                           current_feeders: List[Feeder] = None, base_voltage: BaseVoltage = None, terminals: List[Terminal] = None, length: float = None,
                           per_length_sequence_impedance: PerLengthSequenceImpedance = None) -> AcLineSegment:
    """
    AcLineSegment(Conductor(ConductingEquipment(Equipment(PowerSystemResource(IdentifiedObject)))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    Equipment: in_service, normally_in_service, usage_points, equipment_containers, operational_restrictions, current_feeders
    ConductingEquipment: base_voltage, terminals
    Conductor: length
    AcLineSegment: per_length_sequence_impedance
    """
    return AcLineSegment(**locals())


def create_battery_unit(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                        asset_info: AssetInfo = None, in_service: bool = True, normally_in_service: bool = True, usage_points: List[UsagePoint] = None,
                        equipment_containers: List[EquipmentContainer] = None, operational_restrictions: List[OperationalRestriction] = None,
                        current_feeders: List[Feeder] = None, power_electronics_connection: PowerElectronicsConnection = None, max_p: int = None,
                        min_p: int = None, battery_state: BatteryStateKind = BatteryStateKind.UNKNOWN, rated_e: int = None, stored_e: int = None
                        ) -> BatteryUnit:
    """
    BatteryUnit(PowerElectronicsUnit(Equipment(PowerSystemResource(IdentifiedObject))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    Equipment: in_service, normally_in_service, usage_points, equipment_containers, operational_restrictions, current_feeders
    PowerElectronicsUnit: power_electronics_connection, max_p, min_p
    BatteryUnit: battery_state, rated_e, stored_e
    """
    return BatteryUnit(**locals())


# noinspection PyShadowingBuiltins,PyShadowingNames
def create_breaker(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                   asset_info: AssetInfo = None, in_service: bool = True, normally_in_service: bool = True, usage_points: List[UsagePoint] = None,
                   equipment_containers: List[EquipmentContainer] = None, operational_restrictions: List[OperationalRestriction] = None,
                   current_feeders: List[Feeder] = None, base_voltage: BaseVoltage = None, terminals: List[Terminal] = None, _open: int = 0,
                   _normally_open: int = 0) -> Breaker:
    """
    Breaker(ProtectedSwitch(Switch(ConductingEquipment(Equipment(PowerSystemResource(IdentifiedObject))))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    Equipment: in_service, normally_in_service, usage_points, equipment_containers, operational_restrictions, current_feeders
    ConductingEquipment: base_voltage, terminals
    Switch: _open, _normally_open
    ProtectedSwitch:
    Breaker:
    """
    return Breaker(**locals())


def create_busbar_section(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                          asset_info: AssetInfo = None, in_service: bool = True, normally_in_service: bool = True, usage_points: List[UsagePoint] = None,
                          equipment_containers: List[EquipmentContainer] = None, operational_restrictions: List[OperationalRestriction] = None,
                          current_feeders: List[Feeder] = None, base_voltage: BaseVoltage = None, terminals: List[Terminal] = None) -> BusbarSection:
    """
    BusbarSection(Connector(ConductingEquipment(Equipment(PowerSystemResource(IdentifiedObject)))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    Equipment: in_service, normally_in_service, usage_points, equipment_containers, operational_restrictions, current_feeders
    ConductingEquipment: base_voltage, terminals
    Connector:
    BusbarSection:
    """
    return BusbarSection(**locals())


# noinspection PyShadowingBuiltins,PyShadowingNames
def create_disconnector(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                        asset_info: AssetInfo = None, in_service: bool = True, normally_in_service: bool = True, usage_points: List[UsagePoint] = None,
                        equipment_containers: List[EquipmentContainer] = None, operational_restrictions: List[OperationalRestriction] = None,
                        current_feeders: List[Feeder] = None, base_voltage: BaseVoltage = None, terminals: List[Terminal] = None, _open: int = 0,
                        _normally_open: int = 0) -> Disconnector:
    """
    Disconnector(Switch(ConductingEquipment(Equipment(PowerSystemResource(IdentifiedObject)))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    Equipment: in_service, normally_in_service, usage_points, equipment_containers, operational_restrictions, current_feeders
    ConductingEquipment: base_voltage, terminals
    Switch: _open, _normally_open
    Disconnector:
    """
    return Disconnector(**locals())


def create_energy_consumer(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                           asset_info: AssetInfo = None, in_service: bool = True, normally_in_service: bool = True, usage_points: List[UsagePoint] = None,
                           equipment_containers: List[EquipmentContainer] = None, operational_restrictions: List[OperationalRestriction] = None,
                           current_feeders: List[Feeder] = None, base_voltage: BaseVoltage = None, terminals: List[Terminal] = None,
                           energy_consumer_phases: List[EnergyConsumerPhase] = None, customer_count: int = None, grounded: bool = False,
                           phase_connection: PhaseShuntConnectionKind = PhaseShuntConnectionKind.D, p: float = None, p_fixed: float = None, q: float = None,
                           q_fixed: float = None) -> EnergyConsumer:
    """
    EnergyConsumer(EnergyConnection(ConductingEquipment(Equipment(PowerSystemResource(IdentifiedObject)))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    Equipment: in_service, normally_in_service, usage_points, equipment_containers, operational_restrictions, current_feeders
    ConductingEquipment: base_voltage, terminals
    EnergyConnection:
    EnergyConsumer: energy_consumer_phases, customer_count, grounded, phase_connection, p, p_fixed, q, q_fixed
    """
    return EnergyConsumer(**locals())


# noinspection PyShadowingNames
def create_energy_consumer_phase(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                                 asset_info: AssetInfo = None, energy_consumer: EnergyConsumer = None, phase: SinglePhaseKind = SinglePhaseKind.X,
                                 p: float = None, q: float = None, p_fixed: float = None, q_fixed: float = None) -> EnergyConsumerPhase:
    """
    EnergyConsumerPhase(EnergyConnection(ConductingEquipment(Equipment(PowerSystemResource(IdentifiedObject)))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    EnergyConsumerPhase: energy_consumer, phase, p, q, p_fixed, q_fixed
    """
    return EnergyConsumerPhase(**locals())


def create_energy_source(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                         asset_info: AssetInfo = None, in_service: bool = True, normally_in_service: bool = True, usage_points: List[UsagePoint] = None,
                         equipment_containers: List[EquipmentContainer] = None, operational_restrictions: List[OperationalRestriction] = None,
                         current_feeders: List[Feeder] = None, base_voltage: BaseVoltage = None, terminals: List[Terminal] = None,
                         energy_source_phases: List[EnergySourcePhase] = None, active_power: float = None, reactive_power: float = None,
                         voltage_angle: float = None, voltage_magnitude: float = None, p_max: float = None, p_min: float = None, r: float = None,
                         r0: float = None, rn: float = None, x: float = None, x0: float = None, xn: float = None, is_external_grid: bool = False,
                         r_min: float = None, rn_min: float = None, r0_min: float = None, x_min: float = None, xn_min: float = None, x0_min: float = None,
                         r_max: float = None, rn_max: float = None, r0_max: float = None, x_max: float = None, xn_max: float = None, x0_max: float = None
                         ) -> EnergySource:
    """
    EnergyConsumer(EnergyConnection(ConductingEquipment(Equipment(PowerSystemResource(IdentifiedObject)))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    Equipment: in_service, normally_in_service, usage_points, equipment_containers, operational_restrictions, current_feeders
    ConductingEquipment: base_voltage, terminals
    EnergyConnection:
    EnergySource: energy_source_phases, active_power, reactive_power, voltage_angle, voltage_magnitude, p_max, p_min, r, r0, rn, x, x0, xn
    """
    return EnergySource(**locals())


# noinspection PyShadowingNames
def create_energy_source_phase(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                               asset_info: AssetInfo = None, energy_source: EnergySource = None, phase: SinglePhaseKind = SinglePhaseKind.NONE
                               ) -> EnergySourcePhase:
    """
    EnergySourcePhase(PowerSystemResource(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    EnergySourcePhase: energy_source, phase
    """
    return EnergySourcePhase(**locals())


# noinspection PyShadowingBuiltins,PyShadowingNames
def create_fuse(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                asset_info: AssetInfo = None, in_service: bool = True, normally_in_service: bool = True, usage_points: List[UsagePoint] = None,
                equipment_containers: List[EquipmentContainer] = None, operational_restrictions: List[OperationalRestriction] = None,
                current_feeders: List[Feeder] = None, base_voltage: BaseVoltage = None, terminals: List[Terminal] = None, _open: int = 0,
                _normally_open: int = 0) -> Fuse:
    """
    Fuse(Switch(ConductingEquipment(Equipment(PowerSystemResource(IdentifiedObject)))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    Equipment: in_service, normally_in_service, usage_points, equipment_containers, operational_restrictions, current_feeders
    ConductingEquipment: base_voltage, terminals
    Switch: _open, _normally_open
    Fuse:
    """
    return Fuse(**locals())


# noinspection PyShadowingBuiltins,PyShadowingNames
def create_jumper(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                  asset_info: AssetInfo = None, in_service: bool = True, normally_in_service: bool = True, usage_points: List[UsagePoint] = None,
                  equipment_containers: List[EquipmentContainer] = None, operational_restrictions: List[OperationalRestriction] = None,
                  current_feeders: List[Feeder] = None, base_voltage: BaseVoltage = None, terminals: List[Terminal] = None, _open: int = 0,
                  _normally_open: int = 0) -> Jumper:
    """
    Jumper(Switch(ConductingEquipment(Equipment(PowerSystemResource(IdentifiedObject)))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    Equipment: in_service, normally_in_service, usage_points, equipment_containers, operational_restrictions, current_feeders
    ConductingEquipment: base_voltage, terminals
    Switch: _open, _normally_open
    Jumper:
    """
    return Jumper(**locals())


def create_junction(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                    asset_info: AssetInfo = None, in_service: bool = True, normally_in_service: bool = True, usage_points: List[UsagePoint] = None,
                    equipment_containers: List[EquipmentContainer] = None, operational_restrictions: List[OperationalRestriction] = None,
                    current_feeders: List[Feeder] = None, base_voltage: BaseVoltage = None, terminals: List[Terminal] = None) -> Junction:
    """
    Junction(Connector(ConductingEquipment(Equipment(PowerSystemResource(IdentifiedObject)))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    Equipment: in_service, normally_in_service, usage_points, equipment_containers, operational_restrictions, current_feeders
    ConductingEquipment: base_voltage, terminals
    Connector:
    Junction:
    """
    return Junction(**locals())


def create_linear_shunt_compensator(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                                    asset_info: AssetInfo = None, in_service: bool = True, normally_in_service: bool = True, 
                                    usage_points: List[UsagePoint] = None, equipment_containers: List[EquipmentContainer] = None,
                                    operational_restrictions: List[OperationalRestriction] = None, current_feeders: List[Feeder] = None,
                                    base_voltage: BaseVoltage = None, terminals: List[Terminal] = None, control_enabled: bool = True, grounded: bool = False,
                                    nom_u: int = None, phase_connection: PhaseShuntConnectionKind = PhaseShuntConnectionKind.UNKNOWN, sections: float = None,
                                    b0_per_section: float = None, b_per_section: float = None, g0_per_section: float = None, g_per_section: float = None
                                    ) -> LinearShuntCompensator:
    """
    LinearShuntCompensator(ShuntCompensator(RegulatingCondEq(EnergyConnection(ConductingEquipment(Equipment(PowerSystemResource(IdentifiedObject)))))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    Equipment: in_service, normally_in_service, usage_points, equipment_containers, operational_restrictions, current_feeders
    ConductingEquipment: base_voltage, terminals
    EnergyConnection:
    RegulatingCondEq: control_enabled
    ShuntCompensator: grounded, nom_u, phase_connection, sections
    LinearShuntCompensator: b0_per_section, b_per_section, g0_per_section, g_per_section
    """
    return LinearShuntCompensator(**locals())


# noinspection PyShadowingBuiltins,PyShadowingNames
def create_load_break_switch(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                             asset_info: AssetInfo = None, in_service: bool = True, normally_in_service: bool = True, usage_points: List[UsagePoint] = None,
                             equipment_containers: List[EquipmentContainer] = None, operational_restrictions: List[OperationalRestriction] = None,
                             current_feeders: List[Feeder] = None, base_voltage: BaseVoltage = None, terminals: List[Terminal] = None, _open: int = 0,
                             _normally_open: int = 0) -> LoadBreakSwitch:
    """
    LoadBreakSwitch(ProtectedSwitch(Switch(ConductingEquipment(Equipment(PowerSystemResource(IdentifiedObject))))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    Equipment: in_service, normally_in_service, usage_points, equipment_containers, operational_restrictions, current_feeders
    ConductingEquipment: base_voltage, terminals
    Switch: _open, _normally_open
    ProtectedSwitch:
    LoadBreakSwitch:
    """
    return LoadBreakSwitch(**locals())


def create_per_length_sequence_impedance(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, r: float = None, x: float = None, 
                                         bch: float = None, gch: float = None, r0: float = None, x0: float = None, b0ch: float = None, g0ch: float = None
                                         ) -> PerLengthSequenceImpedance:
    """
    PerLengthSequenceImpedance(PerLengthImpedance(PerLengthLineParameter(IdentifiedObject)))
    IdentifiedObject: mrid, name, description, names
    PerLengthLineParameter:
    PerLengthImpedance:
    PerLengthSequenceImpedance: r, x, bch, gch, r0, x0, b0ch, g0ch
    """
    return PerLengthSequenceImpedance(**locals())


def create_photo_voltaic_unit(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                              asset_info: AssetInfo = None, in_service: bool = True, normally_in_service: bool = True, usage_points: List[UsagePoint] = None,
                              equipment_containers: List[EquipmentContainer] = None, operational_restrictions: List[OperationalRestriction] = None,
                              current_feeders: List[Feeder] = None, power_electronics_connection: PowerElectronicsConnection = None, max_p: int = None,
                              min_p: int = None) -> PhotoVoltaicUnit:
    """
    PhotoVoltaicUnit(PowerElectronicsUnit(Equipment(PowerSystemResource(IdentifiedObject))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    Equipment: in_service, normally_in_service, usage_points, equipment_containers, operational_restrictions, current_feeders
    PowerElectronicsUnit: power_electronics_connection, max_p, min_p
    PhotoVoltaicUnit:
    """
    return PhotoVoltaicUnit(**locals())


def create_power_electronics_connection(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                                        asset_info: AssetInfo = None, in_service: bool = True, normally_in_service: bool = True, 
                                        usage_points: List[UsagePoint] = None, equipment_containers: List[EquipmentContainer] = None, 
                                        operational_restrictions: List[OperationalRestriction] = None, current_feeders: List[Feeder] = None, 
                                        base_voltage: BaseVoltage = None, terminals: List[Terminal] = None, control_enabled: bool = True,
                                        max_i_fault: int = None, p: float = None, q: float = None, max_q: float = None, min_q: float = None,
                                        rated_s: int = None, rated_u: int = None, power_electronics_units: List[PowerElectronicsUnit] = None,
                                        power_electronics_connection_phases: List[PowerElectronicsConnectionPhase] = None) -> PowerElectronicsConnection:
    """
    PowerElectronicsConnection(RegulatingCondEq(EnergyConnection(ConductingEquipment(Equipment(PowerSystemResource(IdentifiedObject))))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    Equipment: in_service, normally_in_service, usage_points, equipment_containers, operational_restrictions, current_feeders
    ConductingEquipment: base_voltage, terminals
    EnergyConnection:
    RegulatingCondEq: control_enabled
    PowerElectronicsConnection: max_i_fault, p, q, max_q, min_q, rated_s, rated_u, power_electronics_units, power_electronics_connection_phases
    """
    return PowerElectronicsConnection(**locals())


# noinspection PyShadowingNames
def create_power_electronics_connection_phase(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                                              asset_info: AssetInfo = None, power_electronics_connection: PowerElectronicsConnection = None, p: float = None, 
                                              phase: SinglePhaseKind = SinglePhaseKind.X, q: float = None, ) -> PowerElectronicsConnectionPhase:
    """
    PowerElectronicsConnectionPhase(PowerSystemResource(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    PowerElectronicsConnectionPhase: power_electronics_connection, p, phase, q
    """
    return PowerElectronicsConnectionPhase(**locals())


def create_power_electronics_wind_unit(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                                       asset_info: AssetInfo = None, in_service: bool = True, normally_in_service: bool = True,
                                       usage_points: List[UsagePoint] = None, equipment_containers: List[EquipmentContainer] = None,
                                       operational_restrictions: List[OperationalRestriction] = None, current_feeders: List[Feeder] = None,
                                       power_electronics_connection: PowerElectronicsConnection = None, max_p: int = None, min_p: int = None
                                       ) -> PowerElectronicsWindUnit:
    """
    PowerElectronicsWindUnit(PowerElectronicsUnit(Equipment(PowerSystemResource(IdentifiedObject))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    Equipment: in_service, normally_in_service, usage_points, equipment_containers, operational_restrictions, current_feeders
    PowerElectronicsUnit: power_electronics_connection, max_p, min_p
    PowerElectronicsWindUnit:
    """
    return PowerElectronicsWindUnit(**locals())


def create_power_transformer(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                             asset_info: AssetInfo = None, in_service: bool = True, normally_in_service: bool = True, usage_points: List[UsagePoint] = None,
                             equipment_containers: List[EquipmentContainer] = None, operational_restrictions: List[OperationalRestriction] = None,
                             current_feeders: List[Feeder] = None, base_voltage: BaseVoltage = None, terminals: List[Terminal] = None,
                             vector_group: VectorGroup = VectorGroup.UNKNOWN, power_transformer_ends: List[PowerTransformerEnd] = None,
                             transformer_utilisation: float = None, construction_kind: TransformerConstructionKind = TransformerConstructionKind.unknown,
                             function: TransformerFunctionKind = TransformerFunctionKind.other) -> PowerTransformer:
    """
    PowerTransformer(ConductingEquipment(Equipment(PowerSystemResource(IdentifiedObject))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    Equipment: in_service, normally_in_service, usage_points, equipment_containers, operational_restrictions, current_feeders
    ConductingEquipment: base_voltage, terminals
    PowerTransformer: vector_group, power_transformer_ends, transformer_utilisation
    """
    return PowerTransformer(**locals())


def create_power_transformer_end(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, grounded: bool = False,
                                 r_ground: float = None, x_ground: float = None, ratio_tap_changer: RatioTapChanger = None, terminal: Terminal = None,
                                 base_voltage: BaseVoltage = None, end_number: int = 0, star_impedance: TransformerStarImpedance = None,
                                 power_transformer: PowerTransformer = None, rated_s: int = None, rated_u: int = None, r: float = None, x: float = None,
                                 r0: float = None, x0: float = None, g: float = None, g0: float = None, b: float = None, b0: float = None,
                                 connection_kind: WindingConnection = WindingConnection.UNKNOWN_WINDING, phase_angle_clock: int = None) -> PowerTransformerEnd:
    """
    PowerTransformerEnd(TransformerEnd(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    TransformerEnd: grounded, r_ground, x_ground, ratio_tap_changer, terminal, base_voltage, end_number, star_impedance
    PowerTransformerEnd: power_transformer, rated_s, rated_u, r, x, r0, x0, g, g0, b, b0, connection_kind, phase_angle_clock
    """
    return PowerTransformerEnd(**locals())


def create_ratio_tap_changer(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None,  location: Location = None,
                             asset_info: AssetInfo = None, control_enabled: bool = True, neutral_u: int = None, high_step: int = None, low_step: int = None,
                             neutral_step: int = None, normal_step: int = None, step: float = None, transformer_end: TransformerEnd = None,
                             step_voltage_increment: float = None) -> RatioTapChanger:
    """
    RatioTapChanger(TapChanger(PowerSystemResource(IdentifiedObject)))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    TapChanger: control_enabled, neutral_u, high_step, low_step, neutral_step, normal_step, step
    RatioTapChanger: transformer_end, step_voltage_increment
    """
    return RatioTapChanger(**locals())


# noinspection PyShadowingBuiltins,PyShadowingNames
def create_recloser(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                    asset_info: AssetInfo = None, in_service: bool = True, normally_in_service: bool = True, usage_points: List[UsagePoint] = None,
                    equipment_containers: List[EquipmentContainer] = None, operational_restrictions: List[OperationalRestriction] = None,
                    current_feeders: List[Feeder] = None, base_voltage: BaseVoltage = None, terminals: List[Terminal] = None, _open: int = 0,
                    _normally_open: int = 0) -> Recloser:
    """
    Recloser(ProtectedSwitch(Switch(ConductingEquipment(Equipment(PowerSystemResource(IdentifiedObject))))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    Equipment: in_service, normally_in_service, usage_points, equipment_containers, operational_restrictions, current_feeders
    ConductingEquipment: base_voltage, terminals
    Switch: _open, _normally_open
    ProtectedSwitch:
    Recloser:
    """
    return Recloser(**locals())


def create_transformer_star_impedance(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, r: float = 0.0, r0: float = 0.0,
                                      x: float = 0.0, x0: float = 0.0, transformer_end_info: TransformerEndInfo = None) -> TransformerStarImpedance:
    """
    TransformerStarImpedance(IdentifiedObject)
    IdentifiedObject: mrid, name, description, names
    TransformerStarImpedance: r, r0, x, x0, transformer_end_info
    """
    return TransformerStarImpedance(**locals())
