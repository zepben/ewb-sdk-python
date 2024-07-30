#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections import Counter

from cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE
from hypothesis import given
from hypothesis.strategies import text

from zepben.evolve.model.cim.iec61970.base.core.name_type import NameType
from zepben.evolve.model.cim.iec61970.base.wires.connectors import Junction

name_type_kwargs = {
    "name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "description": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
}

# noinspection PyArgumentList
name_type_args = ["1", "2"]


def test_name_type_constructor_default():
    # noinspection PyArgumentList
    nt = NameType("nt")

    assert nt.name == "nt"
    assert not nt.description
    assert not list(nt.names)


@given(**name_type_kwargs)
def test_name_type_constructor_kwargs(name, description, **kwargs):
    # noinspection PyArgumentList
    nt = NameType(name=name, description=description, **kwargs)

    assert nt.name == name
    assert nt.description == description
    assert not list(nt.names)


def test_name_type_constructor_args():
    # noinspection PyArgumentList
    nt = NameType(*name_type_args)

    assert nt.name == name_type_args[0]
    assert nt.description == name_type_args[1]
    assert not list(nt.names)


#
# NOTE: The names collection is non-standard and can't be tested with the verify_container methods.
#


def test_get_or_add_names():
    # noinspection PyArgumentList
    nt = NameType("nt")

    j1 = Junction()
    j2 = Junction()

    n1 = nt.get_or_add_name("n", j1)
    n2 = nt.get_or_add_name("n", j2)

    assert nt.has_name("n")
    assert n1 is not n2

    # test returns same instance if added again
    assert n1 == nt.get_or_add_name("n", j1)
    assert n2 == nt.get_or_add_name("n", j2)


def test_names():
    # noinspection PyArgumentList
    nt = NameType("nt")

    j1 = Junction()
    j2 = Junction()

    n1a = nt.get_or_add_name("n1", j1)
    n1b = nt.get_or_add_name("n1", j2)
    n2 = nt.get_or_add_name("n2", j2)

    assert Counter(list(nt.names)) == Counter({n1a, n1b, n2})


def test_get_names():
    # noinspection PyArgumentList
    nt = NameType("nt")

    j1 = Junction()
    j2 = Junction()

    n1a = nt.get_or_add_name("n1", j1)
    n1b = nt.get_or_add_name("n1", j2)
    n2 = nt.get_or_add_name("n2", j2)

    assert Counter(list(nt.get_names("n1"))) == Counter({n1a, n1b})
    assert Counter([entry for entries in list(nt.get_names(j2)) for entry in entries]) == Counter({n1b, n2})
    assert list(nt.get_names("n2")) == [n2]
    assert not list(nt.get_names("n3"))


def test_removes_names():
    # noinspection PyArgumentList
    nt = NameType("nt")

    j1 = Junction()
    j2 = Junction()

    n1a = nt.get_or_add_name("n1", j1)
    n1b = nt.get_or_add_name("n1", j2)
    n2 = nt.get_or_add_name("n2", j2)

    assert Counter(list(nt.names)) == Counter({n1a, n1b, n2})

    assert nt.remove_names("n1")
    assert list(nt.names) == [n2]

    assert nt.remove_names("n2")
    assert not list(nt.names)


def test_remove_name():
    # noinspection PyArgumentList
    nt = NameType("nt")

    j1 = Junction()
    j2 = Junction()

    n1a = nt.get_or_add_name("n1", j1)
    n1b = nt.get_or_add_name("n1", j2)
    n2 = nt.get_or_add_name("n2", j2)

    assert Counter(list(nt.names)) == Counter({n1a, n1b, n2})

    assert nt.remove_name(n1b)
    assert Counter(list(nt.names)) == Counter({n1a, n2})

    assert nt.remove_name(n1a)
    assert list(nt.names) == [n2]

    assert nt.remove_name(n2)
    assert not list(nt.names)


def test_clear_names():
    # noinspection PyArgumentList
    nt = NameType("nt")

    j1 = Junction()

    n1 = nt.get_or_add_name("n1", j1)
    n2 = nt.get_or_add_name("n2", j1)

    assert Counter(list(nt.names)) == Counter({n1, n2})

    nt.clear_names()
    assert not list(nt.names)
