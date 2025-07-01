#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import uuid
from typing import Any, Generator

from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.services.network.tracing.networktrace.actions.tree_node import TreeNode
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.traversal.step_action import StepActionWithContextValue
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext

EquipmentTreeNode = TreeNode[ConductingEquipment]

__all__ = ['EquipmentTreeBuilder']


class EquipmentTreeBuilder(StepActionWithContextValue):
    """
    
    A `StepAction` that can be added to a `NetworkTrace` to build a tree structure representing the paths taken during a trace.
    The `_roots` are the start items of the trace and the children of a tree node represent the next step paths from a given step in the trace.
    
    eg:

    >>> from zepben.evolve import Tracing, NetworkStateOperators
    >>>
    >>> tree_builder = EquipmentTreeBuilder()
    >>> state_operators = NetworkStateOperators.NORMAL
    >>> (Tracing.network_trace_branching(network_state_operators=state_operators)
    >>>     .add_condition(state_operators.downstream())
    >>>     .add_step_action(tree_builder)).run()
    """

    _roots: dict[ConductingEquipment, EquipmentTreeNode] = {}

    def __init__(self):
        super().__init__(key=str(uuid.uuid4()))

    @property
    def roots(self) -> Generator[TreeNode[ConductingEquipment], None, None]:
        return (r for r in self._roots.values())

    def compute_initial_value(self, item: NetworkTraceStep[Any]) -> EquipmentTreeNode:
        node = self._roots.get(item.path.to_equipment)
        if node is None:
            node = TreeNode(item.path.to_equipment, None)
            self._roots[item.path.to_equipment] = node
        return node

    def compute_next_value(
        self,
        next_item: NetworkTraceStep[Any],
        current_item: NetworkTraceStep[Any],
        current_value: EquipmentTreeNode
    ) -> EquipmentTreeNode:

        if next_item.path.traced_internally:
            return current_value
        else:
            return TreeNode(next_item.path.to_equipment, current_value)

    def _apply(self, item: NetworkTraceStep[Any], context: StepContext):
        current_node: TreeNode = self.get_context_value(context)
        if current_node.parent:
            current_node.parent.add_child(current_node)

    def clear(self):
        self._roots.clear()
