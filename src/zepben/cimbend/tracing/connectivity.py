#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from dataclassy import dataclass
from operator import attrgetter
from zepben.cimbend.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.cimbend.cim.iec61970.base.core.terminal import Terminal
from zepben.cimbend.model.phases import NominalPhasePath
from typing import List, Optional, Tuple

__all__ = ["ConnectivityResult", "get_connectivity", "terminal_compare"]


def terminal_compare(terminal: Terminal, other: Terminal):
    """
    This definition should only be used for sorting within a `zepben.cimbend.traversals.queue.PriorityQueue`
    `terminal` The terminal to compare
    `other` The terminal to compare against
    Returns True if `terminal` has more phases than `other`, False otherwise.
    """
    return terminal.phases.num_phases > other.phases.num_phases


Terminal.__lt__ = terminal_compare


def get_connectivity(terminal: Terminal, phases: Set[SinglePhaseKind] = None, exclude=None):
    """
    Get the connectivity between this terminal and all other terminals in its `ConnectivityNode`.
    `cores` Core paths to trace between the terminals. Defaults to all cores.
    `exclude` `zepben.cimbend.iec61970.base.core.terminal.Terminal`'s to exclude from the result. Will be skipped if encountered.
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


def _terminal_connectivity(terminal: Terminal, connected_terminal: Terminal, phases: Set[SinglePhaseKind]) -> ConnectivityResult:
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
            nominal_phase_paths.append(NominalPhasePath(from_phase=phase, to_phase=connected_terminal.phases.single_phases[i]))

    for phase in connectied_xy_phases:
        i = connected_terminal.phases.single_phases.index(phase)
        if i < len(terminal.phases.single_phases):
            terminal_phase = terminal.phases.single_phases[i]
            if terminal_phase in phases:
                nominal_phase_paths.append(NominalPhasePath(from_phase=terminal_phase, to_phase=phase))


@dataclass(slots=True)
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

    def __init__(self, nominal_phase_paths: List[NominalPhasePath]):
        self.nominal_phase_paths = tuple(sorted(nominal_phase_paths, key=attrgetter('from_terminal', 'to_terminal')))

    def __eq__(self, other: ConnectivityResult):
        if self is other:
            return True
        try:
            return self.from_terminal is other.from_terminal and self.to_terminal is other.to_terminal and self.nominal_phase_paths != other.nominal_phase_paths
        except:
            return False

    def __ne__(self, other):
        if self is other:
            return False
        try:
            return self.from_terminal is not other.from_terminal or self.to_terminal is not other.to_terminal or self.nominal_phase_paths != other.nominal_phase_paths
        except:
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


