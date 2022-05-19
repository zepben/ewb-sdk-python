#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from zepben.evolve import TestNetworkBuilder, Feeder, ConductingEquipment, set_direction, FeederDirection, NetworkService


@pytest.mark.asyncio
async def test_set_direction():
    network = _get_single_feeder_network()
    await set_direction().run(network)

    assert network.get("b0-t1").normal_feeder_direction == FeederDirection.NONE
    assert network.get("b0-t2").normal_feeder_direction == FeederDirection.DOWNSTREAM
    assert network.get("c1-t1").normal_feeder_direction == FeederDirection.UPSTREAM
    assert network.get("c1-t2").normal_feeder_direction == FeederDirection.DOWNSTREAM
    assert network.get("j2-t1").normal_feeder_direction == FeederDirection.UPSTREAM
    assert network.get("j2-t2").normal_feeder_direction == FeederDirection.DOWNSTREAM


@pytest.mark.asyncio
async def test_set_direction_doesnt_flow_through_feeder_heads():
    network = _get_dual_parallel_feeders_network()
    await set_direction().run(network)

    assert network.get("b0-t1").normal_feeder_direction == FeederDirection.NONE
    assert network.get("b0-t2").normal_feeder_direction == FeederDirection.BOTH
    assert network.get("c1-t1").normal_feeder_direction == FeederDirection.BOTH
    assert network.get("c1-t2").normal_feeder_direction == FeederDirection.BOTH
    assert network.get("b2-t1").normal_feeder_direction == FeederDirection.BOTH
    assert network.get("b2-t2").normal_feeder_direction == FeederDirection.NONE


# feeder_heads:     feeder
#                   v
# network:          b0 -- c1 -- j2
def _get_single_feeder_network() -> NetworkService:
    network = TestNetworkBuilder().from_breaker().to_acls().to_junction().network
    feeder = Feeder(mrid="f")
    network.add(feeder)

    for ce in network.objects(ConductingEquipment):
        _assign_feeder(ce, feeder)

    feeder.normal_head_terminal = network.get("b0-t2")
    return network


# feeder_heads:     feeder1     feeder2
#                   v           v
# network:          b0 -- c1 -- b2
def _get_dual_parallel_feeders_network() -> NetworkService:
    network = TestNetworkBuilder().from_breaker().to_acls().to_breaker().network
    feeder1 = Feeder(mrid="f1")
    network.add(feeder1)
    feeder2 = Feeder(mrid="f2")
    network.add(feeder2)

    _assign_feeder(network.get("b0"), feeder1)
    _assign_feeder(network.get("c1"), feeder1, feeder2)
    _assign_feeder(network.get("b2"), feeder2)

    feeder1.normal_head_terminal = network.get("b0-t2")
    feeder2.normal_head_terminal = network.get("b2-t1")
    return network


def _assign_feeder(ce: ConductingEquipment, *feeders: Feeder) -> ConductingEquipment:
    for feeder in feeders:
        feeder.add_equipment(ce)
        ce.add_container(feeder)
    return ce
