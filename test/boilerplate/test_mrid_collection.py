#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection
from zepben.ewb.model.cim.iec61970.base.core.identifiable import Identifiable


class Item(Identifiable):
    pass


class MridCollectionImpl(MridCollection[Item]):
    def __init__(self, items: list[Item] | None = None):
        self.items = items or []
        self.element_description = "Item"
        self._instance = "owner"

    def _get_collection(self) -> list[Item]:
        return self.items

    def _safe_get_by_mrid(self, mrid: str) -> Item | None:
        return next(
            (item for item in self.items if item.mrid == mrid),
            None,
        )

    def append(self, item: Item) -> None:
        if self._can_add_by_mrid(item):
            self.items.append(item)

    def remove(self, item: Item) -> None:
        self.items.remove(item)

    def clear(self) -> None:
        self.items.clear()


def test_get_by_mrid_returns_matching_item():
    item = Item("item")
    collection = MridCollectionImpl([item])

    assert collection.get_by_mrid("item") is item


def test_get_by_mrid_raises_for_missing_item():
    collection = MridCollectionImpl()

    with pytest.raises(KeyError, match="missing"):
        collection.get_by_mrid("missing")


def test_append_accepts_new_mrid():
    item = Item("item")
    collection = MridCollectionImpl()

    collection.append(item)

    assert collection.items == [item]


def test_append_ignores_same_instance():
    item = Item("item")
    collection = MridCollectionImpl([item])

    collection.append(item)

    assert collection.items == [item]


def test_append_rejects_different_instance_with_same_mrid():
    existing = Item("duplicate")
    collection = MridCollectionImpl([existing])

    with pytest.raises(
        ValueError,
        match=r"Item with mRID duplicate already exists in owner",
    ):
        collection.append(Item("duplicate"))

    assert collection.items == [existing]
