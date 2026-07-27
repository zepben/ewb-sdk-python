#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC, abstractmethod
from typing import Sequence, Generic, overload

from zepben.ewb.boilerplate.collections.abstract_backed_collection import AbstractBackedCollection, T


class AbstractBackedList(
    AbstractBackedCollection[T],
    Sequence[T],
    Generic[T],
    ABC,
):

    @abstractmethod
    def _get_collection(self) -> Sequence[T]:
        ...

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[T]:
        ...

    def __getitem__(self, index: int | slice) -> T | Sequence[T]:
        return self._get_collection()[index]
