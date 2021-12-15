#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import text, builds

from test.cim.extract_testing_args import extract_testing_args
from test.cim.iec61970.base.core.test_name_type import name_type_kwargs
from test.cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE, sampled_equipment
from zepben.evolve import Junction, IdentifiedObject
from zepben.evolve.model.cim.iec61970.base.core.create_core_components import create_name
from zepben.evolve.model.cim.iec61970.base.core.name import Name
from zepben.evolve.model.cim.iec61970.base.core.name_type import NameType

name_kwargs = {
    "name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "type": builds(NameType, **name_type_kwargs),
    "identified_object": sampled_equipment(True)
}

# noinspection PyArgumentList
name_args = ["1", NameType("nt1"), Junction()]


#
# NOTE: There is no default constructor so no need to test it.
#
# def test_name_constructor_default():


# noinspection PyShadowingBuiltins,PyArgumentList
@given(**name_kwargs)
def test_name_constructor_kwargs(name, type, identified_object, **kwargs):
    args = extract_testing_args(locals())
    n = Name(**args, **kwargs)
    validate_name_values(n, **args)


# noinspection PyShadowingBuiltins
@given(**name_kwargs)
def test_name_creator(name, type, identified_object, **kwargs):
    args = extract_testing_args(locals())
    n = create_name(**args, **kwargs)
    validate_name_values(n, **args)


def validate_name_values(n, name, type, identified_object):
    assert n.name == name
    assert n.type == type
    assert n.identified_object == identified_object


def test_name_constructor_args():
    # noinspection PyArgumentList
    n = Name(*name_args)

    assert n.name == name_args[0]
    assert n.type == name_args[1]
    assert n.identified_object == name_args[2]


def test_auto_two_way_connections_for_name_constructor():
    nt = NameType(name='nameType')
    io = IdentifiedObject()
    n = create_name(name='name', type=nt, identified_object=io)

    assert nt.get_or_add_name(n, io).name == n
    assert nt.get_or_add_name(n, io).identified_object == io
    assert io.get_name(nt.name, n.name) == n
