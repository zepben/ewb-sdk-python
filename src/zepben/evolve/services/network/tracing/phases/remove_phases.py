#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Set, Optional, Union, FrozenSet

from zepben.evolve import connected_terminals
from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.services.network.tracing.phases.phase_status import normal_phases, current_phases
from zepben.evolve.services.network.tracing.traversals.branch_recursive_tracing import BranchRecursiveTraversal
from zepben.evolve.services.network.tracing.traversals.queue import PriorityQueue
if TYPE_CHECKING:
    from zepben.evolve import ConnectivityResult, ConductingEquipment, NetworkService
    from zepben.evolve.types import PhaseSelector
    EbbPhases = Tuple[Terminal, FrozenSet[SinglePhaseKind]]

__all__ = ["RemovePhases", "remove_all_traced_phases"]


class RemovePhases(object):
    """
    Convenience class that provides methods for removing phases on a `NetworkService`
    This class is backed by a `BranchRecursiveTraversal`.
    """

    def __init__(self):
        # The `BranchRecursiveTraversal` used when tracing the normal state of the network.
        # NOTE: If you add stop conditions to this traversal it may no longer work correctly, use at your own risk.
        # noinspection PyArgumentList
        self.normal_traversal = BranchRecursiveTraversal(queue_next=_ebb_and_queue_normal_phases,
                                                         process_queue=PriorityQueue(),
                                                         branch_queue=PriorityQueue())

        # The `BranchRecursiveTraversal` used when tracing the current state of the network.
        # NOTE: If you add stop conditions to this traversal it may no longer work correctly, use at your own risk.
        # noinspection PyArgumentList
        self.current_traversal = BranchRecursiveTraversal(queue_next=_ebb_and_queue_current_phases,
                                                          process_queue=PriorityQueue(),
                                                          branch_queue=PriorityQueue())

    async def run(self, terminal: Terminal, nominal_phases_to_ebb: Union[None, PhaseCode, FrozenSet[SinglePhaseKind]] = None):
        """
        Allows the removal of traced phases from a terminal and the connected equipment chain.
        @param terminal: The terminal from which to start the phase removal.
        @param nominal_phases_to_ebb: The nominal phases to remove traced phasing from. Defaults to all phases.
        """
        nominal_phases_to_ebb = nominal_phases_to_ebb or terminal.phases
        if isinstance(nominal_phases_to_ebb, PhaseCode):
            nominal_phases_to_ebb = frozenset(nominal_phases_to_ebb.single_phases)

        for traversal in (self.normal_traversal, self.current_traversal):
            traversal.reset()
            await traversal.run((terminal, nominal_phases_to_ebb))


def remove_all_traced_phases(network_service: NetworkService):
    for terminal in network_service.objects(Terminal):
        terminal.traced_phases.phase_status = 0


def _ebb_and_queue_normal_phases(ebb_phases: EbbPhases, traversal: BranchRecursiveTraversal[EbbPhases]):
    _ebb_and_queue(ebb_phases, traversal, normal_phases)


def _ebb_and_queue_current_phases(ebb_phases: EbbPhases, traversal: BranchRecursiveTraversal[EbbPhases]):
    _ebb_and_queue(ebb_phases, traversal, current_phases)


def _ebb_and_queue(ebb_phases: EbbPhases, traversal: BranchRecursiveTraversal[EbbPhases], phase_selector: PhaseSelector):
    terminal, nominal_phases = ebb_phases
    ebbed_phases = _ebb(terminal, nominal_phases, phase_selector)

    for cr in connected_terminals(terminal, nominal_phases):
        _queue_through_equipment(traversal, cr.to_equip, cr.to_terminal, _ebb_from_connected_terminal(ebbed_phases, cr, phase_selector))


def _ebb(terminal: Terminal, phases_to_ebb: Set[SinglePhaseKind], phase_selector: PhaseSelector) -> Set[SinglePhaseKind]:
    phases = phase_selector(terminal)
    ebbed_phases = set(filter(lambda p: phases[p] != SinglePhaseKind.NONE, phases_to_ebb))
    for phase in ebbed_phases:
        phases[phase] = SinglePhaseKind.NONE

    return phases_to_ebb


def _ebb_from_connected_terminal(phases_to_ebb: Set[SinglePhaseKind], cr: ConnectivityResult, phase_selector: PhaseSelector) -> Set[SinglePhaseKind]:
    connected_phases = set()
    for phase in phases_to_ebb:
        connected_phase = next((path.to_phase for path in cr.nominal_phase_paths if path.from_phase == phase), None)
        if connected_phase:
            connected_phases.add(connected_phase)

    return _ebb(cr.to_terminal, connected_phases, phase_selector)


def _queue_through_equipment(traversal: BranchRecursiveTraversal[EbbPhases],
                             conducting_equipment: Optional[ConductingEquipment],
                             terminal: Terminal,
                             phases_to_ebb: Set[SinglePhaseKind]):
    if conducting_equipment:
        for term in filter(lambda t: t != terminal, conducting_equipment.terminals):
            traversal.process_queue.put((term, frozenset(phases_to_ebb)))
