#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Type, Callable, TypeVar

import pytest
from zepben.evolve.services.network.tracing.phases import phase_step

from zepben.evolve.services.network.tracing.tree.downstream_tree import DownstreamTree

from network_fixtures import phase_swap_loop_network  # noqa (fixture)
from zepben.evolve import Traversal, SetPhases, RemovePhases, AssignToFeeders, Breaker, Terminal, PhaseCode, ConductingEquipment, \
    connected_equipment_trace, SetDirection, RemoveDirection
from zepben.evolve.services.network.tracing import tracing

T = TypeVar("T")


@pytest.mark.asyncio
async def test_basic_asset_trace(phase_swap_loop_network):
    """
    Just trace all connected assets and make sure we actually visit every item.
    """
    expected = phase_swap_loop_network.objects(ConductingEquipment)
    visited = set()
    start = phase_swap_loop_network["n0"]

    async def add_to_visited(ce, _):
        visited.add(ce)

    trace = connected_equipment_trace().add_step_action(add_to_visited)
    await trace.trace(start)
    assert visited == set(expected)


def test_suppliers():
    validate_supplier(lambda: tracing.create_basic_depth_trace(lambda i, t: None), Traversal)
    validate_supplier(lambda: tracing.create_basic_breadth_trace(lambda i, t: None), Traversal)
    validate_supplier(tracing.connected_equipment_trace, Traversal)
    validate_supplier(tracing.normal_connected_equipment_trace, Traversal)
    validate_supplier(tracing.current_connected_equipment_trace, Traversal)
    validate_supplier(tracing.phase_trace, Traversal)
    validate_supplier(tracing.normal_phase_trace, Traversal)
    validate_supplier(tracing.current_phase_trace, Traversal)
    validate_supplier(tracing.normal_downstream_trace, Traversal)
    validate_supplier(tracing.current_downstream_trace, Traversal)
    validate_supplier(tracing.normal_upstream_trace, Traversal)
    validate_supplier(tracing.current_upstream_trace, Traversal)
    validate_supplier(tracing.set_phases, SetPhases)
    validate_supplier(tracing.remove_phases, RemovePhases)

    validate_supplier(tracing.set_direction, SetDirection)
    validate_supplier(tracing.remove_direction, RemoveDirection)

    validate_supplier(tracing.assign_equipment_containers_to_feeders, AssignToFeeders)
    validate_supplier(tracing.normal_downstream_tree, DownstreamTree)
    validate_supplier(tracing.normal_downstream_tree, DownstreamTree)

    # TODO
    # validate_supplier(tracing.find_with_usage_points, FindWithUsagePoints)


@pytest.mark.asyncio
async def test_downstream_trace_with_too_many_phases():
    t = Terminal()
    t.phases = PhaseCode.AB

    b1 = Breaker()
    b1.add_terminal(t)

    await tracing.normal_downstream_trace().trace(phase_step.start_at(b1, PhaseCode.ABCN))


def validate_supplier(supplier: Callable[[], T], expected_class: Type):
    assert isinstance(supplier(), expected_class)
    assert supplier() is not supplier()
