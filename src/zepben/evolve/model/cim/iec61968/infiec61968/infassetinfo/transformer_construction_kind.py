#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum

__all__ = ["TransformerConstructionKind"]


class TransformerConstructionKind(Enum):
    """
    Kind of transformer construction.
    """

    unknown = 0
    """"""

    onePhase = 1
    """"""

    threePhase = 2
    """"""

    aerial = 3
    """"""

    overhead = 4
    """"""

    dryType = 5
    """"""

    network = 6
    """"""

    padmountDeadFront = 7
    """"""

    padmountFeedThrough = 8
    """"""

    padmountLiveFront = 9
    """"""

    padmountLoopThrough = 10
    """"""

    padmounted = 11
    """"""

    subway = 12
    """"""

    underground = 13
    """"""

    vault = 14
    """"""

    vaultThreePhase = 15
    """"""

    @property
    def short_name(self):
        return str(self)[28:]
