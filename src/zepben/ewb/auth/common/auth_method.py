#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["AuthMethod"]

from enum import Enum


class AuthMethod(Enum):
    """
    An enum class that represents the different authentication methods that could be returned from the server's
    ewb/config/auth endpoint.
    """

    @classmethod
    def _missing_(cls, value: str):
        for member in cls:
            if member.value == value.upper():
                return member

    NONE = "NONE"
    SELF = "self"
    AUTH0 = "AUTH0"
    ENTRAID = "ENTRAID"
    OAUTH = "OAUTH"
