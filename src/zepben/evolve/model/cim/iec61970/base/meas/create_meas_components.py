#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime
from typing import List

from zepben.evolve import *

__all__ = ["create_accumulator", "create_accumulator_value", "create_analog", "create_analog_value", "create_control", "create_discrete",
           "create_discrete_value"]


def create_accumulator(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, power_system_resource_mrid: str = None,
                       remote_source: RemoteSource = None, terminal_mrid: str = None, phases: PhaseCode = PhaseCode.ABC,
                       unit_symbol: UnitSymbol = UnitSymbol.NONE) -> Accumulator:
    """
    Accumulator(Measurement(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    Measurement: power_system_resource_mrid, remote_source, terminal_mrid, phases, unit_symbol
    Accumulator:
    """
    a = Accumulator(**locals())
    if remote_source:
        remote_source.measurement = a
    return a


def create_accumulator_value(time_stamp: datetime = None, value: int = 0, accumulator_mrid: str = None) -> AccumulatorValue:
    """
    AccumulatorValue(MeasurementValue())
    MeasurementValue: time_stamp
    AccumulatorValue: value, accumulator_mrid
    """
    # noinspection PyArgumentList
    return AccumulatorValue(**locals())


def create_analog(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, power_system_resource_mrid: str = None,
                  remote_source: RemoteSource = None, terminal_mrid: str = None, phases: PhaseCode = PhaseCode.ABC, unit_symbol: UnitSymbol = UnitSymbol.NONE,
                  positive_flow_in: bool = False) -> Analog:
    """
    Analog(Measurement(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    Measurement: power_system_resource_mrid, remote_source, terminal_mrid, phases, unit_symbol
    Analog: positive_flow_in
    """
    a = Analog(**locals())
    if remote_source:
        remote_source.measurement = a
    return a


def create_analog_value(time_stamp: datetime = None, value: float = 0.0, analog_mrid: str = None) -> AnalogValue:
    """
    AnalogValue(MeasurementValue())
    MeasurementValue: time_stamp
    AnalogValue: value, analog_mrid
    """
    # noinspection PyArgumentList
    return AnalogValue(**locals())


def create_control(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, power_system_resource_mrid: str = None, 
                   remote_control: RemoteControl = None) -> Control:
    """
    Control(IoPoint(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    IoPoint:
    Control: power_system_resource_mrid, remote_control
    """
    c = Control(**locals())
    if remote_control:
        remote_control.control = c
    return c


def create_discrete(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, power_system_resource_mrid: str = None,
                    remote_source: RemoteSource = None, terminal_mrid: str = None, phases: PhaseCode = PhaseCode.ABC, unit_symbol: UnitSymbol = UnitSymbol.NONE
                    ) -> Discrete:
    """
    Discrete(Measurement(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    Measurement: power_system_resource_mrid, remote_source, terminal_mrid, phases, unit_symbol
    Discrete:
    """
    d = Discrete(**locals())
    if remote_source:
        remote_source.measurement = d
    return d


def create_discrete_value(time_stamp: datetime = None, value: int = 0, discrete_mrid: str = None) -> DiscreteValue:
    """
    DiscreteValue(MeasurementValue())
    MeasurementValue: time_stamp
    DiscreteValue: value, discrete_mrid
    """
    # noinspection PyArgumentList
    return DiscreteValue(**locals())
