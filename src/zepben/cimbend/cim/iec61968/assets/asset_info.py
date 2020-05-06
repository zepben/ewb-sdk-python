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

from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject

__all__ = ["AssetInfo"]


class AssetInfo(IdentifiedObject):
    """
    Set of attributes of an asset, representing typical datasheet information of a physical device that can be
    instantiated and shared in different data exchange contexts:
        - as attributes of an asset instance (installed or in stock)
        - as attributes of an asset model (product by a manufacturer)
        - as attributes of a type asset (generic type of an asset as used in designs/extension planning).
    """
    pass

