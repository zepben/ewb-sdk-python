#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from operator import attrgetter
from typing import List, Optional, Tuple, TYPE_CHECKING, Iterable

from dataclassy import dataclass

from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.model.phases import NominalPhasePath

if TYPE_CHECKING:
    pass

__all__ = ["ConnectivityResult", "terminal_compare"]


def terminal_compare(terminal: Terminal, other: Terminal):
    """
    This definition should only be used for sorting within a `PriorityQueue`
    `terminal` The terminal to compare
    `other` The terminal to compare against
    Returns True if `terminal` has more phases than `other`, False otherwise.
    """
    return terminal.phases.num_phases > other.phases.num_phases


Terminal.__lt__ = terminal_compare


@dataclass(slots=True, init=False)
class ConnectivityResult:
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

    def __init__(self, from_terminal: Terminal, to_terminal: Terminal, nominal_phase_paths: Iterable[NominalPhasePath]):
        self.nominal_phase_paths = tuple(sorted(nominal_phase_paths, key=attrgetter('from_phase', 'to_phase')))
        self.from_terminal = from_terminal
        self.to_terminal = to_terminal

    def __eq__(self, other: ConnectivityResult):
        if self is other:
            return True

        # noinspection PyBroadException
        try:
            return self.from_terminal is other.from_terminal and self.to_terminal is other.to_terminal and self.nominal_phase_paths == other.nominal_phase_paths
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
