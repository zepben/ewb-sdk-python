#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Streetlight"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.model.cim.iec61968.assets.asset import Asset
from zepben.ewb.model.cim.iec61968.infiec61968.infassets.streetlight_lamp_kind import StreetlightLampKind

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.infiec61968.infassets.pole import Pole


class Streetlight(Asset):
    """
    A Streetlight asset.
    """

    pole: Optional['Pole'] = None
    """The `zepben.ewb.model.cim.iec61968.assets.pole.Pole` this Streetlight is attached to."""

    light_rating: Optional[int] = None
    """The power rating of the light in watts."""

    lamp_kind: StreetlightLampKind = StreetlightLampKind.UNKNOWN
    """The kind of lamp."""
