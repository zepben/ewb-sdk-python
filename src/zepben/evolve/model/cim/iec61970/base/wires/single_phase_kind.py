#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum
from typing import Union

#
# NOTE: The following import is actually at the bottom of this file to avoid cyclic imports.
#
# from zepben.evolve.model.cim.iec61970.base.core.phase_code import phase_code_from_single_phases, PhaseCode

__all__ = ["SinglePhaseKind", "single_phase_kind_by_id", "SINGLE_PHASE_KIND_VALUES"]


def single_phase_kind_by_id(value):
    """
    Get a SinglePhaseKind by its value

    `value` ID of the SinglePhaseKind from 0 as per the order of definition
    Returns The SinglePhaseKind
    """
    return SINGLE_PHASE_KIND_VALUES[value]


class SinglePhaseKind(Enum):
    """Enumeration of single phase identifiers. Allows designation of single phases for both transmission and distribution equipment, circuits and loads."""

    NONE = (0, -1)
    """No phase specified"""

    A = (1, 0)
    """Phase A"""

    B = (2, 1)
    """Phase B"""

    C = (3, 2)
    """Phase C"""

    N = (4, 3)
    """Neutral"""

    X = (5, 0)
    """An unknown primary phase."""

    Y = (6, 1)
    """An unknown primary phase."""

    s1 = (7, 0)
    """Secondary phase 1."""

    s2 = (8, 1)
    """Secondary phase 2."""

    INVALID = (9, -1)
    """Invalid phase. Caused by trying to energise with multiple phases simultaneously."""

    @property
    def bit_mask(self):
        return 1 << self.mask_index if self.mask_index >= 0 else 0

    @property
    def id(self):
        return self.value[0]

    @property
    def mask_index(self):
        return self.value[1]

    @property
    def short_name(self):
        return str(self)[16:]

    def __lt__(self, other):
        return self.id < other.id

    def __add__(self, other: Union['SinglePhaseKind', 'PhaseCode']) -> 'PhaseCode':
        if isinstance(other, SinglePhaseKind):
            return phase_code_from_single_phases({self, other})
        elif isinstance(other, PhaseCode):
            return phase_code_from_single_phases(set(other.single_phases + [self]))
        else:
            return PhaseCode.NONE

    def __sub__(self, other: Union['SinglePhaseKind', 'PhaseCode']) -> 'PhaseCode':
        if isinstance(other, SinglePhaseKind):
            return phase_code_from_single_phases({} if (self == other) else {self})
        elif isinstance(other, PhaseCode):
            return phase_code_from_single_phases({} if (self in other) else {self})
        else:
            return PhaseCode.NONE


SINGLE_PHASE_KIND_VALUES = list(SinglePhaseKind.__members__.values())

#
# NOTE: The following import is deliberately at the bottom of this file to avoid cyclic imports.
#
from zepben.evolve.model.cim.iec61970.base.core.phase_code import phase_code_from_single_phases, PhaseCode  # noqa: E402
