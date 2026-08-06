#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import TypeVar

from zepben.ewb.boilerplate.collections.abstract_backed_list import AbstractBackedList
from zepben.ewb.boilerplate.collections.wrapper import _IterableWrapper


T = TypeVar("T")


class LazyList(_IterableWrapper[T], AbstractBackedList[T]):
    """
    A list-like wrapper backed by a nullable list.

    A backing value of ``None`` is exposed as an empty collection. The backing
    list is created when the first item is appended and reset to ``None`` when
    the last item is removed or the collection is cleared.

    For example::

        @zb_dataclass
        class Container(DataclassBase):
            _items: list[str] | None = field(default=None)
            items: LazyList[str] = LazyList(_items)

        container = Container()

        assert list(container.items) == []
        assert container._items is None

        container.items.append("value")
        assert container._items == ["value"]

        container.items.clear()
        assert container._items is None
    """
    def __init__(
        self,
        private_field: list[T] | None,
        validate=None,
        sort_by=None
    ) -> None:
        super().__init__(private_field)
        self.validate = validate
        self.sort_by = sort_by

    def _get(self) -> list[T] | None:
        return getattr(self._instance, self._backing_name)

    def _get_collection(self) -> list[T]:
        """Return the backing list, or an unbound empty list when absent."""
        return getattr(self._instance, self._backing_name) or []

    def _append_raw(self, item: T) -> None:
        """Append ``item`` to the backing list, creating it if needed.

        This hook performs storage; validation and optional sorting are
        inherited.
        """
        existing = getattr(self._instance, self._backing_name)
        if existing is None:
            existing = [item]
            setattr(self._instance, self._backing_name, existing)
        else:
            existing.append(item)

    def _post_remove(self, item: T) -> None:
        """Reset the backing list after its last item is removed."""
        if not self._get_collection():
            self._clear_raw(self._get_collection())

    def _clear_raw(self, collection) -> None:
        """Reset the backing list to ``None``."""
        setattr(self._instance, self._backing_name, None)

    def __repr__(self) -> str:
        if self._instance is None:
            return object.__repr__(self)
        return repr(self._get_collection())
