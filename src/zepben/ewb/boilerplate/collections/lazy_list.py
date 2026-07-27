#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import field
from typing import TypeVar, Protocol

from zepben.ewb import DataclassBase, zb_dataclass
from zepben.ewb.boilerplate.collections.base import AbstractBackedList
from zepben.ewb.boilerplate.collections.wrapper import _IterableWrapper


# from descriptor_fix import BackedDescriptor, remove_descriptor_annotations


class HasMrid(Protocol):
    mrid: str

T = TypeVar("T")
S = TypeVar("S", bound=HasMrid)


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

    # clearIfEmpty is inlined for performance

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

if __name__ == '__main__':
    @zb_dataclass
    class C(DataclassBase):
        _xs: list[int] | None = field(default=None)
        xs: LazyIndexedList[int] = LazyIndexedList(
            _xs,
            "Thing"
        )

    c = C(xs=[24, 42])
    print(c._xs, c.xs)
    c.xs.clear()
    print(c._xs, c.xs)
    c.xs.append(1)
    c.xs.append(2)
    c.xs.append(3)
    print(c._xs, c.xs)
    c.xs.insert(2, 42)
    print(c._xs, c.xs)
    c.xs.pop(2)
    print(c._xs, c.xs)
