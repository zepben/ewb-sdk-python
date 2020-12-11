#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime
from typing import Optional

from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject

__all__ = ["Document", "Agreement"]


class Document(IdentifiedObject):
    """
    Parent class for different groupings of information collected and managed as a part of a business process.
    It will frequently contain references to other objects, such as assets, people and power system resources.
    """
    title: str = ""
    """Document title."""

    created_date_time: Optional[datetime] = None
    """Date and time that this document was created."""

    author_name: str = ""
    """Name of the author of this document."""

    type: str = ""
    """Utility-specific classification of this document, according to its corporate standards, practices, 
    and existing IT systems (e.g., for management of assets, maintenance, work, outage, customers, etc.)."""

    status: str = ""
    """Status of subject matter (e.g., Agreement, Work) this document represents."""

    comment: str = ""
    """Free text comment"""


class Agreement(Document):
    """
    Formal agreement between two parties defining the terms and conditions for a set of services. The specifics of
    the services are, in turn, defined via one or more service agreements.
    """
    pass
