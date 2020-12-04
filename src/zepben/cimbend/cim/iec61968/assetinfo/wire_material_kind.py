#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum


class WireMaterialKind(Enum):

    UNKNOWN = 0
    """UNKNOWN"""

    aaac = 1
    """Aluminum-alloy conductor steel reinforced."""

    acsr = 2
    """Aluminum conductor steel reinforced."""

    acsrAz = 3
    """Aluminum conductor steel reinforced, aluminumized steel core"""

    aluminum = 4
    """Aluminum wire."""

    aluminumAlloy = 5
    """Aluminum-alloy wire."""

    aluminumAlloySteel = 6
    """Aluminum-alloy-steel wire."""

    aluminumSteel = 7
    """Aluminum-steel wire."""

    copper = 8
    """Copper wire."""

    copperCadmium = 9
    """Copper cadmium wire."""

    other = 10
    """Other wire material."""

    steel = 11
    """Steel wire."""

    @property
    def short_name(self):
        return str(self)[17:]
