#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.ewb.boilerplate.collections.lazy_collection import LazyCollection, T


class LazyList(LazyCollection[T]):

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
        Insert ``item`` at ``index``.
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
