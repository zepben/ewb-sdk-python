from zepben.evolve import NetworkService, Junction, BaseVoltage, Terminal, EnergySource, \
    PowerTransformer, AcLineSegment, EnergyConsumer, PowerTransformerInfo, PositionPoint, Location
import unittest


class TestNetworkCreator(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestNetworkCreator, self).__init__(*args, **kwargs)
        self.net = NetworkService()
        self.bv = BaseVoltage()
        self.bus1 = self.net.create_bus(base_voltage=self.bv)
        self.bus2 = self.net.create_bus(base_voltage=self.bv)
        self.pt_info = PowerTransformerInfo()
        self.point1 = PositionPoint(x_position=149.12791965570293, y_position=-35.277592101000934)
        self.point2 = PositionPoint(x_position=149.12779472660375, y_position=-35.278183862759285)
        self.loc1 = Location().add_point(self.point1)
        self.loc2 = Location().add_point(self.point2)
        self.loc3 = Location().add_point(self.point2).add_point(self.point2)

    def test_create_bus(self):
        self.net.create_bus(base_voltage=self.bv)
        objects = self.net.objects(Junction)
        for ce in objects:
            bus: Junction = ce
            assert isinstance(bus, Junction)
            assert bus.num_terminals() == 1, "num_terminals should be 1"
            t: Terminal = bus.get_terminal_by_sn(1)
            assert t is not None
            assert bus.get_base_voltage() is self.bv, f'bus.get_base_voltage() is not {self.bv}. Instead is {bus.get_base_voltage()}'
            assert t.conducting_equipment is bus, "t.conducting_equipment should be 'bus'"

    def test_create_energy_source(self):
        self.net.create_energy_source(bus=self.bus1)
        objects = self.net.objects(EnergySource)
        for source in objects:
            t: Terminal = source.get_terminal_by_sn(1)
            assert source.num_terminals() == 1
            assert isinstance(t, Terminal)
            assert isinstance(source, EnergySource)
            assert t.conducting_equipment is source, "t.conducting_equipment should be 'source'"

    def test_create_energy_consumer(self):
        self.net.create_energy_consumer(bus=self.bus1, location=self.loc1)
        objects = self.net.objects(EnergyConsumer)
        for ce in objects:
            consumer: EnergyConsumer = ce
            t: Terminal = consumer.get_terminal_by_sn(1)
            assert consumer.num_terminals() == 1
            assert isinstance(t, Terminal)
            assert isinstance(consumer, EnergyConsumer)
            assert t.conducting_equipment is consumer, "t.conducting_equipment should be 'ec'"
            assert consumer.location == self.loc1

    def test_create_two_winding_power_transformer(self):
        self.net.create_two_winding_power_transformer(bus1=self.bus1, bus2=self.bus2, asset_info=self.pt_info,
                                                      location=self.loc1)
        objects = self.net.objects(PowerTransformer)
        for ce in objects:
            pt: PowerTransformer = ce
            t: Terminal = pt.get_terminal_by_sn(1)
            assert pt.num_terminals() == 2
            assert isinstance(t, Terminal)
            assert isinstance(pt, PowerTransformer)
            assert t.conducting_equipment is pt, "t.conducting_equipment should be 'pt'"
            assert pt.location == self.loc1

    def test_create_ac_line_segment(self):
        self.net.create_ac_line_segment(bus1=self.bus1, bus2=self.bus2, location=self.loc3)
        objects = self.net.objects(AcLineSegment)
        for ce in objects:
            line_segment: AcLineSegment = ce
            t: Terminal = line_segment.get_terminal_by_sn(1)
            assert line_segment.num_terminals() == 2
            assert isinstance(t, Terminal)
            assert isinstance(line_segment, AcLineSegment)
            assert t.conducting_equipment is line_segment, "t.conducting_equipment should be 'line_segment'"
            assert line_segment.location == self.loc3
