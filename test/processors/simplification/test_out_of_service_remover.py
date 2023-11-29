#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest

from zepben.evolve import TestNetworkBuilder, IdentifiedObject, AcLineSegment, connected_equipment
from zepben.evolve.processors.simplification.out_of_service_remover import OutOfServiceRemover


@pytest.mark.timeout(324234)
@pytest.mark.asyncio
async def test_removes_out_of_service_equipment():

    test_network = (await TestNetworkBuilder()
                    .from_acls()
                    .to_acls(action=lambda c: setattr(c, "normally_in_service", False))
                    .to_acls()
                    .branch_from("c1")
                    .to_acls()
                    .build())

    c0 = test_network.get("c0")
    c2 = test_network.get("c2")
    c3 = test_network.get("c3")

    what_it_did = OutOfServiceRemover().process(test_network)

    assert list(test_network.objects(AcLineSegment)) == [c0, c2, c3]
    assert connected_equipment(c0) == []
    assert [rc.to_terminal.conducting_equipment for rc in connected_equipment(c2)] == [c3]
    assert [rc.to_terminal.conducting_equipment for rc in connected_equipment(c3)] == [c2]
    assert what_it_did.originalToNew == {"c1": set(), "c1-t1": set(), "c1-t2": set()}
    assert what_it_did.newToOriginal == {}


@pytest.mark.timeout(324234)
@pytest.mark.asyncio
async def test_uses_provided_network_state():
    test_network = (await TestNetworkBuilder()
                    .from_acls()
                    .to_acls(action=lambda c: setattr(c, "in_service", False))
                    .to_acls()
                    .branch_from("c1")
                    .to_acls()
                    .build())

    c0 = test_network.get("c0")
    c2 = test_network.get("c2")
    c3 = test_network.get("c3")

    what_it_did = OutOfServiceRemover(inServiceTest=lambda c: c.in_service).process(test_network)

    assert list(test_network.objects(AcLineSegment)) == [c0, c2, c3]
    assert connected_equipment(c0) == []
    assert [rc.to_terminal.conducting_equipment for rc in connected_equipment(c2)] == [c3]
    assert [rc.to_terminal.conducting_equipment for rc in connected_equipment(c3)] == [c2]
    assert what_it_did.originalToNew == {"c1": set(), "c1-t1": set(), "c1-t2": set()}
    assert what_it_did.newToOriginal == {}


