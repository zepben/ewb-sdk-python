#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import TYPE_CHECKING

from zepben.evolve.services.network.tracing.networktrace.operators import StateOperator
from zepben.evolve.services.network.tracing.phases.phase_status import PhaseStatus

from abc import abstractmethod

if TYPE_CHECKING:
    from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal

__all__ = ['PhaseStateOperators', 'NormalPhaseStateOperators', 'CurrentPhaseStateOperators']


class PhaseStateOperators(StateOperator):
    """
    Interface for accessing the phase status of a terminal.
    """

    @staticmethod
    @abstractmethod
    def phase_status(terminal: 'Terminal') -> PhaseStatus:
        """
        Retrieves the phase status of the specified terminal.

        `terminal` The terminal for which to retrieve the phase status.
        Returns The phase status associated with the specified terminal.
        """
        pass


class NormalPhaseStateOperators(PhaseStateOperators):
    """
    Operates on the normal state of the `Phase`
    """
    @staticmethod
    def phase_status(terminal: 'Terminal') -> PhaseStatus:
        return terminal.normal_phases


class CurrentPhaseStateOperators(PhaseStateOperators):
    """
    Operates on the current state of the `Phase`
    """
    @staticmethod
    def phase_status(terminal: 'Terminal') -> PhaseStatus:
        return terminal.current_phases


PhaseStateOperators.NORMAL = NormalPhaseStateOperators
PhaseStateOperators.CURRENT = CurrentPhaseStateOperators
