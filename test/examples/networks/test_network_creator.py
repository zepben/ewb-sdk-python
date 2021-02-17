from zepben.evolve import NetworkService, Junction, BaseVoltage, Terminal, EnergySource, \
    PowerTransformer, AcLineSegment, EnergyConsumer, PowerTransformerInfo
import unittest


class TestNetworkCreator(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestNetworkCreator, self).__init__(*args, **kwargs)
        self.net = NetworkService()
        self.bv = BaseVoltage()
        self.bus1 = self.net.create_bus(BaseVoltage())
        self.bus2 = self.net.create_bus(BaseVoltage())
        self.pt_info = PowerTransformerInfo()

    def test_create_bus(self):
        bus = self.net.create_bus(base_voltage=self.bv)
        assert isinstance(bus, Junction)
        assert bus.num_terminals() == 1, "num_terminals should be 1"
        t: Terminal = bus.get_terminal_by_sn(1)
        assert t is not None
        assert bus.get_base_voltage() is self.bv, f'bus.get_base_voltage() is not bv. Instead is {bus.get_base_voltage()}'
        assert t.conducting_equipment is bus, "t.conducting_equipment should be 'bus'"

    def test_create_energy_source(self):
        source: EnergySource = self.net.create_energy_source(bus=self.bus1)
        t: Terminal = source.get_terminal_by_sn(1)
        assert source.num_terminals() == 1
        assert isinstance(t, Terminal)
        assert isinstance(source, EnergySource)
        assert t.conducting_equipment is source, "t.conducting_equipment should be 'source'"

    def test_create_energy_consumer(self):
        ec: EnergyConsumer = self.net.create_energy_consumer(bus=self.bus1)
        t: Terminal = ec.get_terminal_by_sn(1)
        assert ec.num_terminals() == 1
        assert isinstance(t, Terminal)
        assert isinstance(ec, EnergyConsumer)
        assert t.conducting_equipment is ec, "t.conducting_equipment should be 'ec'"

    def test_create_two_winding_power_transformer(self):
        pt = self.net.create_two_winding_power_transformer(bus1=self.bus1, bus2=self.bus2, pt_info = self.pt_info)
        t: Terminal = pt.get_terminal_by_sn(1)
        assert pt.num_terminals() == 2
        assert isinstance(t, Terminal)
        assert isinstance(pt, PowerTransformer)
        assert t.conducting_equipment is pt, "t.conducting_equipment should be 'pt'"

    def test_create_ac_line_segment(self):
        line_segment = self.net.create_ac_line_segment(bus1=self.bus1, bus2=self.bus2)
        t: Terminal = line_segment.get_terminal_by_sn(1)
        assert line_segment.num_terminals() == 2
        assert isinstance(t, Terminal)
        assert isinstance(line_segment, AcLineSegment)
        assert t.conducting_equipment is line_segment, "t.conducting_equipment should be 'line_segment'"
