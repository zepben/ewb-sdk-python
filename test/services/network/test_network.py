from zepben.evolve import NetworkService, BaseVoltage


class TestNetworkService(object):

    def test_objects(self):

        network = NetworkService()
        bv = BaseVoltage()
        network.add(bv)

        for obj in network.objects(BaseVoltage):
            assert obj is bv