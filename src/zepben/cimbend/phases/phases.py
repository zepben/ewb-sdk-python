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

from zepben.cimbend.exceptions import PhaseException
from zepben.cimbend.phases.direction import Direction
from zepben.cimbend.cim.iec61970.base.wires import SinglePhaseKind
from zepben.cimbend.cim.iec61970.base.core.phase_code import PhaseCode

__all__ = ["cores_from_phases", "phase", "direction", "pos_shift", "add", "setphs", "remove", "remove_all", "TracedPhases"]
CORE_MASKS = [0x000000ff, 0x0000ff00, 0x00ff0000, 0xff000000]
DIR_MASK = 0b11


def cores_from_phases(phases: PhaseCode):
    """
    Convert a phase into its corresponding number of Cores
    TODO: handle all phases
    :param phases: A :class:`zepben.cimbend.PhaseCode` to convert
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


def _valid_phase_check(nominal_phase):
    if nominal_phase not in SinglePhaseKind[1:6]:
        raise ValueError(f"INTERNAL ERROR: Phase {nominal_phase} is invalid. Must be one of {SinglePhaseKind[1:6]}.")


def phase(status: int, nominal_phase: SinglePhaseKind):
    core_val = (status >> (nominal_phase.mask_index * 8)) & 0xff
    return PHASE_DIR_MAP[core_val]


def direction(status: int, nominal_phase: SinglePhaseKind):
    dir_val = (status >> pos_shift(phase(status, nominal_phase), nominal_phase)) & DIR_MASK
    return Direction(dir_val)


def pos_shift(phs: SinglePhaseKind, nominal_phase: SinglePhaseKind):
    return (nominal_phase.mask_index * 8) + (2 * max(phs.value - 1, 0))


def setphs(status: int, phs: SinglePhaseKind, dir_: Direction, nominal_phase: SinglePhaseKind) -> int:
    return (status & ~CORE_MASKS[nominal_phase.mask_index]) | (dir_.value << pos_shift(phs, nominal_phase))


def add(status: int, phs: SinglePhaseKind, dir_: Direction, nominal_phase: SinglePhaseKind) -> int:
    return status | dir_.value << pos_shift(phs, nominal_phase)


def remove_all(status: int, nominal_phase: SinglePhaseKind) -> int:
    return status & ~CORE_MASKS[nominal_phase.mask_index]


def remove(status: int, phs: SinglePhaseKind, dir_: Direction, nominal_phase: SinglePhaseKind) -> int:
    return status & ~(dir_.value << pos_shift(phs, nominal_phase))


class TracedPhases(object):
    """
    Class that holds the traced phase statuses for the current and normal state of the network.
    Each byte in an int is used to store all possible phases and directions for a core.
    Each byte has 2 bits that represent the direction for a phase. If none of those bits are set the direction is equal to NONE.
    Use the figures below as a reference.
    <p>
    PhaseStatus:     |          integer          |
                     | byte | byte | byte | byte |
                     |Core 3|Core 2|Core 1|Core 0|
    <p>
    Core:            |                 byte                  |
                     |  2bits  |  2bits  |  2bits  |  2bits  |
    Phase:           |    N    |    C    |    B    |    A    |
    Direction:       |OUT | IN |OUT | IN |OUT | IN |OUT | IN |
    """
    def __init__(self):
        self.normal_status = 0
        self.current_status = 0

    def __str__(self):
        s = []
        for phs in (SinglePhaseKind.A, SinglePhaseKind.B, SinglePhaseKind.C, SinglePhaseKind.N):
            pn = self.phase_normal(phs)
            pc = self.phase_current(phs)
            dn = self.direction_normal(phs)
            dc = self.direction_current(phs)
            s.append(f"phase {phs}: n: {pn.short_name}|{dn.short_name} c: {pc.short_name}|{dc.short_name}")
        return ", ".join(s)

    def phase_normal(self, nominal_phase: SinglePhaseKind):
        """
        Get the normal (nominal) phase for a core.
        :param nominal_phase: The number of the core to check (between 0 - 4)
        :return: :class:`zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind` for the core
        :raises: `CoreException` if core is invalid.
        """
        _valid_phase_check(nominal_phase)
        return phase(self.normal_status, nominal_phase)

    def phase_current(self, nominal_phase: SinglePhaseKind):
        """
        Get the current (actual) phase for a core.
        :param nominal_phase: The number of the core to check (between 0 - 4)
        :return: :class:`zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind` for the core
        """
        _valid_phase_check(nominal_phase)
        return phase(self.current_status, nominal_phase)

    def direction_normal(self, nominal_phase: SinglePhaseKind):
        """
        Get the normal (nominal) direction for a core.
        :param nominal_phase: The number of the core to check (between 0 - 4)
        :return: :class:`zepben.phases.direction.Direction` for the core
        """
        _valid_phase_check(nominal_phase)
        return direction(self.normal_status, nominal_phase)

    def direction_current(self, nominal_phase: SinglePhaseKind):
        """
        Get the current (actual) direction for a core.
        :param nominal_phase: The number of the core to check (between 0 - 4)
        :return: :class:`zepben.phases.direction.Direction` for the core
        """
        _valid_phase_check(nominal_phase)
        return direction(self.current_status, nominal_phase)

    def add_normal(self, phs: SinglePhaseKind, nominal_phase: SinglePhaseKind, dir_: Direction):
        """
        Add a normal phase
        :param phs: The :class:`zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind` to add.
        :param nominal_phase: The core number this phase should be applied to
        :param dir_: The direction of this phase relative to the location of the `Terminal` to its feeder circuit breaker.
        :return: True if phase status was changed, False otherwise.
        :raises: :class:`zepben.phases.exceptions.PhaseException` if phases cross,
                 :class:`zepben.phases.exceptions.CoreException` if `nominal_phase` is invalid.
        """
        _valid_phase_check(nominal_phase)
        if phs == SinglePhaseKind.NONE or dir_ == Direction.NONE:
            return False
        if self.phase_normal(nominal_phase) != SinglePhaseKind.NONE and phs != self.phase_normal(nominal_phase):
            raise PhaseException("Crossing phases")
        if self.direction_normal(nominal_phase).has(dir_):
            return False

        self.normal_status = add(self.normal_status, phs, dir_, nominal_phase)
        return True

    def add_current(self, phs: SinglePhaseKind, nominal_phase: SinglePhaseKind, dir_: Direction):
        """
        Add a current phase
        :param phs: The :class:`zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind` to add.
        :param nominal_phase: The core number this phase should be applied to
        :param dir_: The direction of this phase relative to the location of the `Terminal` to its feeder circuit breaker.
        :return: True if phase status was changed, False otherwise.
        :raises: :class:`zepben.phases.exceptions.PhaseException` if phases cross
        """
        _valid_phase_check(nominal_phase)
        if phs == SinglePhaseKind.NONE or dir_ == Direction.NONE:
            return False
        if self.phase_current(nominal_phase) != SinglePhaseKind.NONE and phs != self.phase_current(nominal_phase):
            raise PhaseException("Crossing phases")
        if self.direction_current(nominal_phase).has(dir_):
            return False

        self.current_status = add(self.current_status, phs, dir_, nominal_phase)
        return True

    def set_normal(self, phs: SinglePhaseKind, nominal_phase: SinglePhaseKind, dir_: Direction):
        """
        :param phs: The :class:`zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind` to add.
        :param nominal_phase: The core number this phase should be applied to
        :param dir_: The direction of this phase relative to the location of the `Terminal` to its feeder circuit breaker.
        :return: True if phase status was changed, False otherwise.
        """
        _valid_phase_check(nominal_phase)
        if phs == SinglePhaseKind.NONE or dir_ == Direction.NONE:
            self.remove_normal(self.phase_normal(nominal_phase), nominal_phase)
            return True

        if self.phase_normal(nominal_phase) == phs and self.direction_normal(nominal_phase) == dir_:
            return False

        self.normal_status = setphs(self.normal_status, phs, dir_, nominal_phase)
        return True

    def set_current(self, phs: SinglePhaseKind, dir_: Direction, nominal_phase: SinglePhaseKind):
        """
        :param phs: The :class:`zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind` to add.
        :param nominal_phase: The core number this phase should be applied to
        :param dir_: The direction of this phase relative to the location of the `Terminal` to its feeder circuit breaker.
        :return: True if phase status was changed, False otherwise.
        """
        _valid_phase_check(nominal_phase)
        if phs == SinglePhaseKind.NONE or dir_ == Direction.NONE:
            self.remove_current(self.phase_current(nominal_phase), nominal_phase)
            return True

        if self.phase_current(nominal_phase) == phs and self.direction_current(nominal_phase) == dir_:
            return False

        self.current_status = setphs(self.current_status, phs, dir_, nominal_phase)
        return True

    def remove_normal(self, phs: SinglePhaseKind, nominal_phase: SinglePhaseKind, dir_: Direction = None):
        """
        :param phs: The :class:`zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind` to add.
        :param nominal_phase: The core number this phase should be applied to
        :param dir_: The direction of this phase relative to the location of the `Terminal` to its feeder circuit breaker.
        :return: True if phase status was changed, False otherwise.
        """
        _valid_phase_check(nominal_phase)
        if phs != self.phase_normal(nominal_phase):
            return False

        if dir_ is not None:
            if not self.direction_normal(nominal_phase).has(dir_):
                return False
            self.normal_status = remove(self.normal_status, phs, dir_, nominal_phase)
        else:
            self.normal_status = remove_all(self.normal_status, nominal_phase)
            return True

    def remove_current(self, phs: SinglePhaseKind, nominal_phase: SinglePhaseKind, dir_: Direction = None):
        """
        :param phs: The :class:`zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind` to add.
        :param nominal_phase: The core number this phase should be applied to
        :param dir_: The direction of this phase relative to the location of the `Terminal` to its feeder circuit breaker.
        :return: True if phase status was changed, False otherwise.
        """
        _valid_phase_check(nominal_phase)
        if phs != self.phase_current(nominal_phase):
            return False

        if dir_ is not None:
            if not self.direction_current(nominal_phase).has(dir_):
                return False
            self.current_status = remove(self.current_status, phs, dir_, nominal_phase)
        else:
            self.current_status = remove_all(self.current_status, nominal_phase)
            return True

