#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.ewb.boilerplate.collections.lazy_list import LazyList, T


class LazyIndexList(LazyList[T]):
    """
    Lazy collection with list-style index-based insertion and deletion.

    It retains the nullable backing-list behaviour of ``LazyList``,
    creating the backing list when an item is inserted and resetting it to
    ``None`` when the final item is deleted.

    For example::

        container.items.insert(0, "value")
        assert container._items == ["value"]

        del container.items[0]
        assert container._items is None
    """
    def __init__(
        self,
        private_field: list[T] | None,
        element_description: str,
        validate=None,
    ) -> None:
        super().__init__(private_field, validate=validate, sort_by=None)
        self.element_description = element_description

    def insert(self, index: int, item: T) -> None:
        """
        Insert an item into the collection at a given index.
        Run optional validation.
        """
        size = len(self)

        if not 0 <= index <= size:
            raise ValueError(
                f"Unable to add {self.element_description} to "
                f"{self._instance}. "
                f"Sequence number {index} is invalid. "
                f"Expected a value between 0 and {size}. "
                "Make sure you are adding the items in order and there are "
                "no gaps in the numbering."
            )

        if self.validate is not None:
            self.validate(self._instance, item)

        existing = getattr(self._instance, self._backing_name)

        if existing is None:
            existing = [item]
            setattr(self._instance, self._backing_name, existing)
        else:
            existing.insert(index, item)

    def append(self, item: T) -> None:
        """
        Append an item to the collection.
        Run optional validation.
        Sort the collection if key lambda is provided.
        """
        self.insert(len(self), item)

    def pop(self, index: int = -1) -> T:
        """
        Remove and return the item at ``index``.

        Uses normal Python list semantics, including support for negative
        indexes and raising ``IndexError`` when the index is invalid.
        """
        existing = getattr(self._instance, self._backing_name)

        if existing is None:
            raise IndexError("pop from empty list")

        item = existing.pop(index)

        if not existing:
            self.clear()

        return item

    def __delitem__(self, index: int, /) -> None:
        """Remove the item at the given index."""
        self.remove(self[index])
