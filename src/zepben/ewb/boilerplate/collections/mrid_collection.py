#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC, abstractmethod
from typing import Any, TypeVar

from zepben.ewb.boilerplate.collections.abstract_backed_collection import AbstractBackedCollection
from zepben.ewb.model.cim.iec61970.base.core.identifiable import Identifiable


S = TypeVar("S", bound=Identifiable)


class MridCollection(AbstractBackedCollection[S], ABC):
    """Base collection for objects identified by a unique ``mrid``.

    Provides lookup through :meth:`get_by_mrid` and read-only string indexing.
    Additions enforce mRID uniqueness and apply optional backfill before base
    collection validation.
    """

    _instance: Any
    element_description: str
    backfill: Any = None

    @abstractmethod
    def _safe_get_by_mrid(self, mrid: str) -> S | None: ...

    def get_by_mrid(self, mrid: str) -> S:
        """Return the element with ``mrid``.

        :raises KeyError: If no element has the requested mRID.
        """
        res = self._safe_get_by_mrid(mrid)
        if res is None:
            raise KeyError(mrid)
        return res

    def __getitem__(self, mrid: str, /) -> S:
        """Return the element with ``mrid``.

        :raises KeyError: If no element has the requested mRID.
        """
        return self.get_by_mrid(mrid)

    def _can_add_by_mrid(self, element: S) -> bool:
        """Accept a new mRID, ignore the same instance, and reject collisions."""
        existing = self._safe_get_by_mrid(element.mrid)

        if existing is None:
            return True

        if existing is not element:
            raise ValueError(
                f"{self.element_description} with mRID {element.mrid} "
                f"already exists in {self._instance}."
            )

        return False

    def append(self, item: S, /) -> None:
        """Append ``item`` when its mRID and validation permit it.

        This performs the mRID check, backfill, validation, and storage, but no
        sorting.
        """
        if not self._can_add_by_mrid(item):
            return

        if self.backfill is not None:
            self.backfill.apply(item, self._instance)

        super().append(item)

    def _post_remove(self, item: S, /) -> None:
        """Clear ``item``'s backfill after removal."""
        if self.backfill is not None:
            self.backfill.clear(item)

    def clear(self) -> None:
        """Clear the collection and all backfilled references."""
        collection = self._get_collection()
        if self.backfill is None:
            self._clear_raw(collection)
            return

        former_items = self._clear_and_copy(collection)
        for item in former_items:
            self.backfill.clear(item)
