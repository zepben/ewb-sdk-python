#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from collections.abc import Sequence
from dataclasses import dataclass, field

import pytest

from zepben.ewb.boilerplate.collections.abstract_backed_list import AbstractBackedList
from zepben.ewb.boilerplate.collections.abstract_mrid_list import AbstractMridList
from zepben.ewb.boilerplate.collections.lazy_mrid_list import LazyMridList
from zepben.ewb.boilerplate.collections.lazy_mrid_map import LazyMridMap
from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection
from zepben.ewb.boilerplate.collections.mrid_list import MridList
from zepben.ewb.model.cim.iec61970.base.core.identifiable import Identifiable


class Item(Identifiable):
    pass


@dataclass
class Container:
    list_backing: list[Item] = field(default_factory=list)
    lazy_list_backing: list[Item] | None = field(default=None)
    lazy_map_backing: dict[str, Item] | None = field(default=None)

    list_items = MridList(list_backing, "Item")
    lazy_list_items = LazyMridList(lazy_list_backing, "Item")
    lazy_map_items = LazyMridMap(lazy_map_backing, "Item")


def test_abstract_mrid_list_implements_sequence_directly():
    assert issubclass(AbstractMridList, MridCollection)
    assert issubclass(AbstractMridList, Sequence)
    assert not issubclass(AbstractMridList, AbstractBackedList)


def assert_public_state(
    collections: tuple[MridCollection[Item], ...],
    expected: list[Item],
):
    for collection in collections:
        assert len(collection) == len(expected)
        assert list(collection) == expected

        for item in expected:
            assert item in collection
            assert collection.get_by_mrid(item.mrid) is item


def test_mrid_collections_have_the_same_public_effects():
    container = Container()
    collections = (
        container.list_items,
        container.lazy_list_items,
        container.lazy_map_items,
    )
    first = Item("first")
    second = Item("second")

    for collection in collections:
        collection.append(first)
        collection.append(second)

    assert_public_state(collections, [first, second])

    for collection in collections:
        collection.remove(first)

    assert_public_state(collections, [second])
    for collection in collections:
        assert first not in collection
        with pytest.raises(KeyError, match="first"):
            collection.get_by_mrid("first")

    for collection in collections:
        collection.clear()

    assert_public_state(collections, [])
    for collection in collections:
        assert second not in collection
        with pytest.raises(KeyError, match="second"):
            collection.get_by_mrid("second")
