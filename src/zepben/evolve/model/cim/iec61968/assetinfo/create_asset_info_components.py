#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import *


def create_cable_info(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, rated_current: int = None,
                      material: WireMaterialKind = WireMaterialKind.UNKNOWN) -> CableInfo:
    """
    CableInfo(WireInfo(AssetInfo(IdentifiedObject)))
    IdentifiedObject: mrid, name, description, names
    AssetInfo:
    WireInfo: rated_current, material
    CableInfo:
    """
    return CableInfo(**locals())


def create_no_load_test(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, base_power: int = None, temperature: float = None, 
                        energised_end_voltage: int = None, exciting_current: float = None, exciting_current_zero: float = None, loss: int = None, 
                        loss_zero: int = None) -> NoLoadTest:
    """
    NoLoadTest(TransformerTest(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    TransformerTest: base_power, temperature
    NoLoadTest: energised_end_voltage, exciting_current, exciting_current_zero, loss, loss_zero
    """
    return NoLoadTest(**locals())


def create_open_circuit_test(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, base_power: int = None, 
                             temperature: float = None, energised_end_step: int = None, energised_end_voltage: int = None, open_end_step: int = None,
                             open_end_voltage: int = None, phase_shift: float = None) -> OpenCircuitTest:
    """
    OpenCircuitTest(TransformerTest(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    TransformerTest: base_power, temperature
    OpenCircuitTest: energised_end_step, energised_end_voltage, open_end_step, open_end_voltage, phase_shift
    """
    return OpenCircuitTest(**locals())


def create_overhead_wire_info(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, rated_current: int = None,
                              material: WireMaterialKind = WireMaterialKind.UNKNOWN) -> OverheadWireInfo:
    """
    OverheadWireInfo(WireInfo(AssetInfo(IdentifiedObject)))
    IdentifiedObject: mrid, name, description, names
    AssetInfo:
    WireInfo: rated_current, material
    OverheadWireInfo:
    """
    return OverheadWireInfo(**locals())


def create_power_transformer_info(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, 
                                  transformer_tank_infos: List[TransformerTankInfo] = None) -> PowerTransformerInfo:
    """
    PowerTransformerInfo(AssetInfo(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    AssetInfo:
    PowerTransformerInfo: transformer_tank_infos
    """
    return PowerTransformerInfo(**locals())


def create_short_circuit_test(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, base_power: int = None,
                              temperature: float = None, current: float = None, energised_end_step: int = None, grounded_end_step: int = None, 
                              leakage_impedance: float = None, leakage_impedance_zero: float = None, loss: int = None, loss_zero: int = None, 
                              power: int = None, voltage: float = None, voltage_ohmic_part: float = None) -> ShortCircuitTest:
    """
    ShortCircuitTest(TransformerTest(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    TransformerTest: base_power, temperature
    ShortCircuitTest: current, energised_end_step, grounded_end_step, leakage_impedance, leakage_impedance_zero, loss, loss_zero, power, voltage, 
                      voltage_ohmic_part
    """
    return ShortCircuitTest(**locals())


def create_shunt_compensator_info(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, max_power_loss: int = None, 
                                  rated_current: int = None, rated_reactive_power: int = None, rated_voltage: int = None) -> ShuntCompensatorInfo:
    """
    ShuntCompensatorInfo(AssetInfo(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    AssetInfo:
    ShuntCompensatorInfo: max_power_loss, rated_current, rated_reactive_power, rated_voltage
    """
    return ShuntCompensatorInfo(**locals())


def create_transformer_end_info(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, 
                                connection_kind: WindingConnection = WindingConnection.UNKNOWN_WINDING, emergency_s: int = None, end_number: int = 0, 
                                insulation_u: int = None, phase_angle_clock: int = None, r: float = None, rated_s: int = None, rated_u: int = None, 
                                short_term_s: int = None, transformer_tank_info: TransformerTankInfo = None, 
                                transformer_star_impedance: TransformerStarImpedance = None, 
                                energised_end_no_load_tests: NoLoadTest = None, energised_end_short_circuit_tests: ShortCircuitTest = None, 
                                grounded_end_short_circuit_tests: ShortCircuitTest = None, 
                                open_end_open_circuit_tests: OpenCircuitTest = None, energised_end_open_circuit_tests: OpenCircuitTest = None
                                ) -> TransformerEndInfo:
    """
    TransformerEndInfo(AssetInfo(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    AssetInfo:
    TransformerEndInfo: connection_kind, emergency_s, end_number, insulation_u, phase_angle_clock, r, rated_s, rated_u, short_term_s, transformer_tank_info,
                        transformer_star_impedance, energised_end_no_load_tests, energised_end_short_circuit_tests, grounded_end_short_circuit_tests, 
                        open_end_open_circuit_tests, energised_end_open_circuit_tests
    """
    return TransformerEndInfo(**locals())


def create_transformer_tank_info(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, 
                                 transformer_end_infos: List[TransformerEndInfo] = None) -> TransformerTankInfo:
    """
    TransformerTankInfo(AssetInfo(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    AssetInfo:
    TransformerTankInfo: transformer_end_infos
    """
    return TransformerTankInfo(**locals())
