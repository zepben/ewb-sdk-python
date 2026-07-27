#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import field

from zepben.ewb.boilerplate.dataclass_base import DataclassBase
from zepben.ewb import zb_dataclass, remove_descriptor_annotations
from zepben.ewb.boilerplate.descriptor_fix import BackedDescriptor


@zb_dataclass
class DescriptorTest(DataclassBase):
    _x: int = field(default=0)
    x: int = BackedDescriptor(_x)


def test_backed_descriptor():
    # Check the descriptor gets set
    obj = DescriptorTest(x=42)

    # Check the slots were generated correctly - descriptor is not slotted
    # noinspection PyUnresolvedReferences
    assert obj.__slots__ == ('_x',)

    # Check value is persistent
    assert obj.x == 42
    # Check that the underlying variable was used
    assert obj._x == 42
