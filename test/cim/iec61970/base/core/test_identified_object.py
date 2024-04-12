#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections import Counter
from typing import Tuple

import pytest
from hypothesis.strategies import uuids, text, lists, builds

from cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE, create_name_type
from zepben.evolve import IdentifiedObject, Junction
#
# NOTE: The following should be called in a chain through the inheritance hierarchy:
#       1. verify...default verifies the constructor with no args.
#       2. verify...kwargs verifies the constructor with a given set of named arguments.
#       3. verify...args verifies the constructor with a given set of positional arguments.
# There is a lot of overlap here, but calling both maximises the constructor combinations we check and should catch any breaking changes to
# constructors.
#
from zepben.evolve.model.cim.iec61970.base.core.name_type import Name, NameType

identified_object_kwargs = {
    "mrid": uuids(version=4).map(lambda x: str(x)),
    "name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "description": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "names": lists(builds(Name, text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), create_name_type()),
                   max_size=2,
                   unique_by=lambda it: it.name)
}

# noinspection PyArgumentList
identified_object_args = ["test_mrid", "test_name", "test_description", [Name("1", NameType("nt1"), Junction())]]


def verify_identified_object_constructor_default(io: IdentifiedObject):
    assert io.mrid
    assert io.name == ""
    assert io.description == ""
    assert not list(io.names)


def verify_identified_object_constructor_kwargs(io: IdentifiedObject, mrid, name, description, names, **kwargs):
    assert not kwargs, f"found unexpected args: {kwargs}"

    assert io.mrid == mrid
    assert io.name == name
    assert io.description == description
    # Assign identified object to the names we are checking against due to no identified object requirement on Name creation
    # Note: this is due to automatic two-way association introduced in the name rejig rework
    for name in names:
        name.identified_object = io
    assert list(io.names) == names


def verify_identified_object_constructor_args(io: IdentifiedObject):
    assert io.mrid == identified_object_args[0]
    assert io.name == identified_object_args[1]
    assert io.description == identified_object_args[2]
    assert list(io.names) == identified_object_args[3]


def test_user_can_add_names_to_identified_object():
    identified_object = IdentifiedObject()
    # noinspection PyArgumentList
    name_type = NameType("type")
    assert identified_object.num_names() == 0

    identified_object.add_name(name_type, "1")

    assert identified_object.num_names() == 1


def test_adding_identical_name_to_the_same_object_doesnt_change_the_list_of_names_belonging_to_it():
    identified_object, name_type = _create_multiple_base_names()
    original_names = list(identified_object.names)

    identified_object.add_name(name_type, "1")
    new_names = list(identified_object.names)
    assert original_names == new_names


def test_getname_obtain_expected_name_object():
    identified_object, _ = _create_multiple_base_names()

    name1 = identified_object.get_name("type", "1")
    name2 = identified_object.get_name("type", "2")
    name3 = identified_object.get_name("type", "3")

    assert name2.name == "2"
    assert name2.type.name == "type"

    # Make sure item obtained are different
    assert name1 is not name2
    assert name1 is not name3
    assert name2 is not name3


def test_getname_grabs_the_same_object_with_string_or_name_type():
    identified_object, name_type = _create_multiple_base_names()

    name2 = identified_object.get_name("type", "2")
    dupe_name2 = identified_object.get_name(name_type, "2")
    assert name2 is dupe_name2


def test_name_type_contains_the_names_added_to_the_identified_object():
    _, name_type = _create_multiple_base_names()

    assert name_type.has_name("1"), "expected to have name 1"
    assert name_type.has_name("2"), "expected to have name 2"
    assert name_type.has_name("3"), "expected to have name 3"


def test_get_names_obtains_all_names_of_a_identified_object_with_a_given_name_type():
    identified_object, name_type = _create_multiple_base_names()

    # noinspection PyArgumentList
    name_type2 = NameType("type2")
    # noinspection PyArgumentList
    name_type3 = NameType("type3")
    identified_object.add_name(name_type2, "1")

    assert len(identified_object.get_names(name_type)) == 3
    assert len(identified_object.get_names(name_type2)) == 1
    with pytest.raises(KeyError):
        identified_object.get_names(name_type3)


def test_remove_name_removes_name_from_the_identified_object_and_the_name_type():
    identified_object, name_type = _create_multiple_base_names()
    name1 = identified_object.get_name("type", "1")
    name2 = identified_object.get_name("type", "2")
    name3 = identified_object.get_name("type", "3")

    assert identified_object.remove_name(name1), "name1 successfully removed from name_type"
    with pytest.raises(ValueError):
        assert not identified_object.remove_name(name1), "name1 has already been removed from name_type"
    # not supported in python SDK: assert not identified_object.remove_name(None), "can not remove name null from identified_object"
    assert identified_object.num_names() == 2
    assert not name_type.has_name("1"), "should not have had name 1"

    assert Counter(identified_object.names) == Counter([name2, name3])


def test_clear_names_removes_all_names_from_the_identified_object_and_the_name_type():
    identified_object, name_type = _create_multiple_base_names()

    assert identified_object.num_names() == 3
    assert name_type.has_name("1"), "expected to have name 1"
    assert name_type.has_name("2"), "expected to have name 2"
    assert name_type.has_name("3"), "expected to have name 3"

    identified_object.clear_names()

    assert identified_object.num_names() == 0
    assert not name_type.has_name("1"), "should not have had name 1"
    assert not name_type.has_name("2"), "should not have had name 2"
    assert not name_type.has_name("3"), "should not have had name 3"


def test_user_can_add_the_same_name_back_after_it_has_been_removed():
    identified_object = IdentifiedObject()
    # noinspection PyArgumentList
    name_type = NameType("type")

    identified_object.add_name(name_type, "1")
    name1 = identified_object.get_name("type", "1")
    identified_object.clear_names()

    with pytest.raises(ValueError):
        identified_object.remove_name(name1), "name1 should not be in the collection after a clear"
    assert identified_object.num_names() == 0


def test_removing_name_from_empty_name_list_does_not_cause_any_issue():
    identified_object = IdentifiedObject()
    # noinspection PyArgumentList
    name_type = NameType("type")

    identified_object.add_name(name_type, "1")
    name1 = identified_object.get_name("type", "1")
    assert identified_object.num_names() == 1

    identified_object.remove_name(name1)
    assert identified_object.num_names() == 0

    identified_object.add_name(name_type, "1")
    dupe_name1 = identified_object.get_name(name_type, "1")
    assert name1 is not dupe_name1
    assert identified_object.num_names() == 1


def _create_multiple_base_names() -> Tuple[IdentifiedObject, NameType]:
    identified_object = IdentifiedObject()
    # noinspection PyArgumentList
    name_type = NameType("type")

    identified_object.add_name(name_type, "1")
    identified_object.add_name(name_type, "2")
    identified_object.add_name(name_type, "3")

    return identified_object, name_type
