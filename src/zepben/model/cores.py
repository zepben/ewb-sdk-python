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


from zepben.model.exceptions import CoreException
from zepben.cim.iec61970.base.core.PhaseCode_pb2 import PhaseCode
SUPPORTED_CORES = 4


def validate_core(core: int):
    if core < 0 or core > SUPPORTED_CORES:
        raise CoreException(f"Invalid number of cores, was {core} but must be between 0 and {SUPPORTED_CORES}")
    return core


def from_count(num_cores: int):
    validate_core(num_cores)
    return range(0, num_cores)


def from_phases(phases: PhaseCode):
    """
    Convert a phase into its corresponding number of Cores
    TODO: handle all phases
    :param phases: A :class:`zepben.cim.iec61970.base.core.PhaseCode` to convert
    :return: Number of cores
    """
    if phases == PhaseCode.ABC:
        return 3
    elif phases in (PhaseCode.AB, PhaseCode.AC, PhaseCode.BC):
        return 2
    elif phases in (PhaseCode.A, PhaseCode.B, PhaseCode.C):
        return 1
    elif phases == PhaseCode.ABCN:
        return 4
    else:
        return 4


class CorePath(object):
    def __init__(self, from_core: int, to_core: int):
        self.from_core = validate_core(from_core)
        self.to_core = validate_core(to_core)

    def __eq__(self, other):
        if self is other:
            return True
        return self.from_core == other.from_core and self.to_core == other.to_core

    def __ne__(self, other):
        if self is other:
            return False
        return self.from_core != other.from_core or self.to_core != other.to_core

    def __lt__(self, other):
        if self.from_core < other.from_core and self.to_core < other.to_core:
            return True
        else:
            return False
