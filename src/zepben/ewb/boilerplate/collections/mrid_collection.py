#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC, abstractmethod
from typing import Any, Protocol, TypeVar

from zepben.ewb.boilerplate.collections.abstract_backed_collections import AbstractBackedCollection


class HasMrid(Protocol):
    mrid: str


S = TypeVar("S", bound=HasMrid)


class MridCollection(AbstractBackedCollection[S], ABC):
    instance: Any
    element_description: str

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
                f"already exists in {self.instance}."
            )

        return False
