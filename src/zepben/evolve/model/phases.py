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
from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

__all__ = ["get_phase", "set_phase", "TracedPhases", "NominalPhasePath"]

BITS_TO_PHASE = defaultdict(lambda: SinglePhaseKind.NONE)
BITS_TO_PHASE[0b0001] = SinglePhaseKind.A
BITS_TO_PHASE[0b0010] = SinglePhaseKind.B
BITS_TO_PHASE[0b0100] = SinglePhaseKind.C
BITS_TO_PHASE[0b1000] = SinglePhaseKind.N

PHASE_TO_BITS = defaultdict(lambda: 0)
PHASE_TO_BITS[SinglePhaseKind.A] = 0b0001
PHASE_TO_BITS[SinglePhaseKind.B] = 0b0010
PHASE_TO_BITS[SinglePhaseKind.C] = 0b0100
PHASE_TO_BITS[SinglePhaseKind.N] = 0b1000

NOMINAL_PHASE_MASKS = [0x000f, 0x00f0, 0x0f00, 0xf000]


def _valid_phase_check(nominal_phase):
    if nominal_phase == SinglePhaseKind.NONE or nominal_phase == SinglePhaseKind.INVALID:
        raise ValueError(f"INTERNAL ERROR: Phase {nominal_phase.name} is invalid. Must not be NONE or INVALID.")


def get_phase(status: int, nominal_phase: SinglePhaseKind):
    return BITS_TO_PHASE[(status >> _byte_selector(nominal_phase)) & 0x0f]


def set_phase(status: int, nominal_phase: SinglePhaseKind, traced_phase: SinglePhaseKind) -> int:
    if traced_phase == SinglePhaseKind.NONE:
        return status & ~NOMINAL_PHASE_MASKS[nominal_phase.mask_index]
    else:
        return (status & ~NOMINAL_PHASE_MASKS[nominal_phase.mask_index]) | _shifted_value(nominal_phase, traced_phase)


def _byte_selector(nominal_phase: SinglePhaseKind) -> int:
    return nominal_phase.mask_index * 4


def _shifted_value(nominal_phase: SinglePhaseKind, traced_phase: SinglePhaseKind) -> int:
    return PHASE_TO_BITS[traced_phase] << _byte_selector(nominal_phase)
#todo split file into correct packages

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

    Traced phase status:
    |     integer      |
    | 16 bits |16 bits |
    | current | normal |

    See [TracedPhasesBitManipulation] for details on bit representation for normal and current status.
    """

    phase_status: int = 0
    """
    The underlying implementation value tracking the phase statuses for the current and normal state of the network.
    It is primarily used for data serialisation and debugging within official evolve libraries and utilities.

    NOTE: This property should be considered evolve internal and not for public use as the underlying
          data structure to store the status could change at any time (and thus be a breaking change).
          Use at your own risk.
    """

    _NORMAL_MASK = 0x0000ffff
    _CURRENT_MASK = 0xffff0000
    _CURRENT_SHIFT = 16

    def __str__(self):
        def to_string(select_phase):
            return ', '.join([select_phase(phs).short_name for phs in PhaseCode.ABCN.single_phases])

        return f"TracedPhases(normal={{{to_string(self.normal)}}}, current={{{to_string(self.current)}}})"

    def normal(self, nominal_phase: SinglePhaseKind) -> SinglePhaseKind:
        """
        Get the phase that was traced in the normal state of the network on this nominal phase.

        `nominal_phase` The nominal phase to check.

        Returns The `zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind` traced in the normal state of the network for the nominal phase, or
        SinglePhaseKind.NONE if the nominal phase is de-energised.

        Raises `NominalPhaseException` if the nominal phase is invalid.
        """
        _valid_phase_check(nominal_phase)
        return get_phase(self.phase_status, nominal_phase)

    def current(self, nominal_phase: SinglePhaseKind) -> SinglePhaseKind:
        """
        Get the phase that was traced in the current state of the network on this nominal phase.

        `nominal_phase` The nominal phase to check.

        Returns The `zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind` traced in the current state of the network for the nominal phase, or
        SinglePhaseKind.NONE if the nominal phase is de-energised.

        Raises `NominalPhaseException` if the nominal phase is invalid.
        """
        _valid_phase_check(nominal_phase)
        return get_phase(self.phase_status >> self._CURRENT_SHIFT, nominal_phase)

    def set_normal(self, nominal_phase: SinglePhaseKind, traced_phase: SinglePhaseKind) -> bool:
        """
        Set the phase that was traced in the normal state of the network on this nominal phase.

        `nominal_phase` The nominal phase to use.

        `traced_phase` The traced phase to apply to the nominal phase.

        Returns True if there was a change, otherwise False.

        Raises `PhaseException` if phases cross. i.e. you try to apply more than one phase to a nominal phase.

        Raises `NominalPhaseException` if the nominal phase is invalid.
        """
        it = self.normal(nominal_phase)
        if it == traced_phase:
            return False
        elif (it == SinglePhaseKind.NONE) or (traced_phase == SinglePhaseKind.NONE):
            self.phase_status = (self.phase_status & self._CURRENT_MASK) | set_phase(self.phase_status, nominal_phase, traced_phase)
            return True
        else:
            raise PhaseException("Crossing Phases.")

    def set_current(self, nominal_phase: SinglePhaseKind, traced_phase: SinglePhaseKind) -> bool:
        """
        Set the phase that was traced in the current state of the network on this nominal phase.

        `nominal_phase` The nominal phase to use.

        `traced_phase` The traced phase to apply to the nominal phase.

        Returns True if there was a change, otherwise False.

        Raises `PhaseException` if phases cross. i.e. you try to apply more than one phase to a nominal phase.

        Raises `NominalPhaseException` if the nominal phase is invalid.
        """
        it = self.current(nominal_phase)
        if it == traced_phase:
            return False
        elif (it == SinglePhaseKind.NONE) or (traced_phase == SinglePhaseKind.NONE):
            self.phase_status = (self.phase_status & self._NORMAL_MASK) | (
                    set_phase(self.phase_status >> self._CURRENT_SHIFT, nominal_phase, traced_phase) << self._CURRENT_SHIFT)
            return True
        else:
            raise PhaseException("Crossing Phases.")

    @staticmethod
    def copy():
        return TracedPhases()
