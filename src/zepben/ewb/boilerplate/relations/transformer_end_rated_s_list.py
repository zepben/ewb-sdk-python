#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from zepben.ewb import TransformerEndRatedS, TransformerCoolingType
from zepben.ewb.boilerplate.collections.lazy_list import LazyList


class TransformerEndRatedSList(LazyList[TransformerEndRatedS]):
    """A list of rated-power entries for a ``PowerTransformerEnd``."""

    def get_by_cooling_type(
        self,
        cooling_type: TransformerCoolingType,
    ) -> TransformerEndRatedS | None:
        """Return the entry for ``cooling_type``, or ``None``."""
        return next((rating for rating in self if rating.cooling_type == cooling_type), None)

    def remove_by_cooling_type(
        self,
        cooling_type: TransformerCoolingType,
    ) -> TransformerEndRatedS | None:
        """Remove and return the entry for ``cooling_type``, if present."""
        rating = self.get_by_cooling_type(cooling_type)
        if rating is not None:
            self.remove(rating)
        return rating
