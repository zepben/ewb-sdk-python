#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["IncludedEnergizedContainers"]

from enum import Enum

from zepben.ewb import unique


@unique
class IncludedEnergizedContainers(Enum):
    """
    Indicates which energized contains should be included when fetching a container.
    """

    NONE = 0
    """
    All energized containers should be excluded.
    """

    FEEDERS = 1
    """
    Energized HV feeders should be included.
    """

    LV_FEEDERS = 2
    """
    Energized HV feeders and LV feeders should be included.
    """

    @property
    def short_name(self):
        return str(self)[28:]
