#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Pole"]

from typing import List, Optional, Generator, TYPE_CHECKING
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.iec61968.assets.structure import Structure
from zepben.ewb.util import get_by_mrid, ngen, nlen, safe_remove
from zepben.ewb.dataclass_descriptors.dataclass_base import zb_dataclass
from zepben.ewb import remove_descriptor_annotations
from zepben.ewb.dataclass_descriptors.mrid_list import MridCollection, LazyMridList

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.assets.streetlight import Streetlight


@zb_dataclass
class Pole(Structure):
    """A Pole Asset"""

    classification: Optional[str] = None
    """Pole class: 1, 2, 3, 4, 5, 6, 7, H1, H2, Other, Unknown."""

    _streetlights: Optional[List[Streetlight]] = field(default=None)

    streetlights: MridCollection[Streetlight] = LazyMridList(
        _streetlights,
        "A Streetlight",
    )


    # region deprecated list boilerplate
    # region streetlights boilerplate

    @deprecated("Use len(obj.streetlights) instead.")
    def num_streetlights(self) -> int:
        return len(self.streetlights)

    @deprecated("Use obj.streetlights.get_by_mrid(mrid) instead.")
    def get_streetlight(self, mrid: str) -> Streetlight:
        return self.streetlights.get_by_mrid(mrid)

    @deprecated("Use obj.streetlights.append(streetlight) instead.")
    def add_streetlight(self, streetlight: Streetlight) -> Pole:
        self.streetlights.append(streetlight)
        return self

    @deprecated("Use obj.streetlights.remove(streetlight) instead.")
    def remove_streetlight(self, streetlight: Streetlight) -> Pole:
        self.streetlights.remove(streetlight)
        return self

    @deprecated("Use obj.streetlights.clear() instead.")
    def clear_streetlights(self) -> Pole:
        self.streetlights.clear()
        return self

    # endregion streetlights boilerplate

    # endregion deprecated list boilerplate
