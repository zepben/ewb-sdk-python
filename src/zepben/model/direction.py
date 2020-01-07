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


class Direction(Enum):
    NONE = 0
    IN = 1
    OUT = 2
    BOTH = 3

    def has(self, other):
        """
        Check whether this Direction contains Direction other.
        :param other: A `Direction` to compare against.
        :return: True if this is BOTH and other is not NONE, otherwise False
        """
        if self is Direction.BOTH:
            return other is not Direction.NONE
        else:
            return self is other

    @property
    def short_name(self):
        return str(self)[10:]
