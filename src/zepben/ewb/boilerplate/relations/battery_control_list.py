#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from zepben.ewb import BatteryControlMode
from zepben.ewb.boilerplate.collections.lazy_mrid_list import LazyMridList


class BatteryControlList(LazyMridList):
    """A list of ``BatteryControl`` objects for a ``BatteryUnit``."""

    def get_by_mode(self, control_mode: BatteryControlMode):
        """Return a ``BatteryControl`` by its control mode.

        :param control_mode: The mode of the required ``BatteryControl``.
        :raises IndexError: If no control has the requested mode.
        """
        for control in self:
            if control.control_mode == control_mode:
                return control
        raise IndexError(f"No BatteryControl with a control_mode of {control_mode} was found in BatteryUnit {str(self)}")
