#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from zepben.ewb.boilerplate.collections.abstract_backed_list import AbstractBackedList


class BackedList(AbstractBackedList[str]):
    def __init__(self, items: list[str]):
        self.items = items

    def _get_collection(self) -> list[str]:
        return self.items

    def append(self, item: str) -> None:
        self.items.append(item)

    def remove(self, item: str) -> None:
        self.items.remove(item)

    def clear(self) -> None:
        self.items.clear()


def test_getitem_returns_item_at_index():
    collection = BackedList(["first", "second"])

    assert collection[1] == "second"


def test_getitem_supports_negative_index():
    collection = BackedList(["first", "second"])

    assert collection[-1] == "second"


def test_getitem_raises_for_index_out_of_range():
    collection = BackedList(["item"])

    with pytest.raises(IndexError):
        collection[1]


def test_getitem_returns_backing_list_slice():
    collection = BackedList(["first", "second", "third"])

    assert collection[1:] == ["second", "third"]


def test_getitem_supports_slice_step():
    collection = BackedList(
        ["first", "second", "third", "fourth"]
    )

    assert collection[::2] == ["first", "third"]
