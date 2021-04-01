#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import unittest

from _pytest.python_api import raises

from zepben.evolve.model.cim.iec61970.base.core import identified_object
from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.evolve.model.cim.iec61970.base.core.name import Name
from zepben.evolve.model.cim.iec61970.base.core.name_type import NameType
from zepben.evolve.model.cim.iec61970.base.wires.connectors import Junction


class TestNameType(object):

    def test_constructor_coverage(self):
        assert NameType("type").name == "type"

    def test_name_and_description(self):
        name_type = NameType("type")
        assert name_type.name == "type"
        assert name_type.description == ""

        name_type.name = "type"
        name_type.description = ""

        assert name_type.name == "type"
        assert name_type.description == ""

    def test_get_or_add_names(self):
        name_type = NameType("type")
        id_obj_1 = Junction()
        name1 = name_type.get_or_add_name("name1", id_obj_1)

        assert name1 == name_type.get_or_add_name("name1", id_obj_1)
        assert name_type.has_name("name1")

    def test_get_names_returns_all_instances(self):
        name_type = NameType("type")
        id_obj_1 = Junction()
        id_obj_2 = Junction()
        id_obj_3 = Junction()
        name1 = name_type.get_or_add_name("name1", id_obj_1)
        name2 = name_type.get_or_add_name("name1", id_obj_2)
        name3 = name_type.get_or_add_name("name1", id_obj_3)
        names = name_type.get_names("name1")

        for name in [name1, name2, name3]:
            assert name in names
        assert len(names) == 3

    def test_returns_all_names(self):
        name_type = NameType("type")
        id_obj_1 = Junction()
        id_obj_2 = Junction()
        name1 = name_type.get_or_add_name("name1", id_obj_1)
        name2 = name_type.get_or_add_name("name1", id_obj_2)
        name3 = name_type.get_or_add_name("name2", id_obj_2)
        names = list(name_type.names)

        for name in [name1, name2, name3]:
            assert name in names
        assert len(names) == 3

    def test_removes_names(self):
        name_type = NameType("type")
        id_obj_1 = Junction()
        id_obj_2 = Junction()
        name1a = name_type.get_or_add_name("name1", id_obj_1)
        name1b = name_type.get_or_add_name("name1", id_obj_2)
        name2 = name_type.get_or_add_name("name2", id_obj_2)
        names = name_type.get_names("name1")

        for name in [name1a, name1b]:
            assert name in names
        assert len(names) == 2

        assert name2 in name_type.get_names("name2")
        assert name_type.remove_name(name1b)
        assert name1a in name_type.get_names("name1")
        assert name2 in name_type.get_names("name2")

        assert name_type.remove_name(name1a)
        with raises(KeyError):
            name_type.get_names("name1")
        assert name2 in name_type.get_names("name2")

    def test_remove_names_instance(self):
        name_type = NameType("type")
        id_obj_1 = Junction()
        id_obj_2 = Junction()
        name1a = name_type.get_or_add_name("name1", id_obj_1)
        name1b = name_type.get_or_add_name("name1", id_obj_2)
        names = name_type.get_names("name1")

        for name in [name1a, name1b]:
            assert name in names
        assert len(names) == 2

        assert name_type.remove_name(name1a)
        assert name1b in name_type.get_names("name1")

    def test_clear_names(self):
        name_type = NameType("type")
        id_obj_1 = Junction()
        id_obj_2 = Junction()
        name1 = name_type.get_or_add_name("name1", id_obj_1)
        name2 = name_type.get_or_add_name("name2", id_obj_2)

        assert name1 in name_type.get_names("name1")
        assert name2 in name_type.get_names("name2")

        name_type.clear_names()
        assert not list(name_type.names)
