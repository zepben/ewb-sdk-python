#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from zepben.ewb.boilerplate.collections.lazy_index_list import LazyIndexList


def record_validation(owner: Owner, item: str):
    owner.events.append(item)


def reject_validation(_owner: Owner, _item: str):
    raise ValueError("validation failed")


@dataclass
class Owner:
    backing_items: list[str] | None = field(default=None)
    events: list[str] = field(default_factory=list)

    items = LazyIndexList(backing_items, "Item")
    validated_items = LazyIndexList(
        backing_items,
        "Item",
        validate=record_validation,
    )
    rejecting_items = LazyIndexList(
        backing_items,
        "Item",
        validate=reject_validation,
    )


def test_insert_into_empty_creates_backing_list():
    owner = Owner()

    owner.items.insert(0, "item")

    assert owner.backing_items == ["item"]


def test_insert_places_item_at_requested_index():
    owner = Owner(["first", "third"])

    owner.items.insert(1, "second")

    assert owner.backing_items == ["first", "second", "third"]


@pytest.mark.parametrize("index", [-1, 1])
def test_insert_rejects_index_outside_valid_range(index: int):
    owner = Owner()

    with pytest.raises(
        IndexError,
        match=rf"Sequence number {index} is invalid.*between 0 and 0",
    ):
        owner.items.insert(index, "item")

    assert owner.backing_items is None


def test_insert_validates_before_creating_backing_list():
    owner = Owner()

    with pytest.raises(ValueError, match="validation failed"):
        owner.rejecting_items.insert(0, "item")

    assert owner.backing_items is None


def test_insert_runs_validation():
    owner = Owner()

    owner.validated_items.insert(0, "item")

    assert owner.events == ["item"]
    assert owner.backing_items == ["item"]


def test_append_inserts_at_end():
    owner = Owner(["first"])

    owner.items.append("second")

    assert owner.backing_items == ["first", "second"]


def test_pop_returns_and_removes_requested_item():
    owner = Owner(["first", "second"])

    popped = owner.items.pop(0)

    assert popped == "first"
    assert owner.backing_items == ["second"]


def test_pop_uses_last_item_by_default_and_nulls_empty_backing():
    owner = Owner(["item"])

    popped = owner.items.pop()

    assert popped == "item"
    assert owner.backing_items is None


def test_pop_from_empty_raises():
    owner = Owner()

    with pytest.raises(IndexError, match="pop from empty list"):
        owner.items.pop()

    assert owner.backing_items is None


def test_delete_removes_item_at_index():
    owner = Owner(["first", "second"])

    del owner.items[0]

    assert owner.backing_items == ["second"]


def test_delete_last_item_nulls_backing_list():
    owner = Owner(["item"])

    del owner.items[0]

    assert owner.backing_items is None
