#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC, abstractmethod
from typing import Collection, Iterable, Generic, Iterator, Callable, TypeVar


T = TypeVar("T")


class AbstractBackedCollection(Collection[T], Generic[T], ABC):

    @abstractmethod
    def _get_collection(self) -> Collection[T]:
        ...

    @abstractmethod
    def append(self, item: T, /) -> None:
        """Append an item to the collection."""
        ...

    def extend(self, items: Iterable[T] | None, /) -> None:
        """Append each item to the collection."""
        for element in items or []:
            self.append(element)

    @abstractmethod
    def remove(self, item: T, /) -> None:
        """Remove an item from the collection."""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Remove all items from the collection."""
        ...

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
