#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from operator import attrgetter
from typing import List, Optional, Tuple, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import SinglePhaseKind

from dataclassy import dataclass

from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.phases import NominalPhasePath

__all__ = ["ConnectivityResult", "get_connectivity", "terminal_compare", "get_connected_equipment"]


def terminal_compare(terminal: Terminal, other: Terminal):
    """
    This definition should only be used for sorting within a `zepben.evolve.traversals.queue.PriorityQueue`
    `terminal` The terminal to compare
    `other` The terminal to compare against
    Returns True if `terminal` has more phases than `other`, False otherwise.
    """
    return terminal.phases.num_phases > other.phases.num_phases


Terminal.__lt__ = terminal_compare


def get_connectivity(terminal: Terminal, phases: Set[SinglePhaseKind] = None, exclude=None) -> List[ConnectivityResult]:
    """
    Get the connectivity between this terminal and all other terminals in its `ConnectivityNode`.
    `cores` Core paths to trace between the terminals. Defaults to all cores.
    `exclude` `zepben.evolve.iec61970.base.core.terminal.Terminal`'s to exclude from the result. Will be skipped if encountered.
    Returns List of `ConnectivityResult`'s for this terminal.
    """
    if exclude is None:
        exclude = set()
    if phases is None:
        phases = terminal.phases.single_phases
    trace_phases = phases.intersection(terminal.phases.single_phases)
    cn = terminal.connectivity_node if terminal.connectivity_node else []
    results = []
    for term in cn:
        if terminal is not term and term not in exclude:  # Don't include ourselves, or those specifically excluded.
            cr = _terminal_connectivity(terminal, term, trace_phases)
            if cr.nominal_phase_paths:
                results.append(cr)
    return results


Terminal.connected_terminals = get_connectivity


def get_connected_equipment(cond_equip, exclude: Set = None):
    """
    Get all `ConductingEquipment` connected to this piece of equipment. An `Equipment` is connected if it has
    a `zepben.evolve.iec61970.base.core.terminal.Terminal` associated with a `ConnectivityNode` that this `ConductingEquipment` is also associated with.

    `exclude` Equipment to exclude from return.
    Returns A list of `ConductingEquipment` that are connected to this.
    """
    if exclude is None:
        exclude = []
    connected_equip = []
    for terminal in cond_equip.terminals:
        conn_node = terminal.connectivity_node
        for term in conn_node:
            if term.conducting_equipment in exclude:
                continue
            if term != terminal:  # Don't include ourselves.
                connected_equip.append(term.conducting_equipment)
    return connected_equip


ConductingEquipment.connected_equipment = get_connected_equipment


def _terminal_connectivity(terminal: Terminal, connected_terminal: Terminal, phases: Set[SinglePhaseKind]) -> ConnectivityResult:
    # noinspection PyArgumentList
    nominal_phase_paths = [NominalPhasePath(phase, phase) for phase in phases if phase in connected_terminal.phases.single_phases]

    if not nominal_phase_paths:
        xy_phases = {phase for phase in phases if phase == SinglePhaseKind.X or phase == SinglePhaseKind.Y}
        connected_xy_phases = {phase for phase in connected_terminal.phases.single_phases if phase == SinglePhaseKind.X or phase == SinglePhaseKind.Y}

        _process_xy_phases(terminal, connected_terminal, phases, xy_phases, connected_xy_phases, nominal_phase_paths)

    return ConnectivityResult(from_terminal=terminal, to_terminal=connected_terminal, nominal_phase_paths=nominal_phase_paths)


def _process_xy_phases(terminal: Terminal, connected_terminal: Terminal, phases: Set[SinglePhaseKind], xy_phases: Set[SinglePhaseKind],
                       connectied_xy_phases: Set[SinglePhaseKind], nominal_phase_paths: List[NominalPhasePath]):
    if (not xy_phases and not connectied_xy_phases) or (xy_phases and connectied_xy_phases):
        return
    for phase in xy_phases:
        i = terminal.phases.single_phases.index(phase)
        if i < len(connected_terminal.phases.single_phases):
            # noinspection PyArgumentList
            nominal_phase_paths.append(NominalPhasePath(from_phase=phase, to_phase=connected_terminal.phases.single_phases[i]))

    for phase in connectied_xy_phases:
        i = connected_terminal.phases.single_phases.index(phase)
        if i < len(terminal.phases.single_phases):
            terminal_phase = terminal.phases.single_phases[i]
            if terminal_phase in phases:
                # noinspection PyArgumentList
                nominal_phase_paths.append(NominalPhasePath(from_phase=terminal_phase, to_phase=phase))


@dataclass(slots=True, init=False)
class ConnectivityResult(object):
    """
    Stores the connectivity between two terminals, including the mapping between the nominal phases.
    This class is intended to be used in an immutable way. You should avoid modifying it after it has been created.
    """

    from_terminal: Terminal
    """The terminal from which the connectivity was requested."""

    to_terminal: Terminal
    """The terminal which is connected to the requested terminal."""

    nominal_phase_paths: Tuple[NominalPhasePath]
    """The mapping of nominal phase paths between the from and to terminals."""

    def __init__(self, from_terminal: Terminal, to_terminal: Terminal, nominal_phase_paths: List[NominalPhasePath]):
        self.nominal_phase_paths = tuple(sorted(nominal_phase_paths, key=attrgetter('from_phase', 'to_phase')))
        self.from_terminal = from_terminal
        self.to_terminal = to_terminal

    def __eq__(self, other: ConnectivityResult):
        if self is other:
            return True
        # noinspection PyBroadException
        try:
            return self.from_terminal is other.from_terminal and self.to_terminal is other.to_terminal and self.nominal_phase_paths != other.nominal_phase_paths
        except Exception:
            return False

    def __ne__(self, other):
        if self is other:
            return False
        # noinspection PyBroadException
        try:
            return self.from_terminal is not other.from_terminal \
                   or self.to_terminal is not other.to_terminal \
                   or self.nominal_phase_paths != other.nominal_phase_paths
        except Exception:
            return True

    def __str__(self):
        return (f"ConnectivityResult(from_terminal={self.from_equip.mrid}-t{self.from_terminal.sequence_number}"
                f", to_terminal={self.to_equip.mrid}-t{self.to_terminal.sequence_number}, core_paths={self.nominal_phase_paths})")

    def __hash__(self):
        res = self.from_terminal.mrid.__hash__()
        res = 31 * res + self.to_terminal.mrid.__hash__()
        res = 31 * res + self.nominal_phase_paths.__hash__()
        return res

    @property
    def from_equip(self) -> Optional[ConductingEquipment]:
        """The conducting equipment that owns the `from_terminal."""
        return self.from_terminal.conducting_equipment

    @property
    def to_equip(self) -> Optional[ConductingEquipment]:
        """The conducting equipment that owns the `to_terminal`."""
        return self.to_terminal.conducting_equipment

    @property
    def from_nominal_phases(self) -> List[SinglePhaseKind]:
        """The nominal phases that are connected in the `from_terminal`."""
        return [npp.from_phase for npp in self.nominal_phase_paths]

    @property
    def to_nominal_phases(self) -> List[SinglePhaseKind]:
        """The nominal phases that are connected in the `to_terminal`."""
        return [npp.to_phase for npp in self.nominal_phase_paths]
