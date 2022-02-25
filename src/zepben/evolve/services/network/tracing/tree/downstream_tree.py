#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List, Set

from zepben.evolve.services.network.network_service import connected_terminals
from zepben.evolve.exceptions import TracingException
from zepben.evolve.services.network.tracing.feeder.feeder_direction import FeederDirection
from zepben.evolve.services.network.tracing.traversals.queue import PriorityQueue
from zepben.evolve.services.network.tracing.traversals.branch_recursive_tracing import BranchRecursiveTraversal
if TYPE_CHECKING:
    from zepben.evolve import ConductingEquipment, Terminal, SinglePhaseKind
    from zepben.evolve.types import OpenTest, DirectionSelector

__all__ = ["DownstreamTree"]


def _queue_connected_terminals(traversal: BranchRecursiveTraversal[TreeNode],
                               current: TreeNode,
                               down_terminal: Terminal,
                               down_phases: Set[SinglePhaseKind]):
    # Get all the terminals connected to terminals with phases going out
    up_terminals = connected_terminals(down_terminal, down_phases)

    # Make sure we do not loop back out the incoming terminal if its direction is both.
    if current.parent and any(term.to_equip == current.parent.conducting_equipment for term in up_terminals):
        return

    fork = len(up_terminals) > 1 or down_terminal.conducting_equipment.num_terminals() > 2
    for equip in (term.to_equip for term in up_terminals if term.to_equip):
        next_node = TreeNode(equip, current)

        if not traversal.has_visited(next_node):
            current.add_child(next_node)
            if fork:
                branch = traversal.create_branch()
                branch.start_item = next_node
                traversal.branch_queue.put(branch)
            else:
                traversal.process_queue.put(next_node)


class DownstreamTree(object):

    def __init__(self, open_test: OpenTest, direction_selector: DirectionSelector):
        self._open_test = open_test
        self._direction_selector = direction_selector

        # noinspection PyArgumentList
        self._traversal = BranchRecursiveTraversal(queue_next=self._add_and_queue_next,
                                                   process_queue=PriorityQueue(),
                                                   branch_queue=PriorityQueue())

    def _add_and_queue_next(self, current: Optional[TreeNode], traversal: BranchRecursiveTraversal[TreeNode]):
        # Loop through each of the terminals on the current conducting equipment
        if current is None:
            return

        for term in current.conducting_equipment.terminals:
            # Find all the nominal phases which are going out
            down_phases = self._get_down_phases(term)
            if down_phases:
                _queue_connected_terminals(traversal, current, term, down_phases)

    def _get_down_phases(self, terminal: Terminal) -> Set[SinglePhaseKind]:
        direction = self._direction_selector(terminal).value()
        if not direction.has(FeederDirection.DOWNSTREAM):
            return set()

        conducting_equipment = terminal.conducting_equipment
        if conducting_equipment is None:
            raise TracingException(f"Missing conducting equipment for terminal {terminal.mrid}.")

        return set(filter(lambda phase: not self._open_test(conducting_equipment, phase), terminal.phases.single_phases))


class TreeNode(object):

    def __init__(self, conducting_equipment: ConductingEquipment, parent: Optional[TreeNode]):
        self.conducting_equipment = conducting_equipment
        self.parent = parent
        self._children: List[TreeNode] = []
        self._sort_weight = max((len(term.phases.single_phases) for term in conducting_equipment.terminals), default=1)

    def __lt__(self, other: TreeNode):
        """
        This definition should only be used for sorting within a `zepben.evolve.tracing.queue.PriorityQueue`

        @param other: Another PhaseStep to compare against
        @return: True if this node's max phase count over its equipment's terminals is greater than the other's, False otherwise.
        """
        return self._sort_weight > other._sort_weight

    def __str__(self):
        return f"{{conducting_equipment: {self.conducting_equipment.mrid}, parent: {self.parent and self.parent.conducting_equipment.mrid}, " \
               f"num children: {len(self._children)}}}"

    def add_child(self, child: TreeNode):
        self._children.append(child)
