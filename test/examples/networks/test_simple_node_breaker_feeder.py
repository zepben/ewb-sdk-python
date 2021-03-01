import unittest
from zepben.evolve.examples import *
from zepben.evolve import BaseVoltage, EnergySource, Junction, Terminal, Feeder, PowerTransformer, \
    ConnectivityNode, DiagramObject


class TestSimpleNodeBreaker(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSimpleNodeBreaker, self).__init__(*args, **kwargs)
        self.network_service = SimpleNodeBreakerFeeder().network_service
        self.diagram_service = SimpleNodeBreakerFeeder().diagram_service

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
        assert len(junctions) == 0, f'len(junctions) should be 0, len(junctions) is: {len(junctions)}'
        assert len(
            power_transformers) == 1, f'len(power_transformers) should be 1, len(power_transformers) is: {len(power_transformers)}'
        assert len(feeders) == 1, f'len(feeder) should be 2, len(feeder) is: {len(feeders)}'
        assert len(terminals) == 8, f'len(terminals) should be 8, len(terminals) is: {len(terminals)}'
        assert len(
            connectivity_nodes) == 4, f'len(connectivity_nodes) should be 4, len(connectivity_nodes) is: {len(connectivity_nodes)}'

    def test_create_diagram_service(self):
        assert self.diagram_service
        diagram_objects = list(self.diagram_service.objects(DiagramObject))
        assert len(diagram_objects) == 5, f'len(diagram_objects) should be 5, len(cdiagram_objects) is: {len(diagram_objects)}'
