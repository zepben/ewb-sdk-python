#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Location"]

from typing import List, Optional, Generator, Callable

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61968.common.position_point import PositionPoint
from zepben.ewb.model.cim.iec61968.common.street_address import StreetAddress
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.util import require, nlen, ngen, safe_remove


@dataslot
@boilermaker
class Location(IdentifiedObject):
    """
    The place, scene, or point of something where someone or something has been, is, and/or will be at a given moment in time.
    It can be defined with one or more `PositionPoint`'s.
    """
    main_address: StreetAddress | None = None
    """Main address of the location."""

    position_points: List[PositionPoint] | None = ListAccessor()

    def _retype(self):
        self.position_points: ListRouter = ...
    
    @deprecated("BOILERPLATE: Use len(position_points) instead")
    def num_points(self):
        return len(self.position_points)

    @property
    def points(self) -> Generator[PositionPoint, None, None]:
        """
        Returns Generator over the `PositionPoint`s of this `Location`.
        """
        for point in ngen(self.position_points):
            yield point

    @custom_get(position_points)
    def get_point(self, sequence_number: int) -> PositionPoint:
        """
        Get the `sequence_number` `PositionPoint` for this `Location`.

        `sequence_number` The sequence number of the `PositionPoint` to get.
        Returns The `PositionPoint` identified by `sequence_number`
        Raises IndexError if this `Location` didn't contain `sequence_number` points.
        """
        return self.position_points.raw[sequence_number]

    def __getitem__(self, item):
        return self.get_point(item)

    def for_each_point(self, action: Callable[[int, PositionPoint], None]):
        """
        Call the `action` on each :class:`PositionPoint` in the `points` collection

        :param action: An action to apply to each :class:`PositionPoint` in the `points` collection, taking the index of the point, and the point itself.
        """
        for index, point in enumerate(self.points):
            action(index, point)

    def add_point(self, point: PositionPoint) -> Location:
        """
        Associate a `PositionPoint` with this `Location`, assigning it a sequence_number of `num_points`.
        `point` The `PositionPoint` to associate with this `Location`.
        Returns A reference to this `Location` to allow fluent use.
        """
        return self.insert_point(point)

    def insert_point(self, point: PositionPoint, sequence_number: int = None) -> Location:
        """
        Associate a `PositionPoint` with this `Location`

        `point` The `PositionPoint` to associate with this `Location`.
        `sequence_number` The sequence number of the `PositionPoint`.
        Returns A reference to this `Location` to allow fluent use.
        Raises `ValueError` if `sequence_number` < 0 or > `num_points()`.
        """
        if sequence_number is None:
            sequence_number = self.num_points()
        require(0 <= sequence_number <= self.num_points(),
                lambda: f"Unable to add PositionPoint to {str(self)}. Sequence number {sequence_number} "
                        f"is invalid. Expected a value between 0 and {self.num_points()}. Make sure you are "
                        f"adding the items in order and there are no gaps in the numbering.")
        self.position_points.insert_raw(sequence_number, point)
        return self

    def __setitem__(self, key, value):
        return self.insert_point(value, key)

    @deprecated("BOILERPLATE: Use position_points.remove() instead")
    def remove_point(self, point: PositionPoint) -> Location:
        """
        Remove a `PositionPoint` from this `Location`
        `point` The `PositionPoint` to remove.
        Raises `ValueError` if `point` was not part of this `Location`
        Returns A reference to this `Location` to allow fluent use.
        """
        self.position_points.remove(point)
        return self

    def remove_point_by_sequence_number(self, sequence_number: int) -> PositionPoint:
        """
        Remove a :class:`PositionPoint` from this :class:`Location` by its sequence number.

        NOTE: This will update the sequence numbers of all items located after the removed sequence number.

        :param sequence_number: The sequence number of the `PositionPoint` to remove.
        :return: The :class:`PositionPoint` that was removed, or null if there was no :class:`PositionPoint` for the given `sequenceNumber`.
        :raises IndexError: If no :class:`PositionPoint` with the specified `sequence_number` was not associated with this :class:`Location`.
        """
        point = self.get_point(sequence_number)
        self.position_points.raw.remove(point)
        return point

    @deprecated("BOILERPLATE: Use position_points.clear() instead")
    def clear_points(self) -> Location:
        return self.position_points.clear()
        return self
