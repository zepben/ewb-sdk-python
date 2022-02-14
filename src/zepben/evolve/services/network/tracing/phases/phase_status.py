#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from zepben.evolve import Terminal
from zepben.evolve.model.cim.iec61970.base.core.phase_code import phase_code_from_single_phases, PhaseCode

from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from abc import ABC, abstractmethod

__all__ = ["normal_phases", "current_phases", "PhaseStatus", "NormalPhases", "CurrentPhases"]


def normal_phases(terminal: Terminal):
    return NormalPhases(terminal)


def current_phases(terminal: Terminal):
    return CurrentPhases(terminal)


class PhaseStatus(ABC):

    terminal: Terminal

    def __init__(self, terminal: Terminal):
        self.terminal = terminal

    @abstractmethod
    def __getitem__(self, nominal_phase: SinglePhaseKind) -> SinglePhaseKind:
        """
        Get the traced phase for the specified `nominal_phase`.

        `nominal_phase` The nominal phase you are interested in querying.

        Returns the traced phase.
        """
        raise NotImplementedError()

    @abstractmethod
    def __setitem__(self, nominal_phase: SinglePhaseKind, traced_phase: SinglePhaseKind) -> bool:
        """
        Set the traced phase for the specified `nominal_phase`.

        `nominal_phase` The nominal phase you are interested in updating.

        `traced_phase` The phase you wish to set for this `nominal_phase`. Specify `SinglePhaseKind.NONE` to clear the phase.

        Returns True if the phase is updated, otherwise False.
        """
        raise NotImplementedError()

    def as_phase_code(self) -> Optional[PhaseCode]:
        """
        Get the traced phase for each nominal phase as a `PhaseCode`.

        Returns The `PhaseCode` if the combination of phases makes sense, otherwise `None`.
        """
        traced_phases = [self[it] for it in self.terminal.phases]
        phases = set(traced_phases)

        if phases == {SinglePhaseKind.NONE}:
            return PhaseCode.NONE
        elif SinglePhaseKind.NONE in phases:
            return None
        elif len(phases) == len(traced_phases):
            return phase_code_from_single_phases(phases)
        else:
            return None


class NormalPhases(PhaseStatus):
    """
    The traced phases in the normal state of the network.
    """

    def __getitem__(self, nominal_phase: SinglePhaseKind) -> SinglePhaseKind:
        return self.terminal.traced_phases.normal(nominal_phase)

    def __setitem__(self, nominal_phase: SinglePhaseKind, traced_phase: SinglePhaseKind) -> bool:
        return self.terminal.traced_phases.set_normal(nominal_phase, traced_phase)


class CurrentPhases(PhaseStatus):
    """
    The traced phases in the current state of the network.
    """

    def __getitem__(self, nominal_phase: SinglePhaseKind) -> SinglePhaseKind:
        return self.terminal.traced_phases.current(nominal_phase)

    def __setitem__(self, nominal_phase: SinglePhaseKind, traced_phase: SinglePhaseKind) -> bool:
        return self.terminal.traced_phases.set_current(nominal_phase, traced_phase)
