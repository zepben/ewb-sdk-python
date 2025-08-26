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
class StreetAddress(object):
    """
    General purpose street and postal address information.
    """

    postal_code: Optional[str] = None
    """Postal code for the address."""
    town_detail: Optional[TownDetail] = None
    """Optional `TownDetail` for this address."""
    po_box: Optional[str] = None
    """Post office box for the address."""
    street_detail: Optional[StreetDetail] = None
    """Optional `StreetDetail` for this address."""
