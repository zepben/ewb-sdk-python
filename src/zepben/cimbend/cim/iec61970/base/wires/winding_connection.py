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

__all__ = ["WindingConnection"]


class WindingConnection(Enum):
    # Default
    UNKNOWN_WINDING = 0

    # Delta
    D = 1

    # Wye
    Y = 2

    # ZigZag
    Z = 3

    # Wye, with neutral brought out for grounding
    Yn = 4

    # ZigZag, with neutral brought out for grounding
    Zn = 5

    # Autotransformer common winding
    A = 6

    # Independent winding, for single-phase connections
    I = 7

    @property
    def short_name(self):
        return str(self)[18:]
