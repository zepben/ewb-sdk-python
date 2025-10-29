#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["PerLengthSequenceImpedance"]

from typing import Optional

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.wires.per_length_impedance import PerLengthImpedance


@dataslot
class PerLengthSequenceImpedance(PerLengthImpedance):
    """
    Sequence impedance and admittance parameters per unit length, for transposed lines of 1, 2, or 3 phases.
    For 1-phase lines, define x=x0=xself. For 2-phase lines, define x=xs-xm and x0=xs+xm.

    Typically, one PerLengthSequenceImpedance is used for many ACLineSegments.
    """

    r: float | None = None
    """Positive sequence series resistance, per unit of length."""

    x: float | None = None
    """Positive sequence series reactance, per unit of length."""

    bch: float | None = None
    """Positive sequence shunt (charging) susceptance, per unit of length."""

    gch: float | None = None
    """Positive sequence shunt (charging) conductance, per unit of length."""

    r0: float | None = None
    """Zero sequence series resistance, per unit of length."""

    x0: float | None = None
    """Zero sequence series reactance, per unit of length."""

    b0ch: float | None = None
    """Zero sequence shunt (charging) susceptance, per unit of length."""

    g0ch: float | None = None
    """Zero sequence shunt (charging) conductance, per unit of length."""
