#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Type, Callable, TypeVar

import pytest

from zepben.evolve import BasicTraversal, SetPhases, RemovePhases, AssignToFeeders, Breaker, Terminal, PhaseCode, ConductingEquipment, \
    connected_equipment_trace, SetDirection, RemoveDirection, ConductingEquipmentStep, AssignToLvFeeders, FindSwerEquipment, NetworkService, \
    normal_connected_equipment_trace, current_connected_equipment_trace, phase_trace, normal_phase_trace, current_phase_trace, normal_downstream_trace, \
    current_downstream_trace, normal_upstream_trace, current_upstream_trace, set_phases, remove_phases, create_basic_breadth_trace, create_basic_depth_trace, \
    normal_downstream_tree, assign_equipment_to_lv_feeders, assign_equipment_to_feeders, current_downstream_tree, find_swer_equipment, \
    connected_equipment_breadth_trace, normal_limited_connected_equipment_trace, LimitedConnectedEquipmentTrace, current_limited_connected_equipment_trace, \
    remove_direction, set_direction, connectivity_trace, connectivity_breadth_trace, normal_connectivity_trace, current_connectivity_trace, phase_inferrer, \
    PhaseInferrer
from zepben.evolve.services.network.tracing.phases import phase_step
from zepben.evolve.services.network.tracing.tracing import normal_downstream_equipment_trace, current_downstream_equipment_trace, \
    normal_upstream_equipment_trace, current_upstream_equipment_trace
from zepben.evolve.services.network.tracing.tree.downstream_tree import DownstreamTree

T = TypeVar("T")


@pytest.mark.asyncio
@pytest.mark.parametrize('phase_swap_loop_network', [(False,)], indirect=True)
async def test_basic_asset_trace(phase_swap_loop_network: NetworkService):
    """
    Just trace all connected assets and make sure we actually visit every item.
    """
    expected = phase_swap_loop_network.objects(ConductingEquipment)
    visited = set()
    start = phase_swap_loop_network["n0"]

    async def add_to_visited(step: ConductingEquipmentStep, _: bool):
        visited.add(step.conducting_equipment)

    trace = connected_equipment_trace()
    trace.add_step_action(add_to_visited)

    await trace.run_from(start)
    assert visited == set(expected)


def test_suppliers():
    _validate_supplier(lambda: create_basic_depth_trace(lambda i, t: None), BasicTraversal)
    _validate_supplier(lambda: create_basic_breadth_trace(lambda i, t: None), BasicTraversal)

    _validate_supplier(connected_equipment_trace, BasicTraversal)
    _validate_supplier(connected_equipment_breadth_trace, BasicTraversal)
    _validate_supplier(normal_connected_equipment_trace, BasicTraversal)
    _validate_supplier(current_connected_equipment_trace, BasicTraversal)

    _validate_supplier(normal_limited_connected_equipment_trace, LimitedConnectedEquipmentTrace)
    _validate_supplier(current_limited_connected_equipment_trace, LimitedConnectedEquipmentTrace)

    _validate_supplier(normal_downstream_equipment_trace, BasicTraversal)
    _validate_supplier(current_downstream_equipment_trace, BasicTraversal)
    _validate_supplier(normal_upstream_equipment_trace, BasicTraversal)
    _validate_supplier(current_upstream_equipment_trace, BasicTraversal)

    _validate_supplier(connectivity_trace, BasicTraversal)
    _validate_supplier(connectivity_breadth_trace, BasicTraversal)
    _validate_supplier(normal_connectivity_trace, BasicTraversal)
    _validate_supplier(current_connectivity_trace, BasicTraversal)

    _validate_supplier(phase_trace, BasicTraversal)
    _validate_supplier(normal_phase_trace, BasicTraversal)
    _validate_supplier(current_phase_trace, BasicTraversal)

    _validate_supplier(normal_downstream_trace, BasicTraversal)
    _validate_supplier(current_downstream_trace, BasicTraversal)
    _validate_supplier(normal_upstream_trace, BasicTraversal)
    _validate_supplier(current_upstream_trace, BasicTraversal)

    _validate_supplier(normal_downstream_tree, DownstreamTree)
    _validate_supplier(current_downstream_tree, DownstreamTree)

    _validate_supplier(set_phases, SetPhases)
    _validate_supplier(remove_phases, RemovePhases)

    _validate_supplier(set_direction, SetDirection)
    _validate_supplier(remove_direction, RemoveDirection)

    _validate_supplier(phase_inferrer, PhaseInferrer)

    _validate_supplier(assign_equipment_to_feeders, AssignToFeeders)
    _validate_supplier(assign_equipment_to_lv_feeders, AssignToLvFeeders)

    # TODO: EWB-2596
    # _validate_supplier(find_with_usage_points, FindWithUsagePoints)
    _validate_supplier(find_swer_equipment, FindSwerEquipment)


@pytest.mark.asyncio
async def test_downstream_trace_with_too_many_phases():
    t = Terminal()
    t.phases = PhaseCode.AB

    b1 = Breaker()
    b1.add_terminal(t)

    await normal_downstream_trace().run(phase_step.start_at(b1, PhaseCode.ABCN))


def _validate_supplier(supplier: Callable[[], T], expected_class: Type):
    assert isinstance(supplier(), expected_class)
    assert supplier() is not supplier()
