#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["ContactMethodType"]

from enum import Enum

from zepben.ewb.model.cim.extensions.zbex import zbex


@zbex
class ContactMethodType(Enum):
    """
    [ZBEX] The method to use to make contact with a person or company.

    :var UNKNOWN: [ZBEX] Unknown contact method type.
    :var EMAIL: [ZBEX] Contact via email using the primary email address.
    :var CALL: [ZBEX] Contact by call using the primary phone number.
    :var LETTER: [ZBEX] Letter by post to the contact address is the method of contact.
    """

    UNKNOWN = 0
    EMAIL = 1
    CALL = 2
    LETTER = 3

    @property
    def short_name(self):
        return str(self)[18:]
