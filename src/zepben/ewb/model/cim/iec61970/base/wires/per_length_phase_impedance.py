#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["PerLengthPhaseImpedance"]

from typing import List, Generator

from typing_extensions import deprecated

from zepben.ewb.dataslot import dataslot, ListAccessor, custom_add, ListRouter
from zepben.ewb.model.cim.iec61970.base.wires.per_length_impedance import PerLengthImpedance
from zepben.ewb.model.cim.iec61970.base.wires.phase_impedance_data import PhaseImpedanceData
from zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.ewb.util import require, ngen, none


@dataslot
class PerLengthPhaseImpedance(PerLengthImpedance):
    """
    Impedance and admittance parameters per unit length for n-wire unbalanced lines, in matrix form.
    """

    data: List[PhaseImpedanceData] | None = ListAccessor()

    def _retype(self):
        self.data: ListRouter[PhaseImpedanceData] = ...
    
    @property
    def diagonal(self) -> Generator[PhaseImpedanceData, None, None]:
        """
        Get only the diagonal elements of the matrix, i.e toPhase == fromPhase.
        """
        return ngen(pid for pid in self.data if pid.from_phase == pid.to_phase)

    @deprecated("BOILERPLATE: Use len(data) instead")
    def num_data(self):
        return len(self.data)

    def get_data(self, from_phase: SinglePhaseKind, to_phase: SinglePhaseKind) -> PhaseImpedanceData:
        """
        Get the matrix entry for the corresponding to and from phases.

        :param from_phase: The from_phase to lookup.
        :param to_phase: The to_phase to lookup.
        :returns: The :class:`PhaseImpedanceData` with the specified `from_phase` and `to_phase` if it exists.
        :raises KeyError: When no `PhaseImpedanceData` was found with a matching `from_phase` and `to_phase`.
        """
        if self.data:
            phase_impedance_data = next((it for it in self.data if it.from_phase == from_phase and it.to_phase == to_phase), None)
            if phase_impedance_data:
                return phase_impedance_data
        raise KeyError((from_phase, to_phase))

    @custom_add(data)
    def add_data(self, phase_impedance_data: PhaseImpedanceData) -> 'PerLengthPhaseImpedance':
        """
        Add a :class:`PhaseImpedanceData` to this :class:`PerLengthPhaseImpedance`.

        :param phase_impedance_data: The :class:`PhaseImpedanceData` to add.
        :returns: A reference to this :class:`PerLengthPhaseImpedance` to allow fluent use.
        :raises ValueError: If another :class:`PhaseImpedanceData` with the same `from_phase` and `to_phase` already exists for this :class:`PerLengthPhaseImpedance`.
        """

        require(none([it.from_phase == phase_impedance_data.from_phase and it.to_phase == phase_impedance_data.to_phase for it in self.data]),
                lambda: f"""Unable to add PhaseImpedanceData to {self}. A PhaseImpedanceData with from_phase {phase_impedance_data.from_phase} and to_phase {phase_impedance_data.to_phase} already exists in this PerLengthPhaseImpedance.""")

        self.data.append_unchecked(phase_impedance_data)

        return self

    @deprecated("Boilerplate: Use data.remove(phase_impedance_data) instead")
    def remove_data(self, phase_impedance_data: PhaseImpedanceData) -> 'PerLengthPhaseImpedance':
        self.data.remove(phase_impedance_data)
        return self

    @deprecated("BOILERPLATE: Use data.clear() instead")
    def clear_data(self) -> 'PerLengthPhaseImpedance':
        self.data.clear()
        return self

