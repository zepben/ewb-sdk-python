from zepben.evolve import NetworkService, EnergySourcePhase


class TestNetworkService(object):

    def test_objects(self):

        network = NetworkService()
        esf = EnergySourcePhase()
        network.add(esf)

        for obj in network.objects(EnergySourcePhase):
            assert obj is esf