#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.ewb.boilerplate.collections.abstract_backed_collection import AbstractBackedCollection


class BackedCollection(AbstractBackedCollection[str]):
    def __init__(self, items: list[str] | None = None):
        self.items = items or []

    def _get_collection(self) -> list[str]:
        return self.items

    def append(self, item: str) -> None:
        self.items.append(item)

    def remove(self, item: str) -> None:
        self.items.remove(item)

    def clear(self) -> None:
        self.items.clear()


def test_extend_appends_each_item_in_order():
    collection = BackedCollection(["first"])

    collection.extend(["second", "third"])

    assert collection.items == ["first", "second", "third"]


def test_extend_accepts_single_pass_iterable():
    collection = BackedCollection()

    collection.extend(item for item in ["first", "second"])

    assert collection.items == ["first", "second"]


def test_extend_empty_iterable_does_nothing():
    collection = BackedCollection(["item"])

    collection.extend([])

    assert collection.items == ["item"]


def test_extend_none_does_nothing():
    collection = BackedCollection(["item"])

    collection.extend(None)

    assert collection.items == ["item"]


def test_len_returns_backing_collection_size():
    collection = BackedCollection(["first", "second"])

    assert len(collection) == 2


def test_len_returns_zero_for_empty_backing_collection():
    assert len(BackedCollection()) == 0


def test_iter_returns_items_in_backing_collection_order():
    collection = BackedCollection(["first", "second"])

    assert list(collection) == ["first", "second"]


def test_iter_returns_no_items_for_empty_backing_collection():
    assert list(BackedCollection()) == []


def test_contains_finds_item_in_backing_collection():
    collection = BackedCollection(["first", "second"])

    assert "second" in collection


def test_contains_rejects_item_missing_from_backing_collection():
    collection = BackedCollection(["first", "second"])

    assert "missing" not in collection


def test_for_each_indexed_visits_each_item_with_its_index():
    collection = BackedCollection(["first", "second"])
    visited: list[tuple[int, str]] = []

    collection.for_each_indexed(
        lambda index, item: visited.append((index, item))
    )

    assert visited == [(0, "first"), (1, "second")]


def test_for_each_indexed_does_not_call_action_for_empty_collection():
    collection = BackedCollection()
    visited: list[tuple[int, str]] = []

    collection.for_each_indexed(
        lambda index, item: visited.append((index, item))
    )

    assert visited == []
