#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given

from cim.fill_fields import name_kwargs
from zepben.ewb import generate_id
from zepben.ewb.model.cim.iec61970.base.core.name import Name
from zepben.ewb.model.cim.iec61970.base.core.name_type import NameType
from zepben.ewb.model.cim.iec61970.base.wires.junction import Junction

# noinspection PyArgumentList
name_args = ["1", NameType("nt1"), Junction(mrid=generate_id())]


#
# NOTE: There is no default constructor so no need to test it.
#
# def test_name_constructor_default():


# noinspection PyShadowingBuiltins
@given(**name_kwargs())
def test_name_constructor_kwargs(name, type, identified_object, **kwargs):
    assert not kwargs, f"found unexpected args: {kwargs}"

    n = Name(name, type, identified_object)

    assert n.name == name
    assert n.type == type
    assert n.identified_object == identified_object


def test_name_constructor_args():
    n = Name(*name_args)

    assert name_args == [
        n.name,
        n.type,
        n.identified_object
    ]
