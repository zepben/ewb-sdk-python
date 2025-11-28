#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TownDetail"]

from dataclasses import dataclass


@dataclass
class TownDetail(object):
    """
    Town details, in the context of address.
    """

    name: str | None = None
    """Town name."""
    state_or_province: str | None = None
    """Name of the state or province."""
    country: str | None = None
    """Name of the country"""

    def all_fields_null_or_empty(self):
        """Check to see if all fields of this `TownDetail` are null or empty."""
        return not (self.name or self.state_or_province or self.country)

    def all_fields_null(self):
        """Check to see if all fields of this `TownDetail` are null"""
        return all((
            self.name is None,
            self.state_or_province is None,
            self.country is None
        ))
