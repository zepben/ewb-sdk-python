#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from zepben.protobuf.cim.iec61970.base.wires.BusbarSection_pb2 import BusbarSection
from zepben.protobuf.cim.iec61970.base.wires.LoadBreakSwitch_pb2 import LoadBreakSwitch
from zepben.protobuf.cim.iec61970.base.wires.Junction_pb2 import Junction
from zepben.protobuf.cim.iec61970.base.wires.AcLineSegment_pb2 import AcLineSegment
from zepben.protobuf.cim.iec61970.base.wires.EnergySource_pb2 import EnergySource
from zepben.protobuf.cim.iec61970.base.wires.EnergyConsumer_pb2 import EnergyConsumer
from zepben.protobuf.cim.iec61970.base.wires.Disconnector_pb2 import Disconnector
from zepben.protobuf.cim.iec61970.base.wires.Fuse_pb2 import Fuse
from zepben.protobuf.cim.iec61970.base.wires.Jumper_pb2 import Jumper
from zepben.protobuf.cim.iec61970.base.wires.Breaker_pb2 import Breaker
from zepben.protobuf.cim.iec61970.base.wires.LinearShuntCompensator_pb2 import LinearShuntCompensator
from zepben.protobuf.cim.iec61970.base.wires.RatioTapChanger_pb2 import RatioTapChanger



from test.cim_creators import busbarsection, loadbreakswitch, energysource, energyconsumer, junction, aclinesegment, \
disconnector, fuse, jumper, breaker, linearshuntcompensator, ratiotapchanger


@given(bbs=busbarsection())
def test_busbar_to_pb(bbs):
    pb = bbs.to_pb()
    assert pb.mrid() == bbs.mrid
    assert isinstance(pb, BusbarSection)

@given(dis=disconnector())
def test_disconnector_to_pb(dis):
    pb = dis.to_pb()
    assert pb.mrid() == dis.mrid
    assert isinstance(pb, Disconnector)

@given(fus=fuse())
def test_fuse_to_pb(fus):
    pb = fus.to_pb()
    assert pb.mrid() == fus.mrid
    assert isinstance(pb, Fuse)

@given(jum=jumper())
def test_jumper_to_pb(jum):
    pb = jum.to_pb()
    assert pb.mrid() == jum.mrid
    assert isinstance(pb, Jumper)

@given(brk=breaker())
def test_breaker_to_pb(brk):
    pb = brk.to_pb()
    assert pb.mrid() == brk.mrid
    assert isinstance(pb, Breaker)

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

@given(jnc=junction())
def test_junction_to_pb(jnc):
    pb = jnc.to_pb()
    assert pb.mrid() == jnc.mrid
    assert isinstance(pb, Junction)

@given(acl=aclinesegment())
def test_aclinesegment_to_pb(acl):
    pb = acl.to_pb()
    assert pb.mrid() == acl.mrid
    assert isinstance(pb, AcLineSegment)

@given(ens=energysource())
def test_energysource_to_pb(ens):
    pb = ens.to_pb()
    assert pb.mrid() == ens.mrid
    assert isinstance(pb, EnergySource)
    assert pb.activePower == ens.active_power
    assert pb.r == ens.r
    assert pb.x == ens.x
    assert pb.reactivePower == ens.reactive_power
    assert pb.voltageAngle == ens.voltage_angle
    assert pb.voltageMagnitude == ens.voltage_magnitude
    assert pb.pMax == ens.p_max
    assert pb.pMin == ens.p_min
    assert pb.r0 == ens.r0
    assert pb.rn == ens.rn
    assert pb.x0 == ens.x0
    assert pb.xn == ens.xn


@given(enc=energyconsumer())
def test_energyconsumer_to_pb(enc):
    pb = enc.to_pb()
    assert pb.mrid() == enc.mrid
    assert isinstance(pb, EnergyConsumer)

def verify_energyconsumer_parameters():
    pb = enc.to_pb(NetworkService())
    assert pb.p == enc.p
    assert pb.q == enc.q
    assert pb.p_fixed == enc.p_fixed
    assert pb.q_fixed == enc.q_fixed

#@given(lsc=linearshuntcompensator())
#def test_linearshuntcompensator_to_pb(lsc):
    #pb = lsc.to_pb()
    #assert pb.mrid() == lsc.mrid
    #assert isinstance(pb, LinearShuntCompensator)'''
