import unittest
from zepben.evolve import SimpleBusBranch, BaseVoltage, EnergySource, Junction, Terminal, Feeder, PowerTransformer, \
    ConnectivityNode, DiagramObject


class TestSimpleBusBranch(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSimpleBusBranch, self).__init__(*args, **kwargs)
        self.network_service = SimpleBusBranch().network_service
        self.diagram_service = SimpleBusBranch().diagram_service

    def test_self_create_network(self):
        voltages = list(self.network_service.objects(BaseVoltage))
        sources = list(self.network_service.objects(EnergySource))
        junctions = list(self.network_service.objects(Junction))
        terminals = list(self.network_service.objects(Terminal))
        power_transformers = list(self.network_service.objects(PowerTransformer))
        connectivity_nodes = list(self.network_service.objects(ConnectivityNode))
        feeders = list(self.network_service.objects(Feeder))
        assert len(voltages) == 2, f'len(voltages) should be 2, len(voltages) is: {len(voltages)}'
        assert len(sources) == 1, f'len(sources) should be 1, len(sources) is: {len(sources)}'
        assert len(junctions) == 3, f'len(junctions) should be 3, len(junctions) is: {len(junctions)}'
        assert len(
            power_transformers) == 1, f'len(power_transformers) should be 1, len(power_transformers) is: {len(power_transformers)}'
        assert len(feeders) == 1, f'len(feeder) should be 2, len(feeder) is: {len(feeder)}'
        assert len(terminals) == 9, f'len(terminals) should be 9, len(terminals) is: {len(terminals)}'
        assert len(
            connectivity_nodes) == 6, f'len(connectivity_nodes) should be 6, len(connectivity_nodes) is: {len(connectivity_nodes)}'

    def test_create_diagram_service(self):
        assert self.diagram_service
        diagram_objects = list(self.diagram_service.objects(DiagramObject))
        assert len(diagram_objects) == 7, f'len(connectivity_nodes) should be 6, len(connectivity_nodes) is: {len(diagram_objects)}'
