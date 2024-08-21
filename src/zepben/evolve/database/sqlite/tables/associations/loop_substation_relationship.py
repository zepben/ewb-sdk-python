#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum

__all__ = ["LoopSubstationRelationship"]


class LoopSubstationRelationship(Enum):
    SUBSTATION_ENERGIZES_LOOP = 0
    LOOP_ENERGIZES_SUBSTATION = 1

    @property
    def short_name(self):
        return str(self)[27:]
