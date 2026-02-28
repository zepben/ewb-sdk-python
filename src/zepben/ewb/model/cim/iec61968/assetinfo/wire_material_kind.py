#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["WireMaterialKind"]

from enum import Enum

from zepben.ewb import unique


@unique
class WireMaterialKind(Enum):
    """
    Kind of wire material.
    :var UNKNOWN: Unknown material kind.
    :var aaac: Aluminum-alloy conductor steel reinforced.
    :var acsr: Aluminum conductor steel reinforced.
    :var acsrAz: Aluminum conductor steel reinforced, aluminumized steel core
    :var aluminium: Aluminum wire.
    :var aluminiumAlloy: Aluminum-alloy wire.
    :var aluminiumAlloySteel: Aluminum-alloy-steel wire.
    :var aluminiumSteel: Aluminum-steel wire.
    :var copper: Copper wire.
    :var copperCadmium: Copper cadmium wire.
    :var other: Other wire material.
    :var steel: Steel wire.
    """

    UNKNOWN = 0

    aaac = 1

    acsr = 2

    acsrAz = 3

    aluminum = 4

    aluminumAlloy = 5

    aluminumAlloySteel = 6

    aluminumSteel = 7

    copper = 8

    copperCadmium = 9

    other = 10

    steel = 11

    @property
    def short_name(self):
        return str(self)[17:]
