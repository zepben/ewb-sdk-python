#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Callable, Optional, Iterable, Set, List, Sized

from zepben.evolve import LifoQueue
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.services.network.tracing.feeder.associated_terminal_tracker import AssociatedTerminalTracker
from zepben.evolve.services.network.tracing.util import ignore_open, normally_open, currently_open

from zepben.evolve.services.network.tracing.traversals.tracing import Traversal

__all__ = ["new_normal_trace", "new_current_trace", "new_trace", "get_associated_terminals", "queue_next_terminal_if_closed"]


def new_trace(open_test: Callable[[ConductingEquipment, Optional[SinglePhaseKind]], bool] = ignore_open):
    return Traversal(queue_next=queue_next_terminal_if_closed(open_test), process_queue=LifoQueue(), tracker=AssociatedTerminalTracker())


def new_normal_trace() -> Traversal:
    return new_trace(normally_open)


def new_current_trace() -> Traversal:
    return new_trace(currently_open)


def get_associated_terminals(terminal: Terminal, exclude: Set[Terminal] = None) -> List[Terminal]:
    """
    Gets all associated `zepben.evolve.model.cim.iec61970.base.core.terminal.Terminal`s for `terminal`.
    Associated terminals include every other `Terminal` on `terminal`s `connectivity_node`.

    `terminal` The `zepben.evolve.model.cim.iec61970.base.core.terminal.Terminal` to use for associations.
    `exclude` A set of `Terminal`s to exclude from the result.
    Returns the list of `Terminal`s associated with `terminal`
    """
    if exclude is None:
        exclude = set()

    if terminal.connectivity_node is not None:
        return [term for term in terminal.connectivity_node.terminals if term is not terminal and term not in exclude]
    else:
        return []


def queue_next_terminal_if_closed(open_test: Callable[[ConductingEquipment, Optional[SinglePhaseKind]], bool]) -> Callable[[Terminal, Set[Terminal]], List[Terminal]]:
    """
    Creates a queue next function based on the given `open_test` that given a `zepben.evolve.model.cim.iec61970.base.core.terminal.Terminal` where all its
    `phases` are closed, will return all its associated `Terminal`s for queuing as per `get_associated_terminals`.

    `open_test` Function that tests whether a given phase on an equipment is open.
    Returns the queuing function to be used to populate a `zepben.evolve.services.network.tracing.traversals.tracing.Traversal`s `process_queue`.
    """
    def qn(terminal: Terminal, visited: Set[Terminal]) -> List[Terminal]:
        if terminal is not None:
            if terminal.conducting_equipment is not None:
                for phase in terminal.phases.single_phases:
                    # Return all associations as soon as we find a closed phase
                    if not open_test(terminal.conducting_equipment, phase):
                        assoc_terminals = []
                        for term in terminal.conducting_equipment.terminals:
                            if terminal is not term:
                                assoc_terminals.extend(get_associated_terminals(term, visited))
                        return assoc_terminals
        # Return nothing only if all phases are open.
        return []
    return qn
