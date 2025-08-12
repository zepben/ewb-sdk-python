#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["NetworkState"]

from enum import Enum

from zepben.ewb import unique


@unique
class NetworkState(Enum):
    """
    Indicates which state of the network an operation should be performed on.
    """

    ALL = 0
    """
    The operation should be performed on all states of the network.
    """

    NORMAL = 1
    """
    The operation should be performed on the normal state of the network.
    """

    CURRENT = 2
    """
    The operation should be performed on the current state of the network.
    """

    @property
    def short_name(self):
        return str(self)[13:]
