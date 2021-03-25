#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds

from zepben.evolve import phasecode_by_id, WindingConnection, PhaseShuntConnectionKind, RegulatingCondEq

# IEC61970
'''Core'''
from zepben.protobuf.cim.iec61970.base.core.Terminal_pb2 import Terminal
from zepben.protobuf.cim.iec61970.base.core.ConnectivityNode_pb2 import ConnectivityNode
from zepben.protobuf.cim.iec61970.base.core.BaseVoltage_pb2 import BaseVoltage
from zepben.protobuf.cim.iec61970.base.core.Feeder_pb2 import Feeder
from zepben.protobuf.cim.iec61970.base.core.Substation_pb2 import Substation
from zepben.protobuf.cim.iec61970.base.core.GeographicalRegion_pb2 import GeographicalRegion
'''Meas'''
from zepben.protobuf.cim.iec61970.base.meas.Analog_pb2 import Analog
from zepben.protobuf.cim.iec61970.base.meas.Discrete_pb2 import Discrete
from zepben.protobuf.cim.iec61970.base.meas.Accumulator_pb2 import Accumulator
from zepben.protobuf.cim.iec61970.base.meas.AnalogValue_pb2 import AnalogValue
'''SCADA'''
from zepben.protobuf.cim.iec61970.base.scada.RemoteSource_pb2 import RemoteSource
from zepben.protobuf.cim.iec61970.base.scada.RemoteControl_pb2 import RemoteControl
'''Wires'''
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
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformer_pb2 import PowerTransformer
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformerEnd_pb2 import PowerTransformerEnd
from zepben.protobuf.cim.iec61970.base.wires.RatioTapChanger_pb2 import RatioTapChanger

#IEC61968
from zepben.protobuf.cim.iec61968.metering.Meter_pb2 import Meter
from zepben.protobuf.cim.iec61968.assets.Pole_pb2 import Pole

# IEC61970
from test.cim_creators import busbarsection, loadbreakswitch, energysource, energyconsumer, junction, aclinesegment, \
    disconnector, fuse, jumper, breaker, linearshuntcompensator, powertransformer, powertransformerend, ratiotapchanger, \
    terminal, connectivitynode, basevoltage, feeder, substation, geographicalregion, analog, discrete, accumulator, \
    analogvalue, remotesource, remotecontrol, regulatingcondeq

#IEC61968
from test.cim_creators import meter, pole

'''Core'''

def verify_identifiedobject_to_pb(cim, pb):
    ## Top of inheritance hierarchy -- NOT ALL ATTRIBUTES FULFILLED BY ALL OBJECTS
    assert pb.mrid() == cim.mrid
    try:
        assert pb.name == cim.name
    except AttributeError:
        pass
    try:
        assert pb.description == cim.description
    except AttributeError:
        pass

def verify_ACDCTerminal_to_pb(cim, pb):
    verify_identifiedobject_to_pb(cim, pb)

def verify_asset_to_pb(cim, pb):
    verify_identifiedobject_to_pb(cim, pb)

def verify_assetcontainer_to_pb(cim, pb):
    verify_asset_to_pb(cim, pb)

def verify_enddevice_to_pb(cim, pb):
    verify_assetcontainer_to_pb(cim, pb)

#@given(me=meter())
#def test_meter_to_pb(me):
    #pb = me.to_pb()
    #assert pb.mrid() == me.mrid
    #assert isinstance(pb, Meter)
    #verify_enddevice_to_pb(me, pb)

@given(po=pole())
def test_pole_to_pb(po):
    pb = po.to_pb()
    assert pb.mrid() == po.mrid
    assert isinstance(pb, Pole)
    assert pb.classification == po.classification

@given(te=terminal())
def test_terminal_to_pb(te):
    pb = te.to_pb()
    assert pb.mrid() == te.mrid
    assert isinstance(pb, Terminal)
    assert phasecode_by_id(pb.phases) == te.phases
    verify_ACDCTerminal_to_pb(te, pb.ad)

@given(cnn=connectivitynode())
def test_connectivitynode_to_pb(cnn):
    pb = cnn.to_pb()
    assert pb.mrid() == cnn.mrid
    assert isinstance(pb, ConnectivityNode)
    verify_identifiedobject_to_pb(cnn, pb)

@given(bv=basevoltage())
def test_basevoltage_to_pb(bv):
    pb = bv.to_pb()
    assert pb.mrid() == bv.mrid
    assert isinstance(pb, BaseVoltage)
    assert pb.nominalVoltage == bv.nominal_voltage

@given(fe=feeder())
def test_connectivitynode_to_pb(fe):
    pb = fe.to_pb()
    assert pb.mrid() == fe.mrid
    assert isinstance(pb, Feeder)

@given(sub=substation())
def test_substation_to_pb(sub):
    pb = sub.to_pb()
    assert pb.mrid() == sub.mrid
    assert isinstance(pb, Substation)

@given(ger=geographicalregion())
def test_geographicalregion_to_pb(ger):
    pb = ger.to_pb()
    assert pb.mrid() == ger.mrid
    assert isinstance(pb, GeographicalRegion)

'''Meas'''

@given(ana=analog())
def test_analog_to_pb(ana):
    pb = ana.to_pb()
    assert pb.mrid() == ana.mrid
    assert isinstance(pb, Analog)
    assert pb.positiveFlowIn == ana.positive_flow_in

@given(dis=discrete())
def test_discrete_to_pb(dis):
    pb = dis.to_pb()
    assert pb.mrid() == dis.mrid
    assert isinstance(pb, Discrete)

@given(acc=accumulator())
def test_accumulator_to_pb(acc):
    pb = acc.to_pb()
    assert pb.mrid() == acc.mrid
    assert isinstance(pb, Accumulator)

'''SCADA'''

@given(rs=remotesource())
def test_remotesource_to_pb(rs):
    pb = rs.to_pb()
    assert pb.mrid() == rs.mrid
    assert isinstance(pb, RemoteSource)

@given(rc=remotecontrol())
def test_remotecontrol_to_pb(rc):
    pb = rc.to_pb()
    assert pb.mrid() == rc.mrid
    assert isinstance(pb, RemoteControl)

'''Wires'''

def verify_powersystemsresource_to_pb(cim, pb):
    verify_identifiedobject_to_pb(cim, pb)

def verify_equipment_to_pb(cim, pb):
    assert pb.inService == cim.in_service
    assert pb.normallyInService == cim.normally_in_service
    verify_powersystemsresource_to_pb(cim, pb.psr)

def verify_conductingequipment_to_pb(cim, pb):
    verify_equipment_to_pb(cim, pb.eq)

def verify_connector_to_pb(cim, pb):
    verify_conductingequipment_to_pb(cim, pb.ce)

@given(bbs=busbarsection())
def test_busbarsection_to_pb(bbs):
    pb = bbs.to_pb()
    assert pb.mrid() == bbs.mrid
    assert isinstance(pb, BusbarSection)
    #assert pb.ipMax == bbs.ip_max
    verify_connector_to_pb(bbs, pb.cn)

@given(jnc=junction())
def test_junction_to_pb(jnc):
    pb = jnc.to_pb()
    assert pb.mrid() == jnc.mrid
    assert isinstance(pb, Junction)
    verify_connector_to_pb(jnc, pb.cn)

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

def verify_energyconnection_to_pb(cim, pb):
    verify_conductingequipment_to_pb(cim, pb.ce)

@given(pwt=powertransformer())
def test_powertransformer_to_pb(pwt):
    pb = pwt.to_pb()
    assert pb.mrid() == pwt.mrid
    assert isinstance(pb, PowerTransformer)
    verify_conductingequipment_to_pb(pwt, pb.ce)

@given(pte=powertransformerend())
def test_powertransformerend_to_pb(pte):
    pb = pte.to_pb()
    assert pb.mrid() == pte.mrid
    assert isinstance(pb, PowerTransformerEnd)
    assert pb.b == pte.b
    assert pb.b0 == pte.b0
    assert WindingConnection(pb.connectionKind) == pte.connection_kind
    assert pb.g == pte.g
    assert pb.g0 == pte.g0
    assert pb.phaseAngleClock == pte.phase_angle_clock
    assert pb.r == pte.r
    assert pb.r0 == pte.r0
    assert pb.ratedS == pte.rated_s
    assert pb.ratedU == pte.rated_u
    assert pb.x == pte.x
    assert pb.x0 == pte.x0

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
    verify_energyconnection_to_pb(ens, pb.ec)

@given(enc=energyconsumer())
def test_energyconsumer_to_pb(enc):
    pb = enc.to_pb()
    assert pb.mrid() == enc.mrid
    assert isinstance(pb, EnergyConsumer)
    assert pb.customerCount == enc.customer_count
    assert pb.grounded == enc.grounded
    assert PhaseShuntConnectionKind(pb.phaseConnection) == enc.phase_connection
    assert pb.p == enc.p
    assert pb.q == enc.q
    assert pb.pFixed == enc.p_fixed
    assert pb.qFixed == enc.q_fixed
    verify_energyconnection_to_pb(enc, pb.ec)

def verify_regulatingcondeq_to_pb(cim, pb):
    assert pb.controlEnabled == cim.control_enabled
    verify_energyconnection_to_pb(cim, pb.ec)

def verify_shuntcompensator_to_pb(cim, pb):
    assert pb.grounded == cim.grounded
    assert pb.nomU == cim.nom_u
    assert PhaseShuntConnectionKind(pb.phaseConnection) == cim.phase_connection
    assert pb.sections == cim.sections
    verify_regulatingcondeq_to_pb(cim, pb.rce)

def verify_conductor_to_pb(cim, pb):
    assert pb.length == cim.length
    verify_conductingequipment_to_pb(cim, pb.ce)

@given(acl=aclinesegment())
def test_aclinesegment_to_pb(acl):
    pb = acl.to_pb()
    assert pb.mrid() == acl.mrid
    assert isinstance(pb, AcLineSegment)
    verify_conductor_to_pb(acl, pb.cd)

@given(lsc=linearshuntcompensator())
def test_linearshuntcompensator_to_pb(lsc):
    pb = lsc.to_pb()
    assert pb.mrid() == lsc.mrid
    assert isinstance(pb, LinearShuntCompensator)
    assert pb.b0PerSection == lsc.b0_per_section
    assert pb.bPerSection == lsc.b_per_section
    assert pb.g0PerSection == lsc.g0_per_section
    assert pb.gPerSection == lsc.g_per_section
    verify_shuntcompensator_to_pb(lsc, pb.sc)

def verify_tapchanger_to_pb(cim, pb):
    assert pb.controlEnabled == cim.control_enabled
    assert pb.highStep == cim.high_step
    assert pb.lowStep == cim.low_step
    assert pb.neutralStep == cim.neutral_step
    assert pb.neutralU == cim.neutral_u
    assert pb.normalStep == cim.normal_step
    assert pb.step == cim.step
    verify_powersystemsresource_to_pb(cim, pb.psr)

@given(rtc=ratiotapchanger())
def test_ratiotapchanger_to_pb(rtc):
    pb = rtc.to_pb()
    assert pb.mrid() == rtc.mrid
    assert isinstance(pb, RatioTapChanger)
    assert pb.stepVoltageIncrement == rtc.step_voltage_increment
    verify_tapchanger_to_pb(rtc, pb.tc)