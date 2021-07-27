#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import RemoteSource

from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.evolve.model.cim.iec61970.base.domain.unit_symbol import UnitSymbol

__all__ = ["Measurement", "Accumulator", "Analog", "Discrete"]


class Measurement(IdentifiedObject):
    """
    A Measurement represents any measured, calculated or non-measured non-calculated quantity. Any piece of equipment
    may contain Measurements, e.g. a substation may have temperature measurements and door open indications,
    a transformer may have oil temperature and tank pressure measurements, a bay may contain a number of power flow
    measurements and a Breaker may contain a switch status measurement.

    The PSR - Measurement association is intended to capture this use of Measurement and is included in the naming
    hierarchy based on EquipmentContainer. The naming hierarchy typically has Measurements as leafs,
    e.g. Substation-VoltageLevel-Bay-Switch-Measurement.

    Some Measurements represent quantities related to a particular sensor location in the network, e.g. a voltage
    transformer (PT) at a busbar or a current transformer (CT) at the bar between a breaker and an isolator. The
    sensing position is not captured in the PSR - Measurement association. Instead it is captured by the Measurement
    - Terminal association that is used to define the sensing location in the network topology. The location is
    defined by the connection of the Terminal to ConductingEquipment.

    If both a Terminal and PSR are associated, and the PSR is of type ConductingEquipment, the associated Terminal
    should belong to that ConductingEquipment instance.

    When the sensor location is needed both Measurement-PSR and Measurement-Terminal are used. The Measurement-Terminal
    association is never used alone.
    """

    power_system_resource_mrid: Optional[str] = None
    """The MRID of the power system resource that contains the measurement."""

    remote_source: Optional[RemoteSource] = None
    """The `zepben.evolve.cim.iec61970.base.scada.remote_source.RemoteSource` taking the `Measurement`"""

    terminal_mrid: Optional[str] = None
    """A measurement may be associated with a terminal in the network."""

    phases: PhaseCode = PhaseCode.ABC
    """Indicates to which phases the measurement applies and avoids the need to use 'measurementType' to also encode phase information 
    (which would explode the types). The phase information in Measurement, along with 'measurementType' and 'phases' uniquely defines a Measurement for a 
    device, based on normal network phase. Their meaning will not change when the computed energizing phasing is changed due to jumpers or other reasons. 
    If the attribute is missing three phases (ABC) shall be assumed."""

    unit_symbol: UnitSymbol = UnitSymbol.NONE
    """Specifies the type of measurement.  For example, this specifies if the measurement represents an indoor temperature, outdoor temperature, bus voltage, 
    line flow, etc. When the measurementType is set to "Specialization", the type of Measurement is defined in more detail by the specialized class which 
    inherits from Measurement."""


class Accumulator(Measurement):
    """Accumulator represents an accumulated (counted) Measurement, e.g. an energy value."""
    pass


class Analog(Measurement):
    """Analog represents an analog Measurement."""

    positive_flow_in: bool = False
    """If true then this measurement is an active power, reactive power or current with the convention that a positive value measured at the 
    Terminal means power is flowing into the related PowerSystemResource."""


class Discrete(Measurement):
    """Discrete represents a discrete Measurement, i.e. a Measurement representing discrete values, e.g. a Breaker position."""
    pass
