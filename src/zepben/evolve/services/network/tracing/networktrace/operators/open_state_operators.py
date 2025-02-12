#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.


from zepben.evolve.model.cim.iec61970.base.wires.switch import Switch, SinglePhaseKind
from zepben.evolve.services.network.tracing.networktrace.operators import StateOperator

from abc import abstractmethod



class OpenStateOperators(StateOperator):
    """
    Interface for managing the open state of conducting equipment, typically switches.
    """

    @abstractmethod
    def is_open(self, switch: Switch, phase: SinglePhaseKind=None) -> bool:
        """
        Checks if the specified switch is open. Optionally checking the state of a specific phase.

        `switch` The switch to check open state.
        `phase` The specific phase to check, or `null` to check if any phase is open.
        Returns `true` if open; `false` otherwise.
        """
        pass

    @abstractmethod
    def set_open(self, switch: Switch, is_open: bool, phase: SinglePhaseKind=None) -> None:
        """
        Sets the open state of the specified switch. Optionally applies the state to a specific phase.

        `switch` The switch for which to set the open state.
        `isOpen` The desired open state (`true` for open, `false` for closed).
        `phase` The specific phase to set, or `null` to apply to all phases.
        """
        pass


class NormalOpenStateOperators(OpenStateOperators):
    """
    Operates on the normal state of the `Switch`
    """
    def is_open(self, switch: Switch, phase:SinglePhaseKind=None) -> bool:
        return switch.is_normally_open(phase)

    def set_open(self, switch: Switch, is_open: bool, phase: SinglePhaseKind=None) -> None:
        switch.set_normally_open(is_open, phase)


class CurrentOpenStateOperators(OpenStateOperators):
    """
    Operates on the current state of the `Switch`
    """
    def is_open(self, switch: Switch, phase: SinglePhaseKind=None) -> bool:
        return switch.is_open(phase)

    def set_open(self, switch: Switch, is_open: bool, phase: SinglePhaseKind=None) -> None:
        switch.set_open(is_open, phase)


OpenStateOperators.NORMAL = NormalOpenStateOperators()
OpenStateOperators.CURRENT = CurrentOpenStateOperators()