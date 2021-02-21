from collections import namedtuple

from pytest import fixture

from zepben.evolve import NetworkService, Junction, BaseVoltage, Terminal, EnergySource, \
    PowerTransformer, AcLineSegment, EnergyConsumer, PowerTransformerInfo, PositionPoint, Location

TestNetworkCreator = namedtuple("TestNetworkCreator", ["net", "bv", "bus1", "bus2", "pt_info", "loc1", "loc2", "loc3"])


@fixture()
def tnc():
    net = NetworkService()
    bv = BaseVoltage()
    bus1 = net.create_bus(base_voltage=bv)
    bus2 = net.create_bus(base_voltage=bv)
    pt_info = PowerTransformerInfo()
    point1 = PositionPoint(x_position=149.12791965570293, y_position=-35.277592101000934)
    point2 = PositionPoint(x_position=149.12779472660375, y_position=-35.278183862759285)
    loc1 = Location().add_point(point1)
    loc2 = Location().add_point(point2)
    loc3 = Location().add_point(point2).add_point(point2)
    yield TestNetworkCreator(net=net, bv=bv, bus1=bus1, bus2=bus2, pt_info=pt_info, loc1=loc1, loc2=loc2, loc3=loc3)


def test_create_bus(tnc):
    tnc.net.create_bus(base_voltage=tnc.bv)
    objects = tnc.net.objects(Junction)
    for ce in objects:
        bus: Junction = ce
        assert isinstance(bus, Junction)
        assert bus.num_terminals() == 1, "num_terminals should be 1"
        t: Terminal = bus.get_terminal_by_sn(1)
        assert t is not None
        assert bus.get_base_voltage() is tnc.bv, f'bus.get_base_voltage() is not {tnc.bv}. Instead is {bus.get_base_voltage()}'
        assert t.conducting_equipment is bus, "t.conducting_equipment should be 'bus'"


def test_create_energy_source(tnc):
    tnc.net.create_energy_source(bus=tnc.bus1)
    objects = tnc.net.objects(EnergySource)
    for source in objects:
        t: Terminal = source.get_terminal_by_sn(1)
        assert source.num_terminals() == 1
        assert isinstance(t, Terminal)
        assert isinstance(source, EnergySource)
        assert t.conducting_equipment is source, "t.conducting_equipment should be 'source'"


def test_create_energy_consumer(tnc):
    tnc.net.create_energy_consumer(bus=tnc.bus1, location=tnc.loc1)
    objects = tnc.net.objects(EnergyConsumer)
    for ce in objects:
        consumer: EnergyConsumer = ce
        t: Terminal = consumer.get_terminal_by_sn(1)
        assert consumer.num_terminals() == 1
        assert isinstance(t, Terminal)
        assert isinstance(consumer, EnergyConsumer)
        assert t.conducting_equipment is consumer, "t.conducting_equipment should be 'ec'"
        assert consumer.location == tnc.loc1


def test_create_two_winding_power_transformer(tnc):
    tnc.net.create_two_winding_power_transformer(bus1=tnc.bus1, bus2=tnc.bus2, asset_info=tnc.pt_info,
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
    tnc.net.create_ac_line_segment(bus1=tnc.bus1, bus2=tnc.bus2, location=tnc.loc3)
    objects = tnc.net.objects(AcLineSegment)
    for ce in objects:
        line_segment: AcLineSegment = ce
        t: Terminal = line_segment.get_terminal_by_sn(1)
        assert line_segment.num_terminals() == 2
        assert isinstance(t, Terminal)
        assert isinstance(line_segment, AcLineSegment)
        assert t.conducting_equipment is line_segment, "t.conducting_equipment should be 'line_segment'"
        assert line_segment.location == tnc.loc3
