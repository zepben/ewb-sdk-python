#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass, field, fields

import pytest

from zepben.ewb.boilerplate.backed_descriptor import Alias, BackedDescriptor
from zepben.ewb.boilerplate.dataclass_base import DataclassBase, zb_dataclass


@zb_dataclass
class Owner(DataclassBase):
    _value: int = field(default=1)

    value: int = BackedDescriptor(_value)
    alias: int = Alias(value)


@pytest.mark.parametrize("private_field", [None, "_value", 1, object()])
def test_constructor_rejects_non_field_and_non_descriptor(private_field):
    with pytest.raises(TypeError, match="has to be an instance of dataclass Field"):
        BackedDescriptor(private_field)


def test_constructor_accepts_dataclass_field():
    backing_field = field(default=1)

    descriptor = BackedDescriptor(backing_field)

    assert descriptor.private_field is backing_field
    assert descriptor.name is None
    assert descriptor._backing_name is None


def test_constructor_accepts_another_backed_descriptor():
    inner = BackedDescriptor(field(default=1))

    outer = BackedDescriptor(inner)

    assert outer.private_field is inner


def test_alias_is_an_exact_class_alias():
    assert Alias is BackedDescriptor


def test_set_name_records_public_and_backing_names():
    assert Owner.value.name == "value"
    assert Owner.value.__name__ == "value"
    assert Owner.value._backing_name == "_value"


def test_class_access_returns_shared_descriptor():
    assert isinstance(Owner.value, BackedDescriptor)
    assert Owner.value is Owner.__dict__["value"]


def test_instance_access_reads_backing_field():
    owner = Owner()
    owner._value = 7

    assert owner.value == 7


def test_instance_assignment_writes_backing_field():
    owner = Owner()

    owner.value = 7

    assert owner._value == 7
    assert owner.value == 7


def test_constructor_assignment_uses_descriptor():
    owner = Owner(value=7)

    assert owner._value == 7
    assert owner.value == 7


def test_descriptor_values_are_isolated_between_instances():
    first = Owner(value=1)
    second = Owner(value=2)

    first.value = 3

    assert first.value == 3
    assert second.value == 2


def test_descriptor_can_alias_another_descriptor():
    owner = Owner()

    owner.alias = 8

    assert owner.alias == 8
    assert owner.value == 8
    assert owner._value == 8


def test_descriptor_chain_uses_public_name_of_inner_descriptor():
    assert Owner.alias._backing_name == "value"
    assert Owner.alias.private_field is Owner.value


def test_annotated_descriptors_are_not_dataclass_fields_or_slots():
    assert [item.name for item in fields(Owner)] == ["_value"]
    assert Owner.__slots__ == ("_value",)
    assert "value" not in Owner.__annotations__
    assert "alias" not in Owner.__annotations__


def test_get_with_null_instance_returns_descriptor_even_when_unbound():
    descriptor = BackedDescriptor(field(default=1))

    assert descriptor.__get__(None, object) is descriptor


def test_set_before_backing_name_is_known_has_clear_error():
    descriptor = BackedDescriptor(field(default=1))

    with pytest.raises(ValueError, match="not yet aware of the supporting field"):
        descriptor.__set__(object(), 2)


def test_set_name_with_none_is_a_no_op():
    descriptor = BackedDescriptor(field(default=1))

    descriptor.__set_name__(object, None)

    assert descriptor.name is None
    assert descriptor._backing_name is None
    assert not hasattr(descriptor, "__name__")


def test_existing_backing_name_is_not_overwritten_by_set_name():
    backing_field = field(default=1)
    backing_field.name = "_original"
    descriptor = BackedDescriptor(backing_field)
    descriptor._backing_name = "_explicit"

    descriptor.__set_name__(object, "value")

    assert descriptor.name == "value"
    assert descriptor._backing_name == "_explicit"


def test_repeated_set_name_updates_public_name_but_keeps_backing_name():
    backing_field = field(default=1)
    backing_field.name = "_value"
    descriptor = BackedDescriptor(backing_field)

    descriptor.__set_name__(object, "first")
    descriptor.__set_name__(object, "second")

    assert descriptor.name == "second"
    assert descriptor.__name__ == "second"
    assert descriptor._backing_name == "_value"


def test_get_before_backing_name_is_known_currently_raises_type_error():
    descriptor = BackedDescriptor(field(default=1))

    with pytest.raises(TypeError):
        descriptor.__get__(object(), object)


@pytest.mark.xfail(
    strict=True,
    reason="Plain dataclass decoration does not rebind the Field name to the descriptor",
)
def test_descriptor_works_with_plain_non_slotted_dataclass():
    backing_field = field(default=1)

    @dataclass
    class PlainOwner:
        _value: int = backing_field

        value = BackedDescriptor(backing_field)

    owner = PlainOwner()
    owner.value = 2

    assert owner._value == 2
