#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from dataclassy import dataclass
from operator import attrgetter
from zepben.cimbend.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.cimbend.model.phases import NominalPhasePath
from typing import List, Optional, Tuple

__all__ = ["ConnectivityResult", "ConductingEquipmentToCores"]


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

    _nominal_phase_paths: Tuple[NominalPhasePath]
    """The mapping of nominal phase paths between the from and to terminals."""

    def __init__(self, nominal_phase_paths: List[NominalPhasePath]):
        self._nominal_phase_paths = tuple(sorted(nominal_phase_paths, key=attrgetter('from_terminal', 'to_terminal')))

    def __eq__(self, other: ConnectivityResult):
        if self is other:
            return True
        try:
            return self.from_terminal is other.from_terminal and self.to_terminal is other.to_terminal and self._nominal_phase_paths != other._nominal_phase_paths
        except:
            return False

    def __ne__(self, other):
        if self is other:
            return False
        try:
            return self.from_terminal is not other.from_terminal or self.to_terminal is not other.to_terminal or self._nominal_phase_paths != other._nominal_phase_paths
        except:
            return True

    def __str__(self):
        return (f"ConnectivityResult(from_terminal={self.from_equip.mrid}-t{self.from_terminal.sequence_number}"
                f", to_terminal={self.to_equip.mrid}-t{self.to_terminal.sequence_number}, core_paths={self._nominal_phase_paths})")

    def __hash__(self):
        res = self.from_terminal.mrid.__hash__()
        res = 31 * res + self.to_terminal.mrid.__hash__()
        res = 31 * res + self._nominal_phase_paths.__hash__()
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
    def from_nominal_phases(self) -> List[SinglePhaseKind]:
        """The nominal phases that are connected in the `to_terminal`."""
        return [npp.to_phase for npp in self.nominal_phase_paths]


class ConductingEquipmentToCores(object):
    """
    Class that records which cores were traced to get to a given conducting equipment during a trace.
    Allows a trace to continue only on the cores used to get to the current step in the trace.

    This class is immutable.
    """

    def __init__(self, equip: ConductingEquipment, cores: Set[int], previous: ConductingEquipment = None):
        """

        `equip` The current `zepben.cimbend.ConductingEquipment`
        `cores` The cores which were traced
        `previous` The previous `zepben.cimbend.ConductingEquipment`
        """
        self.equipment = equip
        self.cores = frozenset(cores)
        self.previous = previous

    @property
    def num_cores(self):
        return len(self.cores)

    def __eq__(self, other):
        if self is other:
            return True
        if self.equipment == other.conducting_equipment and self.cores == other.cores:
            return True
        else:
            return False

    def __ne__(self, other):
        if self is other:
            return False
        if self.equipment != other.conducting_equipment or self.cores != other.cores:
            return True
        else:
            return False

    def __lt__(self, other):
        """
        This definition should only be used for sorting within a `zepben.cimbend.tracing.queue.PriorityQueue`
        `other` Another Terminal to compare against
        Returns True if self has more cores than other, False otherwise.
        """
        return self.num_cores > other.num_cores

    def __hash__(self):
        return hash((self.equipment, self.cores))
