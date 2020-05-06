"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from zepben.cimbend.cim.iec61970.base.meas.iopoint import IoPoint

__all__ = ["Control"]


@dataclass
class Control(IoPoint):
    """
    Control is used for supervisory/device control. It represents control outputs that are used to change the state in a
    process, e.g. close or open breaker, a set point value or a raise lower command.

    Attributes -
        power_system_resource_mrid : Regulating device governed by this control output.
        remote_control : The remote point controlling the physical actuator.
    """

    power_system_resource_mrid: Optional[str] = None
    remote_control: Optional[RemoteControl] = None
