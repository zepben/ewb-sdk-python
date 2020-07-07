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
from enum import Enum
from typing import Optional

from zepben.cimbend.cim.iec61968.assets.asset import Asset

__all__ = ["Streetlight", "StreetlightLampKind"]


class StreetlightLampKind(Enum):
    UNKNOWN = 0
    HIGH_PRESSURE_SODIUM = 1
    MERCURY_VAPOR = 2
    METAL_HALIDE = 3
    OTHER = 4

    @property
    def short_name(self):
        return str(self)[20:]

@dataclass
class Streetlight(Asset):
    """
    A Streetlight asset.

    Attributes -
        pole : The :class:`zepben.cimbend.cim.iec61968.assets.pole.Pole` this Streetlight is attached to.
        light_rating : The power rating of the light in watts.
        lamp_kind : The kind of lamp.
    """

    pole: Optional[Pole] = None
    light_rating: int = 0
    lamp_kind: StreetlightLampKind = StreetlightLampKind.UNKNOWN
