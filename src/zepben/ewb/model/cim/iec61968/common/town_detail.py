#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TownDetail"]

from dataclasses import dataclass
from typing import Optional


@dataclass
class TownDetail(object):
    """
    Town details, in the context of address.
    """

    name: Optional[str] = None
    """Town name."""
    state_or_province: Optional[str] = None
    """Name of the state or province."""

    def all_fields_null_or_empty(self):
        """Check to see if all fields of this `TownDetail` are null or empty."""
        return not (self.name or self.state_or_province)
