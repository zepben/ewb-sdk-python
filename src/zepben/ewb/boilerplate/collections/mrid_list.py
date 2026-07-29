#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Sequence

from typing_extensions import Self

from zepben.ewb.boilerplate.backfill import Backfill
from zepben.ewb.boilerplate.collections.abstract_backed_list import AbstractBackedList
from zepben.ewb.boilerplate.collections.lazy_collection import LazyCollection
from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection, S
from zepben.ewb.boilerplate.collections.wrapper import _IterableWrapper


class LazyMridList(LazyCollection[S], MridCollection[S]):
    def __init__(
        self,
        private_field,
        element_description: str,
        backfill: Backfill = None,
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
        if not self._can_add_by_mrid(item):
            return

        if self.backfill is not None:
            self.backfill.apply(item, self._instance)

        super().append(item)


class MridList(_IterableWrapper[S], AbstractBackedList[S], MridCollection[S]):
    def __init__(
        self,
        private_field,
        element_description: str,
        backfill: Backfill = None,
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
        return self._backing_list

    def _safe_get_by_mrid(self, mrid: str) -> S | None:
        found = next((element for element in self._backing_list if element.mrid == mrid), None)
        return found

    def append(self, item: S) -> None:
        if not self._can_add_by_mrid(item):
            return

        if self.backfill is not None:
            self.backfill.apply(item, self._instance)

        if self.validate is not None:
            self.validate(self._instance, item)

        self._backing_list.append(item)

        if self.sort_by is not None:
            self._backing_list.sort(key=self.sort_by)

    def remove(self, item: S) -> None:
        self._backing_list.remove(item)

    def clear(self) -> None:
        self._backing_list.clear()

    def __repr__(self) -> str:
        if self._instance is None:
            return object.__repr__(self)
        return repr(self._backing_list)
