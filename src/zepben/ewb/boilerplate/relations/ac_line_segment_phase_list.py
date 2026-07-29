#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from zepben.ewb import SinglePhaseKind
from zepben.ewb.boilerplate.collections.mrid_list import LazyMridList


class AcLineSegmentPhaseList(LazyMridList):
    def get_by_phase(self, phase: SinglePhaseKind):
        """
        The individual phase models for an AcLineSegment.
        `phase` the phase of the required [AcLineSegmentPhase]
        """
        res = next((it for it in self if it.phase == phase), None)
        if res is None:
            raise KeyError(phase)
        return res
