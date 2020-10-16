#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.cimbend.cim.iec61970.base.wires.energy_connection import RegulatingCondEq
from zepben.cimbend.cim.iec61970.base.wires.phase_shunt_connection_kind import PhaseShuntConnectionKind

__all__ = ["ShuntCompensator", "LinearShuntCompensator"]


class ShuntCompensator(RegulatingCondEq):
    """
    A shunt capacitor or reactor or switchable bank of shunt capacitors or reactors. A section of a shunt compensator
    is an individual capacitor or reactor.  A negative value for reactivePerSection indicates that the compensator is
    a reactor. ShuntCompensator is a single terminal device.  Ground is implied.
    """
    grounded: bool = False
    """Used for Yn and Zn connections. True if the neutral is solidly grounded. nom_u : The voltage at which the nominal reactive power may be calculated. 
    This should normally be within 10% of the voltage at which the capacitor is connected to the network."""

    nom_u: int = 0
    """The voltage at which the nominal reactive power may be calculated. This should normally be within 10% of the voltage at which the capacitor is connected 
    to the network."""

    phase_connection: PhaseShuntConnectionKind = PhaseShuntConnectionKind.UNKNOWN
    """The type of phase connection, such as wye or delta."""

    sections: float = 0.0
    """
    Shunt compensator sections in use. Starting value for steady state solution. Non integer values are allowed to support continuous variables. The 
    reasons for continuous value are to support study cases where no discrete shunt compensator's has yet been designed, a solutions where a narrow voltage 
    band force the sections to oscillate or accommodate for a continuous solution as input. 
    
    For `LinearShuntCompensator` the value shall be between zero and `ShuntCompensator.maximumSections`. At value zero the shunt compensator conductance and 
    admittance is zero. Linear interpolation of conductance and admittance between the previous and next integer section is applied in case of non-integer 
    values. 
    
    For `NonlinearShuntCompensator`s shall only be set to one of the NonlinearShuntCompensatorPoint.sectionNumber. There is no interpolation between 
    NonlinearShuntCompensatorPoint-s.
    """


class LinearShuntCompensator(ShuntCompensator):
    """A linear shunt compensator has banks or sections with equal admittance values."""

    b0_per_section: float = 0.0
    """Zero sequence shunt (charging) susceptance per section"""

    b_per_section: float = 0.0
    """Positive sequence shunt (charging) susceptance per section"""

    g0_per_section: float = 0.0
    """Zero sequence shunt (charging) conductance per section"""

    g_per_section: float = 0.0
    """Positive sequence shunt (charging) conductance per section"""
