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
    def append(self, element: T) -> None:
        ...

    def extend(self, elements: Iterable[T] | None) -> None:
        for element in elements or []:
            self.append(element)

    @abstractmethod
    def remove(self, element: T) -> None:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...

    def __len__(self) -> int:
        return len(self._get_collection())

    def __iter__(self) -> Iterator[T]:
        return iter(self._get_collection())

    def __contains__(self, element: object) -> bool:
        return element in self._get_collection()

    def for_each_indexed(self, action: Callable[[int, T], object]) -> None:
        """
        Call the `action` on each item in the list

        :param action: An action to apply to each :class:`RelaySetting` in the `thresholds` collection, taking the index of the threshold, and the threshold itself.
        """
        for index, item in enumerate(self._get_collection()):
            action(index, item)


