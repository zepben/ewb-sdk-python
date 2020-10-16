#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum

__all__ = ["SinglePhaseKind", "phasekind_by_id"]


def phasekind_by_id(spk_id):
    """
    Get a SinglePhaseKind by its ID

    `spk_id` ID of the SinglePhaseKind from 0 as per the order of definition
    Returns The SinglePhaseKind
    """
    return _spk_members[spk_id]


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

    INVALID = (7, -1)
    """Invalid phase. Caused by trying to energise with multiple phases simultaneously."""

    @property
    def bit_mask(self):
        return 1 << self.mask_index if self.mask_index >= 0 else 0

    @property
    def value(self):
        return self.value[0]

    @property
    def mask_index(self):
        return self.value[1]

    @property
    def short_name(self):
        return str(self)[16:]


_spk_members = list(SinglePhaseKind.__members__.values())
