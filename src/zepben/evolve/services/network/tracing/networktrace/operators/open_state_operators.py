#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import TypeVar, Optional, TYPE_CHECKING

from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

from abc import abstractmethod

from zepben.evolve.services.network.tracing.networktrace.conditions.open_condition import OpenCondition
from zepben.evolve.services.network.tracing.networktrace.network_trace_queue_condition import NetworkTraceQueueCondition
from zepben.evolve.services.network.tracing.networktrace.operators import StateOperator

if TYPE_CHECKING:
    from zepben.evolve.model.cim.iec61970.base.wires.switch import Switch

    T = TypeVar('T')


class OpenStateOperators(StateOperator):
    """
    Interface for managing the open state of conducting equipment, typically switches.
    """

    @staticmethod
    @abstractmethod
    def is_open(switch: Switch, phase: SinglePhaseKind=None) -> bool:
        """
        Checks if the specified switch is open. Optionally checking the state of a specific phase.

        `switch` The switch to check open state.
        `phase` The specific phase to check, or `null` to check if any phase is open.
        Returns `true` if open; `false` otherwise.
        """
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def set_open(switch: Switch, is_open: bool, phase: SinglePhaseKind=None) -> None:
        """
        Sets the open state of the specified switch. Optionally applies the state to a specific phase.

        `switch` The switch for which to set the open state.
        `isOpen` The desired open state (`true` for open, `false` for closed).
        `phase` The specific phase to set, or `null` to apply to all phases.
        """
        pass

    @classmethod
    def stop_at_open(cls) -> NetworkTraceQueueCondition[T]:
        return OpenCondition(cls.is_open)


class NormalOpenStateOperators(OpenStateOperators):
    """
    Operates on the normal state of the `Switch`
    """
    @staticmethod
    def is_open(switch: Switch, phase:SinglePhaseKind=None) -> Optional[bool]:
        try:
            return switch.is_normally_open(phase)
        except AttributeError:
            return False

    @staticmethod
    def set_open(switch: Switch, is_open: bool, phase: SinglePhaseKind = None) -> None:
        switch.set_normally_open(is_open, phase)


class CurrentOpenStateOperators(OpenStateOperators):
    """
    Operates on the current state of the `Switch`
    """
    @staticmethod
    def is_open(switch: Switch, phase: SinglePhaseKind = None) -> Optional[bool]:
        try:
            return switch.is_open(phase)
        except AttributeError:
            return False

    @staticmethod
    def set_open(switch: Switch, is_open: bool, phase: SinglePhaseKind = None) -> None:
        switch.set_open(is_open, phase)


OpenStateOperators.NORMAL = NormalOpenStateOperators()
OpenStateOperators.CURRENT = CurrentOpenStateOperators()