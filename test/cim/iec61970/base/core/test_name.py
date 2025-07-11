#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import text, builds
from zepben.ewb.model.cim.iec61970.base.wires.junction import Junction
from zepben.ewb.model.cim.iec61970.base.core.name import Name
from zepben.ewb.model.cim.iec61970.base.core.name_type import NameType

from cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE, sampled_equipment
from cim.iec61970.base.core.test_name_type import name_type_kwargs

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


# noinspection PyShadowingBuiltins
@given(**name_kwargs)
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
