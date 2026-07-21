#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Location"]

from dataclasses import field
from typing import List, Optional, Callable, Any

from typing_extensions import deprecated

from zepben.ewb import Alias
from zepben.ewb.dataclass_descriptors.dataclass_base import zb_dataclass
from zepben.ewb.dataclass_descriptors.lazy_list import LazyIndexedList
from zepben.ewb.model.cim.iec61968.common.position_point import PositionPoint
from zepben.ewb.model.cim.iec61968.common.street_address import StreetAddress
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject


@zb_dataclass
class Location(IdentifiedObject):
    """
    The place, scene, or point of something where someone or something has been, is, and/or will be at a given moment in time.
    It can be defined with one or more `PositionPoint`'s.
    """
    main_address: Optional[StreetAddress] = None
    """Main address of the location."""

    _position_points: Optional[List[PositionPoint]] = field(default=None)

    points: LazyIndexedList[PositionPoint] = LazyIndexedList(
        _position_points,
        "PositionPoint",
    )
    position_points = Alias(points)


    # region deprecated list boilerplate
    #
    # ("region/endregion" is an IntelliJ feature letting you hide the entire thing)
    # This boilerplate exists solely to enable backwards compatibility.
    # It will be removed eventually.
    # Every single method simply forwards the call to the corresponding list.

    # region points boilerplate

    @deprecated("Use points.for_each_indexed(action) instead.")
    def for_each_point(
        self,
        action: Callable[[int, PositionPoint], Any],
    ):
        self.points.for_each_indexed(action)

    @deprecated("Use len(points) instead.")
    def num_points(self):
        return len(self.points)

    @deprecated("Use points[sequence_number] instead.")
    def get_point(self, sequence_number: int) -> PositionPoint:
        return self.points[sequence_number]

    @deprecated("Use points[item] instead.")
    def __getitem__(self, item: int) -> PositionPoint:
        return self.points[item]

    @deprecated("Use points.append(point) instead.")
    def add_point(self, point: PositionPoint) -> Location:
        self.points.append(point)
        return self

    @deprecated("Use points.insert(sequence_number, point)")
    def insert_point(
        self,
        point: PositionPoint,
        sequence_number: int | None = None,
    ) -> Location:
        if sequence_number is None: sequence_number = len(self.points)
        self.points.insert(sequence_number, point)

        return self

    @deprecated("Use points.insert(key, value) instead.")
    def __setitem__(
        self,
        key: int,
        value: PositionPoint,
    ) -> None:
        self.points.insert(key, value)

    @deprecated("Use points.remove(point) instead.")
    def remove_point(self, point: PositionPoint) -> Location:
        self.points.remove(point)
        return self

    @deprecated("Use points.pop(sequence_number) instead.")
    def remove_point_by_sequence_number(
        self,
        sequence_number: int,
    ) -> PositionPoint:
        return self.points.pop(sequence_number)

    @deprecated("Use points.clear() instead.")
    def clear_points(self) -> Location:
        self.points.clear()
        return self

    # endregion

    # endregion
