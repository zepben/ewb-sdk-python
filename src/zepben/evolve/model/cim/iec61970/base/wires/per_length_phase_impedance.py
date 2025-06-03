#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Optional, List, Generator

from zepben.evolve.util import require, ngen, nlen, safe_remove, none
from zepben.evolve.model.cim.iec61970.base.wires.per_length import PerLengthImpedance
from zepben.evolve.model.cim.iec61970.base.wires.phase_impedance_data import PhaseImpedanceData
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

__all__ = ["PerLengthPhaseImpedance"]


class PerLengthPhaseImpedance(PerLengthImpedance):
    """
    Impedance and admittance parameters per unit length for n-wire unbalanced lines, in matrix form.
    """

    _data: Optional[List[PhaseImpedanceData]] = None

    def __init__(self, data: List[PhaseImpedanceData] = None, **kwargs):
        """
        `data` A list of `PhaseImpedanceData`s to associate with this `PerLengthPhaseImpedance`.
        """
        super(PerLengthPhaseImpedance, self).__init__(**kwargs)
        if data:
            for phase_data in data:
                self.add_data(phase_data)

    @property
    def data(self) -> Generator[PhaseImpedanceData, None, None]:
        """
        The point data values that define this phase_impedance, sorted by `x_value` in ascending order.
        """
        return ngen(self._data)

    @property
    def diagonal(self) -> Generator[PhaseImpedanceData, None, None]:
        """
        Get only the diagonal elements of the matrix, i.e toPhase == fromPhase.
        """
        return ngen(pid for pid in self._data if pid.from_phase == pid.to_phase)

    def num_data(self):
        """Return the number of :class:`PhaseImpedanceData` associated with this :class:`PerLengthPhaseImpedance`."""
        return nlen(self._data)

    def get_data(self, from_phase: SinglePhaseKind, to_phase: SinglePhaseKind) -> PhaseImpedanceData:
        """
        Get the matrix entry for the corresponding to and from phases.

        :param from_phase: The from_phase to lookup.
        :param to_phase: The to_phase to lookup.
        :returns: The :class:`PhaseImpedanceData` with the specified `from_phase` and `to_phase` if it exists.
        :raises KeyError: When no `PhaseImpedanceData` was found with a matching `from_phase` and `to_phase`.
        """
        if self._data:
            phase_impedance_data = next((it for it in self._data if it.from_phase == from_phase and it.to_phase == to_phase), None)
            if phase_impedance_data:
                return phase_impedance_data
        raise KeyError((from_phase, to_phase))

    def add_data(self, phase_impedance_data: PhaseImpedanceData) -> "PerLengthPhaseImpedance":
        """
        Add a :class:`PhaseImpedanceData` to this :class:`PerLengthPhaseImpedance`.

        :param phase_impedance_data: The :class:`PhaseImpedanceData` to add.
        :returns: A reference to this :class:`PerLengthPhaseImpedance` to allow fluent use.
        :raises ValueError: If another :class:`PhaseImpedanceData` with the same `from_phase` and `to_phase` already exists for this :class:`PerLengthPhaseImpedance`.
        """

        require(none([it.from_phase == phase_impedance_data.from_phase and it.to_phase == phase_impedance_data.to_phase for it in self.data]),
                lambda: f"""Unable to add PhaseImpedanceData to {self}. A PhaseImpedanceData with from_phase {phase_impedance_data.from_phase} and to_phase {phase_impedance_data.to_phase} already exists in this PerLengthPhaseImpedance.""")

        self._data = self._data or []
        self._data.append(phase_impedance_data)

        return self

    def remove_data(self, phase_impedance_data: PhaseImpedanceData) -> "PerLengthPhaseImpedance":
        """
        Remove a :class:`PhaseImpedanceData` from this :class:`PerLengthPhaseImpedance`.

        :param phase_impedance_data: The :class:`PhaseImpedanceData` to remove from this :class:`PerLengthPhaseImpedance`.
        :returns: A reference to this :class:`PerLengthPhaseImpedance` to allow fluent use.
        :raises ValueError: If `phase_impedance_data` was not associated with this :class:`PerLengthPhaseImpedance`.
        """
        self._data = safe_remove(self._data, phase_impedance_data)
        return self

    def clear_data(self) -> "PerLengthPhaseImpedance":
        """
        Clear all :class:`PhaseImpedanceData` associated with this :class:`PerLengthPhaseImpedance`.
        :returns: A reference to this :class:`PerLengthPhaseImpedance` to allow fluent use.
        """
        self._data = None
        return self
