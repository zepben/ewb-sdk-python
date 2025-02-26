#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import weakref
from typing import List, Self

from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import  ConductingEquipment
from zepben.evolve.services.network.tracing.networktrace.actions.tree_node import TreeNode
from zepben.evolve.services.network.tracing.traversal.step_action import StepAction


class EquipmentTreeNode(StepAction):
    """
    represents a node representing `Conducting Equipment` in the NetworkTrace tree
    """
    def __init__(self, identified_object: ConductingEquipment, parent: Self = None):
        super().__init__(identified_object, parent)


class EquipmentTreeBuilder:
    def __init__(self, step_action_with_context_value: NetworkTraceStep):