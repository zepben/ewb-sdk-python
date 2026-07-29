#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import TYPE_CHECKING

from zepben.ewb.boilerplate.collections.lazy_collection import LazyCollection
if TYPE_CHECKING:
    from zepben.ewb import SinglePhaseKind, PhaseImpedanceData


class PhaseImpedanceDataList(LazyCollection):
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
