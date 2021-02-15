from zepben.evolve import NetworkService, Junction, BaseVoltage, Terminal, EnergySource
import unittest


class TestNetworkCreator(unittest.TestCase):

    def test_create_bus(self):
        net = NetworkService()
        bv = BaseVoltage()
        bus = net.create_bus(bv=bv)
        assert isinstance(bus, Junction)
        assert bus.num_terminals() == 1, "num_terminals should be 1"
        t: Terminal = bus.get_terminal_by_sn(1)
        assert t is not None
        assert bus.get_base_voltage(1) is bv
        assert t.conducting_equipment is bus, "t.conducting_equipment should be 'bus'"

    def test_create_source_for_connecting(self):
        net = NetworkService()
        source: EnergySource = net.create_source_for_connecting()
        t: Terminal = source.get_terminal_by_sn(1)
        assert source.num_terminals() == 1
        assert isinstance(t, Terminal)
        assert isinstance(source, EnergySource)
        assert t.conducting_equipment is source, "t.conducting_equipment should be 'source'"

