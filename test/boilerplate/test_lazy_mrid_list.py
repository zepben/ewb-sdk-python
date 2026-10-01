#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from zepben.ewb.boilerplate.collections.lazy_mrid_list import LazyMridList
from zepben.ewb.model.cim.iec61970.base.core.identifiable import Identifiable


class Item(Identifiable):
    pass


class RecordingBackfill:
    def apply(self, item: Item, owner: Owner):
        owner.events.append(("backfill", item.mrid))


class RejectingBackfill:
    def apply(self, _item: Item, _owner: Owner):
        raise ValueError("backfill failed")


def record_validation(owner: Owner, item: Item):
    owner.events.append(("validate", item.mrid))


@dataclass
class Owner:
    backing_items: list[Item] | None = field(default=None)
    events: list[tuple[str, str]] = field(default_factory=list)

    items = LazyMridList(backing_items, "Item")
    backfilled_items = LazyMridList(
        backing_items,
        "Item",
        backfill=RecordingBackfill(),
        validate=record_validation,
    )
    rejecting_backfill_items = LazyMridList(
        backing_items,
        "Item",
        backfill=RejectingBackfill(),
    )


def test_get_by_mrid_finds_item_in_backing_list():
    item = Item("item")
    owner = Owner([item])

    assert owner.items.get_by_mrid("item") is item


def test_get_by_mrid_treats_null_backing_as_empty():
    owner = Owner()

    with pytest.raises(KeyError, match="missing"):
        owner.items.get_by_mrid("missing")

    assert owner.backing_items is None


def test_append_applies_backfill_before_superclass_validation():
    item = Item("item")
    owner = Owner()

    owner.backfilled_items.append(item)

    assert owner.events == [
        ("backfill", "item"),
        ("validate", "item"),
    ]
    assert owner.backing_items == [item]


def test_backfill_failure_does_not_call_superclass_append():
    owner = Owner()

    with pytest.raises(ValueError, match="backfill failed"):
        owner.rejecting_backfill_items.append(Item("item"))

    assert owner.backing_items is None
