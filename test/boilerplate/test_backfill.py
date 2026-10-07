#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass, field

import pytest

from zepben.ewb.boilerplate.backed_descriptor import Alias
from zepben.ewb.boilerplate.backfill import Backfill, internal


@dataclass
class Container:
    """Container exposing each supported kind of internal back-reference."""

    field_backing: object | None = field(default=None)
    descriptor_backing: object | None = field(default=None)
    property_backing: object | None = field(default=None)

    descriptor = Alias(descriptor_backing)

    @property
    @internal(field_backing)
    def field_parent(self):
        return self.field_backing

    @property
    @internal(descriptor)
    def descriptor_parent(self):
        return self.descriptor

    @property
    def internal_parent(self):
        return self.property_backing

    @internal_parent.setter
    def internal_parent(self, value):
        self.property_backing = value

    @property
    @internal(internal_parent)
    def property_parent(self):
        return self.internal_parent


# @dataclass populates Field.name after the automatic __set_name__ call.
Container.descriptor.__set_name__(Container, "descriptor")


@pytest.mark.parametrize(
    ("property_name", "backing_name"),
    [
        ("field_parent", "field_backing"),
        ("descriptor_parent", "descriptor_backing"),
        ("property_parent", "property_backing"),
    ],
)
def test_apply_sets_back_reference(
    property_name: str,
    backing_name: str,
):
    container = Container()
    owner = object()

    Backfill(getattr(Container, property_name)).apply(container, owner)

    assert getattr(container, property_name) is owner
    assert getattr(container, backing_name) is owner


@pytest.mark.parametrize(
    ("property_name", "backing_name"),
    [
        ("field_parent", "field_backing"),
        ("descriptor_parent", "descriptor_backing"),
        ("property_parent", "property_backing"),
    ],
)
def test_clear_nulls_back_reference(
    property_name: str,
    backing_name: str,
):
    owner = object()
    container = Container()
    setattr(container, backing_name, owner)

    Backfill(getattr(Container, property_name)).clear(container)

    assert getattr(container, property_name) is None
    assert getattr(container, backing_name) is None
