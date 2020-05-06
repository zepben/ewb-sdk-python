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


from dataclasses import dataclass
from typing import Optional

from zepben.cimbend.cim.iec61970.base.meas.measurement import Measurement
from zepben.cimbend.cim.iec61970.base.scada.remote_point import RemotePoint

__all__ = ["RemoteSource"]


@dataclass
class RemoteSource(RemotePoint):
    """
    Remote sources are state variables that are telemetered or calculated within the remote unit.

    Attributes -
        measurement : The :class:`meas.measurement.Measurement` for the ``RemoteSource`` point.
    """
    measurement: Optional[Measurement] = None
