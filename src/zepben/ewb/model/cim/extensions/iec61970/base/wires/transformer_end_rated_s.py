#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TransformerEndRatedS"]

from dataclasses import dataclass

from zepben.ewb.model.cim.extensions.iec61970.base.wires.transformer_cooling_type import TransformerCoolingType
from zepben.ewb.model.cim.extensions.zbex import zbex


@zbex
@dataclass(frozen=True)
class TransformerEndRatedS:
    """
    [ZBEX]
    Normal apparent power rating for a PowerTransformerEnd based on their cooling types.
    """

    cooling_type: TransformerCoolingType
    """[ZBEX] The cooling type for this rating."""

    rated_s: int
    """[ZBEX] The normal apparent power rating for this cooling type."""
