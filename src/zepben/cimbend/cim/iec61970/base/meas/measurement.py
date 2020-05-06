"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject

__all__ = ["Measurement"]


@dataclass
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

    Attributes -
        power_system_resource_mrid : The MRID of the power system resource that contains the measurement.
        remote_source : The :class:`scada.remote_source.RemoteSource` taking the ``Measurement``
    """

    power_system_resource_mrid: Optional[str] = None
    remote_source: Optional[RemoteSource] = None
