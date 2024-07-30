#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Optional

from zepben.evolve.model.cim.iec61970.base.wires.regulating_control import RegulatingControl

__all__ = ["TapChangerControl"]


class TapChangerControl(RegulatingControl):
    """
    Describes behaviour specific to tap changers, e.g. how the voltage at the end of a line varies with the load level and compensation of the voltage drop by
    tap adjustment.
    """
    limit_voltage: Optional[int] = None
    """Maximum allowed regulated voltage on the PT secondary, regardless of line drop compensation. Sometimes referred to as first-house protection."""

    line_drop_compensation: Optional[bool] = None
    """If true, then line drop compensation is to be applied. """

    line_drop_r: Optional[float] = None
    """Line drop compensator resistance setting for normal (forward) power flow in Ohms."""

    line_drop_x: Optional[float] = None
    """Line drop compensator reactance setting for normal (forward) power flow in Ohms."""

    reverse_line_drop_r: Optional[float] = None
    """Line drop compensator resistance setting for reverse power flow in Ohms."""

    reverse_line_drop_x: Optional[float] = None
    """Line drop compensator reactance setting for reverse power flow in Ohms."""

    forward_ldc_blocking: Optional[bool] = None
    """
    True implies this tap changer turns off/ignores reverse current flows for line drop compensation when power flow is reversed and no reverse line drop 
    is set.
    """

    time_delay: Optional[float] = None
    """The time delay for the tap changer in seconds."""

    co_generation_enabled: Optional[bool] = None
    """
    True implies cogeneration mode is enabled and that the control will regulate to the new source bushing (downline bushing), keeping locations downline 
    from experiencing overvoltage situations.
    """
