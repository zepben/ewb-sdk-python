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


class WireMaterialKind(Enum):
    # @property UNKNOWN
    UNKNOWN = 0

    # Aluminum-alloy conductor steel reinforced.
    aaac = 1

    # Aluminum conductor steel reinforced.
    acsr = 2

    # Aluminum conductor steel reinforced, aluminumized steel core
    acsrAz = 3

    # Aluminum wire.
    aluminum = 4

    # Aluminum-alloy wire.
    aluminumAlloy = 5

    # Aluminum-alloy-steel wire.
    aluminumAlloySteel = 6

    # Aluminum-steel wire.
    aluminumSteel = 7

    # Copper wire.
    copper = 8

    # Copper cadmium wire.
    copperCadmium = 9

    # Other wire material.
    other = 10

    # Steel wire.
    steel = 11

    @property
    def short_name(self):
        return str(self)[16:]
