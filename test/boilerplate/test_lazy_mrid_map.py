#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from zepben.ewb.boilerplate.collections.lazy_mrid_map import LazyMridMap


@dataclass(eq=False)
class Item:
    mrid: str


class RecordingBackfill:
    def apply(self, item: Item, owner: Owner):
        owner.events.append(("backfill", item.mrid))


class RejectingBackfill:
    def apply(self, _item: Item, _owner: Owner):
        raise ValueError("backfill failed")


def record_validation(owner: Owner, item: Item):
    owner.events.append(("validate", item.mrid))


def reject_validation(_owner: Owner, _item: Item):
    raise ValueError("validation failed")


@dataclass
class Owner:
    backing_items: dict[str, Item] | None = field(default=None)
    events: list[tuple[str, str]] = field(default_factory=list)

    items = LazyMridMap(backing_items, "Item")
    configured_items = LazyMridMap(
        backing_items,
        "Item",
        backfill=RecordingBackfill(),
        validate=record_validation,
    )
    rejecting_backfill_items = LazyMridMap(
        backing_items,
        "Item",
        backfill=RejectingBackfill(),
    )
    rejecting_validation_items = LazyMridMap(
        backing_items,
        "Item",
        validate=reject_validation,
    )


def test_append_to_empty_creates_map_keyed_by_mrid():
    item = Item("item")
    owner = Owner()

    owner.items.append(item)

    assert owner.backing_items == {"item": item}


def test_append_to_existing_map_adds_mrid_entry():
    first = Item("first")
    second = Item("second")
    owner = Owner({"first": first})

    owner.items.append(second)

    assert owner.backing_items == {
        "first": first,
        "second": second,
    }


def test_append_runs_backfill_before_validation():
    item = Item("item")
    owner = Owner()

    owner.configured_items.append(item)

    assert owner.events == [
        ("backfill", "item"),
        ("validate", "item"),
    ]
    assert owner.backing_items == {"item": item}


def test_backfill_failure_does_not_create_map():
    owner = Owner()

    with pytest.raises(ValueError, match="backfill failed"):
        owner.rejecting_backfill_items.append(Item("item"))

    assert owner.backing_items is None


def test_validation_failure_does_not_create_map():
    owner = Owner()

    with pytest.raises(ValueError, match="validation failed"):
        owner.rejecting_validation_items.append(Item("item"))

    assert owner.backing_items is None


def test_lookup_and_indexing_use_mrid_keys():
    item = Item("item")
    owner = Owner({"item": item})

    assert owner.items.get_by_mrid("item") is item
    assert owner.items["item"] is item

    with pytest.raises(KeyError, match="missing"):
        owner.items.get_by_mrid("missing")

    with pytest.raises(KeyError, match="missing"):
        owner.items["missing"]


def test_collection_view_exposes_map_values():
    first = Item("first")
    second = Item("second")
    owner = Owner({"first": first, "second": second})

    assert len(owner.items) == 2
    assert list(owner.items) == [first, second]
    assert first in owner.items
    assert Item("first") not in owner.items


def test_remove_deletes_item_by_mrid():
    first = Item("first")
    second = Item("second")
    owner = Owner({"first": first, "second": second})

    owner.items.remove(first)

    assert owner.backing_items == {"second": second}


def test_remove_last_item_nulls_backing_map():
    item = Item("item")
    owner = Owner({"item": item})

    owner.items.remove(item)

    assert owner.backing_items is None


def test_clear_nulls_backing_map():
    owner = Owner({"item": Item("item")})

    owner.items.clear()

    assert owner.backing_items is None


def test_repr_matches_backing_map_repr():
    item = Item("item")
    owner = Owner({"item": item})

    assert repr(owner.items) == repr(owner.backing_items)


def test_class_field_repr_uses_descriptor_repr():
    assert repr(Owner.items) == object.__repr__(Owner.items)
