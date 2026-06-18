#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import field
from typing import List

import pytest

from zepben.ewb.dataclass_descriptors import zb_dataclass, remove_descriptor_annotations, DataclassBase


@zb_dataclass
@remove_descriptor_annotations
class Root(DataclassBase):
    mrid: str
    y: int
    x: int = 42

    def __hash__(self):
        return hash(self.mrid)

    def __init__(self, mrid, *_, **kwargs):
        self.mrid = mrid
        super(Root, self).__init__(**kwargs)

@zb_dataclass
@remove_descriptor_annotations
class Child(Root):
    x: float = 42.0
    z: str = "abc"

    dc_default: int = field(default=99)
    dc_default_factory: List[int] = field(default_factory=lambda : [33])


def test_dataclass_base():
    mrid = "CLARKSOOOOOOOON"

    # Check that required fields are all filled
    with pytest.raises(TypeError, match="Missing required field 'y'"):
        Child("mrid")

    # Check instantiation and subclassing
    obj = Child(mrid, y=33, z="Hello there")
    # Memory layout correct
    # noinspection PyUnresolvedReferences
    assert obj.__slots__ == ('mrid', 'y', 'x', 'z', 'dc_default', 'dc_default_factory')

    # positional arg
    assert obj.mrid == mrid
    # type overriding
    assert type(obj.x) is float
    # default values
    assert obj.x == 42.0
    # kwargs
    assert obj.y == 33
    assert obj.z == "Hello there"
    # dataclass fields working as intended
    assert obj.dc_default == 99
    assert obj.dc_default_factory == [33]

    # Assignment
    obj.x = 6.9
    obj.z = "boop"
    assert obj.x == 6.9
    assert obj.z == "boop"

    # Hash overwrite is owned by root
    assert hash(obj) == hash(mrid)

    # Check that field factories dont share memory
    other = Child("mrid2", y=42)
    other.dc_default_factory.append(24)
    assert obj.dc_default_factory == [33]
