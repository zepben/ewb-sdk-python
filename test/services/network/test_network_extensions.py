#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections import namedtuple

from pytest import fixture

from zepben.evolve import NetworkService, BaseVoltage, Terminal, EnergySource, \
    PowerTransformer, AcLineSegment, EnergyConsumer, PowerTransformerInfo, PositionPoint, Location, \
    ConnectivityNode, Breaker

NetworkCreator = namedtuple("TestNetworkCreator", ["net", "bv", "cn1", "cn2", "pt_info", "loc1", "loc2", "loc3"])


@fixture()
def tnc():
    net = NetworkService()
    bv = BaseVoltage()
    cn1 = ConnectivityNode()
    cn2 = ConnectivityNode()
    pt_info = PowerTransformerInfo()
    # noinspection PyArgumentList
    point1 = PositionPoint(x_position=149.12791965570293, y_position=-35.277592101000934)
    # noinspection PyArgumentList
    point2 = PositionPoint(x_position=149.12779472660375, y_position=-35.278183862759285)
    loc1 = Location().add_point(point1)
    loc2 = Location().add_point(point2)
    loc3 = Location().add_point(point2).add_point(point2)
    yield NetworkCreator(net=net, bv=bv, cn1=cn1, cn2=cn2, pt_info=pt_info, loc1=loc1, loc2=loc2, loc3=loc3)


def test_create_energy_source(tnc):
    ce1 = tnc.net.create_energy_source(cn=tnc.cn1)
    ce2 = tnc.net.get(ce1.mrid)
    assert ce1 is ce2
    assert isinstance(ce1, EnergySource)
    t: Terminal = ce1.get_terminal_by_sn(1)
    assert ce1.num_terminals() == 1
    assert isinstance(t, Terminal)
    assert t.conducting_equipment is ce1, "t.conducting_equipment should be 'source'"


def test_create_energy_consumer(tnc):
    ce1 = tnc.net.create_energy_consumer(cn=tnc.cn1, location=tnc.loc1)
    ce2 = tnc.net.get(ce1.mrid)
    assert ce1 is ce2
    assert ce2.num_terminals() == 1
    t: Terminal = ce2.get_terminal_by_sn(1)
    assert isinstance(t, Terminal)
    assert isinstance(ce2, EnergyConsumer)
    assert t.conducting_equipment is ce2, "t.conducting_equipment should be 'ce1'"
    assert ce2.location == tnc.loc1


def test_create_two_winding_power_transformer(tnc):
    tnc.net.create_two_winding_power_transformer(cn1=tnc.cn1, cn2=tnc.cn2, asset_info=tnc.pt_info,
                                                 location=tnc.loc1)
    objects = tnc.net.objects(PowerTransformer)
    for ce in objects:
        pt: PowerTransformer = ce
        t: Terminal = pt.get_terminal_by_sn(1)
        assert pt.num_terminals() == 2
        assert isinstance(t, Terminal)
        assert isinstance(pt, PowerTransformer)
        assert t.conducting_equipment is pt, "t.conducting_equipment should be 'pt'"
        assert pt.location == tnc.loc1


def test_create_ac_line_segment(tnc):
    ce1 = tnc.net.create_ac_line_segment(cn1=tnc.cn1, cn2=tnc.cn2, location=tnc.loc3)
    ce2 = tnc.net.get(ce1.mrid)
    assert ce1 is ce2
    t: Terminal = ce1.get_terminal_by_sn(1)
    assert ce1.num_terminals() == 2
    assert isinstance(t, Terminal)
    assert isinstance(ce1, AcLineSegment)
    assert t.conducting_equipment is ce1, "t.conducting_equipment should be 'line_segment'"
    assert ce1.location == tnc.loc3


def test_create_breaker(tnc):
    b1 = tnc.net.create_breaker(cn1=tnc.cn1, cn2=tnc.cn2, location=tnc.loc3)
    b2 = tnc.net.get(b1.mrid)
    assert b1 is b2
    assert isinstance(b1, Breaker)
    assert b1.num_terminals() == 2
    t1: Terminal = b1.get_terminal_by_sn(1)
    t2: Terminal = b1.get_terminal_by_sn(2)
    assert isinstance(t1, Terminal)
    assert isinstance(t2, Terminal)
    assert t1.conducting_equipment is b1, "t.conducting_equipment should be 'line_segment'"
    assert t1.conducting_equipment is b1, "t.conducting_equipment should be 'line_segment'"
    assert b1.location == tnc.loc3
