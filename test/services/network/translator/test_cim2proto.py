#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from zepben.protobuf.cim.iec61970.base.wires.BusbarSection_pb2 import BusbarSection
from zepben.protobuf.cim.iec61970.base.wires.LoadBreakSwitch_pb2 import LoadBreakSwitch

from test.cim_creators import busbarsection
from test.cim_creators import loadbreakswitch


@given(bbs=busbarsection())
def test_busbar_to_pb(bbs):
    pb = bbs.to_pb()
    assert pb.mrid() == bbs.mrid
    assert isinstance(pb, BusbarSection)


@given(lbs=loadbreakswitch())
def test_loadbreakswitch_to_pb(lbs):
    pb = lbs.to_pb()
    assert pb.mrid() == lbs.mrid
    verify_protected_switch(lbs, pb)
    assert isinstance(pb, LoadBreakSwitch)


def verify_protected_switch(cim, pb):
    verify_switch(cim, pb)


def verify_switch(cim, pb):
    # Protobuf switch open/normalOpen are currently bools, so we can only perform a naive check of if all phases are closed
    # or if a single phase is open.
    if not cim.is_open():
        assert not pb.ps.sw.open
    if not cim.is_normally_open():
        assert not pb.ps.sw.normalOpen

    if cim.is_open():
        assert pb.ps.sw.open
    if cim.is_normally_open():
        assert pb.ps.sw.normalOpen
