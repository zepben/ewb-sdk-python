#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC, abstractmethod
from typing import Any, Callable, Sequence, overload

from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection, S


class AbstractMridList(MridCollection[S], Sequence[S], ABC):
    """
    Common list behaviour for mRID-addressable collections.

    NOTE: This can be simplified by inheriting from AbstractBackedList.
          But that cannot be done on the Kotlin side, so for better parity,
          this class duplicates some of the functionality from that class
    """

    sort_by: Callable[[S], Any] | None = None

    @abstractmethod
    def _get_collection(self) -> Sequence[S]:
        ...

    def append(self, item: S, /) -> None:
        MridCollection.append(self, item)
        if self.sort_by is not None:
            self._get_collection().sort(key=self.sort_by)  # type: ignore[attr-defined]

    @overload
    def __getitem__(self, index: int) -> S:
        ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[S]:
        ...

    def __getitem__(self, index: int | slice) -> S | Sequence[S]:
        return self._get_collection()[index]
