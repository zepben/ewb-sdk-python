#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["PerLengthPhaseImpedance"]

from dataclasses import field
from typing import List, Generator

from typing_extensions import deprecated

from zepben.ewb import zb_dataclass
from zepben.ewb.boilerplate.collections.lazy_list import LazyValidatedList
from zepben.ewb.model.cim.iec61970.base.wires.per_length_impedance import PerLengthImpedance
from zepben.ewb.model.cim.iec61970.base.wires.phase_impedance_data import PhaseImpedanceData
from zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.ewb.util import require, none


class PhaseImpedanceDataList(LazyValidatedList):
    def get(self, from_phase: SinglePhaseKind, to_phase: SinglePhaseKind) -> PhaseImpedanceData:
        """
        Get the matrix entry for the corresponding to and from phases.

        :param from_phase: The from_phase to lookup.
        :param to_phase: The to_phase to lookup.
        :returns: The :class:`PhaseImpedanceData` with the specified `from_phase` and `to_phase` if it exists.
        :raises KeyError: When no `PhaseImpedanceData` was found with a matching `from_phase` and `to_phase`.
        """
        phase_impedance_data = next((it for it in self if it.from_phase == from_phase and it.to_phase == to_phase), None)
        if phase_impedance_data:
            return phase_impedance_data

        raise KeyError((from_phase, to_phase))

    @property
    def diagonal(self):
        """
        Get only the diagonal elements of the matrix, i.e toPhase == fromPhase.
        """
        return (pid for pid in self if pid.from_phase == pid.to_phase)


@zb_dataclass
class PerLengthPhaseImpedance(PerLengthImpedance):
    """
    Impedance and admittance parameters per unit length for n-wire unbalanced lines, in matrix form.
    """

    _data: List[PhaseImpedanceData] | None = field(default=None)

    data: PhaseImpedanceDataList[PhaseImpedanceData] = PhaseImpedanceDataList(
        _data,
        validate=lambda self, it: self._validate_data(it)
    )

    def _validate_data(self, phase_impedance_data: PhaseImpedanceData):
        require(none([it.from_phase == phase_impedance_data.from_phase and it.to_phase == phase_impedance_data.to_phase for it in self.data]),
                lambda: f"""Unable to add PhaseImpedanceData to {self}. A PhaseImpedanceData with from_phase {phase_impedance_data.from_phase} and to_phase {phase_impedance_data.to_phase} already exists in this PerLengthPhaseImpedance.""")


    # region deprecated list boilerplate
    # region data boilerplate

    @property
    @deprecated("Use data.diagonal instead")
    def diagonal(self) -> Generator[PhaseImpedanceData, None, None]:
        return self.data.diagonal

    @deprecated("Use len(data) instead.")
    def num_data(self):
        return len(self.data)

    @deprecated("Use data.get(from_phase, to_phase) instead.")
    def get_data(self, from_phase: SinglePhaseKind, to_phase: SinglePhaseKind) -> PhaseImpedanceData:
        return self.data.get(from_phase, to_phase)

    @deprecated("Use data.append(phase_impedance_data) instead.")
    def add_data(self, phase_impedance_data: 'PhaseImpedanceData') -> PerLengthPhaseImpedance:
        self.data.append(phase_impedance_data)
        return self

    @deprecated("Use data.remove(phase_impedance_data) instead.")
    def remove_data(self, phase_impedance_data: 'PhaseImpedanceData') -> PerLengthPhaseImpedance:
        self.data.remove(phase_impedance_data)
        return self

    @deprecated("Use data.clear() instead.")
    def clear_data(self) -> PerLengthPhaseImpedance:
        self.data.clear()
        return self

    # endregion data boilerplate

    # endregion deprecated list boilerplate