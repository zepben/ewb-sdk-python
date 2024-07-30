#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import sys
from typing import Callable, Awaitable

import pytest

from zepben.evolve import ConnectedEquipmentTraversal, NetworkService, Feeder, FindSwerEquipment, Junction, TestNetworkBuilder, PhaseCode, BaseVoltage, \
    ConductingEquipment, verify_stop_conditions, ConductingEquipmentStep, step_on_when_run, step_on_when_run_with_is_stopping

# AsyncMock was not included in the base module until 3.8, so use the backport instead if required
v = sys.version_info
if v.major == 3 and v.minor < 8:
    # noinspection PyPackageRequirements
    # noinspection PyUnresolvedReferences
    # pylint: disable=import-error
    from mock import create_autospec, patch, call, Mock
    # pylint: enable=import-error
else:
    from unittest.mock import create_autospec, patch, call, Mock


def create_mock_connected_equipment_traversal() -> Mock:
    """Create a mock version of the `ConnectedEquipmentTraversal` which calls through the run method."""
    trace = create_autospec(ConnectedEquipmentTraversal, instance=True)

    async def call_run(it):
        # noinspection PyArgumentList
        await trace.run(ConductingEquipmentStep(it))

    trace.run_from.side_effect = call_run

    return trace


class TestFindSwerEquipment:

    # pylint: disable=attribute-defined-outside-init
    # noinspection PyArgumentList
    def setup_method(self):
        self.trace1 = create_mock_connected_equipment_traversal()
        self.trace2 = create_mock_connected_equipment_traversal()
        self.create_trace = create_autospec(Callable[[], ConnectedEquipmentTraversal], side_effect=[self.trace1, self.trace2])

        self.find_swer_equipment = FindSwerEquipment(self.create_trace)
    # pylint: enable=attribute-defined-outside-init

    @pytest.mark.asyncio
    async def test_processes_all_feeders_in_a_network(self):
        ns = NetworkService()
        feeder1 = Feeder()
        feeder2 = Feeder()
        j1 = Junction()
        j2 = Junction()
        j3 = Junction()

        ns.add(feeder1)
        ns.add(feeder2)
        ns.add(j1)
        ns.add(j2)
        ns.add(j3)

        with patch.object(self.find_swer_equipment, 'find_on_feeder', side_effect=[[j1, j2], [j2, j3]]) as find_on_feeder:
            assert await self.find_swer_equipment.find_all(ns) == {j1, j2, j3}

            find_on_feeder.assert_has_calls([call(feeder1), call(feeder2)])

    @pytest.mark.asyncio
    async def test_only_runs_trace_from_swer_transformers_and_only_runs_non_swer_from_lv(self):
        ns = (await TestNetworkBuilder()
              .from_breaker()  # b0
              .to_power_transformer()  # tx1
              .to_acls()  # c2
              .to_power_transformer([PhaseCode.AB, PhaseCode.A])  # tx3
              .to_acls(PhaseCode.A)  # c4
              .to_acls(PhaseCode.A)  # c5
              .to_power_transformer([PhaseCode.A, PhaseCode.AN])  # tx6
              .to_acls(PhaseCode.AN, action=self._make_lv)  # c7
              .add_feeder("b0")  # fdr8
              .build())

        self.create_trace.side_effect = [self.trace1, self.trace2, self.trace1, self.trace2]

        assert await self.find_swer_equipment.find_on_feeder(ns["fdr8"]) == {ns["tx3"], ns["tx6"]}

        assert self.create_trace.call_count == 4
        self.trace1.run_from.assert_has_calls([call(ns["c4"]), call(ns["c5"])])
        self.trace2.run_from.assert_called_once_with(ns["c7"])

    @pytest.mark.asyncio
    async def test_does_not_run_from_swer_regulators(self):
        ns = (await TestNetworkBuilder()
              .from_breaker(PhaseCode.A)  # b0
              .to_power_transformer([PhaseCode.A, PhaseCode.A])  # tx1
              .to_acls(PhaseCode.A)  # c2
              .add_feeder("b0")  # fdr3
              .build())

        await self.find_swer_equipment.find_on_feeder(ns["fdr3"])

        self.trace1.run.assert_not_called()
        self.trace2.run.assert_not_called()

    @pytest.mark.asyncio
    async def test_validate_swer_trace_stop_conditions(self):
        ns = (await TestNetworkBuilder()
              .from_power_transformer([PhaseCode.A, PhaseCode.AN])  # tx0
              .from_power_transformer([PhaseCode.A, PhaseCode.AN])  # tx0
              .from_power_transformer()  # tx2
              .add_feeder("tx0")  # fdr3
              .build())

        await self.find_swer_equipment.find_on_feeder(ns["fdr3"])

        # noinspection PyArgumentList
        async def stops_on_equipment_in_swer_collection(stop_condition: Callable[[ConductingEquipmentStep], Awaitable[None]]):
            assert await stop_condition(ConductingEquipmentStep(ns["tx0"])), "Stops on equipment in swer collection"
            assert not await stop_condition(ConductingEquipmentStep(ns["tx1"])), "Does not stop on equipment not in SWER collection"
            assert not await stop_condition(ConductingEquipmentStep(ns["tx2"])), "Does not stop on equipment not in SWER collection"

        # noinspection PyArgumentList
        async def stops_on_equipment_without_swer_terminal(stop_condition: Callable[[ConductingEquipmentStep], Awaitable[None]]):
            assert not await stop_condition(ConductingEquipmentStep(ns["tx0"])), "Does not stop on equipment with SWER terminal"
            assert not await stop_condition(ConductingEquipmentStep(ns["tx1"])), "Does not stop on equipment with SWER terminal"
            assert await stop_condition(ConductingEquipmentStep(ns["tx2"])), "Stops on equipment without SWER terminals"

        await verify_stop_conditions(self.trace1, stops_on_equipment_in_swer_collection, stops_on_equipment_without_swer_terminal)

    @pytest.mark.asyncio
    async def test_validate_swer_trace_step_action(self):
        ns = (await TestNetworkBuilder()
              .from_power_transformer([PhaseCode.AN, PhaseCode.A])  # tx0
              .to_acls()  # c1 -- this is here to make the trace actually run, so things are stepped on.
              .from_power_transformer([PhaseCode.A, PhaseCode.AN])  # tx2
              .from_power_transformer([PhaseCode.A, PhaseCode.AN])  # tx3
              .from_breaker()  # b4
              .add_feeder("tx0")  # fdr5
              .build())

        # noinspection PyArgumentList
        step_on_when_run_with_is_stopping(
            self.trace1,
            (ConductingEquipmentStep(ns["tx2"]), False),
            (ConductingEquipmentStep(ns["tx3"]), True),
            (ConductingEquipmentStep(ns["b4"]), True)
        )

        # tx2 should not have been added as it was stopping. b3 should have been added even though it was stopping.
        assert await self.find_swer_equipment.find_on_feeder(ns["fdr5"]) == {ns["tx0"], ns["tx2"], ns["b4"]}

        # This is here to make sure the above block is actually run.
        self.trace1.run.assert_called_once()

    @pytest.mark.asyncio
    async def test_validate_lv_trace_stop_condition(self):
        ns = (await TestNetworkBuilder()
              .from_power_transformer([PhaseCode.A, PhaseCode.AN])  # tx0
              .from_power_transformer([PhaseCode.A, PhaseCode.AN])  # tx0
              .add_feeder("tx0")  # fdr2
              .build())

        await self.find_swer_equipment.find_on_feeder(ns["fdr2"])

        # noinspection PyArgumentList
        async def stops_on_equipment_in_swer_collection(stop_condition: Callable[[ConductingEquipmentStep], Awaitable[None]]):
            assert await stop_condition(ConductingEquipmentStep(ns["tx0"])), "Stops on equipment in swer collection"
            assert not await stop_condition(ConductingEquipmentStep(ns["tx1"])), "Does not stop on equipment not in SWER collection"

        await verify_stop_conditions(self.trace2, stops_on_equipment_in_swer_collection)

    @pytest.mark.asyncio
    async def test_validate_lv_trace_step_action(self):
        ns = (await TestNetworkBuilder()
              .from_power_transformer([PhaseCode.A, PhaseCode.AN])  # tx0
              .to_acls(PhaseCode.AN, action=self._make_lv)  # c1 -- this is here to make the trace actually run, so things are stepped on.
              .from_power_transformer([PhaseCode.A, PhaseCode.AN])  # tx2
              .add_feeder("tx0")  # fdr3
              .build())

        # noinspection PyArgumentList
        step_on_when_run(self.trace2, ConductingEquipmentStep(ns["tx2"]))

        assert await self.find_swer_equipment.find_on_feeder(ns["fdr3"]) == {ns["tx0"], ns["tx2"]}
        # await self.find_swer_equipment.find_on_feeder(ns["fdr3"])

        # This is here to make sure the above block is actually run.
        self.trace2.run.assert_called_once()

    @pytest.mark.asyncio
    async def test_runs_off_multiple_terminals(self):
        ns = (await TestNetworkBuilder()
              .from_power_transformer([PhaseCode.A, PhaseCode.A, PhaseCode.AN, PhaseCode.AN])  # tx0
              .to_acls(PhaseCode.AN, action=self._make_lv)  # c1
              .branch_from("tx0", 1)
              .to_acls(PhaseCode.A)  # c2
              .branch_from("tx0", 2)
              .to_acls(PhaseCode.A)  # c3
              .branch_from("tx0", 3)
              .to_acls(PhaseCode.AN, action=self._make_lv)  # c4
              .add_feeder("tx0")  # fdr5
              .build())

        # We need to run the actual trace rather than a mock to make sure it is being reset, as the mock does not have the same requirement.
        await FindSwerEquipment().find_on_feeder(ns["fdr5"])

    @pytest.mark.asyncio
    async def test_does_not_loop_back_out_of_swer_from_lv(self):
        ns = (await TestNetworkBuilder()
              .from_junction(num_terminals=1)  # j0
              .to_acls()  # c1
              .to_acls(PhaseCode.A)  # c2
              .to_power_transformer([PhaseCode.A, PhaseCode.AN])  # tx3
              .to_acls(PhaseCode.AN, action=self._make_lv)  # c4
              .to_power_transformer([PhaseCode.AN, PhaseCode.A])  # tx5
              .to_acls(PhaseCode.A)  # c6
              .connect("c6", "c1", 2, 1)
              .add_feeder("j0")  # fdr7
              .build())

        # We need to run the actual trace rather than a mock to make sure it does not loop back through the LV.
        assert await FindSwerEquipment().find_all(ns) == {ns["c2"], ns["tx3"], ns["c4"], ns["tx5"], ns["c6"]}

    @staticmethod
    def _make_lv(ce: ConductingEquipment):
        bv = BaseVoltage()
        bv.nominal_voltage = 415
        ce.base_voltage = bv
