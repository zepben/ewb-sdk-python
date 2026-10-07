#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, Sequence, overload

from zepben.ewb.boilerplate.collections.abstract_backed_collection import AbstractBackedCollection, T


class AbstractBackedList(
    AbstractBackedCollection[T],
    Sequence[T],
    Generic[T],
    ABC,
):
    """An :class:`AbstractBackedCollection` with sequence-style access.

    Integer indexes return individual items and slices return sequences. When
    a sort selector is supplied, additions reorder the backing list. Indexed
    mutation is only exposed by specialisations such as :class:`LazyIndexList`.
    """

    sort_by: Callable[[T], Any] | None = None

    @abstractmethod
    def _get_collection(self) -> Sequence[T]:
        """Return the current backing list."""
        ...

    def append(self, item: T, /) -> None:
        """Append ``item`` with validation and optional sorting.

        This performs validation, storage, and optional sorting, but no mRID
        check or backfill.
        """
        super().append(item)
        if self.sort_by is not None:
            self._get_collection().sort(key=self.sort_by)  # type: ignore[attr-defined]

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[T]:
        ...

    def __getitem__(self, index: int | slice) -> T | Sequence[T]:
        """Return the item or slice at ``index``."""
        collection = self._get_collection()
        if isinstance(index, slice):
            return collection[index]
        return collection[index]
