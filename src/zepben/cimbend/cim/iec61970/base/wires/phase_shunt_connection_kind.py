#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum

__all__ = ["PhaseShuntConnectionKind"]


class PhaseShuntConnectionKind(Enum):

    UNKNOWN = 0
    """Unknown `PhaseShuntConnectionKind`"""

    D = 1
    """Delta Connection"""

    Y = 2
    """Wye connection"""

    Yn = 3
    """Wye, with neutral brought out for grounding."""

    I = 4
    """Independent winding, for single-phase connections."""

    G = 5
    """Ground connection; use when explicit connection to ground needs to be expressed in combination with the phase code,
    such as for electrical wire/cable or for meters."""

    @property
    def short_name(self):
        return str(self)[25:]
