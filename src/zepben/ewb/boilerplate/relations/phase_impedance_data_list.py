#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import TYPE_CHECKING

from zepben.ewb.boilerplate.collections.lazy_list import LazyList
if TYPE_CHECKING:
    from zepben.ewb import SinglePhaseKind, PhaseImpedanceData


class PhaseImpedanceDataList(LazyList):
    """A list of phase impedance data for a per-length phase impedance."""

    def get(self, from_phase: SinglePhaseKind, to_phase: SinglePhaseKind) -> PhaseImpedanceData:
        """Return the matrix entry for the corresponding phases.

        :param from_phase: The "from" phase to look up.
        :param to_phase: The "to" phase to look up.
        :raises KeyError: If no matching phase impedance data exists.
        """

        phase_impedance_data = self.find_by(lambda it: it.to_phase == to_phase)
        if phase_impedance_data:
            return phase_impedance_data

        raise KeyError((from_phase, to_phase))

    @property
    def diagonal(self):
        """Return the diagonal entries where ``to_phase == from_phase``."""
        return (pid for pid in self if pid.from_phase == pid.to_phase)
