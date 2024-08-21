#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum

__all__ = ["TableLocationStreetAddressField"]


class TableLocationStreetAddressField(Enum):
    mainAddress = 0
#     secondaryAddress = 1

    @property
    def short_name(self):
        return str(self)[32:]
