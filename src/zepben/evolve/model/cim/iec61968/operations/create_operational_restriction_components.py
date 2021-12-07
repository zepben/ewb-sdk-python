#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime
from typing import List

from zepben.evolve import *


def create_operational_restriction(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, title: str = "",
                                   created_date_time: datetime = None, author_name: str = "", type: str = "", status: str = "", comment: str = "",
                                   equipment: List[Equipment] = None) -> OperationalRestriction:
    """
    OperationalRestriction(Document(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    Document: title, created_date_time, author_name, type, status, comment
    OperationalRestriction: equipment
    """
    args = locals()
    return OperationalRestriction(**args)
