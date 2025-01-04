#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Optional
from dataclasses import dataclass
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

__all__ = ["PhaseImpedanceData"]


@dataclass(frozen=True)
class PhaseImpedanceData(object):
    """
    Impedance and conductance matrix element values. The diagonal elements are described by the elements having the same toPhase and fromPhase value and the
    off diagonal elements have different to_phase and from_phase values.
    """

    from_phase: SinglePhaseKind
    """Refer to the class description."""
    
    to_phase: SinglePhaseKind
    """Refer to the class description."""
    
    b: Optional[float] = None
    """Susceptance matrix element value, per length of unit."""

    g: Optional[float] = None
    """Conductance matrix element value, per length of unit."""

    r: Optional[float] = None
    """Resistance matrix element value, per length of unit."""

    x: Optional[float] = None
    """Reactance matrix element value, per length of unit."""
