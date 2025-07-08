#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["StreetDetail"]

from dataclasses import dataclass


@dataclass
class StreetDetail(object):
    """
    Street details, in the context of address.
    """

    building_name: str = ""
    """
    (if applicable) In certain cases the physical location of the place of interest does not have a direct point of entry from the street, 
    but may be located inside a larger structure such as a building, complex, office block, apartment, etc.
    """
    floor_identification: str = ""
    """The identification by name or number, expressed as text, of the floor in the building as part of this address."""
    name: str = ""
    """Name of the street."""
    number: str = ""
    """Designator of the specific location on the street."""
    suite_number: str = ""
    """Number of the apartment or suite."""
    type: str = ""
    """Type of street. Examples include: street, circle, boulevard, avenue, road, drive, etc."""
    display_address: str = ""
    """The address as it should be displayed to a user."""

    def all_fields_empty(self):
        """Check to see if all fields of this `StreetDetail` are empty."""
        return not (
            self.building_name or
            self.floor_identification or
            self.name or
            self.number or
            self.suite_number or
            self.type or
            self.display_address
        )
