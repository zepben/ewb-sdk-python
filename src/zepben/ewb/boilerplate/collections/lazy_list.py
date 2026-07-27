#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import TypeVar

from zepben.ewb.boilerplate.collections.abstract_backed_collections import AbstractBackedList
from zepben.ewb.boilerplate.collections.wrapper import _IterableWrapper


T = TypeVar("T")


class LazyValidatedList(_IterableWrapper, AbstractBackedList[T]):

    def __init__(self,
                 private_field,
                 validate=None,
                 sort_by=None):
        super().__init__(private_field)
        self.validate = validate
        self.sort_by = sort_by

    def _get(self):
        return getattr(self.instance, self.backing_name)

    def _get_collection(self) -> list[T]:
        return getattr(self.instance, self.backing_name) or []

    def append(self, item):
        if self.validate is not None:
            self.validate(self.instance, item)

        existing = getattr(self.instance, self.backing_name)
        if existing is None:
            existing = [item]
            setattr(self.instance, self.backing_name, existing)
        else:
            existing.append(item)

        if self.sort_by is not None:
            existing.sort(key=self.sort_by)

    def __len__(self):
        return len(self._get_collection())

    def __iter__(self):
        return iter(self._get_collection())

    def __contains__(self, item):
        return item in (self._get_collection())

    def remove(self, item):
        existing = self._get_collection()
        existing.remove(item)
        if not existing:
            self.clear()

    def clear(self):
        setattr(self.instance, self.backing_name, None)

    def __repr__(self):
        if self.instance is None:
            return self.__class__.__repr__()
        return str(self._get_collection())

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, item):
        return (self._get_collection())[item]


class LazyIndexedList(LazyValidatedList[T]):

    def __init__(
        self,
        private_field,
        element_description: str
    ):
        super().__init__(private_field)
        self.element_description = element_description

    def insert(self, index: int, item: T) -> None:
        """
        Insert ``item`` at ``index``.
        """
        size = len(self)

        if not 0 <= index <= size:
            raise ValueError(
                f"Unable to add {self.element_description} to "
                f"{self.instance}. "
                f"Sequence number {index} is invalid. "
                f"Expected a value between 0 and {size}. "
                "Make sure you are adding the items in order and there are "
                "no gaps in the numbering."
            )

        existing = getattr(self.instance, self.backing_name)

        if existing is None:
            existing = [item]
            setattr(self.instance, self.backing_name, existing)
        else:
            existing.insert(index, item)

        if self.sort_by is not None:
            existing.sort(key=self.sort_by)

    def append(self, item: T) -> None:
        self.insert(len(self), item)

    def pop(self, index: int = -1) -> T:
        """
        Remove and return the item at ``index``.

        Uses normal Python list semantics, including support for negative
        indexes and raising ``IndexError`` when the index is invalid.
        """
        existing = getattr(self.instance, self.backing_name)

        if existing is None:
            raise IndexError("pop from empty list")

        item = existing.pop(index)

        if not existing:
            self.clear()

        return item
