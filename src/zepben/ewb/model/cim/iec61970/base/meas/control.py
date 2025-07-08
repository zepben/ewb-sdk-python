#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Control"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.meas.iopoint import IoPoint

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.scada.remote_control import RemoteControl


class Control(IoPoint):
    """
    Control is used for supervisory/device control. It represents control outputs that are used to change the state in a
    process, e.g. close or open breaker, a set point value or a raise lower command.
    """

    power_system_resource_mrid: Optional[str] = None
    """AnalogValue represents an analog MeasurementValue."""

    remote_control: Optional['RemoteControl'] = None
    """AnalogValue represents an analog MeasurementValue."""
