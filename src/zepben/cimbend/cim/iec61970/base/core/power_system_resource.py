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


from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject

__all__ = ['PowerSystemResource']


@dataclass
class PowerSystemResource(IdentifiedObject):
    """
    Abstract class, should only be used through subclasses.
    A power system resource can be an item of equipment such as a switch, an equipment container containing many individual
    items of equipment such as a substation, or an organisational entity such as sub-control area. Power system resources
    can have measurements associated.

    Attributes -
        - location : A :class:`zepben.cimbend.Location` for this resource.
        - asset_info : A subclass of :class:`zepben.cimbend.AssetInfo` providing information about the asset associated
                       with this PowerSystemResource.
    """

    location: Optional[Location] = None
    asset_info: Optional[AssetInfo] = None

