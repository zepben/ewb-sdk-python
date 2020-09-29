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

from enum import Enum

__all__ = ["PhaseShuntConnectionKind"]


class PhaseShuntConnectionKind(Enum):

    UNKNOWN = 0

    # Delta Connection
    D = 1

    # Wye connection
    Y = 2

    # Wye, with neutral brought out for grounding.
    Yn = 3

    # Independent winding, for single-phase connections.
    I = 4

    # Ground connection; use when explicit connection to ground needs to be expressed in combination with the phase
    # code, such as for electrical wire/cable or for meters.
    G = 5

    @property
    def short_name(self):
        return str(self)[25:]
