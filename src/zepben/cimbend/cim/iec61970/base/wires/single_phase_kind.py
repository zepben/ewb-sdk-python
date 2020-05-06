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

__all__ = ["SinglePhaseKind"]


class SinglePhaseKind(Enum):
    NONE = (0, -1)
    A = (1, 0)
    B = (2, 1)
    C = (3, 2)
    N = (4, 3)
    X = (5, 0)
    Y = (6, 1)
    INVALID = (7, -1)

    @property
    def bit_mask(self):
        return 1 << self.mask_index if self.mask_index >= 0 else 0

    @property
    def mask_index(self):
        return self.value[1]

    @property
    def short_name(self):
        return str(self)[16:]
