import unittest
from zepben.evolve import SimpleBusBranch, BaseVoltage, EnergySource, Junction, Terminal


class TestSimpleBusBranch(unittest.TestCase):

    def test_create_network(self):
        network = SimpleBusBranch()
        voltages = list(network.network_service.objects(BaseVoltage))
        sources = list(network.network_service.objects(EnergySource))
        junctions = list(network.network_service.objects(Junction))
        terminals = list(network.network_service.objects(Terminal))
        assert len(voltages) == 2
        assert len(sources) == 1
        assert len(junctions) == 1
        assert len(terminals) == 2



