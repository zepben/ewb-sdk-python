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
    """
    Lazy mRID collection backed by a nullable dictionary.

    Items are stored by their ``mrid`` while iteration exposes the dictionary
    values. A backing value of ``None`` is treated as an empty collection. The
    dictionary is created when the first item is appended and reset to ``None``
    when the collection becomes empty.

    For example::

        container.items.append(item)

        assert container._items == {item.mrid: item}
        assert container.items.get_by_mrid(item.mrid) is item

        container.items.remove(item)
        assert container._items is None
    """
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

    def append(self, item: S) -> None:
        """
        Add an item to the collection.
        Check for mRID collisions with existing items.
        Optionally fill the backref field on the added item.
        Run optional validation.
        """
        if not self._can_add_by_mrid(item):
            return

        if self.backfill is not None:
            self.backfill.apply(item, self._instance)

        if self.validate is not None:
            self.validate(self._instance, item)

        existing = getattr(self._instance, self._backing_name)
        if existing is None:
            existing = {item.mrid: item}
            setattr(self._instance, self._backing_name, existing)
        else:
            existing[item.mrid] = item

    def __len__(self) -> int:
        return len(self._get_or_empty())

    def __contains__(self, item: object) -> bool:
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
