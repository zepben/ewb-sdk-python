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

from enum import Enum, unique

from zepben.cimbend.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

__all__ = ["PhaseCode", "phasecode_by_id"]


def phasecode_by_id(id: int):
    return _phasecode_members[id]


@unique
class PhaseCode(Enum):
    NONE = (SinglePhaseKind.NONE,)
    A = (SinglePhaseKind.A,)
    B = (SinglePhaseKind.B,)
    C = (SinglePhaseKind.C,)
    N = (SinglePhaseKind.N,)
    AB = (SinglePhaseKind.A, SinglePhaseKind.B)
    AC = (SinglePhaseKind.A, SinglePhaseKind.C)
    AN = (SinglePhaseKind.A, SinglePhaseKind.N)
    BC = (SinglePhaseKind.B, SinglePhaseKind.C)
    BN = (SinglePhaseKind.B, SinglePhaseKind.N)
    CN = (SinglePhaseKind.C, SinglePhaseKind.N)
    ABC = (SinglePhaseKind.A, SinglePhaseKind.B, SinglePhaseKind.C)
    ABN = (SinglePhaseKind.A, SinglePhaseKind.B, SinglePhaseKind.N)
    ACN = (SinglePhaseKind.A, SinglePhaseKind.C, SinglePhaseKind.N)
    BCN = (SinglePhaseKind.B, SinglePhaseKind.C, SinglePhaseKind.N)
    ABCN = (SinglePhaseKind.A, SinglePhaseKind.B, SinglePhaseKind.C, SinglePhaseKind.N)
    X = (SinglePhaseKind.X,)
    XN = (SinglePhaseKind.X, SinglePhaseKind.N)
    XY = (SinglePhaseKind.X, SinglePhaseKind.Y)
    XYN = (SinglePhaseKind.X, SinglePhaseKind.Y, SinglePhaseKind.N)
    Y = (SinglePhaseKind.Y,)
    YN = (SinglePhaseKind.Y, SinglePhaseKind.N)

    @property
    def short_name(self):
        return str(self)[10:]

    @property
    def single_phases(self):
        return self.value[:1]

    def num_phases(self):
        return len(self.value)


_phasecode_members = list(PhaseCode.__members__.values())
