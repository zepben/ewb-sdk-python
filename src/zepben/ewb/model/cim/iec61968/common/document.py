#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Document"]

from datetime import datetime

from zepben.ewb.dataslot import dataslot
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject


@dataslot
class Document(IdentifiedObject):
    """
    Parent class for different groupings of information collected and managed as a part of a business process.
    It will frequently contain references to other objects, such as assets, people and power system resources.
    """
    title: str | None = None
    """Document title."""

    created_date_time: datetime | None = None
    """Date and time that this document was created."""

    author_name: str | None = None
    """Name of the author of this document."""

    type: str | None = None
    """Utility-specific classification of this document, according to its corporate standards, practices, 
    and existing IT systems (e.g., for management of assets, maintenance, work, outage, customers, etc.)."""

    status: str | None = None
    """Status of subject matter (e.g., Agreement, Work) this document represents."""

    comment: str | None = None
    """Free text comment"""
