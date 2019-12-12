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


import re
from collections.abc import Iterable
from typing import Set, List
from zepben.cim.iec61970.base.wires.SinglePhaseKind_pb2 import SinglePhaseKind

phs_to_cores = { SinglePhaseKind.A: 0,
                 SinglePhaseKind.B: 1,
                 SinglePhaseKind.C: 2,
                 SinglePhaseKind.N: 3}


def snake2camelback(name):
    return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), name)


def iter_but_not_str(obj):
    return isinstance(obj, Iterable) and not isinstance(obj, (str, bytes, bytearray, dict))


def get_equipment_connections(cond_equip, exclude: Set = None) -> List:
    """ Utility function wrapping :meth:`zepben.model.ConductingEquipment.get_connections` """
    return cond_equip.get_connections(exclude=exclude)


def phs_kind_to_idx(phase: SinglePhaseKind):
    return phs_to_cores[phase]
