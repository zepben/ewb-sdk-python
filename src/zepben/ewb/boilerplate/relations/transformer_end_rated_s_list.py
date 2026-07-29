#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from zepben.ewb import TransformerEndRatedS, TransformerCoolingType
from zepben.ewb.boilerplate.collections.lazy_collection import LazyCollection


class TransformerEndRatedSList(LazyCollection[TransformerEndRatedS]):

    def get_by_cooling_type(
        self,
        cooling_type: TransformerCoolingType,
    ) -> TransformerEndRatedS | None:
        return next((rating for rating in self if rating.cooling_type == cooling_type), None)

    def remove_by_cooling_type(
        self,
        cooling_type: TransformerCoolingType,
    ) -> TransformerEndRatedS | None:
        rating = self.get_by_cooling_type(cooling_type)
        if rating is not None:
            self.remove(rating)
        return rating
