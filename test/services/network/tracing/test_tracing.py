#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest

from test.network_fixtures import phase_swap_loop_network  # noqa (fixture)
from zepben.evolve import ConductingEquipment, connected_equipment_trace


@pytest.mark.asyncio
async def test_basic_asset_trace(phase_swap_loop_network):
    expected = phase_swap_loop_network.objects(ConductingEquipment)
    visited = set()
    start = phase_swap_loop_network["n0"]

    async def add_to_visited(ce, _):
        visited.add(ce)

    trace = connected_equipment_trace().add_step_action(add_to_visited)
    await trace.trace(start)
    assert visited == set(expected)
