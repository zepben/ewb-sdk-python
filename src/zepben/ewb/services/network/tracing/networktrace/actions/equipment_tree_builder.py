#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ['EquipmentTreeBuilder']

import uuid
from typing import Any, Generator

from zepben.ewb.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.ewb.services.network.tracing.networktrace.actions.tree_node import TreeNode
from zepben.ewb.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.ewb.services.network.tracing.traversal.step_action import StepActionWithContextValue
from zepben.ewb.services.network.tracing.traversal.step_context import StepContext

EquipmentTreeNode = TreeNode[ConductingEquipment]


class EquipmentTreeBuilder(StepActionWithContextValue):
    """
    
    A `StepAction` that can be added to a `NetworkTrace` to build a tree structure representing the paths taken during a trace.
    The `_roots` are the start items of the trace and the children of a tree node represent the next step paths from a given step in the trace.
    
    eg:

    >>> from zepben.ewb import Tracing, NetworkStateOperators
    >>>
    >>> tree_builder = EquipmentTreeBuilder()
    >>> state_operators = NetworkStateOperators.NORMAL
    >>> (Tracing.network_trace_branching(network_state_operators=state_operators)
    >>>     .add_condition(state_operators.downstream())
    >>>     .add_step_action(tree_builder)).run()
    """

    _roots: dict[ConductingEquipment, EquipmentTreeNode] = {}
    _leaves: set[EquipmentTreeNode] = set()

    def __init__(self):
        super().__init__(key=str(uuid.uuid4()))

    @property
    def roots(self) -> Generator[TreeNode[ConductingEquipment], None, None]:
        return (r for r in self._roots.values())

    def recurse_nodes(self) -> Generator[TreeNode[ConductingEquipment], None, None]:
        """
        Returns a generator that will yield every node in the tree structure.
        """
        def recurse(node: TreeNode[ConductingEquipment]):
            yield node
            for child in node.children:
                yield from recurse(child)

        for root in self._roots.values():
            yield from recurse(root)

    @property
    def leaves(self) -> set[EquipmentTreeNode]:
        """
        Return the leaves of the tree structure. Depending on how the backing trace is configured,
        there may be extra unexpected leaves in loops.
        """
        return set(self._leaves)

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
        self._leaves.add(current_node) # add this node to _leaves as it has no children
        if current_node.parent:
            self._leaves.discard(current_node.parent) # this nodes parent now has a child, it's not a leaf anymore
            current_node.parent.add_child(current_node)

    def clear(self):
        self._roots.clear()
