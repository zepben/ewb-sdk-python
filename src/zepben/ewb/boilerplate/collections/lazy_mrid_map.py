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
    An mRID collection backed by a nullable dictionary.

    Items are stored by their ``mrid`` while iteration exposes the dictionary
    values. A backing value of ``None`` is treated as an empty collection. The
    dictionary is created when the first item is appended and reset to ``None``
    when the collection becomes empty.

    For example::

        @zb_dataclass
        class Container(DataclassBase):
            _items: dict[str, Identifiable] | None = field(default=None)
            items: MridCollection[Identifiable] = LazyMridMap(_items, "item")

        container = Container()
        item = Identifiable("item")
        container.items.append(item)

        assert container._items == {item.mrid: item}
        assert container.items.get_by_mrid(item.mrid) is item
        assert container.items[item.mrid] is item

        container.items.remove(item)
        assert container._items is None
    """
    def __init__(
        self,
        private_field: dict[str, S] | None,
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
        """Return the map values, or an unbound empty view when absent."""
        return self._get_or_empty().values()

    def _safe_get_by_mrid(self, mrid: str) -> S | None:
        """Return the element with ``mrid``, or ``None``."""
        return self._get_or_empty().get(mrid, None)

    def get_by_mrid(self, mrid: str) -> S:
        """Return the element with ``mrid``.

        :raises KeyError: If no element has the requested mRID.
        """
        return self._get_or_empty()[mrid]

    def _append_raw(self, item: S) -> None:
        """Store ``item`` by mRID, creating the backing map if needed.

        This hook performs storage; mRID checking, backfill, and validation are
        inherited.
        """
        existing = getattr(self._instance, self._backing_name)
        if existing is None:
            existing = {item.mrid: item}
            setattr(self._instance, self._backing_name, existing)
        else:
            existing[item.mrid] = item

    def __len__(self) -> int:
        return len(self._get_or_empty())

    def __contains__(self, item: object) -> bool:
        """Return whether ``item`` is stored under its mRID by identity."""
        return self._get_or_empty().get(getattr(item, "mrid", None)) is item

    def remove(self, item: S) -> None:
        """Remove ``item`` only when the stored instance is identical."""
        existing = self._get_or_empty()
        if existing.get(item.mrid) is not item:
            raise ValueError(f"{item!r} not in collection")
        del existing[item.mrid]
        self._post_remove(item)

    def _post_remove(self, item: S) -> None:
        """Reset an empty map and clear backfill for ``item``."""
        if not self._get_or_empty():
            self._clear_raw(self._get_collection())
        super()._post_remove(item)

    def _clear_raw(self, collection) -> None:
        """Reset the backing map to ``None``."""
        setattr(self._instance, self._backing_name, None)

    def _clear_and_copy(self, collection):
        """Reset the backing map and return its former values."""
        former_items = self._get_collection()
        self._clear_raw(collection)
        return former_items

    def __repr__(self) -> str:
        if self._instance is None:
            return object.__repr__(self)
        return repr(self._get_or_empty())
