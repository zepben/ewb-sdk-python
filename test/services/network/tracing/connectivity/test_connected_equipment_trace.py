#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections import Counter

import pytest

from zepben.evolve import connected_equipment_trace, BasicTraversal, ConductingEquipmentStep, normal_connected_equipment_trace, \
    current_connected_equipment_trace, normal_limited_connected_equipment_trace, current_limited_connected_equipment_trace, TestNetworkBuilder, \
    ConductingEquipment, PhaseCode, NetworkService
from zepben.evolve.services.network.tracing.connectivity.connected_equipment_trace import new_normal_downstream_equipment_trace, \
    new_current_downstream_equipment_trace, new_normal_upstream_equipment_trace, new_current_upstream_equipment_trace
from zepben.evolve.services.network.tracing.connectivity.limited_connected_equipment_trace import LimitedConnectedEquipmentTrace


class TestConnectedEquipmentTrace:
    straight_network = (TestNetworkBuilder()
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

    @pytest.fixture
    async def branched_network(self):
        """
        1 c0 21--b1--21 b2(no) 21--c3--2
                  1
                  b4(c0) 21--c5--2
        """
        return await (TestNetworkBuilder()
                      .from_acls()  # c0
                      .to_breaker()  # b1
                      .to_breaker(action=lambda b: b.set_normally_open(True))  # b2
                      .to_acls()  # c3
                      .branch_from("b1")
                      .to_breaker(action=lambda b: b.set_open(True))  # b4
                      .to_acls()  # c5
                      .add_feeder("c0")  # fdr6
                      .build())

    @pytest.mark.asyncio
    async def test_connected_equipment_trace_checks_open_state(self):
        await self._validate_run(connected_equipment_trace(), "j3", "b2", "b1", "j0", "b4", "b5", "j6")
        await self._validate_run(normal_connected_equipment_trace(), "j3", "b2", "b4", "b5")
        await self._validate_run(current_connected_equipment_trace(), "j3", "b2", "b1", "b4")

    @staticmethod
    @pytest.mark.asyncio
    async def test_limited_trace_coverage():
        # These traces are implemented and tested in a separate class, so just do a simple type check coverage test.
        assert isinstance(normal_limited_connected_equipment_trace(), LimitedConnectedEquipmentTrace)
        assert isinstance(current_limited_connected_equipment_trace(), LimitedConnectedEquipmentTrace)

    @pytest.mark.asyncio
    async def test_connected_equipment_trace_can_start_on_open_switch(self):
        await self._validate_run(normal_connected_equipment_trace(), "b1", "j0", "b2")
        await self._validate_run(current_connected_equipment_trace(), "b5", "b4", "j6")

    @pytest.mark.asyncio
    async def test_direction_based_trace_respects_direction_and_state(self, branched_network):
        await self._validate_trace(branched_network, new_normal_downstream_equipment_trace(), "c0", "b1", "b2", "b4", "c5")
        await self._validate_trace(branched_network, new_normal_downstream_equipment_trace(), "b2")
        await self._validate_trace(branched_network, new_normal_downstream_equipment_trace(), "b4", "c5")

        await self._validate_trace(branched_network, new_current_downstream_equipment_trace(), "c0", "b1", "b2", "c3", "b4")
        await self._validate_trace(branched_network, new_current_downstream_equipment_trace(), "b2", "c3")
        await self._validate_trace(branched_network, new_current_downstream_equipment_trace(), "b4")

        await self._validate_trace(branched_network, new_normal_upstream_equipment_trace(), "b1", "c0")
        await self._validate_trace(branched_network, new_normal_upstream_equipment_trace(), "c3")
        await self._validate_trace(branched_network, new_normal_upstream_equipment_trace(), "c5", "b4", "b1", "c0")

        await self._validate_trace(branched_network, new_current_upstream_equipment_trace(), "b1", "c0")
        await self._validate_trace(branched_network, new_current_upstream_equipment_trace(), "c3", "b2", "b1", "c0")
        await self._validate_trace(branched_network, new_current_upstream_equipment_trace(), "c5")

    @pytest.mark.asyncio
    async def test_direction_based_trace_ignores_phase_connectivity(self, branched_network):
        for it in branched_network.get("b4", ConductingEquipment).terminals:
            it.phases = PhaseCode.A
        for it in branched_network.get("c5", ConductingEquipment).terminals:
            it.phases = PhaseCode.B

        await self._validate_trace(branched_network, new_normal_downstream_equipment_trace(), "b4", "c5")

    async def _validate_run(self, traversal: BasicTraversal[ConductingEquipmentStep], start: str, *expected: str):
        visited = set()

        async def step_action(it: ConductingEquipmentStep, _: bool):
            visited.add(it.conducting_equipment.mrid)

        # noinspection PyArgumentList
        await traversal.add_step_action(step_action).run(ConductingEquipmentStep(self.straight_network[start]))

        assert Counter(visited) == Counter([start, *expected])

    @staticmethod
    async def _validate_trace(branched_network: NetworkService, trace: BasicTraversal[ConductingEquipment], start: str, *expected: str):
        visited = []

        async def step_action(it: ConductingEquipment, _: bool):
            visited.append(it.mrid)

        await trace.add_step_action(step_action).run(branched_network.get(start))

        assert Counter(visited) == Counter([start, *expected])
