#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import IdentifiedObject
from zepben.evolve.model.cim.iec61970.base.core.name import Name
from zepben.evolve.model.cim.iec61970.base.core.name_type import NameType


def test_names():
    identified_object = IdentifiedObject("id")
    name1 = Name("1", NameType("type"), identified_object)
    name2 = Name("2", NameType("type"), identified_object)
    name3 = Name("3", NameType("type"), identified_object)
    duplicate1 = Name("1", NameType("type"), identified_object)

    assert not name1 == name2
    assert not name1 == name3
    assert not name2 == name3

    assert identified_object.num_names() == 0

    identified_object.add_name(name1)
    identified_object.add_name(name2)
    identified_object.add_name(name3)
    assert identified_object.num_names() == 3
    identified_object.add_name(duplicate1)

    assert identified_object.num_names() == 3

    assert identified_object.remove_name(name1)
    assert not identified_object.remove_name(name1)
    assert not identified_object.remove_name(None)
    assert identified_object.num_names() == 2

    assert identified_object.get_name("type", name2.name) == name2

    assert name1 and name2 in identified_object.names

    identified_object.clear_names()
    assert identified_object.num_names() == 0

    identified_object.add_name(name1)
    assert identified_object.num_names() == 1

    identified_object.remove_name(name1)
    assert identified_object.num_names() == 0

    identified_object.remove_name(name2)
    assert identified_object.num_names() == 0


