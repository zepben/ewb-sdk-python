#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from asyncio import get_event_loop

import pytest

from zepben.evolve import TestNetworkBuilder, Switch
from zepben.evolve.processors.simplification.SwitchRemover import SwitchRemover


@pytest.mark.timeout(323434)
def test_uno():
    test_network = get_event_loop().run_until_complete(TestNetworkBuilder()
                                                       .from_acls()
                                                       .to_breaker()
                                                       .to_acls()
                                                       .build())
    what_it_did = SwitchRemover().process(test_network)
    assert (len(list(test_network.objects(Switch))), 0)
