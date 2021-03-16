#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from zepben.evolve import NetworkService, WindingConnection, phasecode_by_id, PhaseShuntConnectionKind, IdentifiedObject, Terminal, ConnectivityNode, \
BaseVoltage, Feeder, Substation, GeographicalRegion, Analog, Discrete, Accumulator, RemoteControl, BusbarSection, Junction, \
EnergySource, EnergyConsumer, AcLineSegment, Disconnector, Fuse, Jumper, Breaker, LoadBreakSwitch, PowerTransformer, \
PowerTransformerEnd, LinearShuntCompensator, RatioTapChanger

from test.pb_creators import terminal, connectivitynode, basevoltage, feeder, substation, geographicalregion, analog, \
discrete, accumulator, remotecontrol, busbarsection, junction, energysource, energyconsumer, aclinesegment, disconnector, \
fuse, jumper, breaker, loadbreakswitch, powertransformer, powertransformerend, linearshuntcompensator, ratiotapchanger


'''Core'''

@given(te=terminal())
def test_terminal_to_cim(te):
    cim = te.to_cim(NetworkService())
    assert cim.mrid == te.mrid()
    assert isinstance(cim, Terminal)
    assert cim.phases == phasecode_by_id(te.phases)

@given(cnn=connectivitynode())
def test_connectivitynode_to_cim(cnn):
    cim = cnn.to_cim(NetworkService())
    assert cim.mrid == cnn.mrid()
    assert isinstance(cim, ConnectivityNode)

@given(bv=basevoltage())
def test_basevoltage_to_cim(bv):
    cim = bv.to_cim(NetworkService())
    assert cim.mrid == bv.mrid()
    assert isinstance(cim, BaseVoltage)
    assert cim.nominal_voltage == bv.nominalVoltage

@given(fe=feeder())
def test_feeder_to_cim(fe):
    cim = fe.to_cim(NetworkService())
    assert cim.mrid == fe.mrid()
    assert isinstance(cim, Feeder)

@given(sub=substation())
def test_substation_to_cim(sub):
    cim = sub.to_cim(NetworkService())
    assert cim.mrid == sub.mrid()
    assert isinstance(cim, Substation)

@given(ger=geographicalregion())
def test_geographicalregion_to_cim(ger):
    cim = ger.to_cim(NetworkService())
    assert cim.mrid == ger.mrid()
    assert isinstance(cim, GeographicalRegion)

'''Meas'''

@given(ana=analog())
def test_analog_to_cim(ana):
    cim = ana.to_cim(NetworkService())
    assert cim.mrid == ana.mrid()
    assert isinstance(cim, Analog)

@given(dis=discrete())
def test_discrete_to_cim(dis):
    cim = dis.to_cim(NetworkService())
    assert cim.mrid == dis.mrid()
    assert isinstance(cim, Discrete)

@given(acc=accumulator())
def test_accumulator_to_cim(acc):
    cim = acc.to_cim(NetworkService())
    assert cim.mrid == acc.mrid()
    assert isinstance(cim, Accumulator)

'''SCADA'''

#@given(rs=remotesource())
#def test_remotesource_to_cim(rs):
    #cim = rs.to_cim(NetworkService())
    #assert cim.mrid == rs.mrid()
    #assert isinstance(cim, RemoteSource)

@given(rc=remotecontrol())
def test_remotecontrol_to_cim(rc):
    cim = rc.to_cim(NetworkService())
    assert cim.mrid == rc.mrid()
    assert isinstance(cim, RemoteControl)

'''Wires'''

@given(bbs=busbarsection())
def test_busbarsection_to_cim(bbs):
    cim = bbs.to_cim(NetworkService())
    assert cim.mrid == bbs.mrid()
    assert isinstance(cim, BusbarSection)
    #assert cim.ipMax == bbs.ipMax

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
    assert cim.customer_count == enc.customerCount
    assert cim.grounded == enc.grounded
    assert cim.phase_connection == PhaseShuntConnectionKind(enc.phaseConnection)
    assert cim.p == enc.p
    assert cim.q == enc.q
    assert cim.p_fixed == enc.pFixed
    assert cim.q_fixed == enc.qFixed

@given(pwt=powertransformer())
def test_powertransformer_to_cim(pwt):
    cim = pwt.to_cim(NetworkService())
    assert cim.mrid == pwt.mrid()
    assert isinstance(cim, PowerTransformer)

@given(lsc=linearshuntcompensator())
def test_linearshuntcompensator_to_cim(lsc):
    cim = lsc.to_cim(NetworkService())
    assert cim.mrid == lsc.mrid()
    assert isinstance(cim, LinearShuntCompensator)
    assert cim.b0_per_section == lsc.b0PerSection
    assert cim.b_per_section == lsc.bPerSection
    #assert cim.g0_per_section == lsc.g0PerSection
    #assert cim.g_per_section == lsc.gPerSection

@given(pte=powertransformerend())
def test_powertransformerend_to_cim(pte):
    cim = pte.to_cim(NetworkService())
    assert cim.mrid == pte.mrid()
    assert isinstance(cim, PowerTransformerEnd)
    assert cim.b == pte.b
    assert cim.b0 == pte.b0
    assert cim.connection_kind == WindingConnection(pte.connectionKind)
    assert cim.g == pte.g
    assert cim.g0 == pte.g0
    assert cim.phase_angle_clock == pte.phaseAngleClock
    assert cim.r == pte.r
    assert cim.r0 == pte.r0
    assert cim.rated_s == pte.ratedS
    assert cim.rated_u == pte.ratedU
    assert cim.x == pte.x
    assert cim.x0 == pte.x0

#@given(rtc=ratiotapchanger())
#def test_ratiotapchanger_to_cim(rtc):
    #cim = rtc.to_cim(NetworkService())
    #assert cim.mrid == rtc.mrid()
    #assert isinstance(cim, RatioTapChanger)
    #assert cim.step_voltage_increment == rtc.stepVoltageIncrement



