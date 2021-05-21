#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from zepben.protobuf.cim.iec61968.common.Location_pb2 import Location as PBLocation
from zepben.protobuf.cim.iec61970.base.core.BaseVoltage_pb2 import BaseVoltage as PBBaseVoltage
from zepben.protobuf.cim.iec61970.base.core.ConnectivityNode_pb2 import ConnectivityNode as PBConnectivityNode
from zepben.protobuf.cim.iec61970.base.core.Feeder_pb2 import Feeder as PBFeeder
from zepben.protobuf.cim.iec61970.base.core.GeographicalRegion_pb2 import GeographicalRegion as PBGeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.SubGeographicalRegion_pb2 import SubGeographicalRegion as PBSubGeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.Substation_pb2 import Substation as PBSubstation
from zepben.protobuf.cim.iec61970.base.core.Terminal_pb2 import Terminal as PBTerminal
from zepben.protobuf.cim.iec61970.base.meas.Accumulator_pb2 import Accumulator as PBAccumulator
from zepben.protobuf.cim.iec61970.base.meas.Analog_pb2 import Analog as PBAnalog
from zepben.protobuf.cim.iec61970.base.meas.Discrete_pb2 import Discrete as PBDiscrete
from zepben.protobuf.cim.iec61970.base.scada.RemoteControl_pb2 import RemoteControl as PBRemoteControl
from zepben.protobuf.cim.iec61970.base.scada.RemoteSource_pb2 import RemoteSource as PBRemoteSource
from zepben.protobuf.cim.iec61970.base.wires.AcLineSegment_pb2 import AcLineSegment as PBAcLineSegment
from zepben.protobuf.cim.iec61970.base.wires.Breaker_pb2 import Breaker as PBBreaker
from zepben.protobuf.cim.iec61970.base.wires.BusbarSection_pb2 import BusbarSection as PBBusbarSection
from zepben.protobuf.cim.iec61970.base.wires.Disconnector_pb2 import Disconnector as PBDisconnector
from zepben.protobuf.cim.iec61970.base.wires.EnergyConsumer_pb2 import EnergyConsumer as PBEnergyConsumer
from zepben.protobuf.cim.iec61970.base.wires.EnergySource_pb2 import EnergySource as PBEnergySource
from zepben.protobuf.cim.iec61970.base.wires.Fuse_pb2 import Fuse as PBFuse
from zepben.protobuf.cim.iec61970.base.wires.Jumper_pb2 import Jumper as PBJumper
from zepben.protobuf.cim.iec61970.base.wires.Junction_pb2 import Junction as PBJunction
from zepben.protobuf.cim.iec61970.base.wires.LinearShuntCompensator_pb2 import LinearShuntCompensator as PBLinearShuntCompensator
from zepben.protobuf.cim.iec61970.base.wires.LoadBreakSwitch_pb2 import LoadBreakSwitch as PBLoadBreakSwitch
from zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance_pb2 import PerLengthSequenceImpedance as PBPerLengthSequenceImpedance
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformerEnd_pb2 import PowerTransformerEnd as PBPowerTransformerEnd
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformer_pb2 import PowerTransformer as PBPowerTransformer
from zepben.protobuf.cim.iec61970.base.wires.RatioTapChanger_pb2 import RatioTapChanger as PBRatioTapChanger
from zepben.protobuf.cim.iec61970.base.wires.generation.production.BatteryUnit_pb2 import BatteryUnit as PBBatteryUnit
from zepben.protobuf.cim.iec61970.infiec61970.feeder.Circuit_pb2 import Circuit as PBCircuit
from zepben.protobuf.cim.iec61970.infiec61970.feeder.Loop_pb2 import Loop as PBLoop

from test.cim_creators import busbarsection, loadbreakswitch, energysource, energyconsumer, junction, aclinesegment, \
    disconnector, fuse, jumper, breaker, linearshuntcompensator, powertransformer, powertransformerend, ratiotapchanger, \
    terminal, connectivitynode, basevoltage, feeder, substation, geographicalregion, analog, discrete, accumulator, \
    remotesource, remotecontrol, perlengthsequenceimpedance, batteryunit, subgeographicalregion, circuit, loop, location
from zepben.evolve import phasecode_by_id, WindingConnection, PhaseShuntConnectionKind, unit_symbol_from_id, VectorGroup, BatteryStateKind, CableInfo, \
    OverheadWireInfo, WireInfo, PowerTransformerInfo, Asset, TransformerTankInfo, TransformerEndInfo, AssetContainer, AssetInfo, AssetOrganisationRole, \
    AssetOwner, Pole, Streetlight, Structure, PositionPoint, TownDetail, StreetAddress, Location, EndDevice, Meter, UsagePoint, OperationalRestriction, \
    AuxiliaryEquipment, FaultIndicator, AcDcTerminal, ConductingEquipment, ConnectivityNodeContainer, Equipment, EquipmentContainer, PowerSystemResource, \
    PerLengthLineParameter, PerLengthImpedance, PowerElectronicsUnit, PhotoVoltaicUnit, PowerElectronicsWindUnit, Conductor, Connector, EnergyConnection, \
    EnergyConsumerPhase, EnergySourcePhase, Line, PowerElectronicsConnection, PowerElectronicsConnectionPhase, TransformerStarImpedance, ProtectedSwitch, \
    Recloser, RegulatingCondEq, ShuntCompensator, Switch, TapChanger, TransformerEnd, Control, IoPoint, Measurement, RemotePoint, TracedPhases, Site, \
    PowerTransformer, BaseVoltage, ConnectivityNode, Feeder, GeographicalRegion, SubGeographicalRegion, Substation, Terminal, BatteryUnit, AcLineSegment, \
    Breaker, Disconnector, EnergyConsumer, EnergySource, Fuse, Jumper, Junction, BusbarSection, LinearShuntCompensator, LoadBreakSwitch, \
    PerLengthSequenceImpedance, PowerTransformerEnd, RatioTapChanger, Circuit, Loop, Accumulator, Analog, Discrete, RemoteControl, RemoteSource


# Core
def verify_identified_object_to_pb(cim, pb):
    # Top of inheritance hierarchy
    assert pb.mRID == cim.mrid
    assert pb.name == cim.name
    assert pb.description == cim.description


def verify_ac_dc_terminal_to_pb(cim, pb):
    verify_identified_object_to_pb(cim, pb.io)


def verify_asset_info_to_pb(cim, pb):
    verify_identified_object_to_pb(cim, pb.io)


def verify_asset_to_pb(cim, pb):
    verify_identified_object_to_pb(cim, pb.io)


def verify_asset_container_to_pb(cim, pb):
    verify_asset_to_pb(cim, pb.at)


def verify_end_device_to_pb(cim, pb):
    verify_asset_container_to_pb(cim, pb.ac)


@given(te=terminal())
def test_terminal_to_pb(te):
    pb = te.to_pb()
    assert pb.mrid() == te.mrid
    assert isinstance(pb, PBTerminal)
    assert phasecode_by_id(pb.phases) == te.phases
    verify_ac_dc_terminal_to_pb(te, pb.ad)


@given(cnn=connectivitynode())
def test_connectivity_node_to_pb(cnn):
    pb = cnn.to_pb()
    assert pb.mrid() == cnn.mrid
    assert isinstance(pb, PBConnectivityNode)
    verify_identified_object_to_pb(cnn, pb.io)


@given(bv=basevoltage())
def test_base_voltage_to_pb(bv):
    pb = bv.to_pb()
    assert pb.mrid() == bv.mrid
    assert isinstance(pb, PBBaseVoltage)
    assert pb.nominalVoltage == bv.nominal_voltage
    verify_identified_object_to_pb(bv, pb.io)


@given(fe=feeder())
def test_feeder_to_pb(fe):
    pb = fe.to_pb()
    assert pb.mrid() == fe.mrid
    assert isinstance(pb, PBFeeder)
    verify_equipment_container_to_pb(fe, pb.ec)


@given(sub=substation())
def test_substation_to_pb(sub):
    pb = sub.to_pb()
    assert pb.mrid() == sub.mrid
    assert isinstance(pb, PBSubstation)
    verify_equipment_container_to_pb(sub, pb.ec)


@given(ger=geographicalregion())
def test_geographical_region_to_pb(ger):
    pb = ger.to_pb()
    assert pb.mrid() == ger.mrid
    assert isinstance(pb, PBGeographicalRegion)
    verify_identified_object_to_pb(ger, pb.io)


@given(sgr=subgeographicalregion())
def test_sub_geographical_region_to_pb(sgr):
    pb = sgr.to_pb()
    assert pb.mrid() == sgr.mrid
    assert isinstance(pb, PBSubGeographicalRegion)
    verify_identified_object_to_pb(sgr, pb.io)


# Meas
def verify_measurement_to_pb(cim, pb):
    assert phasecode_by_id(pb.phases) == cim.phases
    assert unit_symbol_from_id(pb.unitSymbol) == cim.unit_symbol


@given(ana=analog())
def test_analog_to_pb(ana):
    pb = ana.to_pb()
    assert pb.mrid() == ana.mrid
    assert isinstance(pb, PBAnalog)
    assert pb.positiveFlowIn == ana.positive_flow_in
    verify_measurement_to_pb(ana, pb.measurement)


@given(dis=discrete())
def test_discrete_to_pb(dis):
    pb = dis.to_pb()
    assert pb.mrid() == dis.mrid
    assert isinstance(pb, PBDiscrete)
    verify_measurement_to_pb(dis, pb.measurement)


@given(acc=accumulator())
def test_accumulator_to_pb(acc):
    pb = acc.to_pb()
    assert pb.mrid() == acc.mrid
    assert isinstance(pb, PBAccumulator)
    verify_measurement_to_pb(acc, pb.measurement)


# SCADA
def verify_remote_point_to_pb(cim, pb):
    verify_identified_object_to_pb(cim, pb.io)


@given(rs=remotesource())
def test_remote_source_to_pb(rs):
    pb = rs.to_pb()
    assert pb.mrid() == rs.mrid
    assert isinstance(pb, PBRemoteSource)
    verify_remote_point_to_pb(rs, pb.rp)


@given(rc=remotecontrol())
def test_remote_control_to_pb(rc):
    pb = rc.to_pb()
    assert pb.mrid() == rc.mrid
    assert isinstance(pb, PBRemoteControl)
    verify_remote_point_to_pb(rc, pb.rp)


# Wires - Generation - Production
def verify_power_systems_resource_to_pb(cim, pb):
    verify_identified_object_to_pb(cim, pb.io)


def verify_equipment_to_pb(cim, pb):
    assert pb.inService == cim.in_service
    assert pb.normallyInService == cim.normally_in_service
    verify_power_systems_resource_to_pb(cim, pb.psr)


def verify_conducting_equipment_to_pb(cim, pb):
    verify_equipment_to_pb(cim, pb.eq)


def verify_connector_to_pb(cim, pb):
    verify_conducting_equipment_to_pb(cim, pb.ce)


def verify_connectivity_node_container_to_pb(cim, pb):
    verify_power_systems_resource_to_pb(cim, pb.psr)


def verify_equipment_container_to_pb(cim, pb):
    verify_connectivity_node_container_to_pb(cim, pb.cnc)


@given(bbs=busbarsection())
def test_busbar_section_to_pb(bbs):
    pb = bbs.to_pb()
    assert pb.mrid() == bbs.mrid
    assert isinstance(pb, PBBusbarSection)
    verify_connector_to_pb(bbs, pb.cn)


def verify_per_length_line_parameter_to_pb(cim, pb):
    verify_identified_object_to_pb(cim, pb.io)


def verify_per_length_impedance_to_pb(cim, pb):
    verify_per_length_line_parameter_to_pb(cim, pb.lp)


@given(imp=perlengthsequenceimpedance())
def test_per_length_sequence_impedance_to_pb(imp):
    pb = imp.to_pb()
    assert isinstance(pb, PBPerLengthSequenceImpedance)
    assert pb.mrid() == imp.mrid
    assert pb.b0ch == imp.b0ch
    assert pb.bch == imp.bch
    assert pb.g0ch == imp.g0ch
    assert pb.gch == imp.gch
    assert pb.r == imp.r
    assert pb.r0 == imp.r0
    assert pb.x == imp.x
    assert pb.x0 == imp.x0
    verify_per_length_impedance_to_pb(imp, pb.pli)


@given(jnc=junction())
def test_junction_to_pb(jnc):
    pb = jnc.to_pb()
    assert pb.mrid() == jnc.mrid
    assert isinstance(pb, PBJunction)
    verify_connector_to_pb(jnc, pb.cn)


@given(dis=disconnector())
def test_disconnector_to_pb(dis):
    pb = dis.to_pb()
    assert pb.mrid() == dis.mrid
    assert isinstance(pb, PBDisconnector)
    verify_switch(dis, pb.sw)


@given(fus=fuse())
def test_fuse_to_pb(fus):
    pb = fus.to_pb()
    assert pb.mrid() == fus.mrid
    assert isinstance(pb, PBFuse)
    verify_switch(fus, pb.sw)


@given(jum=jumper())
def test_jumper_to_pb(jum):
    pb = jum.to_pb()
    assert pb.mrid() == jum.mrid
    assert isinstance(pb, PBJumper)
    verify_switch(jum, pb.sw)


@given(brk=breaker())
def test_breaker_to_pb(brk):
    pb = brk.to_pb()
    assert pb.mrid() == brk.mrid
    assert isinstance(pb, PBBreaker)
    verify_protected_switch(brk, pb.sw)


@given(lbs=loadbreakswitch())
def test_load_break_switch_to_pb(lbs):
    pb = lbs.to_pb()
    assert pb.mrid() == lbs.mrid
    assert isinstance(pb, PBLoadBreakSwitch)
    verify_protected_switch(lbs, pb.ps)


def verify_protected_switch(cim, pb):
    verify_switch(cim, pb.sw)


def verify_switch(cim, pb):
    # Protobuf switch open/normalOpen are currently booleans, so we can only perform a naive check of if all phases are closed
    # or if a single phase is open.
    if not cim.is_open():
        assert not pb.open
    if not cim.is_normally_open():
        assert not pb.normalOpen

    if cim.is_open():
        assert pb.open
    if cim.is_normally_open():
        assert pb.normalOpen


def verify_energy_connection_to_pb(cim, pb):
    verify_conducting_equipment_to_pb(cim, pb.ce)


def verify_transformer_end_to_pb(cim, pb):
    assert pb.endNumber == cim.end_number
    assert pb.grounded == cim.grounded
    assert pb.rGround == cim.r_ground
    assert pb.xGround == cim.x_ground
    verify_identified_object_to_pb(cim, pb.io)


@given(pwt=powertransformer())
def test_power_transformer_to_pb(pwt):
    pb = pwt.to_pb()
    assert pb.mrid() == pwt.mrid
    assert isinstance(pb, PBPowerTransformer)
    assert VectorGroup(pb.vectorGroup) == pwt.vector_group
    assert pb.transformerUtilisation == pwt.transformer_utilisation
    verify_conducting_equipment_to_pb(pwt, pb.ce)


@given(pte=powertransformerend())
def test_power_transformer_end_to_pb(pte):
    pb = pte.to_pb()
    assert pb.mrid() == pte.mrid
    assert isinstance(pb, PBPowerTransformerEnd)
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
    verify_transformer_end_to_pb(pte, pb.te)


@given(ens=energysource())
def test_energy_source_to_pb(ens):
    pb = ens.to_pb()
    assert pb.mrid() == ens.mrid
    assert isinstance(pb, PBEnergySource)
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
    verify_energy_connection_to_pb(ens, pb.ec)


@given(enc=energyconsumer())
def test_energy_consumer_to_pb(enc):
    pb = enc.to_pb()
    assert pb.mrid() == enc.mrid
    assert isinstance(pb, PBEnergyConsumer)
    assert pb.customerCount == enc.customer_count
    assert pb.grounded == enc.grounded
    assert PhaseShuntConnectionKind(pb.phaseConnection) == enc.phase_connection
    assert pb.p == enc.p
    assert pb.q == enc.q
    assert pb.pFixed == enc.p_fixed
    assert pb.qFixed == enc.q_fixed
    verify_energy_connection_to_pb(enc, pb.ec)


def verify_regulating_cond_eq_to_pb(cim, pb):
    assert pb.controlEnabled == cim.control_enabled
    verify_energy_connection_to_pb(cim, pb.ec)


def verify_shunt_compensator_to_pb(cim, pb):
    assert pb.grounded == cim.grounded
    assert pb.nomU == cim.nom_u
    assert PhaseShuntConnectionKind(pb.phaseConnection) == cim.phase_connection
    assert pb.sections == cim.sections
    verify_regulating_cond_eq_to_pb(cim, pb.rce)


def verify_conductor_to_pb(cim, pb):
    assert pb.length == cim.length
    verify_conducting_equipment_to_pb(cim, pb.ce)


@given(acl=aclinesegment())
def test_ac_line_segment_to_pb(acl):
    pb = acl.to_pb()
    assert pb.mrid() == acl.mrid
    assert isinstance(pb, PBAcLineSegment)
    verify_conductor_to_pb(acl, pb.cd)


def verify_line_to_pb(cim, pb):
    verify_equipment_container_to_pb(cim, pb.ec)


@given(lsc=linearshuntcompensator())
def test_linear_shunt_compensator_to_pb(lsc):
    pb = lsc.to_pb()
    assert pb.mrid() == lsc.mrid
    assert isinstance(pb, PBLinearShuntCompensator)
    assert pb.b0PerSection == lsc.b0_per_section
    assert pb.bPerSection == lsc.b_per_section
    assert pb.g0PerSection == lsc.g0_per_section
    assert pb.gPerSection == lsc.g_per_section
    verify_shunt_compensator_to_pb(lsc, pb.sc)


def verify_tap_changer_to_pb(cim, pb):
    assert pb.controlEnabled == cim.control_enabled
    assert pb.highStep == cim.high_step
    assert pb.lowStep == cim.low_step
    assert pb.neutralStep == cim.neutral_step
    assert pb.neutralU == cim.neutral_u
    assert pb.normalStep == cim.normal_step
    assert pb.step == cim.step
    verify_power_systems_resource_to_pb(cim, pb.psr)


@given(rtc=ratiotapchanger())
def test_ratio_tap_changer_to_pb(rtc):
    pb = rtc.to_pb()
    assert pb.mrid() == rtc.mrid
    assert isinstance(pb, PBRatioTapChanger)
    assert pb.stepVoltageIncrement == rtc.step_voltage_increment
    verify_tap_changer_to_pb(rtc, pb.tc)


def verify_power_electronics_unit_to_pb(cim, pb):
    assert pb.maxP == cim.max_p
    assert pb.minP == cim.min_p
    verify_equipment_to_pb(cim, pb.eq)


@given(bu=batteryunit())
def test_battery_unit_to_pb(bu):
    pb = bu.to_pb()
    assert pb.mrid() == bu.mrid
    assert isinstance(pb, PBBatteryUnit)
    assert BatteryStateKind(pb.batteryState) == bu.battery_state
    assert pb.ratedE == bu.rated_e
    assert pb.storedE == bu.stored_e
    verify_power_electronics_unit_to_pb(bu, pb.peu)


@given(c=circuit())
def test_circuit_to_pb(c):
    pb = c.to_pb()
    assert pb.mrid() == c.mrid
    assert isinstance(pb, PBCircuit)
    verify_line_to_pb(c, pb.l)


@given(lp=loop())
def test_loop_to_pb(lp):
    pb = lp.to_pb()
    assert pb.mrid() == lp.mrid
    assert isinstance(pb, PBLoop)
    verify_identified_object_to_pb(lp, pb.io)


@given(loc=location())
def test_location_to_pb(loc):
    pb = loc.to_pb()
    assert pb.mrid() == loc.mrid
    assert isinstance(pb, PBLocation)
    verify_identified_object_to_pb(loc, pb.io)


# noinspection PyUnresolvedReferences
def test_empty_objects():
    # this test is here to make sure objects that have not been filled out still work as there have been several bugs found
    # when using semi-complete objects.
    CableInfo().to_pb()
    OverheadWireInfo().to_pb()
    WireInfo().to_pb()
    PowerTransformerInfo().to_pb()
    Asset().to_pb()
    TransformerTankInfo().to_pb()
    TransformerEndInfo().to_pb()
    AssetContainer().to_pb()
    AssetInfo().to_pb()
    AssetOrganisationRole().to_pb()
    AssetOwner().to_pb()
    Pole().to_pb()
    Streetlight().to_pb()
    Structure().to_pb()
    PositionPoint(0, 0).to_pb()
    TownDetail().to_pb()
    StreetAddress().to_pb()
    Location().to_pb()
    EndDevice().to_pb()
    Meter().to_pb()
    UsagePoint().to_pb()
    OperationalRestriction().to_pb()
    AuxiliaryEquipment().to_pb()
    FaultIndicator().to_pb()
    AcDcTerminal().to_pb()
    BaseVoltage().to_pb()
    ConductingEquipment().to_pb()
    ConnectivityNode().to_pb()
    ConnectivityNodeContainer().to_pb()
    Equipment().to_pb()
    EquipmentContainer().to_pb()
    Feeder().to_pb()
    GeographicalRegion().to_pb()
    PowerSystemResource().to_pb()
    Site().to_pb()
    SubGeographicalRegion().to_pb()
    Substation().to_pb()
    Terminal().to_pb()
    PerLengthLineParameter().to_pb()
    PerLengthImpedance().to_pb()
    PowerElectronicsUnit().to_pb()
    BatteryUnit().to_pb()
    PhotoVoltaicUnit().to_pb()
    PowerElectronicsWindUnit().to_pb()
    AcLineSegment().to_pb()
    Breaker().to_pb()
    Conductor().to_pb()
    Connector().to_pb()
    Disconnector().to_pb()
    EnergyConnection().to_pb()
    EnergyConsumer().to_pb()
    EnergyConsumerPhase().to_pb()
    EnergySource().to_pb()
    EnergySourcePhase().to_pb()
    Fuse().to_pb()
    Jumper().to_pb()
    Junction().to_pb()
    BusbarSection().to_pb()
    Line().to_pb()
    LinearShuntCompensator().to_pb()
    LoadBreakSwitch().to_pb()
    PerLengthSequenceImpedance().to_pb()
    PowerElectronicsConnection().to_pb()
    PowerElectronicsConnectionPhase().to_pb()
    PowerTransformer().to_pb()
    PowerTransformerEnd().to_pb()
    TransformerStarImpedance().to_pb()
    ProtectedSwitch().to_pb()
    RatioTapChanger().to_pb()
    Recloser().to_pb()
    RegulatingCondEq().to_pb()
    ShuntCompensator().to_pb()
    Switch().to_pb()
    TapChanger().to_pb()
    TransformerEnd().to_pb()
    Circuit().to_pb()
    Loop().to_pb()
    Control().to_pb()
    IoPoint().to_pb()
    Accumulator().to_pb()
    Analog().to_pb()
    Discrete().to_pb()
    Measurement().to_pb()
    RemoteControl().to_pb()
    RemotePoint().to_pb()
    RemoteSource().to_pb()
    TracedPhases().to_pb()
