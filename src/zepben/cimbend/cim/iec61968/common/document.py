"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""


from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject

__all__ = ["Document", "Agreement"]


@dataclass
class Document(IdentifiedObject):
    title: str = ""
    created_date_time: Optional[datetime] = None
    author_name: str = ""
    type: str = ""
    status: str = ""
    comment: str = ""


class Agreement(Document):
    pass
