#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject

__all__ = ["PerLengthLineParameter", "PerLengthImpedance", "PerLengthSequenceImpedance"]


class PerLengthLineParameter(IdentifiedObject):
    """Common type for per-length electrical catalogues describing line parameters."""
    pass


class PerLengthImpedance(PerLengthLineParameter):
    """Common type for per-length impedance electrical catalogues."""
    pass


class PerLengthSequenceImpedance(PerLengthImpedance):
    """
    Sequence impedance and admittance parameters per unit length, for transposed lines of 1, 2, or 3 phases.
    For 1-phase lines, define x=x0=xself. For 2-phase lines, define x=xs-xm and x0=xs+xm.

    Typically, one PerLengthSequenceImpedance is used for many ACLineSegments.
    """

    r: float = 0.0
    """Positive sequence series resistance, per unit of length."""

    x: float = 0.0
    """Positive sequence series reactance, per unit of length."""

    bch: float = 0.0
    """Positive sequence shunt (charging) susceptance, per unit of length."""

    gch: float = 0.0
    """Positive sequence shunt (charging) conductance, per unit of length."""

    r0: float = 0.0
    """Zero sequence series resistance, per unit of length."""

    x0: float = 0.0
    """Zero sequence series reactance, per unit of length."""

    b0ch: float = 0.0
    """Zero sequence shunt (charging) susceptance, per unit of length."""

    g0ch: float = 0.0
    """Zero sequence shunt (charging) conductance, per unit of length."""
