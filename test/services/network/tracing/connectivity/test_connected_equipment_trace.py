#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections import Counter

import pytest

from zepben.evolve import connected_equipment_trace, BasicTraversal, ConductingEquipmentStep, normal_connected_equipment_trace, \
    current_connected_equipment_trace, normal_limited_connected_equipment_trace, current_limited_connected_equipment_trace, TestNetworkBuilder
from zepben.evolve.services.network.tracing.connectivity.limited_connected_equipment_trace import LimitedConnectedEquipmentTrace


class TestConnectedEquipmentTrace:
    network = (TestNetworkBuilder()
               .from_junction()
               .to_breaker(is_normally_open=True, is_open=True)
               .to_breaker(is_normally_open=True, is_open=False)
               .to_junction()
               .to_breaker(is_normally_open=False, is_open=True)
               .to_breaker(is_normally_open=True, is_open=True)
               .to_junction()
               .network)
    """
    j0--b1--b2--j3--b4--b5--j6
        bo  no      co  bo

    bo = both open
    no = normally open
    co = currently open
    """

    @pytest.mark.asyncio
    async def test_connected_equipment_trace_ignores_open_state(self):
        await self._validate_run(connected_equipment_trace(), "j3", "b2", "b1", "j0", "b4", "b5", "j6")

    @pytest.mark.asyncio
    async def test_normal_connected_equipment_trace_uses_open_state(self):
        await self._validate_run(normal_connected_equipment_trace(), "j3", "b2", "b4", "b5")

    @pytest.mark.asyncio
    async def test_current_connected_equipment_trace_uses_open_state(self):
        await self._validate_run(current_connected_equipment_trace(), "j3", "b2", "b1", "b4")

    @staticmethod
    @pytest.mark.asyncio
    async def test_limited_trace_coverage():
        # These traces are implemented and tested in a separate class, so just do a simple type check coverage test.
        assert isinstance(normal_limited_connected_equipment_trace(), LimitedConnectedEquipmentTrace)
        assert isinstance(current_limited_connected_equipment_trace(), LimitedConnectedEquipmentTrace)

    @pytest.mark.asyncio
    async def test_can_start_on_open_switch(self):
        await self._validate_run(normal_connected_equipment_trace(), "b1", "j0", "b2")
        await self._validate_run(current_connected_equipment_trace(), "b5", "b4", "j6")

    async def _validate_run(self, traversal: BasicTraversal[ConductingEquipmentStep], start: str, *expected: str):
        visited = set()

        async def step_action(it: ConductingEquipmentStep, _: bool):
            visited.add(it.conducting_equipment.mrid)

        # noinspection PyArgumentList
        await traversal.add_step_action(step_action).run(ConductingEquipmentStep(self.network[start]))

        assert Counter(visited) == Counter([start, *expected])
