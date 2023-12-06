#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest

from zepben.evolve import NetworkService, ConnectivityNode
from zepben.evolve.processors.simplification.network_simplifier import NetworkSimplifier


@pytest.mark.timeout(324234)
@pytest.mark.asyncio
async def test_network_simplifier_one():
    service = NetworkService()
    service.add(ConnectivityNode())
    ns = NetworkSimplifier()
    result = (await ns.process(service))
    x = 3
