#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations
from collections import defaultdict
from dataclassy import dataclass


from zepben.evolve.exceptions import PhaseException
from zepben.evolve.model.phasedirection import PhaseDirection
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind, SINGLE_PHASE_KIND_VALUES

__all__ = ["phase", "direction", "pos_shift", "add", "setphs", "remove", "remove_all", "TracedPhases", "NominalPhasePath"]
CORE_MASKS = [0x000000ff, 0x0000ff00, 0x00ff0000, 0xff000000]
DIR_MASK = 0b11


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
    if nominal_phase not in SINGLE_PHASE_KIND_VALUES[1:7]:
        raise ValueError(f"INTERNAL ERROR: Phase {nominal_phase} is invalid. Must be one of {SINGLE_PHASE_KIND_VALUES[1:7]}.")


def phase(status: int, nominal_phase: SinglePhaseKind):
    core_val = (status >> (nominal_phase.mask_index * 8)) & 0xff
    return PHASE_DIR_MAP[core_val]


def direction(status: int, nominal_phase: SinglePhaseKind):
    dir_val = (status >> pos_shift(phase(status, nominal_phase), nominal_phase)) & DIR_MASK
    return PhaseDirection(dir_val)


def pos_shift(phs: SinglePhaseKind, nominal_phase: SinglePhaseKind):
    return (2 * max(phs.value - 1, 0)) + (nominal_phase.mask_index * 8)


def setphs(status: int, phs: SinglePhaseKind, direction: PhaseDirection, nominal_phs: SinglePhaseKind) -> int:
    return (status & ~CORE_MASKS[nominal_phs.mask_index]) | _shifted_value(direction, phs, nominal_phs)


def add(status: int, phs: SinglePhaseKind, direction: PhaseDirection, nominal_phs: SinglePhaseKind) -> int:
    return status | _shifted_value(direction, phs, nominal_phs)


def remove_all(status: int, nominal_phase: SinglePhaseKind) -> int:
    return status & ~CORE_MASKS[nominal_phase.mask_index]


def remove(status: int, phs: SinglePhaseKind, direction: PhaseDirection, nominal_phs: SinglePhaseKind) -> int:
    return status & ~_shifted_value(direction, phs, nominal_phs)


def _shifted_value(pd: PhaseDirection, spk: SinglePhaseKind, nom: SinglePhaseKind) -> int:
    return pd.value << pos_shift(spk, nom)


@dataclass(slots=True)
class NominalPhasePath(object):
    """
    Defines how a nominal phase is wired through a connectivity node between two terminals
    """

    from_phase: SinglePhaseKind
    """The nominal phase where the path comes from."""

    to_phase: SinglePhaseKind
    """The nominal phase where the path goes to."""


@dataclass(slots=True)
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
    _normal_status: int = 0
    _current_status: int = 0

    def __init__(self, normal_status: int = 0, current_status: int = 0):
        self._normal_status = normal_status
        self._current_status = current_status

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
        `nominal_phase` The number of the core to check (between 0 - 4)
        Returns `zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind` for the core
        Raises `CoreException` if core is invalid.
        """
        _valid_phase_check(nominal_phase)
        return phase(self._normal_status, nominal_phase)

    def phase_current(self, nominal_phase: SinglePhaseKind):
        """
        Get the current (actual) phase for a core.
        `nominal_phase` The number of the core to check (between 0 - 4)
        Returns `zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind` for the core
        """
        _valid_phase_check(nominal_phase)
        return phase(self._current_status, nominal_phase)

    def direction_normal(self, nominal_phase: SinglePhaseKind):
        """
        Get the normal (nominal) direction for a core.
        `nominal_phase` The number of the core to check (between 0 - 4)
        Returns `zepben.phases.direction.Direction` for the core
        """
        _valid_phase_check(nominal_phase)
        return direction(self._normal_status, nominal_phase)

    def direction_current(self, nominal_phase: SinglePhaseKind):
        """
        Get the current (actual) direction for a core.
        `nominal_phase` The number of the core to check (between 0 - 4)
        Returns `zepben.phases.direction.Direction` for the core
        """
        _valid_phase_check(nominal_phase)
        return direction(self._current_status, nominal_phase)

    def add_normal(self, phs: SinglePhaseKind, nominal_phase: SinglePhaseKind, dir_: PhaseDirection):
        """
        Add a normal phase
        `phs` The `zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind` to add.
        `nominal_phase` The core number this phase should be applied to
        `dir_` The direction of this phase relative to the location of the `zepben.evolve.iec61970.base.core.terminal.Terminal` to its feeder circuit breaker.
        Returns True if phase status was changed, False otherwise.
        Raises `zepben.phases.exceptions.PhaseException` if phases cross,
                 `zepben.phases.exceptions.CoreException` if `nominal_phase` is invalid.
        """
        _valid_phase_check(nominal_phase)
        if phs == SinglePhaseKind.NONE or dir_ == PhaseDirection.NONE:
            return False
        if self.phase_normal(nominal_phase) != SinglePhaseKind.NONE and phs != self.phase_normal(nominal_phase):
            raise PhaseException("Crossing phases")
        if self.direction_normal(nominal_phase).has(dir_):
            return False

        self._normal_status = add(self._normal_status, phs, dir_, nominal_phase)
        return True

    def add_current(self, phs: SinglePhaseKind, nominal_phase: SinglePhaseKind, dir_: PhaseDirection):
        """
        Add a current phase
        `phs` The `zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind` to add.
        `nominal_phase` The core number this phase should be applied to
        `dir_` The direction of this phase relative to the location of the `zepben.evolve.iec61970.base.core.terminal.Terminal` to its feeder circuit breaker.
        Returns True if phase status was changed, False otherwise.
        Raises `zepben.phases.exceptions.PhaseException` if phases cross
        """
        _valid_phase_check(nominal_phase)
        if phs == SinglePhaseKind.NONE or dir_ == PhaseDirection.NONE:
            return False
        if self.phase_current(nominal_phase) != SinglePhaseKind.NONE and phs != self.phase_current(nominal_phase):
            raise PhaseException("Crossing phases")
        if self.direction_current(nominal_phase).has(dir_):
            return False

        self._current_status = add(self._current_status, phs, dir_, nominal_phase)
        return True

    def set_normal(self, phs: SinglePhaseKind, nominal_phase: SinglePhaseKind, dir_: PhaseDirection):
        """
        `phs` The `zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind` to add.
        `nominal_phase` The core number this phase should be applied to
        `dir_` The direction of this phase relative to the location of the `zepben.evolve.iec61970.base.core.terminal.Terminal` to its feeder circuit breaker.
        Returns True if phase status was changed, False otherwise.
        """
        _valid_phase_check(nominal_phase)
        if phs == SinglePhaseKind.NONE or dir_ == PhaseDirection.NONE:
            self.remove_normal(self.phase_normal(nominal_phase), nominal_phase)
            return True

        if self.phase_normal(nominal_phase) == phs and self.direction_normal(nominal_phase) == dir_:
            return False

        self._normal_status = setphs(self._normal_status, phs, dir_, nominal_phase)
        return True

    def set_current(self, phs: SinglePhaseKind, dir_: PhaseDirection, nominal_phase: SinglePhaseKind):
        """
        `phs` The `zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind` to add.
        `nominal_phase` The core number this phase should be applied to
        `dir_` The direction of this phase relative to the location of the `zepben.evolve.iec61970.base.core.terminal.Terminal` to its feeder circuit breaker.
        Returns True if phase status was changed, False otherwise.
        """
        _valid_phase_check(nominal_phase)
        if phs == SinglePhaseKind.NONE or dir_ == PhaseDirection.NONE:
            self.remove_current(self.phase_current(nominal_phase), nominal_phase)
            return True

        if self.phase_current(nominal_phase) == phs and self.direction_current(nominal_phase) == dir_:
            return False

        self._current_status = setphs(self._current_status, phs, dir_, nominal_phase)
        return True

    def remove_normal(self, phs: SinglePhaseKind, nominal_phase: SinglePhaseKind, dir_: PhaseDirection = None):
        """
        `phs` The `zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind` to add.
        `nominal_phase` The core number this phase should be applied to
        `dir_` The direction of this phase relative to the location of the `zepben.evolve.iec61970.base.core.terminal.Terminal` to its feeder circuit breaker.
        Returns True if phase status was changed, False otherwise.
        """
        _valid_phase_check(nominal_phase)
        if phs != self.phase_normal(nominal_phase):
            return False

        if dir_ is not None:
            if not self.direction_normal(nominal_phase).has(dir_):
                return False
            self._normal_status = remove(self._normal_status, phs, dir_, nominal_phase)
        else:
            self._normal_status = remove_all(self._normal_status, nominal_phase)
            return True

    def remove_current(self, phs: SinglePhaseKind, nominal_phase: SinglePhaseKind, dir_: PhaseDirection = None):
        """
        `phs` The `zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind` to add.
        `nominal_phase` The core number this phase should be applied to
        `dir_` The direction of this phase relative to the location of the `zepben.evolve.iec61970.base.core.terminal.Terminal` to its feeder circuit breaker.
        Returns True if phase status was changed, False otherwise.
        """
        _valid_phase_check(nominal_phase)
        if phs != self.phase_current(nominal_phase):
            return False

        if dir_ is not None:
            if not self.direction_current(nominal_phase).has(dir_):
                return False
            self._current_status = remove(self._current_status, phs, dir_, nominal_phase)
        else:
            self._current_status = remove_all(self._current_status, nominal_phase)
            return True

    def copy(self):
        return TracedPhases()
