#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import TypeVar

from zepben.ewb.boilerplate.collections.abstract_backed_list import AbstractBackedList
from zepben.ewb.boilerplate.collections.wrapper import _IterableWrapper


T = TypeVar("T")


class LazyCollection(_IterableWrapper[T], AbstractBackedList[T]):

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
        return getattr(self._instance, self._backing_name) or []

    def append(self, item: T) -> None:
        if self.validate is not None:
            self.validate(self._instance, item)

        existing = getattr(self._instance, self._backing_name)
        if existing is None:
            existing = [item]
            setattr(self._instance, self._backing_name, existing)
        else:
            existing.append(item)

        if self.sort_by is not None:
            existing.sort(key=self.sort_by)

    def remove(self, item: T) -> None:
        existing = self._get_collection()
        existing.remove(item)
        if not existing:
            self.clear()

    def clear(self) -> None:
        setattr(self._instance, self._backing_name, None)

    def __repr__(self) -> str:
        if self._instance is None:
            return object.__repr__(self)
        return repr(self._get_collection())
