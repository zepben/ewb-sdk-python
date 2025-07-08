#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["RatioTapChanger"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.wires.tap_changer import TapChanger

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.transformer_end import TransformerEnd


class RatioTapChanger(TapChanger):
    """
    A tap changer that changes the voltage ratio impacting the voltage magnitude but not the phase angle across the transformer.

    Angle sign convention (general): Positive value indicates a positive phase shift from the winding where the tap is located to the other winding
    (for a two-winding transformer).
    """

    transformer_end: Optional[TransformerEnd] = None
    """`TransformerEnd` to which this ratio tap changer belongs."""

    step_voltage_increment: Optional[float] = None
    """Tap step increment, in per cent of neutral voltage, per step position."""
