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

from zepben.cimbend.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.cimbend.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

__all__ = ["EnergySourcePhase"]


@dataclass
class EnergySourcePhase(PowerSystemResource):
    """
    A single phase of an energy source.

    Attributes:
        energy_source : The :class:`zepben.cimbend.iec61970.wires.EnergySource` with this ``EnergySourcePhase``
        phase : A :class:`zepben.cimbend.SinglePhaseKind`
                Phase of this energy source component. If the energy source is wye connected, the connection is from
                the indicated phase to the central ground or neutral point. If the energy source is delta connected,
                the phase indicates an energy source connected from the indicated phase to the next logical
                non-neutral phase.
    """
    energy_source: Optional[EnergySource] = None
    phase: SinglePhaseKind = SinglePhaseKind.NONE

