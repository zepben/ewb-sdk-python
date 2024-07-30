#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import inspect
import sys

import pytest

from zepben.evolve import TestNetworkBuilder, ConductingEquipmentStep, Junction, FeederDirection, Terminal, ConductingEquipment, \
    normal_connected_equipment_trace
from zepben.evolve.services.network.tracing.connectivity.connected_equipment_traversal import ConnectedEquipmentTraversal
from zepben.evolve.services.network.tracing.connectivity.limited_connected_equipment_trace import LimitedConnectedEquipmentTrace

# AsyncMock was not included in the base module until 3.8, so use the backport instead if required
v = sys.version_info
if v.major == 3 and v.minor < 8:
    # noinspection PyPackageRequirements
    # noinspection PyUnresolvedReferences
    # pylint: disable=import-error
    from mock import MagicMock, Mock, create_autospec
    # pylint: enable=import-error
else:
    from unittest.mock import MagicMock, Mock, create_autospec


def with_mock_trace(func):
    """
    A decorator that creates the mock traversal and trace instances used by the tests.
    """

    async def create_mocks_and_call(self, *args, **kwargs):
        traversal = create_autospec(ConnectedEquipmentTraversal, instance=True)
        get_terminal_direction = Mock(wraps=lambda it: it.normal_feeder_direction)
        # noinspection PyArgumentList
        trace = LimitedConnectedEquipmentTrace(lambda: traversal, get_terminal_direction)

        if "get_terminal_direction" in inspect.signature(func).parameters:
            await func(self, traversal=traversal, trace=trace, get_terminal_direction=get_terminal_direction, *args, **kwargs)
        else:
            await func(self, traversal=traversal, trace=trace, *args, **kwargs)

    return create_mocks_and_call


def with_simple_ns(func):
    """
    A decorator that will provide the simple network.
    """

    async def create_simple_ns(self, *args, **kwargs):
        simple_ns = (await TestNetworkBuilder()
                     .from_junction(num_terminals=1)  # j0
                     .to_acls()  # c1
                     .to_breaker()  # b2
                     .to_acls()  # c3
                     .add_feeder("j0")
                     .build())

        await func(self, simple_ns=simple_ns, *args, **kwargs)

    return create_simple_ns


# noinspection PyArgumentList
class TestLimitedConnectedEquipmentTrace:

    @pytest.mark.asyncio
    @with_mock_trace
    async def test_without_direction_adds_stop_condition_and_step_action(self, traversal, trace):
        await trace.run([MagicMock()])

        traversal.add_stop_condition.assert_called_once()
        traversal.add_step_action.assert_called_once()

    @pytest.mark.asyncio
    @with_mock_trace
    async def test_without_direction_stop_condition_checks_provided_maximum_steps(self, traversal, trace):
        await trace.run([MagicMock()], 2)

        stop_condition = traversal.add_stop_condition.call_args.args[0]
        assert not await stop_condition(ConductingEquipmentStep(MagicMock())), "Step 0 does not stop"
        assert not await stop_condition(ConductingEquipmentStep(MagicMock(), 1)), "Step 1 does not stop"
        assert await stop_condition(ConductingEquipmentStep(MagicMock(), 2)), "Step 2 stops"

    @pytest.mark.asyncio
    @with_mock_trace
    async def test_without_direction_runs_the_trace_from_each_start_item(self, traversal, trace):
        j1 = Junction()
        j2 = Junction()

        await trace.run([j1, j2])

        assert traversal.run_from.call_count == 2
        traversal.run_from.assert_any_call(j1, False)
        traversal.run_from.assert_called_with(j2, False)

    @pytest.mark.asyncio
    @with_mock_trace
    async def test_without_direction_step_action_adds_to_results(self, traversal, trace):
        j = Junction()
        await self._configure_run_step_actions(traversal, ConductingEquipmentStep(j, 2))

        results = await trace.run([j], 2)

        assert results == {j: 2}

    @pytest.mark.asyncio
    @with_simple_ns
    @with_mock_trace
    async def test_with_direction_adds_stop_condition_and_step_action(self, traversal, trace, simple_ns):
        await trace.run([simple_ns["j0"]], feeder_direction=FeederDirection.DOWNSTREAM)

        assert traversal.add_stop_condition.call_count == 3
        traversal.add_step_action.assert_called_once()

    @pytest.mark.asyncio
    @with_simple_ns
    @with_mock_trace
    async def test_with_direction_first_stop_condition_checks_provided_maximum_steps_minus_one(self, traversal, trace, simple_ns):
        await trace.run([simple_ns["j0"]], 2, feeder_direction=FeederDirection.DOWNSTREAM)

        stop_condition = traversal.add_stop_condition.call_args_list[0].args[0]
        assert not await stop_condition(ConductingEquipmentStep(MagicMock())), "Step 0 does not stop"
        assert await stop_condition(ConductingEquipmentStep(MagicMock(), 1)), "Step 1 stops"
        assert await stop_condition(ConductingEquipmentStep(MagicMock(), 2)), "Step 2 stops"

    @pytest.mark.asyncio
    @with_simple_ns
    @with_mock_trace
    async def test_with_direction_second_stop_condition_checks_starting_equipment(self, traversal, trace, simple_ns):
        await trace.run([simple_ns["j0"]], feeder_direction=FeederDirection.DOWNSTREAM)

        stop_condition = traversal.add_stop_condition.call_args_list[1].args[0]
        assert await stop_condition(ConductingEquipmentStep(simple_ns["j0"])), "Stops on start equipment"
        assert not await stop_condition(ConductingEquipmentStep(Junction())), "Does not stop on other equipment"

    @pytest.mark.asyncio
    @with_simple_ns
    @with_mock_trace
    async def test_with_direction_third_stop_condition_checks_direction(self, traversal, trace, get_terminal_direction, simple_ns):
        t1 = Terminal()
        j = Junction(terminals=[t1])

        await trace.run([simple_ns["j0"]], feeder_direction=FeederDirection.DOWNSTREAM)

        stop_condition = traversal.add_stop_condition.call_args_list[2].args[0]
        get_terminal_direction.side_effect = [FeederDirection.DOWNSTREAM, FeederDirection.BOTH, FeederDirection.UPSTREAM]

        assert not await stop_condition(ConductingEquipmentStep(j)), "Does not stop with matching feeder direction"
        assert await stop_condition(ConductingEquipmentStep(j)), "Stops with partial match on feeder direction"
        assert await stop_condition(ConductingEquipmentStep(j)), "Stops with mismatch on feeder direction"

    @pytest.mark.asyncio
    @with_simple_ns
    @with_mock_trace
    async def test_with_direction_starts_from_connected_assets_down(self, traversal, trace, simple_ns):
        await trace.run([simple_ns["b2"]], 2, FeederDirection.DOWNSTREAM)

        traversal.run_from.assert_called_once_with(simple_ns["c3"])

    @pytest.mark.asyncio
    @with_simple_ns
    @with_mock_trace
    async def test_with_direction_starts_from_connected_assets_up(self, traversal, trace, simple_ns):
        await trace.run([simple_ns["b2"]], 2, FeederDirection.UPSTREAM)

        traversal.run_from.assert_called_once_with(simple_ns["c1"])

    @pytest.mark.asyncio
    @with_mock_trace
    async def test_with_direction_starts_from_connected_assets_both(self, traversal, trace):
        ns = (await TestNetworkBuilder()
              .from_junction(num_terminals=1)  # j0
              .to_acls()  # c1
              .to_junction(num_terminals=3)  # j2
              .to_acls()  # c3
              .to_junction(num_terminals=1)  # j4
              .branch_from("j2", 2)
              .to_acls()  # c5
              .to_junction(num_terminals=1)  # j6
              .add_feeder("j0")
              .add_feeder("j6")
              .build())

        await trace.run([ns["j2"]], 2, FeederDirection.BOTH)

        assert traversal.run_from.call_count == 2
        traversal.run_from.assert_any_call(ns["c1"])
        traversal.run_from.assert_called_with(ns["c5"])

    @pytest.mark.asyncio
    @with_mock_trace
    async def test_with_direction_starts_from_connected_assets_none(self, traversal, trace):
        # We build the network halfway through to assign things to feeders before we add more network
        builder = (TestNetworkBuilder()
                   .from_junction(num_terminals=1)  # j0
                   .to_acls()  # c1
                   .to_junction()  # j2
                   .to_acls()  # c3
                   .add_feeder("j0"))  # fdr4
        ns = await builder.build()
        ns.get("j2", ConductingEquipment).add_terminal(Terminal())
        builder.branch_from("j2").to_acls()  # c5

        await trace.run([ns["j2"]], 2, FeederDirection.NONE)

        traversal.run_from.assert_called_once_with(ns["c5"])

    @pytest.mark.asyncio
    @with_simple_ns
    @with_mock_trace
    async def test_with_direction_step_action_adds_next_step_to_results(self, traversal, trace, simple_ns):
        j = Junction()
        await self._configure_run_step_actions(traversal, ConductingEquipmentStep(j, 2))

        results = await trace.run([simple_ns["j0"]], 2, FeederDirection.DOWNSTREAM)

        assert results == {
            simple_ns["j0"]: 0,
            j: 3
        }

    @pytest.mark.asyncio
    @with_mock_trace
    async def test_with_direction_results_are_filtered_by_valid_direction_both(self, traversal, trace, get_terminal_direction):
        ns = (await TestNetworkBuilder()
              .from_junction(num_terminals=1)  # j0
              .to_acls()  # c1
              .to_junction(num_terminals=1)  # j2
              .add_feeder("j0")
              .add_feeder("j2")
              .build())

        def get_feeder_direction(obj):
            if obj == ns["j0-t1"]:
                return FeederDirection.BOTH
            elif obj == ns["c1-t1"]:
                return FeederDirection.UPSTREAM
            elif obj == ns["c1-t2"]:
                return FeederDirection.NONE
            else:
                raise Exception(f"Unexpected object {obj}")

        await self._configure_run_step_actions(traversal, ConductingEquipmentStep(ns["j0"]), ConductingEquipmentStep(ns["c1"]))
        get_terminal_direction.side_effect = get_feeder_direction

        results = await trace.run([ns["j0"]], 2, FeederDirection.BOTH)

        assert results == {ns["j0"]: 0}

    @pytest.mark.asyncio
    @with_mock_trace
    async def test_with_direction_results_are_filtered_by_valid_direction_none(self, traversal, trace, get_terminal_direction):
        ns = (await TestNetworkBuilder()
              .from_junction(num_terminals=1)  # j0
              .to_acls()  # c1
              .to_junction(num_terminals=1)  # j2
              .build())

        def get_feeder_direction(obj):
            if obj == ns["j0-t1"]:
                return FeederDirection.NONE
            elif obj == ns["c1-t1"]:
                return FeederDirection.UPSTREAM
            elif obj == ns["c1-t2"]:
                return FeederDirection.BOTH
            else:
                raise Exception(f"Unexpected object {obj}")

        await self._configure_run_step_actions(traversal, ConductingEquipmentStep(ns["j0"]), ConductingEquipmentStep(ns["c1"]))
        get_terminal_direction.side_effect = get_feeder_direction

        results = await trace.run([ns["j0"]], 2, FeederDirection.NONE)

        assert results == {ns["j0"]: 0}

    @pytest.mark.asyncio
    async def test_with_direction_can_stop_on_start_item(self):
        ns = (await TestNetworkBuilder()
              .from_junction(num_terminals=1)  # j0
              .to_acls()  # c1
              .to_junction(num_terminals=1)  # j2
              .add_feeder("j0")
              .build())

        lcet = LimitedConnectedEquipmentTrace(normal_connected_equipment_trace, lambda it: it.normal_feeder_direction)
        matching_equipment = await lcet.run([ns["j0"]], 1, FeederDirection.DOWNSTREAM)
        assert matching_equipment == {
            ns["j0"]: 0,
            ns["c1"]: 1
        }

    @pytest.mark.asyncio
    @with_mock_trace
    async def test_results_only_include_minimum_steps_grouped_by_equipment(self, traversal, trace):
        j1 = Junction()
        j2 = Junction()
        await self._configure_run_step_actions(
            traversal,
            ConductingEquipmentStep(j1, 2),
            ConductingEquipmentStep(j1, 1),
            ConductingEquipmentStep(j2, 0),
            ConductingEquipmentStep(j2, 2)
        )

        results = await trace.run([MagicMock()], 2)

        assert results == {
            j1: 1,
            j2: 0
        }

    @staticmethod
    async def _configure_run_step_actions(traversal, *steps: ConductingEquipmentStep):
        # noinspection PyUnusedLocal
        # pylint: disable=unused-argument
        async def perform_step_actions(*args):
            print()
            step_action = traversal.add_step_action.call_args.args[0]
            for step in steps:
                print("stepping on" + str(step))
                await step_action(step, False)

        # pylint: enable=unused-argument

        traversal.run_from.side_effect = perform_step_actions
