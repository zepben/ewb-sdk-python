#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Optional

from zepben.evolve.model.cim.iec61970.base.meas.control import Control
from zepben.evolve.model.cim.iec61970.base.scada.remote_point import RemotePoint

__all__ = ["RemoteControl"]


class RemoteControl(RemotePoint):
    """
    Remote controls are outputs that are sent by the remote unit to actuators in the process.
    """

    control: Optional[Control] = None
    """The `zepben.evolve.iec61970.base.meas.control.Control` for the `RemoteControl` point."""
