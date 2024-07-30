#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import re

from cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE, create_name_type
from hypothesis.strategies import uuids, text, lists, builds

from test.cim.collection_validator import validate_identified_object_name_collection
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


def test_names_collection():
    # noinspection PyTypeChecker, PyArgumentList
    validate_identified_object_name_collection(IdentifiedObject,
                                               lambda mrid, io: Name(mrid, NameType("name_type"), io),
                                               IdentifiedObject.num_names,
                                               lambda io, name: io.get_name(name.type.name, name.name),
                                               lambda io, name: io.get_names(name),
                                               IdentifiedObject.names,
                                               IdentifiedObject.add_name,
                                               IdentifiedObject.remove_name,
                                               IdentifiedObject.clear_names,
                                               lambda it, dup: re.escape(rf"Failed to add duplicate name {str(dup)} to {str(it)}."))
