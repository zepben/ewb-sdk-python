#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC, abstractmethod
from typing import Any, Callable, Collection, Generic, Iterable, Iterator, TypeVar


T = TypeVar("T")


class AbstractBackedCollection(Collection[T], Generic[T], ABC):

    _instance: Any
    validate: Callable[[Any, T], object] | None = None

    @abstractmethod
    def _get_collection(self) -> Collection[T]:
        ...

    def _append_raw(self, item: T, /) -> None:
        """Append without running collection lifecycle hooks."""
        self._get_collection().append(item)  # type: ignore[attr-defined]

    def _post_remove(self, item: T, /) -> None:
        """Run cleanup after one item has been removed."""

    def _clear_raw(self, collection: Collection[T], /) -> None:
        """Clear the backing storage without per-item cleanup."""
        collection.clear()  # type: ignore[attr-defined]

    def _clear_and_copy(self, collection: Collection[T], /) -> Collection[T]:
        """Clear the backing storage and return its former contents."""
        former_items = list(collection)
        self._clear_raw(collection)
        return former_items

    def append(self, item: T, /) -> None:
        """Validate and append an item to the collection."""
        if self.validate is not None:
            self.validate(self._instance, item)
        self._append_raw(item)

    def extend(self, items: Iterable[T] | None, /) -> None:
        """Append each item to the collection."""
        for element in items or []:
            self.append(element)

    def remove(self, item: T, /) -> None:
        """Remove an item from the collection."""
        self._get_collection().remove(item)  # type: ignore[attr-defined]
        self._post_remove(item)

    def clear(self) -> None:
        """Remove all items from the collection."""
        self._clear_raw(self._get_collection())

    def __len__(self) -> int:
        return len(self._get_collection())

    def __iter__(self) -> Iterator[T]:
        return iter(self._get_collection())

    def __contains__(self, item: object) -> bool:
        return item in self._get_collection()

    def for_each_indexed(self, action: Callable[[int, T], object]) -> None:
        """Call the `action` on each item in the list."""
        for index, item in enumerate(self._get_collection()):
            action(index, item)
