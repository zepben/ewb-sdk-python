#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Sequence

from typing_extensions import Self

from zepben.ewb.boilerplate.backfill import Backfill
from zepben.ewb.boilerplate.collections.abstract_mrid_list import AbstractMridList
from zepben.ewb.boilerplate.collections.mrid_collection import S
from zepben.ewb.boilerplate.collections.wrapper import _IterableWrapper


class MridList(_IterableWrapper[S], AbstractMridList[S]):
    """An mRID collection backed by a non-nullable list.

    Items retain list order and are retrieved by mRID using a linear search.
    Without a sort selector this is insertion order; when sorting is configured,
    the list is reordered after successful additions and disregarded re-adds of
    the same instance. Appending enforces mRID uniqueness and can optionally
    apply backfill and validation.

    Unlike ``LazyMridList``, clearing the collection leaves an empty backing list
    rather than resetting the backing field to ``None``.
    """
    def __init__(
        self,
        private_field: list[S],
        element_description: str,
        backfill: Backfill | None = None,
        validate=None,
        sort_by=None
    ) -> None:
        super().__init__(private_field)
        self.element_description = element_description
        self.backfill = backfill
        self.validate = validate
        self.sort_by = sort_by
        self._backing_list = None

    def __get__(self, instance, owner=None) -> Self:
        obj = super().__get__(instance, owner)
        if obj is not self:
            # noinspection PyUnresolvedReferences
            obj.__post_init__()
        return obj

    def __post_init__(self) -> None:
        self._backing_list = getattr(self._instance, self._backing_name)

    def _get_collection(self) -> Sequence[S]:
        """Return the backing list."""
        return self._backing_list

    def _safe_get_by_mrid(self, mrid: str) -> S | None:
        """Return the element with ``mrid``, or ``None``."""
        found = next((element for element in self._backing_list if element.mrid == mrid), None)
        return found

    def _append_raw(self, item: S) -> None:
        self._backing_list.append(item)

    def __repr__(self) -> str:
        if self._instance is None:
            return object.__repr__(self)
        return repr(self._backing_list)
