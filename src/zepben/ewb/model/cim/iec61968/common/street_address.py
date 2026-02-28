#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["StreetAddress"]

from dataclasses import dataclass
from typing import Optional

from zepben.ewb.model.cim.iec61968.common.street_detail import StreetDetail
from zepben.ewb.model.cim.iec61968.common.town_detail import TownDetail


@dataclass
class StreetAddress:
    """
    General purpose street and postal address information.

    :var postal_code: Postal code for the address.
    :var town_detail: Optional :class:`TownDetail` for this address.
    :var po_box: Post office box for the address.
    :var street_detail: Optional :class:`StreetDetail` for this address.
    """

    postal_code: str | None = None
    town_detail: TownDetail | None = None
    po_box: str | None = None
    street_detail: StreetDetail | None = None

    def __init__(self, postal_code=None, town_detail=None, po_box=None, street_detail=None):
        self.postal_code = str(postal_code) if postal_code is not None else None
        self.town_detail = town_detail
        self.po_box = str(po_box) if po_box is not None else None
        self.street_detail = street_detail

    def all_fields_null_or_empty(self):
        """Check to see if all fields of this `TownDetail` are null or empty."""
        return not (self.postal_code or self.town_detail or self.po_box or self.street_detail)

    def all_fields_null(self):
        """Check to see if all fields of this `TownDetail` are null"""
        return all((
            self.postal_code is None,
            self.town_detail is None,
            self.po_box is None,
            self.street_detail is None
        ))
