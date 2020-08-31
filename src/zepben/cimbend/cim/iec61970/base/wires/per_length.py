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

from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject

__all__ = ["PerLengthLineParameter", "PerLengthImpedance", "PerLengthSequenceImpedance"]


class PerLengthLineParameter(IdentifiedObject):
    """ Common type for per-length electrical catalogues describing line parameters. """
    pass


class PerLengthImpedance(PerLengthLineParameter):
    """ Common type for per-length impedance electrical catalogues. """
    pass


@dataclass
class PerLengthSequenceImpedance(PerLengthImpedance):
    """
    Sequence impedance and admittance parameters per unit length, for transposed lines of 1, 2, or 3 phases.
    For 1-phase lines, define x=x0=xself. For 2-phase lines, define x=xs-xm and x0=xs+xm.

    Typically, one PerLengthSequenceImpedance is used for many ACLineSegments.

    Attributes -
        r : Positive sequence series resistance, per unit of length.
        x : Positive sequence series reactance, per unit of length.
        r0 : Zero sequence series resistance, per unit of length.
        x0 : Zero sequence series reactance, per unit of length.
        b0ch : Zero sequence shunt (charging) susceptance, per unit of length.
        bch : Positive sequence shunt (charging) susceptance, per unit of length.
        gch : Positive sequence shunt (charging) conductance, per unit of length.
        g0ch : Zero sequence shunt (charging) conductance, per unit of length.

    """

    r: float = 0.0
    x: float = 0.0
    bch: float = 0.0
    gch: float = 0.0
    r0: float = 0.0
    x0: float = 0.0
    b0ch: float = 0.0
    g0ch: float = 0.0
