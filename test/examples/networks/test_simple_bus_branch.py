import unittest
from zepben.evolve import SimpleBusBranch, BaseVoltage, EnergySource, Junction, Terminal, Feeder


class TestSimpleBusBranch(unittest.TestCase):

    def test_create_network(self):
        network = SimpleBusBranch()
        voltages = list(network.network_service.objects(BaseVoltage))
        sources = list(network.network_service.objects(EnergySource))
        junctions = list(network.network_service.objects(Junction))
        terminals = list(network.network_service.objects(Terminal))
        feeder = list(network.network_service.objects(Feeder))
        assert len(voltages) == 2, f'len(voltages) should be 2, len(voltages) is: {len(voltages)}'
        assert len(sources) == 1,  f'len(sources) should be 1, len(sources) is: {len(sources)}'
        assert len(junctions) == 3, f'len(junctions) should be 3, len(junctions) is: {len(junctions)}'
        assert len(feeder) == 1, f'len(feeder) should be 2, len(feeder) is: {len(feeder)}'
        assert len(terminals) == 4, f'len(terminals) should be 4, len(terminals) is: {len(terminals)}'




