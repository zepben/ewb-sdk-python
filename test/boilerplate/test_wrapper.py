#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass, field

import pytest

# noinspection PyProtectedMember
from zepben.ewb.boilerplate.collections.wrapper import _IterableWrapper, _Wrapper


class RecordingWrapper(_Wrapper):
    def __init__(self, private_field, marker: str):
        super().__init__(private_field)
        self.marker = marker

    @property
    def bound_instance(self):
        return self._instance

    @property
    def backing_name(self):
        return self._backing_name


class ListWrapper(_IterableWrapper[str]):
    def _get_collection(self) -> list[str]:
        return getattr(self._instance, self._backing_name)

    def append(self, item: str) -> None:
        self._get_collection().append(item)

    def remove(self, item: str) -> None:
        self._get_collection().remove(item)

    def clear(self) -> None:
        self._get_collection().clear()

    @property
    def bound_instance(self):
        return self._instance


@dataclass
class Owner:
    backing_items: list[str] = field(default_factory=list)

    wrapped = RecordingWrapper(backing_items, marker="marker")
    items = ListWrapper(backing_items)


# @dataclass populates Field.name after the automatic __set_name__ call.
Owner.wrapped.__set_name__(Owner, "wrapped")
Owner.items.__set_name__(Owner, "items")


def test_class_access_returns_shared_descriptor():
    assert isinstance(Owner.wrapped, RecordingWrapper)


def test_instance_access_returns_bound_copy_with_init_arguments():
    owner = Owner()

    first = owner.wrapped
    second = owner.wrapped

    assert first is not Owner.wrapped
    assert first is not second
    assert first.marker == "marker"
    assert first.bound_instance is owner
    assert first.backing_name == "backing_items"


def test_fget_is_named_after_descriptor_and_returns_bound_wrapper():
    owner = Owner()

    wrapper = Owner.items.fget(owner)

    assert Owner.items.fget.__name__ == "items"
    assert Owner.items.fget.__qualname__ == "Owner.items"
    assert wrapper.bound_instance is owner


def test_assigning_iterable_to_empty_backing_extends_collection():
    owner = Owner()

    owner.items = ["first", "second"]

    assert owner.backing_items == ["first", "second"]


def test_assigning_none_to_empty_backing_keeps_it_empty():
    owner = Owner()

    owner.items = None

    assert owner.backing_items == []


def test_assigning_to_non_empty_backing_raises():
    owner = Owner(["existing"])

    with pytest.raises(ValueError, match="currently non-empty"):
        owner.items = ["new"]

    assert owner.backing_items == ["existing"]


def test_assignment_resolves_missing_default_before_extending():
    owner = Owner.__new__(Owner)

    Owner.items.__set__(owner, ["item"])

    assert owner.backing_items == ["item"]
