import unittest
from zepben.evolve.examples import *
from zepben.evolve import BaseVoltage, EnergySource, Junction, Terminal, Feeder, PowerTransformer, \
    ConnectivityNode, DiagramObject, Breaker


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
        breakers = list(self.network_service.objects(Breaker))
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
        assert len(breakers) == 1, f'len(breakers) should be 2, len(breakers) is: {len(breakers)}'

    def test_create_diagram_service(self):
        assert self.diagram_service
        diagram_objects = list(self.diagram_service.objects(DiagramObject))
        assert len(
            diagram_objects) == 5, f'len(diagram_objects) should be 5, len(cdiagram_objects) is: {len(diagram_objects)}'

    def test_breaker_is_open(self):
        net = SimpleNodeBreakerFeeder(breaker_is_open=True)
        breakers = list(net.network_service.objects(Breaker))
        assert len(breakers) == 1
        breaker: Breaker = breakers[0]
        assert isinstance(breaker, Breaker)
        assert breaker.is_open() is True
        net2 = SimpleNodeBreakerFeeder(breaker_is_open=False)
        breakers2 = list(net2.network_service.objects(Breaker))
        assert len(breakers2) == 1
        breaker2 = breakers2[0]
        assert isinstance(breaker2, Breaker)
        assert breaker2.is_open() is False


