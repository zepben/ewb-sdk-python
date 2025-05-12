#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import weakref
from random import random
from typing import List, Self
import uuid

from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import  ConductingEquipment
from zepben.evolve.services.network.tracing.networktrace.actions.tree_node import TreeNode
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.traversal.step_action import StepActionWithContextValue
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext

EquipmentTreeNode = TreeNode[ConductingEquipment]


class EquipmentTreeBuilder(StepActionWithContextValue):
    _roots: dict[ConductingEquipment, EquipmentTreeNode]={}

    def __init__(self):
        self.key = str(uuid.uuid4())

    @property
    def roots(self):
        return self._roots.values()

    def compute_initial_value(self, item: NetworkTraceStep[...]) -> EquipmentTreeNode:
        node = self._roots.get(item.path.to_equipment)
        if node is None:
            node = TreeNode(item.path.to_equipment, None)
            self._roots[item.path.to_equipment] = node
        return node

    def compute_next_value_typed(self, next_item: NetworkTraceStep[...], current_item: NetworkTraceStep[...], current_value: EquipmentTreeNode) -> EquipmentTreeNode:
        if next_item.path.traced_internally:
            return current_value
        else:
            return TreeNode(next_item.path.to_equipment, current_value)

    def apply(self, item: NetworkTraceStep[...], context: StepContext):
        current_node: TreeNode = self.get_context_value(context)
        if current_node.parent:
            current_node.parent.add_child(current_node)

    def clear(self):
        self._roots.clear()