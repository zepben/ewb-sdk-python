#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass, field

import pytest

from zepben.ewb.boilerplate.collections.lazy_mrid_list import LazyMridList
from zepben.ewb.boilerplate.collections.lazy_mrid_map import LazyMridMap
from zepben.ewb.boilerplate.collections.mrid_list import MridList
from zepben.ewb.model.cim.iec61970.base.core.identifiable import Identifiable


class Item(Identifiable):
    def __init__(self, mrid: str):
        super().__init__(mrid)
        self.owner = None


class TrackingBackfill:
    def apply(self, item: Item, owner: object) -> None:
        if item.owner is None:
            item.owner = owner
        if item.owner is not owner:
            raise ValueError("item belongs to another owner")

    def clear(self, item: Item) -> None:
        item.owner = None


@dataclass
class Owner:
    list_backing: list[Item] = field(default_factory=list)
    lazy_list_backing: list[Item] | None = field(default=None)
    lazy_map_backing: dict[str, Item] | None = field(default=None)

    list_items = MridList(list_backing, "Item", backfill=TrackingBackfill())
    lazy_list_items = LazyMridList(
        lazy_list_backing,
        "Item",
        backfill=TrackingBackfill(),
    )
    lazy_map_items = LazyMridMap(
        lazy_map_backing,
        "Item",
        backfill=TrackingBackfill(),
    )


@pytest.mark.parametrize(
    "collection_name",
    ["list_items", "lazy_list_items", "lazy_map_items"],
)
def test_remove_clears_backfill(collection_name: str):
    owner = Owner()
    item = Item("item")
    collection = getattr(owner, collection_name)
    collection.append(item)

    collection.remove(item)

    assert item.owner is None
    assert list(collection) == []


@pytest.mark.parametrize(
    "collection_name",
    ["list_items", "lazy_list_items", "lazy_map_items"],
)
def test_clear_clears_every_backfill(collection_name: str):
    owner = Owner()
    items = [Item("first"), Item("second")]
    collection = getattr(owner, collection_name)
    collection.extend(items)

    collection.clear()

    assert all(item.owner is None for item in items)
    assert list(collection) == []
