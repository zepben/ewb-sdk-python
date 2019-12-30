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
from zepben.model.exceptions import CoreException, PhaseException
from zepben.model.direction import Direction
from zepben.cim.iec61970.base.wires.SinglePhaseKind_pb2 import SinglePhaseKind
from zepben.cim.iec61970.base.core.PhaseCode_pb2 import PhaseCode
from typing import Sequence

CORE_MASKS = [0x000000ff, 0x0000ff00, 0x00ff0000, 0xff000000]
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
PC_TO_SPK = defaultdict(lambda: SinglePhaseKind)
PC_TO_SPK[PhaseCode.ABCN] = [SinglePhaseKind.A, SinglePhaseKind.B, SinglePhaseKind.C, SinglePhaseKind.N]
PC_TO_SPK[PhaseCode.ABC] = [SinglePhaseKind.A, SinglePhaseKind.B, SinglePhaseKind.C]
PC_TO_SPK[PhaseCode.ABN] = [SinglePhaseKind.A, SinglePhaseKind.B, SinglePhaseKind.N]
PC_TO_SPK[PhaseCode.ACN] = [SinglePhaseKind.A, SinglePhaseKind.C, SinglePhaseKind.N]
PC_TO_SPK[PhaseCode.BCN] = [SinglePhaseKind.B, SinglePhaseKind.C, SinglePhaseKind.N]
PC_TO_SPK[PhaseCode.AB] = [SinglePhaseKind.A, SinglePhaseKind.B]
PC_TO_SPK[PhaseCode.AC] = [SinglePhaseKind.A, SinglePhaseKind.C]
PC_TO_SPK[PhaseCode.AN] = [SinglePhaseKind.A, SinglePhaseKind.N]
PC_TO_SPK[PhaseCode.BC] = [SinglePhaseKind.B, SinglePhaseKind.C]
PC_TO_SPK[PhaseCode.BN] = [SinglePhaseKind.B, SinglePhaseKind.N]
PC_TO_SPK[PhaseCode.CN] = [SinglePhaseKind.C, SinglePhaseKind.N]
PC_TO_SPK[PhaseCode.A] = [SinglePhaseKind.A]
PC_TO_SPK[PhaseCode.B] = [SinglePhaseKind.B]
PC_TO_SPK[PhaseCode.C] = [SinglePhaseKind.C]
PC_TO_SPK[PhaseCode.N] = [SinglePhaseKind.N]
DIR_MASK = 0b11


def get_single_phases(pc: PhaseCode) -> Sequence[SinglePhaseKind]:
    return PC_TO_SPK[pc]


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
    return (core_num * 8) + (2 * max(phase - 1, 0))


class Phases(object):
    def __init__(self, phase: PhaseCode = PhaseCode.ABCN):
        self.phase = phase
        self.normal_status = 0
        self.current_status = 0

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
        return self.phase

    @staticmethod
    def from_pb(pb_pc: PhaseCode, **kwargs):
        """
        Convert a phase code into a :class:`zepben.model.phases.Phases`.
        Will initialise the `Phases` with the normal phase as indicated by the passed in `PhaseCode`.
        :param pb_pc: Protobuf nominal :class:`zepben.cim.iec61970.base.core.PhaseCode`
        :return: a :class:`zepben.model.phases.Phases` with the normal phases set for the corresponding `PhaseCode`,
                 but no current phases or `Direction`'s.
        """
        return Phases(pb_pc)


