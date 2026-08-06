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
    """
    Collection of objects identified by a unique ``mrid``.

    Provides lookup by mRID and rejects distinct objects with duplicate mRIDs.
    """

    _instance: Any
    element_description: str
    backfill: Any = None

    @abstractmethod
    def _safe_get_by_mrid(self, mrid: str) -> S | None: ...

    def get_by_mrid(self, mrid: str) -> S:
        """
        Get an element matching given ``mrid``

        raises KeyError if one is not present
        """
        res = self._safe_get_by_mrid(mrid)
        if res is None:
            raise KeyError(mrid)
        return res

    def _can_add_by_mrid(self, element: S) -> bool:
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
        if not self._can_add_by_mrid(item):
            return

        if self.backfill is not None:
            self.backfill.apply(item, self._instance)

        super().append(item)

    def _post_remove(self, item: S, /) -> None:
        if self.backfill is not None:
            self.backfill.clear(item)

    def clear(self) -> None:
        collection = self._get_collection()
        if self.backfill is None:
            self._clear_raw(collection)
            return

        former_items = self._clear_and_copy(collection)
        for item in former_items:
            self.backfill.clear(item)
