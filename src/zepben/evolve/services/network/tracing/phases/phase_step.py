#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from zepben.evolve import PhaseCode
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

from typing import FrozenSet, Optional, Union, Iterable
from dataclassy import dataclass

__all__ = ["PhaseStep"]


@dataclass(slots=True)
class PhaseStep(object):
    """
    Class that records which phases were traced to get to a given conducting equipment during a trace.
    Allows a trace to continue only on the phases used to get to the current step in the trace.

    This class is immutable.
    """
    conducting_equipment: ConductingEquipment
    """The current `zepben.evolve.cim.iec61970.base.core.conducting_equipment.ConductingEquipment`"""

    phases: FrozenSet[SinglePhaseKind]
    """The phases which were traced"""

    previous: Optional[ConductingEquipment] = None
    """`previous` The previous `zepben.evolve.cim.iec61970.base.core.conducting_equipment.ConductingEquipment`"""

    def __eq__(self, other):
        if self is other:
            return True
        return self.conducting_equipment is other.conducting_equipment and self.phases == other.phases

    def __ne__(self, other):
        if self is other:
            return False
        return self.equipment is not other.conducting_equipment or self.phases != other.phases

    def __lt__(self, other):
        """
        This definition should only be used for sorting within a `PriorityQueue`
        `other` Another PhaseStep to compare against
        Returns True if self has more phases than other, False otherwise.
        """
        return len(self.phases) > len(other.phases)

    def __hash__(self):
        return hash((self.conducting_equipment, self.phases))


def start_at(conducting_equipment: ConductingEquipment, phases: Union[PhaseCode, Iterable[SinglePhaseKind]]):
    if isinstance(phases, PhaseCode):
        phases = phases.single_phases

    return PhaseStep(conducting_equipment, frozenset(phases), None)


def continue_at(conducting_equipment: ConductingEquipment, phases: Union[PhaseCode, Iterable[SinglePhaseKind]], previous: Optional[ConductingEquipment]):
    if isinstance(phases, PhaseCode):
        phases = phases.single_phases

    return PhaseStep(conducting_equipment, frozenset(phases), previous)
