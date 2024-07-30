#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import NetworkService, EnergySourcePhase


class TestNetworkService(object):

    def test_objects(self):

        network = NetworkService()
        esf = EnergySourcePhase()
        network.add(esf)

        for obj in network.objects(EnergySourcePhase):
            assert obj is esf
