#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["ElectronicAddress"]

from dataclasses import dataclass


@dataclass
class ElectronicAddress:
    """
    Electronic address information.
    """

    email1: str | None = None
    """Primary email address."""
    is_primary: bool | None = None
    """[ZBEX] Whether this email is the primary address of the contact."""
    description: str | None = None
    """[ZBEX] A description for this email, e.g: work, personal."""
