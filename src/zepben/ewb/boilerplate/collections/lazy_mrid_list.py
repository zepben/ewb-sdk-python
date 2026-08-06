#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.ewb.boilerplate.backfill import Backfill
from zepben.ewb.boilerplate.collections.abstract_mrid_list import AbstractMridList
from zepben.ewb.boilerplate.collections.mrid_collection import S
from zepben.ewb.boilerplate.collections.wrapper import _IterableWrapper


class LazyMridList(_IterableWrapper[S], AbstractMridList[S]):
    """
    Nullable list implementation of :class:`MridCollection`.

    Inherits mRID lookup and uniqueness semantics from ``MridCollection`` and
    lazy backing-list behavior from ``LazyList``.
    """
    def __init__(
        self,
        private_field: list[S] | None,
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

    def _get(self) -> list[S] | None:
        return getattr(self._instance, self._backing_name)

    def _get_collection(self) -> list[S]:
        return self._get() or []

    def _safe_get_by_mrid(self, mrid: str) -> S | None:
        existing = self._get()
        if existing is None:
            return None
        found = next((element for element in existing if element.mrid == mrid), None)
        return found

    def _append_raw(self, item: S) -> None:
        existing = self._get()
        if existing is None:
            setattr(self._instance, self._backing_name, [item])
        else:
            existing.append(item)

    def _post_remove(self, item: S) -> None:
        super()._post_remove(item)
        if not self._get_collection():
            self._clear_raw(self._get_collection())

    def _clear_raw(self, collection) -> None:
        setattr(self._instance, self._backing_name, None)

    def _clear_and_copy(self, collection):
        self._clear_raw(collection)
        return collection

    def __repr__(self) -> str:
        if self._instance is None:
            return object.__repr__(self)
        return repr(self._get_collection())
