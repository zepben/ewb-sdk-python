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

    def __init__(self, calculate_leaves: bool = False):
        super().__init__(key=str(uuid.uuid4()))

        self._roots: dict[ConductingEquipment, EquipmentTreeNode] = {}
        self._leaves: set[EquipmentTreeNode] = set()

        self._calculate_leaves = calculate_leaves

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
        Return the leaves of the tree structure.
        Depending on how the backing trace is configured, there may be extra unexpected leaves in loops.
        """
        if not self._calculate_leaves:
            raise AttributeError('leaves were not calculated, you must pass calculate_leaves=True to the EquipmentTreeBuilder when creating.')
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

    def _apply(self, _: NetworkTraceStep[Any], context: StepContext):
        current_node: TreeNode = self.get_context_value(context)
        if current_node.parent:
            current_node.parent.add_child(current_node)

        if self._calculate_leaves:
            self._process_leaf(current_node)

    def _process_leaf(self, current_node: TreeNode[ConductingEquipment]):
        self._leaves.add(current_node) # add this node to _leaves as it has no children
        if current_node.parent:
            self._leaves.discard(current_node.parent) # this nodes parent now has a child, it's not a leaf anymore

    def clear(self):
        self._roots.clear()
