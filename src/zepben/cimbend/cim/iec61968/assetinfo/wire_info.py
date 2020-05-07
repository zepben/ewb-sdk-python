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

from zepben.cimbend.cim.iec61968.assetinfo.wire_material_kind import WireMaterialKind
from zepben.cimbend.cim.iec61968.assets.asset_info import AssetInfo

__all__ = ["WireInfo", "CableInfo", "OverheadWireInfo"]


@dataclass
class WireInfo(AssetInfo):
    """
    Wire data that can be specified per line segment phase, or for the line segment as a whole in case its phases all
    have the same wire characteristics

    Attributes -
        rated_current : Current carrying capacity of the wire under stated thermal conditions.
        material : :class:`zepben.protobuf.cim.iec61968.assetinfo.WireMaterialKind` - Conductor material.
    """
    rated_current: float = 0.0
    material: WireMaterialKind = WireMaterialKind.UNKNOWN


@dataclass
class CableInfo(WireInfo):
    """
    Cable data. A cable is an underground conductor.
    """
    pass


@dataclass
class OverheadWireInfo(WireInfo):
    """
    Overhead wire data. A "wire" is an above ground conductor.
    """
    pass

