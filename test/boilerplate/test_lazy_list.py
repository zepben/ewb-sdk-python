#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from zepben.ewb.boilerplate.collections.lazy_list import LazyList


def record_validation(owner: Owner, item: str):
    owner.events.append(("validate", item))


def reject_validation(_owner: Owner, _item: str):
    raise ValueError("validation failed")


@dataclass
class Owner:
    backing_items: list[str] | None = field(
        default=None,
        repr=False,
    )
    events: list[tuple[str, str]] = field(
        default_factory=list,
        repr=False,
    )

    items = LazyList(backing_items)
    validated_items = LazyList(
        backing_items,
        validate=record_validation,
    )
    rejecting_validation_items = LazyList(
        backing_items,
        validate=reject_validation,
    )
    sorted_items = LazyList(
        backing_items,
        sort_by=lambda item: item,
    )


def test_append_to_empty_creates_owner_backing_list():
    owner = Owner()

    owner.items.append("item")

    assert owner.backing_items == ["item"]


def test_append_adds_item_to_existing_owner_backing_list():
    owner = Owner()
    owner.backing_items = ["first"]

    owner.items.append("second")

    assert owner.backing_items == ["first", "second"]


def test_append_runs_validation():
    owner = Owner()

    owner.validated_items.append("item")

    assert owner.events == [("validate", "item")]
    assert owner.backing_items == ["item"]


def test_failed_append_to_empty_does_not_create_backing_list():
    owner = Owner()

    with pytest.raises(ValueError, match="validation failed"):
        owner.rejecting_validation_items.append("item")

    assert owner.backing_items is None


def test_validation_failure_does_not_append_to_existing_list():
    owner = Owner()
    owner.backing_items = ["existing"]

    with pytest.raises(ValueError, match="validation failed"):
        owner.rejecting_validation_items.append("item")

    assert owner.backing_items == ["existing"]


def test_append_sorts_owner_backing_list():
    owner = Owner()

    owner.sorted_items.append("second")
    owner.sorted_items.append("first")

    assert owner.backing_items == ["first", "second"]


def test_remove_removes_item_from_owner_backing_list():
    owner = Owner()
    owner.backing_items = ["retained", "removed"]

    owner.items.remove("removed")

    assert owner.backing_items == ["retained"]


def test_remove_last_item_sets_owner_backing_list_to_null():
    owner = Owner()
    owner.backing_items = ["item"]

    owner.items.remove("item")

    assert owner.backing_items is None


def test_clear_sets_owner_backing_list_to_null():
    owner = Owner()
    owner.backing_items = ["first", "second"]

    owner.items.clear()

    assert owner.backing_items is None


def test_repr_matches_owner_backing_list_repr():
    owner = Owner()
    owner.backing_items = ["first", "second"]

    assert owner.backing_items is not None
    assert repr(owner.items) == repr(owner.backing_items)


def test_empty_repr_matches_empty_list_repr():
    owner = Owner()

    assert repr(owner.items) == repr([])
    assert owner.backing_items is None


def test_class_field_repr_uses_descriptor_repr() -> None:
    assert repr(Owner.items) == object.__repr__(Owner.items)
