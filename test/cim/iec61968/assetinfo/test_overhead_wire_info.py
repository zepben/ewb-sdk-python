#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.fill_fields import overhead_wire_info_kwargs
from cim.iec61968.assetinfo.test_wire_info import verify_wire_info_constructor_default, \
    verify_wire_info_constructor_kwargs
from zepben.ewb import generate_id
from zepben.ewb.model.cim.iec61968.assetinfo.overhead_wire_info import OverheadWireInfo


def test_overhead_wire_info_constructor_default():
    verify_wire_info_constructor_default(OverheadWireInfo(mrid=generate_id()))


@given(**overhead_wire_info_kwargs())
def test_overhead_wire_info_constructor_kwargs(**kwargs):
    verify_wire_info_constructor_kwargs(OverheadWireInfo(**kwargs), **kwargs)
