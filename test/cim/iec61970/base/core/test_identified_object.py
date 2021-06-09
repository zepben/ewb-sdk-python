#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis.strategies import uuids, text

from test.cim_creators import ALPHANUM, TEXT_MAX_SIZE
from zepben.evolve import IdentifiedObject

#
# NOTE: The following should be called in a chain through the inheritance hierarchy:
#       1. verify...default verifies the constructor with no args.
#       2. verify...kwargs verifies the constructor with a given set of named arguments.
#       3. verify...args verifies the constructor with a given set of positional arguments.
# There is a lot of overlap here, but calling both maximises the constructor combinations we check and should catch any breaking changes to
# constructors.
#

identified_object_kwargs = {
    "mrid": uuids(version=4).map(lambda x: str(x)),
    "name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "description": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
}

identified_object_args = ["test_mrid", "test_name", "test_description"]


def verify_identified_object_constructor_default(io: IdentifiedObject):
    assert io.mrid
    assert io.name == ""
    assert io.description == ""


def verify_identified_object_constructor_kwargs(io: IdentifiedObject, mrid, name, description, **kwargs):
    assert not kwargs, f"found unexpected args: {kwargs}"

    assert io.mrid == mrid
    assert io.name == name
    assert io.description == description


def verify_identified_object_constructor_args(io: IdentifiedObject):
    assert io.mrid == identified_object_args[0]
    assert io.name == identified_object_args[1]
    assert io.description == identified_object_args[2]
