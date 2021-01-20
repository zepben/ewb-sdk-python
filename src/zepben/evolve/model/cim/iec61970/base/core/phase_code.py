#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum, unique

from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

__all__ = ["PhaseCode", "phasecode_by_id"]


def phasecode_by_id(id: int):
    return _phasecode_members[id]


@unique
class PhaseCode(Enum):
    """
    An unordered enumeration of phase identifiers.  Allows designation of phases for both transmission and distribution equipment,
    circuits and loads. The enumeration, by itself, does not describe how the phases are connected together or connected to ground.
    Ground is not explicitly denoted as a phase.

    Residential and small commercial loads are often served from single-phase, or split-phase, secondary circuits. For example of s12N,
    phases 1 and 2 refer to hot wires that are 180 degrees out of phase, while N refers to the neutral wire. Through single-phase
    transformer connections, these secondary circuits may be served from one or two of the primary phases A, B, and C. For three-phase
    loads, use the A, B, C phase codes instead of s12N.
    """

    NONE = (SinglePhaseKind.NONE,)
    """No phases specified"""

    A = (SinglePhaseKind.A,)
    """Phase A"""

    B = (SinglePhaseKind.B,)
    """Phase B"""

    C = (SinglePhaseKind.C,)
    """Phase C"""

    N = (SinglePhaseKind.N,)
    """Neutral Phase"""

    AB = (SinglePhaseKind.A, SinglePhaseKind.B)
    """Phases A and B"""

    AC = (SinglePhaseKind.A, SinglePhaseKind.C)
    """Phases A and C"""

    AN = (SinglePhaseKind.A, SinglePhaseKind.N)
    """Phases A and N"""

    BC = (SinglePhaseKind.B, SinglePhaseKind.C)
    """Phases B and C"""

    BN = (SinglePhaseKind.B, SinglePhaseKind.N)
    """Phases B and N"""

    CN = (SinglePhaseKind.C, SinglePhaseKind.N)
    """Phases C and N"""

    ABC = (SinglePhaseKind.A, SinglePhaseKind.B, SinglePhaseKind.C)
    """Phases A, B and C"""

    ABN = (SinglePhaseKind.A, SinglePhaseKind.B, SinglePhaseKind.N)
    """Phases A, B and neutral"""

    ACN = (SinglePhaseKind.A, SinglePhaseKind.C, SinglePhaseKind.N)
    """Phases A, C and neutral"""

    BCN = (SinglePhaseKind.B, SinglePhaseKind.C, SinglePhaseKind.N)
    """Phases B, C and neutral"""

    ABCN = (SinglePhaseKind.A, SinglePhaseKind.B, SinglePhaseKind.C, SinglePhaseKind.N)
    """Phases A, B, C and neutral"""

    X = (SinglePhaseKind.X,)
    """Unknown non-neutral phase"""

    XN = (SinglePhaseKind.X, SinglePhaseKind.N)
    """Unknown non-neutral phase plus neutral"""

    XY = (SinglePhaseKind.X, SinglePhaseKind.Y)
    """Two Unknown non-neutral phases"""

    XYN = (SinglePhaseKind.X, SinglePhaseKind.Y, SinglePhaseKind.N)
    """Two Unknown non-neutral phases plus neutral"""

    Y = (SinglePhaseKind.Y,)
    """Unknown non-neutral phase"""

    YN = (SinglePhaseKind.Y, SinglePhaseKind.N)
    """Unknown non-neutral phase plus neutral"""

    @property
    def short_name(self):
        return str(self)[10:]

    @property
    def single_phases(self):
        return self.value

    @property
    def num_phases(self):
        return len(self.value)


_phasecode_members = list(PhaseCode.__members__.values())
