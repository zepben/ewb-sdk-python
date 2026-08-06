#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from zepben.ewb import SinglePhaseKind
from zepben.ewb.boilerplate.collections.lazy_mrid_list import LazyMridList


class AcLineSegmentPhaseList(LazyMridList):
    """A list of ``AcLineSegmentPhase`` objects for an ``AcLineSegment``."""

    def get_by_phase(self, phase: SinglePhaseKind):
        """Return the individual phase model for an ``AcLineSegment``.

        :param phase: The phase of the required ``AcLineSegmentPhase``.
        :raises KeyError: If no model has the requested phase.
        """
        res = self.find_by(lambda it: it.phase == phase)
        if res is None:
            raise KeyError(phase)
        return res
