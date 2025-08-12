#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["StreetlightLampKind"]

from enum import Enum

from zepben.ewb import unique


@unique
class StreetlightLampKind(Enum):
    """
    Kind of lamp for a `Streetlight`
    """

    UNKNOWN = 0
    HIGH_PRESSURE_SODIUM = 1
    MERCURY_VAPOR = 2
    METAL_HALIDE = 3
    OTHER = 4

    @property
    def short_name(self):
        return str(self)[20:]
