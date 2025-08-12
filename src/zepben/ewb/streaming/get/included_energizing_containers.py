#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["IncludedEnergizingContainers"]

from enum import Enum

from zepben.ewb.util import unique


@unique
class IncludedEnergizingContainers(Enum):
    """
    Indicates which energizing contains should be included when fetching a container.
    """

    NONE = 0
    """
    All energizing containers should be excluded.
    """

    FEEDERS = 1
    """
    Energizing feeders should be included.
    """

    SUBSTATIONS = 2
    """
    Energizing feeders and substations should be included.
    """

    @property
    def short_name(self):
        return str(self)[29:]
