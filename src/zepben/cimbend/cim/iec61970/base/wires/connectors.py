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

from zepben.cimbend.cim.iec61970.base.core.conducting_equipment import ConductingEquipment

__all__ = ["Connector", "Junction"]


class Connector(ConductingEquipment):
    """
    A conductor, or group of conductors, with negligible impedance, that serve to connect other conducting equipment
    within a single substation and are modelled with a single logical terminal.
    """
    pass


@dataclass
class Junction(Connector):
    """
    A point where one or more conducting equipments are connected with zero resistance.
    """
    pass

