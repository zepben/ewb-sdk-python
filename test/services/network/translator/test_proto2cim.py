#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from zepben.evolve import NetworkService, BusbarSection, Junction, EnergySource, EnergyConsumer, AcLineSegment, Disconnector, \
Fuse, Jumper, Breaker, LoadBreakSwitch, PowerTransformer, LinearShuntCompensator, RatioTapChanger

from test.pb_creators import busbarsection, junction, energysource, energyconsumer, aclinesegment, disconnector, fuse, \
jumper, breaker, loadbreakswitch, powertransformer, linearshuntcompensator, ratiotapchanger


@given(bbs=busbarsection())
def test_busbar_to_cim(bbs):
    cim = bbs.to_cim(NetworkService())
    assert cim.mrid == bbs.mrid()
    assert isinstance(cim, BusbarSection)

@given(jnc=junction())
def test_junction_to_cim(jnc):
    cim = jnc.to_cim(NetworkService())
    assert cim.mrid == jnc.mrid()
    assert isinstance(cim, Junction)

@given(acl=aclinesegment())
def test_aclinesegment_to_cim(acl):
    cim = acl.to_cim(NetworkService())
    assert cim.mrid == acl.mrid()
    assert isinstance(cim, AcLineSegment)

@given(ens=energysource())
def test_energysource_to_cim(ens):
    cim = ens.to_cim(NetworkService())
    assert cim.mrid == ens.mrid()
    assert isinstance(cim, EnergySource)
    assert cim.active_power == ens.activePower
    assert cim.r == ens.r
    assert cim.x == ens.x
    assert cim.reactive_power == ens.reactivePower
    assert cim.voltage_angle == ens.voltageAngle
    assert cim.voltage_magnitude == ens.voltageMagnitude
    assert cim.p_max == ens.pMax
    assert cim.p_min == ens.pMin
    assert cim.r0 == ens.r0
    assert cim.rn == ens.rn
    assert cim.x0 == ens.x0
    assert cim.xn == ens.xn

@given(enc=energyconsumer())
def test_energyconsumer_to_cim(enc):
    cim = enc.to_cim(NetworkService())
    assert cim.mrid == enc.mrid()
    assert isinstance(cim, EnergyConsumer)

def verify_energyconsumer_parameters():
    cim = enc.to_cim(NetworkService())
    assert cim.p == enc.p
    assert cim.q == enc.q
    assert cim.p_fixed == enc.p_fixed
    assert cim.q_fixed == enc.q_fixed

@given(dis=disconnector())
def test_disconnector_to_cim(dis):
    cim = dis.to_cim(NetworkService())
    assert cim.mrid == dis.mrid()
    assert isinstance(cim, Disconnector)

@given(fus=fuse())
def test_fuse_to_cim(fus):
    cim = fus.to_cim(NetworkService())
    assert cim.mrid == fus.mrid()
    assert isinstance(cim, Fuse)

@given(jum=jumper())
def test_jumper_to_cim(jum):
    cim = jum.to_cim(NetworkService())
    assert cim.mrid == jum.mrid()
    assert isinstance(cim, Jumper)

@given(brk=breaker())
def test_breaker_to_cim(brk):
    cim = brk.to_cim(NetworkService())
    assert cim.mrid == brk.mrid()
    assert isinstance(cim, Breaker)

@given(lbs=loadbreakswitch())
def test_loadbreakswitch_to_cim(lbs):
    cim = lbs.to_cim(NetworkService())
    assert cim.mrid == lbs.mrid()
    assert isinstance(cim, LoadBreakSwitch)

@given(pwt=powertransformer())
def test_disconnector_to_cim(pwt):
    cim = pwt.to_cim(NetworkService())
    assert cim.mrid == pwt.mrid()
    assert isinstance(cim, PowerTransformer)


#@given(rtc=ratiotapchanger())
#def test_ratiotapchanger_to_cim(rtc):
    #cim = rtc.to_cim(NetworkService())
    #assert cim.mrid == rtc.mrid()
    #assert isinstance(cim, RatioTapChanger)

#@given(lsc=LinearShuntCompensator())
#def test_linearshuntcompensator_to_cim(lsc):
    #cim = lsc.to_cim(NetworkService())
    #assert cim.mrid == lsc.mrid()
    #assert isinstance(cim, LinearShuntCompensator)'''