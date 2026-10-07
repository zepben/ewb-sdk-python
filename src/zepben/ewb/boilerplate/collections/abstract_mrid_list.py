#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC, abstractmethod
from typing import Any, Callable, Sequence, overload

from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection, S


class AbstractMridList(MridCollection[S], Sequence[S], ABC):
    """
    List-shaped specialisation of :class:`MridCollection`.

    This class represents the deliberate intersection of the mRID collection
    and backed-list branches so downstream mRID list implementations do not
    duplicate sequence delegation or sorting behaviour. It intentionally does
    not inherit :class:`AbstractBackedList` to preserve SDK hierarchy parity.
    """

    sort_by: Callable[[S], Any] | None = None

    @abstractmethod
    def _get_collection(self) -> Sequence[S]:
        """Return the current backing list."""
        ...

    def append(self, item: S, /) -> None:
        """Append ``item`` when its mRID and validation permit it.

        This performs the mRID check, backfill, validation, storage, and
        optional sorting.
        """
        MridCollection.append(self, item)
        if self.sort_by is not None:
            self._get_collection().sort(key=self.sort_by)  # type: ignore[attr-defined]

    @overload
    def __getitem__(self, index: str) -> S:
        ...

    @overload
    def __getitem__(self, index: int) -> S:
        ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[S]:
        ...

    def __getitem__(self, index: str | int | slice) -> S | Sequence[S]:
        """Return an element by mRID or an item or slice by list index."""
        if isinstance(index, str):
            return self.get_by_mrid(index)
        return self._get_collection()[index]
