#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum, unique

from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

__all__ = ["PhaseCode", "phase_code_by_id"]


def phase_code_by_id(value: int):
    """
    Get a PhaseCode by its value

    `value` ID of the PhaseCode from 0 as per the order of definition
    Returns The PhaseCode
    """
    return _PHASE_CODE_VALUES[value]


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

    NONE = (0, [SinglePhaseKind.NONE])
    """No phases specified"""

    A = (1, [SinglePhaseKind.A])
    """Phase A"""

    B = (2, [SinglePhaseKind.B])
    """Phase B"""

    C = (3, [SinglePhaseKind.C])
    """Phase C"""

    N = (4, [SinglePhaseKind.N])
    """Neutral Phase"""

    AB = (5, [SinglePhaseKind.A, SinglePhaseKind.B])
    """Phases A and B"""

    AC = (6, [SinglePhaseKind.A, SinglePhaseKind.C])
    """Phases A and C"""

    AN = (7, [SinglePhaseKind.A, SinglePhaseKind.N])
    """Phases A and N"""

    BC = (8, [SinglePhaseKind.B, SinglePhaseKind.C])
    """Phases B and C"""

    BN = (9, [SinglePhaseKind.B, SinglePhaseKind.N])
    """Phases B and N"""

    CN = (10, [SinglePhaseKind.C, SinglePhaseKind.N])
    """Phases C and N"""

    ABC = (11, [SinglePhaseKind.A, SinglePhaseKind.B, SinglePhaseKind.C])
    """Phases A, B and C"""

    ABN = (12, [SinglePhaseKind.A, SinglePhaseKind.B, SinglePhaseKind.N])
    """Phases A, B and neutral"""

    ACN = (13, [SinglePhaseKind.A, SinglePhaseKind.C, SinglePhaseKind.N])
    """Phases A, C and neutral"""

    BCN = (14, [SinglePhaseKind.B, SinglePhaseKind.C, SinglePhaseKind.N])
    """Phases B, C and neutral"""

    ABCN = (15, [SinglePhaseKind.A, SinglePhaseKind.B, SinglePhaseKind.C, SinglePhaseKind.N])
    """Phases A, B, C and neutral"""

    X = (16, [SinglePhaseKind.X])
    """Unknown non-neutral phase"""

    XN = (17, [SinglePhaseKind.X, SinglePhaseKind.N])
    """Unknown non-neutral phase plus neutral"""

    XY = (18, [SinglePhaseKind.X, SinglePhaseKind.Y])
    """Two Unknown non-neutral phases"""

    XYN = (19, [SinglePhaseKind.X, SinglePhaseKind.Y, SinglePhaseKind.N])
    """Two Unknown non-neutral phases plus neutral"""

    Y = (20, [SinglePhaseKind.Y])
    """Unknown non-neutral phase"""

    YN = (21, [SinglePhaseKind.Y, SinglePhaseKind.N])
    """Unknown non-neutral phase plus neutral"""

    s1 = (22, [SinglePhaseKind.s1])
    """Secondary phase 1"""

    s1N = (23, [SinglePhaseKind.s1, SinglePhaseKind.N])
    """Secondary phase 1 plus neutral"""

    s12 = (24, [SinglePhaseKind.s1, SinglePhaseKind.s2])
    """Secondary phase 1 and 2"""

    s12N = (25, [SinglePhaseKind.s1, SinglePhaseKind.s2, SinglePhaseKind.N])
    """Secondary phases 1, 2, and neutral"""

    s2 = (26, [SinglePhaseKind.s2])
    """Secondary phase 2"""

    s2N = (27, [SinglePhaseKind.s2, SinglePhaseKind.N])
    """Secondary phase 2 plus neutral"""

    @property
    def short_name(self):
        return str(self)[10:]

    @property
    def single_phases(self):
        return self.value[1]

    @property
    def num_phases(self):
        return len(self.value)


_PHASE_CODE_VALUES = list(PhaseCode.__members__.values())
