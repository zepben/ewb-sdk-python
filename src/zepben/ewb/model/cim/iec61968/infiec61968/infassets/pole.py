#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Pole"]

from typing import List, TYPE_CHECKING

from typing_extensions import deprecated

from zepben.ewb.dataslot import MRIDListRouter, dataslot, MRIDListAccessor
from zepben.ewb.model.cim.iec61968.assets.structure import Structure

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.assets.streetlight import Streetlight


@dataslot
class Pole(Structure):
    """A Pole Asset"""

    classification: str | None = None
    """Pole class: 1, 2, 3, 4, 5, 6, 7, H1, H2, Other, Unknown."""

    streetlights: List[Streetlight] | None = MRIDListAccessor()

    def _retype(self):
        self.streetlights: MRIDListRouter[Streetlight] = ...
    
    @deprecated("BOILERPLATE: Use len(streetlights) instead")
    def num_streetlights(self) -> int:
        return len(self.streetlights)

    @deprecated("BOILERPLATE: Use streetlights.get_by_mrid(mrid) instead")
    def get_streetlight(self, mrid: str) -> Streetlight:
        return self.streetlights.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use streetlights.append(streetlight) instead")
    def add_streetlight(self, streetlight: Streetlight) -> Pole:
        self.streetlights.append(streetlight)
        return self

    @deprecated("Boilerplate: Use streetlights.remove(streetlight) instead")
    def remove_streetlight(self, streetlight: Streetlight) -> Pole:
        self.streetlights.remove(streetlight)
        return self

    @deprecated("BOILERPLATE: Use streetlights.clear() instead")
    def clear_streetlights(self) -> Pole:
        self.streetlights.clear()
        return self

