#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import TypeVar, Optional, TYPE_CHECKING, Callable

from abc import abstractmethod

from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.services.network.tracing.networktrace.conditions.open_condition import OpenCondition
from zepben.evolve.services.network.tracing.networktrace.conditions.network_trace_queue_condition import NetworkTraceQueueCondition
from zepben.evolve.services.network.tracing.networktrace.operators import StateOperator

if TYPE_CHECKING:
    from zepben.evolve.model.cim.iec61970.base.wires.switch import Switch
    from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment

    T = TypeVar('T')

__all__ = ['OpenStateOperators', 'NormalOpenStateOperators', 'CurrentOpenStateOperators']


class OpenStateOperators(StateOperator):
    """
    Interface for managing the open state of conducting equipment, typically switches.
    """

    @staticmethod
    @abstractmethod
    def is_open_switch(switch: Switch, phase: SinglePhaseKind=None) -> bool:
        """
        Checks if the specified switch is open. Optionally checking the state of a specific phase.

        `switch` The switch to check open state.
        `phase` The specific phase to check, or `null` to check if any phase is open.
        Returns `True` if open; `False` otherwise.
        """
        raise NotImplementedError()

    @classmethod
    def is_open(cls, conducting_equipment: ConductingEquipment, phase: SinglePhaseKind=None) -> bool:
        """
        Convenience method that checks if the `conducting_equipment` is a `Switch` before checking if its open

        :param conducting_equipment: The conducting equipment to check open state
        :param phase: The specified phase to check, or 'None' to check if any phase is open
        Returns `True` if conducting equipment is a switch and its open; `False`  otherwise
        """
        from zepben.evolve.model.cim.iec61970.base.wires.switch import Switch  # FIXME: circular import

        if isinstance(conducting_equipment, Switch):
            return cls.is_open_switch(conducting_equipment, phase)
        return False

    @staticmethod
    @abstractmethod
    def set_open(switch: Switch, is_open: bool, phase: SinglePhaseKind=None) -> None:
        """
        Sets the open state of the specified switch. Optionally applies the state to a specific phase.

        `switch` The switch for which to set the open state.
        `isOpen` The desired open state (`True` for open, `False` for closed).
        `phase` The specific phase to set, or `None` to apply to all phases.
        """
        raise NotImplementedError()

    @classmethod
    def stop_at_open(cls, open_test: Optional[Callable[[Switch, Optional[SinglePhaseKind]], bool]]=None, phase: Optional[SinglePhaseKind]=None) -> NetworkTraceQueueCondition[T]:
        return OpenCondition(open_test or cls.is_open, phase)


class NormalOpenStateOperators(OpenStateOperators):
    """
    Operates on the normal state of the `Switch`
    """
    @staticmethod
    def is_open_switch(switch: Switch, phase:SinglePhaseKind=None) -> Optional[bool]:
        return switch.is_normally_open(phase)

    @staticmethod
    def set_open(switch: Switch, is_open: bool, phase: SinglePhaseKind = None) -> None:
        switch.set_normally_open(is_open, phase)


class CurrentOpenStateOperators(OpenStateOperators):
    """
    Operates on the current state of the `Switch`
    """
    @staticmethod
    def is_open_switch(switch: Switch, phase: SinglePhaseKind = None) -> Optional[bool]:
        return switch.is_open(phase)

    @staticmethod
    def set_open(switch: Switch, is_open: bool, phase: SinglePhaseKind = None) -> None:
        switch.set_open(is_open, phase)


OpenStateOperators.NORMAL = NormalOpenStateOperators
OpenStateOperators.CURRENT = CurrentOpenStateOperators
