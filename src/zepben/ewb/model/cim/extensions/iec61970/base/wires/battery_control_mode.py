#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["BatteryControlMode"]

from enum import Enum

from zepben.ewb.model.cim.extensions.zbex import zbex


@zbex
class BatteryControlMode(Enum):
    """
    [ZBEX]
    Mode of operation for the dispatch (charging/discharging) function of BatteryControl.
    """

    UNKNOWN = 0
    """[ZBEX] Unknown control mode."""

    peakShaveDischarge = 1
    """
    [ZBEX]
    This mode directs the BatteryUnit to discharge as needed to maintain the power level of the monitored element within a defined range
    (specified by target_deadband) or to keep it at or below the value specified by max_allowed_target_value. This mode helps prevent power spikes by 
    discharging the BatteryUnit to manage peak demand effectively.
    """

    currentPeakShaveDischarge = 2
    """
    [ZBEX]
    This mode directs the BatteryUnit to discharge as needed to maintain the current (in amps) at a monitored element below a specified target. Similar
    to peakShaveDischarge, this mode aims to reduce demand peaks, focusing specifically on current levels to manage capacity and enhance system stability where
    current control is essential.
    """

    following = 3
    """[ZBEX] The control is triggered by time and resets the targetValue property to the present monitored element power."""

    support = 4
    """[ZBEX] 
    This is essentially the opposite of peakShave modes. The fleet is dispatched to keep the power in the monitored terminal at or above target_value.
    """

    schedule = 5
    """
    [ZBEX]
    In Schedule mode, a trapezoidal-shaped discharge schedule is specified through Tup (up ramp duration), TFlat (at duration),
    and Tdn (down ramp duration) properties.
    """

    peakShaveCharge = 6
    """
    [ZBEX]
    This mode directs the BatteryUnit to initiate charging when the power level at a monitored element falls below a specified threshold 
    (min_allowed_target_value). This mode supports demand leveling by charging the BatteryUnit during low-demand periods, optimizing overall power management.
    """

    currentPeakShaveCharge = 7
    """
    [ZBEX]
    This mode initiates charging when the current (in Amps) at a monitored element falls below a specified threshold (min_allowed_target_value).
    Similar to peakShaveCharge, this mode aims to manage demand effectively, but it operates based on current levels rather than power, providing finer
    control in systems where current management is prioritized.
    """

    time = 8
    """
    [ZBEX] 
    In Time mode all storage elements are set to discharge when in the course of simulation the time of day passes the specified hour of day by the
    TimeDisChargeTrigger property (hour is a decimal value, e.g., 10.5 = 1030)
    """

    profile = 9
    """[ZBEX] In this mode both discharging and charging precisely follow a per-unit curve."""

    @property
    def short_name(self):
        return str(self)[19:]
