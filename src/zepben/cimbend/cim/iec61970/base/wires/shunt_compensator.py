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


from dataclasses import dataclass

from zepben.cimbend.cim.iec61970.base.wires.energy_connection import RegulatingCondEq
from zepben.cimbend.cim.iec61970.base.wires.phase_shunt_connection_kind import PhaseShuntConnectionKind

__all__ = ["ShuntCompensator", "LinearShuntCompensator"]


@dataclass
class ShuntCompensator(RegulatingCondEq):
    """
    A shunt capacitor or reactor or switchable bank of shunt capacitors or reactors. A section of a shunt compensator
    is an individual capacitor or reactor.  A negative value for reactivePerSection indicates that the compensator is
    a reactor. ShuntCompensator is a single terminal device.  Ground is implied.

    Attributes -
        grounded : Used for Yn and Zn connections. True if the neutral is solidly grounded. nom_u : The voltage at which
        the nominal reactive power may be calculated. This should normally be within 10% of the voltage at which the
        capacitor is connected to the network.

        nom_u : The voltage at which the nominal reactive power may be calculated. This should normally be within 10%
                of the voltage at which the capacitor is connected to the network.
        phase_connection : The type of phase connection, such as wye or delta.
        sections : Shunt compensator sections in use. Starting value for steady state solution. Non integer values are
                   allowed to support continuous variables. The reasons for continuous value are to support study cases where no
                   discrete shunt compensator's has yet been designed, a solutions where a narrow voltage band force the sections to
                   oscillate or accommodate for a continuous solution as input.

                   For ``LinearShuntCompensator`` the value shall be between zero and ``ShuntCompensator.maximumSections``.
                   At value zero the shunt compensator conductance and admittance is zero. Linear interpolation of
                   conductance and admittance between the previous and next integer section is applied in case of
                   non-integer values.

                   For ``NonlinearShuntCompensator``s shall only be set to one of the
                   NonlinearShuntCompensatorPoint.sectionNumber. There is no interpolation between
                   NonlinearShuntCompensatorPoint-s.
    """
    grounded: bool = False
    nom_u: int = 0
    phase_connection: PhaseShuntConnectionKind = PhaseShuntConnectionKind.UNRECOGNIZED
    sections: float = 0.0


@dataclass
class LinearShuntCompensator(ShuntCompensator):
    """
    A linear shunt compensator has banks or sections with equal admittance values.

    Attributes -
        b0PerSection : Zero sequence shunt (charging) susceptance per section
        bPerSection : Positive sequence shunt (charging) susceptance per section
        g0PerSection : Zero sequence shunt (charging) conductance per section
        gPerSection : Positive sequence shunt (charging) conductance per section
    """
    b0_per_section: float = 0.0
    b_per_section: float = 0.0
    g0_per_section: float = 0.0
    g_per_section: float = 0.0
