#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["StreetDetail"]

from dataclasses import dataclass
from typing import Optional


@dataclass
class StreetDetail(object):
    """
    Street details, in the context of address.
    """

    building_name: Optional[str] = None
    """
    (if applicable) In certain cases the physical location of the place of interest does not have a direct point of entry from the street, 
    but may be located inside a larger structure such as a building, complex, office block, apartment, etc.
    """
    floor_identification: str | None = None
    """The identification by name or number, expressed as text, of the floor in the building as part of this address."""
    name: str | None = None
    """Name of the street."""
    number: str | None = None
    """Designator of the specific location on the street."""
    suite_number: str | None = None
    """Number of the apartment or suite."""
    type: str | None = None
    """Type of street. Examples include: street, circle, boulevard, avenue, road, drive, etc."""
    display_address: str | None = None
    """The address as it should be displayed to a user."""
    building_number: str | None = None
    """[ZBEX] The number of the building."""

    def all_fields_empty(self):
        """Check to see if all fields of this `StreetDetail` are empty."""
        return not any(
            (
                self.building_name,
                self.floor_identification,
                self.name,
                self.number,
                self.suite_number,
                self.type,
                self.display_address,
                self.building_number,
            )
        )

    def all_fields_null(self):
        """Check to see if all fields of this `StreetDetail` are null."""
        return all(
            (
                self.building_name is None,
                self.floor_identification is None,
                self.name is None,
                self.number is None,
                self.suite_number is None,
                self.type is None,
                self.display_address is None,
                self.building_number is None,
            ))
