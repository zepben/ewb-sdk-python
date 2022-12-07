#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Callable, Optional, Set, List

from zepben.evolve import BasicTraversal
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.services.network.tracing.feeder.associated_terminal_tracker import AssociatedTerminalTracker
from zepben.evolve.services.network.tracing.util import ignore_open, normally_open, currently_open

__all__ = ["new_normal_trace", "new_current_trace", "new_trace", "get_associated_terminals", "queue_next_terminal_if_closed"]


def new_trace(open_test: Callable[[ConductingEquipment, Optional[SinglePhaseKind]], bool] = ignore_open) -> BasicTraversal[Terminal]:
    # noinspection PyArgumentList
    return BasicTraversal(queue_next=queue_next_terminal_if_closed(open_test), tracker=AssociatedTerminalTracker())


def new_normal_trace() -> BasicTraversal[Terminal]:
    return new_trace(normally_open)


def new_current_trace() -> BasicTraversal[Terminal]:
    return new_trace(currently_open)


def get_associated_terminals(terminal: Terminal, exclude: Set[Terminal] = None) -> List[Terminal]:
    """
    Gets all associated `Terminal`s for `terminal`.
    Associated terminals include every other `Terminal` on `terminal`s `connectivity_node`.

    `terminal` The `Terminal` to use for associations.
    `exclude` A set of `Terminal`s to exclude from the result.
    Returns the list of `Terminal`s associated with `terminal`
    """
    if exclude is None:
        exclude = set()

    if terminal.connectivity_node is not None:
        return [term for term in terminal.connectivity_node.terminals if term is not terminal and term not in exclude]
    else:
        return []


def queue_next_terminal_if_closed(
    open_test: Callable[[ConductingEquipment, Optional[SinglePhaseKind]], bool]
) -> Callable[[Terminal, BasicTraversal[Terminal]], None]:
    """
    Creates a queue next function based on the given `open_test` that given a `Terminal` where all its
    `phases` are closed, will return all its associated `Terminal`s for queuing as per `get_associated_terminals`.

    `open_test` Function that tests whether a given phase on an equipment is open.
    Returns the queuing function to be used to populate a `Traversal`s `process_queue`.
    """

    def queue_next(terminal: Terminal, traversal: BasicTraversal[Terminal]):
        if terminal is not None:
            if terminal.conducting_equipment is not None:
                # Stop only if all phases are open.
                if any(not open_test(terminal.conducting_equipment, phase) for phase in terminal.phases.single_phases):
                    for term in terminal.conducting_equipment.terminals:
                        if terminal is not term:
                            traversal.process_queue.extend(get_associated_terminals(term))

    return queue_next
