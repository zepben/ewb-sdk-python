#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import TypeVar, ValuesView

from zepben.ewb.boilerplate.backfill import Backfill
from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection, S
from zepben.ewb.boilerplate.collections.wrapper import _IterableWrapper

T = TypeVar("T")


class LazyMridMap(_IterableWrapper[S], MridCollection[S]):
    def __init__(
        self,
        private_field: list[S] | None,
        element_description: str,
        backfill: Backfill | None = None,
        validate=None
    ) -> None:
        super().__init__(private_field)
        self.element_description = element_description
        self.backfill = backfill
        self.validate = validate

    def _get(self) -> dict[str, S] | None:
        return getattr(self._instance, self._backing_name)

    def _get_or_empty(self) -> dict[str, S]:
        return getattr(self._instance, self._backing_name) or {}

    def _get_collection(self) -> ValuesView[S]:
        return self._get_or_empty().values()

    def _safe_get_by_mrid(self, mrid: str) -> S | None:
        return self._get_or_empty().get(mrid, None)

    def get_by_mrid(self, mrid: str) -> S:
        return self._get_or_empty()[mrid]

    def append(self, element: S) -> None:
        if not self._can_add_by_mrid(element):
            return

        if self.backfill is not None:
            self.backfill.apply(element, self._instance)

        if self.validate is not None:
            self.validate(self._instance, element)

        existing = getattr(self._instance, self._backing_name)
        if existing is None:
            existing = {element.mrid: element}
            setattr(self._instance, self._backing_name, existing)
        else:
            existing[element.mrid] = element

    def __len__(self) -> int:
        return len(self._get_or_empty())

    def __contains__(self, item: S) -> bool:
        return self._get_or_empty().get(getattr(item, "mrid", None)) == item

    def remove(self, item) -> None:
        existing = self._get_or_empty()

        del existing[item.mrid]
        if not existing:
            self.clear()

    def clear(self) -> None:
        setattr(self._instance, self._backing_name, None)

    def __repr__(self) -> str:
        if self._instance is None:
            return object.__repr__(self)
        return repr(self._get_or_empty())

    def __getitem__(self, item) -> S:
        return (self._get_or_empty())[item]
