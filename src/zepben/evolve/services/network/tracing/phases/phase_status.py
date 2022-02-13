#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import Terminal

from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from abc import ABC, abstractmethod

__all__ = ["normal_phases", "current_phases", "PhaseStatus", "NormalPhases", "CurrentPhases"]


def normal_phases(terminal: Terminal):
    return NormalPhases(terminal)


def current_phases(terminal: Terminal):
    return CurrentPhases(terminal)


class PhaseStatus(ABC):

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


class NormalPhases(PhaseStatus):
    """
    The traced phases in the normal state of the network.
    """

    def __init__(self, terminal: Terminal):
        self.terminal = terminal

    def __getitem__(self, nominal_phase: SinglePhaseKind) -> SinglePhaseKind:
        return self.terminal.traced_phases.normal(nominal_phase)

    def __setitem__(self, nominal_phase: SinglePhaseKind, traced_phase: SinglePhaseKind) -> bool:
        return self.terminal.traced_phases.set_normal(nominal_phase, traced_phase)


class CurrentPhases(PhaseStatus):
    """
    The traced phases in the current state of the network.
    """

    def __init__(self, terminal: Terminal):
        self.terminal = terminal

    def __getitem__(self, nominal_phase: SinglePhaseKind) -> SinglePhaseKind:
        return self.terminal.traced_phases.current(nominal_phase)

    def __setitem__(self, nominal_phase: SinglePhaseKind, traced_phase: SinglePhaseKind) -> bool:
        return self.terminal.traced_phases.set_current(nominal_phase, traced_phase)
