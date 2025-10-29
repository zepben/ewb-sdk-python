#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TapChangerControl"]

from typing import Optional

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.wires.regulating_control import RegulatingControl


@dataslot
class TapChangerControl(RegulatingControl):
    """
    Describes behaviour specific to tap changers, e.g. how the voltage at the end of a line varies with the load level and compensation of the voltage drop by
    tap adjustment.
    """
    limit_voltage: int | None = None
    """Maximum allowed regulated voltage on the PT secondary, regardless of line drop compensation. Sometimes referred to as first-house protection."""

    line_drop_compensation: bool | None = None
    """If true, then line drop compensation is to be applied. """

    line_drop_r: float | None = None
    """Line drop compensator resistance setting for normal (forward) power flow in Ohms."""

    line_drop_x: float | None = None
    """Line drop compensator reactance setting for normal (forward) power flow in Ohms."""

    reverse_line_drop_r: float | None = None
    """Line drop compensator resistance setting for reverse power flow in Ohms."""

    reverse_line_drop_x: float | None = None
    """Line drop compensator reactance setting for reverse power flow in Ohms."""

    forward_ldc_blocking: bool | None = None
    """
    True implies this tap changer turns off/ignores reverse current flows for line drop compensation when power flow is reversed and no reverse line drop 
    is set.
    """

    time_delay: float | None = None
    """The time delay for the tap changer in seconds."""

    co_generation_enabled: bool | None = None
    """
    True implies cogeneration mode is enabled and that the control will regulate to the new source bushing (downline bushing), keeping locations downline 
    from experiencing overvoltage situations.
    """
