#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Protocol, TypeVar, Collection

from zepben.ewb.boilerplate.backfill import Backfill
from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection, S
from zepben.ewb.boilerplate.collections.wrapper import _IterableWrapper


T = TypeVar("T")


class LazyMridMap(_IterableWrapper[S], MridCollection[S]):
    def __init__(
        self,
        private_field,
        element_description: str,
        backfill: Backfill = None,
        validate=None):
        super().__init__(private_field)
        self.element_description = element_description
        self.backfill = backfill
        self.validate = validate

    def _get(self):
        return getattr(self.instance, self.backing_name)

    def _get_or_empty(self) -> dict[str, S]:
        return getattr(self.instance, self.backing_name) or {}

    def _get_collection(self) -> list[S]:
        return list(self._get_or_empty().values())

    def _safe_get_by_mrid(self, mrid: str) -> S | None:
        return self._get_or_empty().get(mrid, None)

    def get_by_mrid(self, mrid: str) -> S:
        return self._get_or_empty()[mrid]

    def append(self, element: S):
        if not self._can_add_by_mrid(element):
            return

        if self.backfill is not None:
            self.backfill.apply(element, self.instance)

        if self.validate is not None:
            self.validate(self.instance, element)

        existing = getattr(self.instance, self.backing_name)
        if existing is None:
            existing = {element.mrid: element}
            setattr(self.instance, self.backing_name, existing)
        else:
            existing[element.mrid] = element

    def __len__(self):
        return len(self._get_or_empty())

    def __contains__(self, item: S):
        return self._get_or_empty().get(getattr(item, "mrid", None), None) == item

    def remove(self, item):
        existing = self._get_or_empty()

        del existing[item.mrid]
        if not existing:
            self.clear()

    def clear(self):
        setattr(self.instance, self.backing_name, None)

    def __repr__(self):
        return str(self._get_or_empty())

    def __getitem__(self, item):
        return (self._get_or_empty())[item]
