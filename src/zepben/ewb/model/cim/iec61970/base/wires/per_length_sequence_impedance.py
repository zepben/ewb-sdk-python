#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["PerLengthSequenceImpedance"]

from typing import Optional

from zepben.ewb.model.cim.iec61970.base.wires.per_length_impedance import PerLengthImpedance


class PerLengthSequenceImpedance(PerLengthImpedance):
    """
    Sequence impedance and admittance parameters per unit length, for transposed lines of 1, 2, or 3 phases.
    For 1-phase lines, define x=x0=xself. For 2-phase lines, define x=xs-xm and x0=xs+xm.

    Typically, one PerLengthSequenceImpedance is used for many ACLineSegments.
    """

    r: Optional[float] = None
    """Positive sequence series resistance, per unit of length."""

    x: Optional[float] = None
    """Positive sequence series reactance, per unit of length."""

    bch: Optional[float] = None
    """Positive sequence shunt (charging) susceptance, per unit of length."""

    gch: Optional[float] = None
    """Positive sequence shunt (charging) conductance, per unit of length."""

    r0: Optional[float] = None
    """Zero sequence series resistance, per unit of length."""

    x0: Optional[float] = None
    """Zero sequence series reactance, per unit of length."""

    b0ch: Optional[float] = None
    """Zero sequence shunt (charging) susceptance, per unit of length."""

    g0ch: Optional[float] = None
    """Zero sequence shunt (charging) conductance, per unit of length."""
