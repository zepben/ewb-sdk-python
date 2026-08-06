#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import Field, field, fields, is_dataclass

import pytest

from zepben.ewb.boilerplate.backed_descriptor import BackedDescriptor
from zepben.ewb.boilerplate.dataclass_base import (
    DataclassBase,
    _is_set,
    remove_descriptor_annotations,
    resolve_default,
    zb_dataclass,
)


# Exhaustive behavioural coverage for the custom dataclass lifecycle.


@zb_dataclass
class Example(DataclassBase):
    required: int
    scalar_default: str = "default"
    factory_default: list[int] = field(default_factory=list)
    init_false_default: int = field(default=42, init=False)


@zb_dataclass
class Parent(DataclassBase):
    parent_required: int
    overridden: int = 1

    def __init__(self, parent_required: int, **kwargs):
        self.parent_required = parent_required
        super(Parent, self).__init__(**kwargs)


@zb_dataclass
class Child(Parent):
    overridden: float = 2.5
    child_default: str = "child"


@zb_dataclass
class DescriptorExample(DataclassBase):
    _value: int = field(default=0)
    writes: list[int] = field(default_factory=list)

    value: int = BackedDescriptor(_value)

    @property
    def recorded_value(self) -> int:
        return self._value

    @recorded_value.setter
    def recorded_value(self, value: int) -> None:
        self.writes.append(value)
        self._value = value


def test_zb_dataclass_creates_a_slotted_dataclass_without_generated_init():
    assert is_dataclass(Example)
    assert Example.__init__ is DataclassBase.__init__
    assert set(Example.__slots__) == {
        "required",
        "scalar_default",
        "factory_default",
        "init_false_default",
    }
    assert not hasattr(Example(required=1), "__dict__")


def test_zb_dataclass_preserves_identity_equality_and_object_repr():
    first = Example(required=1)
    second = Example(required=1)

    assert first == first
    assert first != second
    assert repr(first).startswith("<")
    assert "Example object at" in repr(first)


def test_constructor_populates_scalar_and_factory_defaults():
    instance = Example(required=1)

    assert instance.scalar_default == "default"
    assert instance.factory_default == []
    assert instance.init_false_default == 42


def test_default_factory_is_evaluated_once_per_instance():
    first = Example(required=1)
    second = Example(required=2)

    first.factory_default.append(1)

    assert first.factory_default == [1]
    assert second.factory_default == []
    assert first.factory_default is not second.factory_default


def test_constructor_keywords_override_defaults():
    supplied = [1, 2]

    instance = Example(
        required=3,
        scalar_default="supplied",
        factory_default=supplied,
    )

    assert instance.required == 3
    assert instance.scalar_default == "supplied"
    assert instance.factory_default is supplied


def test_missing_required_field_reports_field_and_class():
    with pytest.raises(
        TypeError,
        match=r"Missing required field 'required' for Example",
    ):
        Example()


def test_init_false_field_uses_default_but_rejects_constructor_value():
    assert Example(required=1).init_false_default == 42

    with pytest.raises(
        TypeError,
        match=r"Example.__init__\(\) got an unexpected keyword argument 'init_false_default'",
    ):
        Example(required=1, init_false_default=2)


def test_slots_reject_unknown_constructor_keywords():
    with pytest.raises(AttributeError, match="unknown"):
        Example(required=1, unknown="value")


def test_preassigned_required_field_is_not_resolved_again():
    instance = Child(7)

    assert instance.parent_required == 7
    assert instance.overridden == 2.5
    assert instance.child_default == "child"


def test_inherited_field_can_be_overridden_by_keyword():
    instance = Child(7, overridden=9.5)

    assert instance.overridden == 9.5


def test_subclass_field_override_uses_subclass_default_and_type():
    parent = Parent(1)
    child = Child(1)

    assert parent.overridden == 1
    assert child.overridden == 2.5
    assert type(child.overridden) is float


def test_constructor_keyword_invokes_backed_descriptor():
    instance = DescriptorExample(value=12)

    assert instance.value == 12
    assert instance._value == 12


def test_constructor_keyword_invokes_property_setter():
    instance = DescriptorExample(recorded_value=12)

    assert instance.recorded_value == 12
    assert instance.writes == [12]


def test_descriptor_annotations_are_excluded_from_fields_and_slots():
    assert [item.name for item in fields(DescriptorExample)] == [
        "_value",
        "writes",
    ]
    assert set(DescriptorExample.__slots__) == {"_value", "writes"}
    assert "value" not in DescriptorExample.__annotations__


def test_post_init_is_explicitly_rejected_before_initialisation():
    @zb_dataclass
    class WithPostInit(DataclassBase):
        value: int = 1

        def __post_init__(self):
            raise AssertionError("must not be called")

    with pytest.raises(NotImplementedError, match="does not support __post_init__"):
        WithPostInit()


def test_is_set_distinguishes_populated_and_unpopulated_slots():
    instance = Example.__new__(Example)

    assert not _is_set(instance, "required")

    instance.required = 1

    assert _is_set(instance, "required")


def test_is_set_treats_attribute_error_from_descriptor_as_unset():
    class RaisingDescriptor:
        def __get__(self, instance, owner=None):
            raise AttributeError("missing")

    class Owner:
        value = RaisingDescriptor()

    assert not _is_set(Owner(), "value")


def test_remove_descriptor_annotations_returns_same_class_and_new_mapping():
    class Descriptor:
        def __get__(self, instance, owner=None):
            return None

    class Undecorated:
        plain: int
        descriptor: int = Descriptor()
        dc_field: int = field(default=1)

    original_annotations = Undecorated.__annotations__

    result = remove_descriptor_annotations(Undecorated)

    assert result is Undecorated
    assert Undecorated.__annotations__ == {"plain": int, "dc_field": int}
    assert Undecorated.__annotations__ is not original_annotations
    assert original_annotations == {
        "plain": int,
        "descriptor": int,
        "dc_field": int,
    }


@pytest.mark.parametrize("method_name", ["__get__", "__set__"])
def test_remove_descriptor_annotations_recognises_either_descriptor_method(
    method_name: str,
):
    descriptor_type = type(
        "PartialDescriptor",
        (),
        {method_name: lambda *args: None},
    )

    class Undecorated:
        value: int = descriptor_type()

    remove_descriptor_annotations(Undecorated)

    assert Undecorated.__annotations__ == {}


def test_remove_descriptor_annotations_preserves_dataclass_fields():
    class Undecorated:
        value: int = field(default=1)

    remove_descriptor_annotations(Undecorated)

    assert Undecorated.__annotations__ == {"value": int}
    assert isinstance(Undecorated.value, Field)


def test_remove_descriptor_annotations_handles_class_without_annotations():
    class Undecorated:
        pass

    assert remove_descriptor_annotations(Undecorated) is Undecorated
    assert Undecorated.__annotations__ == {}


def test_resolve_default_assigns_scalar_default():
    instance = Example.__new__(Example)
    scalar_field = next(item for item in fields(Example) if item.name == "scalar_default")

    resolve_default(instance, scalar_field)

    assert instance.scalar_default == "default"


def test_resolve_default_calls_default_factory():
    instance = Example.__new__(Example)
    factory_field = next(item for item in fields(Example) if item.name == "factory_default")

    resolve_default(instance, factory_field)

    assert instance.factory_default == []


def test_resolve_default_rejects_field_without_default():
    instance = Example.__new__(Example)
    required_field = next(item for item in fields(Example) if item.name == "required")

    with pytest.raises(
        TypeError,
        match=r"Missing required field 'required' for Example",
    ):
        resolve_default(instance, required_field)


@pytest.mark.xfail(
    strict=True,
    reason="Required backing fields are resolved before descriptor keywords are assigned",
)
def test_descriptor_keyword_can_supply_required_backing_field():
    @zb_dataclass
    class RequiredBacking(DataclassBase):
        _value: int = field()
        value: int = BackedDescriptor(_value)

    instance = RequiredBacking(value=3)

    assert instance._value == 3


@pytest.mark.xfail(
    strict=True,
    reason="slots=True returns a replacement class and breaks zero-argument super()",
)
def test_zb_dataclass_supports_zero_argument_super():
    @zb_dataclass
    class ZeroArgSuper(DataclassBase):
        value: int = 1

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

    assert ZeroArgSuper().value == 1
