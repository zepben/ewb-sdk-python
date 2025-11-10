#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["ConnectivityResult", "terminal_compare"]

from dataclasses import dataclass
from operator import attrgetter
from typing import List, Optional, Tuple, TYPE_CHECKING, Iterable


from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal
from zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

if TYPE_CHECKING:
    from zepben.ewb import NominalPhasePath


def terminal_compare(terminal: Terminal, other: Terminal):
    """
    This definition should only be used for sorting within a `PriorityQueue`
    `terminal` The terminal to compare
    `other` The terminal to compare against
    Returns True if `terminal` has more phases than `other`, False otherwise.
    """
    return terminal.phases.num_phases > other.phases.num_phases


Terminal.__lt__ = terminal_compare


@dataclass(slots=True)
class ConnectivityResult:
    """
    Stores the connectivity between two terminals, including the mapping between the nominal phases.
    This class is intended to be used in an immutable way. You should avoid modifying it after it has been created.
    """

    from_terminal: Terminal
    """The terminal from which the connectivity was requested."""

    to_terminal: Terminal
    """The terminal which is connected to the requested terminal."""

    nominal_phase_paths: Iterable[NominalPhasePath]
    """The mapping of nominal phase paths between the from and to terminals."""

    def __post_init__(self):
        self.nominal_phase_paths: Tuple[NominalPhasePath] = (
            *sorted(self.nominal_phase_paths, key=attrgetter('from_phase', 'to_phase')),)

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
    def from_equip(self) -> ConductingEquipment | None:
        """The conducting equipment that owns the `from_terminal."""
        return self.from_terminal.conducting_equipment

    @property
    def to_equip(self) -> ConductingEquipment | None:
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
