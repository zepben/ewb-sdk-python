#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.ewb.boilerplate.backfill import Backfill
from zepben.ewb.boilerplate.collections.lazy_list import LazyList
from zepben.ewb.boilerplate.collections.mrid_collection import S, MridCollection


class LazyMridList(LazyList[S], MridCollection[S]):
    """
    Nullable list implementation of :class:`MridCollection`.

    Inherits mRID lookup and uniqueness semantics from ``MridCollection`` and
    lazy backing-list behavior from ``LazyCollection``.
    """
    def __init__(
        self,
        private_field: list[S] | None,
        element_description: str,
        backfill: Backfill | None = None,
        validate=None,
        sort_by=None
    ) -> None:
        super().__init__(private_field, validate, sort_by)
        self.element_description = element_description
        self.backfill = backfill

    def _safe_get_by_mrid(self, mrid: str) -> S | None:
        existing = self._get()
        if existing is None:
            return None
        found = next((element for element in existing if element.mrid == mrid), None)
        return found

    def append(self, item: S) -> None:
        """
        Append an item to the collection.
        Check for mRID collisions with existing items.
        Optionally fill the backref field on the added item.
        Run optional validation.
        Sort the collection if key lambda is provided.
        """
        if not self._can_add_by_mrid(item):
            return

        if self.backfill is not None:
            self.backfill.apply(item, self._instance)

        super().append(item)
