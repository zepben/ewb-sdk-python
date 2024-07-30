#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import NetworkService, BaseVoltage


class TestNetworkService(object):

    def test_objects(self):

        network = NetworkService()
        bv = BaseVoltage()
        network.add(bv)

        for obj in network.objects(BaseVoltage):
            assert obj is bv
