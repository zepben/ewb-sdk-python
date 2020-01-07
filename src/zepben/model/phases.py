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
from collections import defaultdict
from enum import Enum

from zepben.model.cores import SUPPORTED_CORES
from zepben.model.exceptions import CoreException, PhaseException
from zepben.model.direction import Direction
from zepben.cim.iec61970.base.wires.SinglePhaseKind_pb2 import SinglePhaseKind as PBSinglePhaseKind
from zepben.cim.iec61970.base.core.PhaseCode_pb2 import PhaseCode as PBPhaseCode

CORE_MASKS = [0x000000ff, 0x0000ff00, 0x00ff0000, 0xff000000]
DIR_MASK = 0b11


class SinglePhaseKind(Enum):
    NONE = 0
    A = 1
    B = 2
    C = 3
    N = 4
    INVALID = 5

    @property
    def short_name(self):
        return str(self)[16:]

    def to_pb(self):
        return PBSinglePhaseKind.Value(self.name)

    @staticmethod
    def from_pb(pb_spk, **kwargs):
        return SinglePhaseKind[PBSinglePhaseKind.Name(pb_spk)]


def cores_from_phases(phases: PhaseCode):
    """
    Convert a phase into its corresponding number of Cores
    TODO: handle all phases
    :param phases: A :class:`zepben.model.phases.PhaseCode` to convert
    :return: Number of cores
    """
    if phases in (PhaseCode.ABC, PhaseCode.ABN, PhaseCode.ACN, PhaseCode.BCN):
        return 3
    elif phases in (PhaseCode.AB, PhaseCode.AC, PhaseCode.BC, PhaseCode.AN, PhaseCode.BN, PhaseCode.CN):
        return 2
    elif phases in (PhaseCode.A, PhaseCode.B, PhaseCode.C, PhaseCode.N):
        return 1
    elif phases == PhaseCode.ABCN:
        return 4
    else:
        return 4


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
    X = (SinglePhaseKind.NONE,)
    XN = (SinglePhaseKind.NONE, SinglePhaseKind.N)
    XY = (SinglePhaseKind.NONE, SinglePhaseKind.NONE)
    XYN = (SinglePhaseKind.NONE, SinglePhaseKind.NONE, SinglePhaseKind.N)

    @property
    def short_name(self):
        return str(self)[10:]

    @property
    def single_phases(self):
        return self.value

    def to_pb(self):
        return PBPhaseCode.Value(self.name)

    @staticmethod
    def from_pb(pb_pc, **kwargs):
        return PhaseCode[PBPhaseCode.Name(pb_pc)]


PHASE_DIR_MAP = defaultdict(lambda: SinglePhaseKind.NONE)
PHASE_DIR_MAP[0b01] = SinglePhaseKind.A
PHASE_DIR_MAP[0b10] = SinglePhaseKind.A
PHASE_DIR_MAP[0b11] = SinglePhaseKind.A
PHASE_DIR_MAP[0b0100] = SinglePhaseKind.B
PHASE_DIR_MAP[0b1000] = SinglePhaseKind.B
PHASE_DIR_MAP[0b1100] = SinglePhaseKind.B
PHASE_DIR_MAP[0b010000] = SinglePhaseKind.C
PHASE_DIR_MAP[0b100000] = SinglePhaseKind.C
PHASE_DIR_MAP[0b110000] = SinglePhaseKind.C
PHASE_DIR_MAP[0b01000000] = SinglePhaseKind.N
PHASE_DIR_MAP[0b10000000] = SinglePhaseKind.N
PHASE_DIR_MAP[0b11000000] = SinglePhaseKind.N


def validate_core(core_num):
    if core_num > 3 or core_num < 0:
        raise CoreException(f"INTERNAL ERROR: Core index {core_num} is invalid. There are only 4 possible core indexes {0,1,2,3}.")


def _phase(status: int, core_num: int):
    validate_core(core_num)

    core_val = (status >> (core_num * 8)) & 0xff
    return PHASE_DIR_MAP[core_val]


def _direction(status: int, core_num: int):
    validate_core(core_num)
    dir_val = DIR_MASK & (status >> _pos_shift(_phase(status, core_num), core_num))
    return Direction(dir_val)


def _pos_shift(phase: SinglePhaseKind, core_num: int):
    return (core_num * 8) + (2 * max(phase.value - 1, 0))


class Phases(object):
    def __init__(self, phase: PhaseCode = PhaseCode.ABCN):
        self.phase = phase
        self.normal_status = 0
        self.current_status = 0

    def __str__(self):
        s = []
        for core in range(SUPPORTED_CORES):
            pn = self.phase_normal(core)
            pc = self.phase_current(core)
            dn = self.direction_normal(core)
            dc = self.direction_current(core)
            s = s.append(f"core {core}: n: {pn.short_name}|{dn.short_name} c: {pc.short_name}|{dc.short_name}")
        return ", ".join(s)

    def phase_normal(self, core_num):
        """
        Get the normal (nominal) phase for a core.
        :param core_num: The number of the core to check (between 0 - 4)
        :return: :class:`zepben.cim.iec61970.base.wires.SinglePhaseKind` for the core
        :raises: `CoreException` if core is invalid.
        """
        return _phase(self.normal_status, core_num)

    def phase_current(self, core_num):
        """
        Get the current (actual) phase for a core.
        :param core_num: The number of the core to check (between 0 - 4)
        :return: :class:`zepben.cim.iec61970.base.wires.SinglePhaseKind` for the core
        """
        return _phase(self.current_status, core_num)

    def direction_normal(self, core_num):
        """
        Get the normal (nominal) direction for a core.
        :param core_num: The number of the core to check (between 0 - 4)
        :return: :class:`zepben.model.direction.Direction` for the core
        """
        return _direction(self.normal_status, core_num)

    def direction_current(self, core_num):
        """
        Get the current (actual) direction for a core.
        :param core_num: The number of the core to check (between 0 - 4)
        :return: :class:`zepben.model.direction.Direction` for the core
        """
        return _direction(self.current_status, core_num)

    def add_normal(self, phase: SinglePhaseKind, core_num: int, direction: Direction):
        """
        Add a normal phase
        :param phase: The :class:`zepben.cim.iec61970.base.wires.SinglePhaseKind` to add.
        :param core_num: The core number this phase should be applied to
        :param direction: The direction of this phase relative to the location of the `Terminal` to its feeder circuit breaker.
        :return: True if phase status was changed, False otherwise.
        :raises: :class:`zepben.model.exceptions.PhaseException` if phases cross,
                 :class:`zepben.model.exceptions.CoreException` if `core_num` is invalid.
        """
        validate_core(core_num)
        if phase == SinglePhaseKind.NONE or direction == Direction.NONE:
            return False
        if self.phase_normal(core_num) != SinglePhaseKind.NONE and phase != self.phase_normal(core_num):
            raise PhaseException("Crossing phases")
        if self.direction_normal(core_num).has(direction):
            return False

        self.normal_status |= direction.value << _pos_shift(phase, core_num)
        return True

    def add_current(self, phase: SinglePhaseKind, core_num: int, direction: Direction):
        """
        Add a current phase
        :param phase: The :class:`zepben.cim.iec61970.base.wires.SinglePhaseKind` to add.
        :param core_num: The core number this phase should be applied to
        :param direction: The direction of this phase relative to the location of the `Terminal` to its feeder circuit breaker.
        :return: True if phase status was changed, False otherwise.
        :raises: :class:`zepben.model.exceptions.PhaseException` if phases cross
        """
        validate_core(core_num)
        if phase == SinglePhaseKind.NONE or direction == Direction.NONE:
            return False
        if self.phase_current(core_num) != SinglePhaseKind.NONE and phase != self.phase_current(core_num):
            raise PhaseException("Crossing phases")
        if self.direction_current(core_num).has(direction):
            return False

        self.current_status |= direction.value << _pos_shift(phase, core_num)
        return True

    def set_normal(self, phase: SinglePhaseKind, core_num: int, direction: Direction ):
        """
        :param phase: The :class:`zepben.cim.iec61970.base.wires.SinglePhaseKind` to add.
        :param core_num: The core number this phase should be applied to
        :param direction: The direction of this phase relative to the location of the `Terminal` to its feeder circuit breaker.
        :return: True if phase status was changed, False otherwise.
        """
        validate_core(core_num)
        if phase == SinglePhaseKind.NONE or direction == Direction.NONE:
            self.remove_normal(self.phase_normal(core_num), core_num)
            return True

        if self.phase_normal(core_num) == phase and self.direction_normal(core_num) == direction:
            return False

        self.normal_status = (self.normal_status & CORE_MASKS[core_num]) | (direction.value << _pos_shift(phase, core_num))
        return True

    def set_current(self, phase: SinglePhaseKind, direction: Direction, core_num: int):
        """
        :param phase: The :class:`zepben.cim.iec61970.base.wires.SinglePhaseKind` to add.
        :param core_num: The core number this phase should be applied to
        :param direction: The direction of this phase relative to the location of the `Terminal` to its feeder circuit breaker.
        :return: True if phase status was changed, False otherwise.
        """
        validate_core(core_num)
        if phase == SinglePhaseKind.NONE or direction == Direction.NONE:
            self.remove_current(self.phase_current(core_num), core_num)
            return True

        if self.phase_current(core_num) == phase and self.direction_current(core_num) == direction:
            return False

        self.current_status = (self.current_status & CORE_MASKS[core_num]) | (direction.value << _pos_shift(phase, core_num))
        return True

    def remove_normal(self, phase: SinglePhaseKind, core_num: int, direction: Direction = None):
        """
        :param phase: The :class:`zepben.cim.iec61970.base.wires.SinglePhaseKind` to add.
        :param core_num: The core number this phase should be applied to
        :param direction: The direction of this phase relative to the location of the `Terminal` to its feeder circuit breaker.
        :return: True if phase status was changed, False otherwise.
        """
        validate_core(core_num)
        if phase != self.phase_normal(core_num):
            return False

        if direction is not None:
            if not self.direction_normal(core_num).has(direction):
                return False
            self.normal_status &= ~(direction.value << _pos_shift(phase, core_num))
        else:
            self.normal_status &= ~CORE_MASKS[core_num]
            return True

    def remove_current(self, phase: SinglePhaseKind, core_num: int,  direction: Direction = None):
        """
        :param phase: The :class:`zepben.cim.iec61970.base.wires.SinglePhaseKind` to add.
        :param core_num: The core number this phase should be applied to
        :param direction: The direction of this phase relative to the location of the `Terminal` to its feeder circuit breaker.
        :return: True if phase status was changed, False otherwise.
        """
        validate_core(core_num)
        if phase != self.phase_current(core_num):
            return False

        if direction is not None:
            if not self.direction_current(core_num).has(direction):
                return False
            self.current_status &= ~(direction.value << _pos_shift(phase, core_num))
        else:
            self.current_status &= ~CORE_MASKS[core_num]
            return True

    def to_pb(self):
        return self.phase.to_pb()

    @staticmethod
    def from_pb(pb_pc: PBPhaseCode, **kwargs):
        """
        Convert a phase code into a :class:`zepben.model.phases.Phases`.
        Will initialise the `Phases` with the normal phase as indicated by the passed in `PhaseCode`.
        :param pb_pc: Protobuf nominal :class:`zepben.cim.iec61970.base.core.PhaseCode`
        :return: a :class:`zepben.model.phases.Phases` with the normal phases set for the corresponding `PhaseCode`,
                 but no current phases or `Direction`'s.
        """
        return Phases(PhaseCode.from_pb(pb_pc))


