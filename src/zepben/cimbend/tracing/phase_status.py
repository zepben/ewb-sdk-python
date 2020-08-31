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


from zepben.cimbend.cim.iec61970.base.wires import SinglePhaseKind
from zepben.cimbend.phases.direction import Direction
from abc import ABC, abstractmethod

__all__ = ["normal_phases", "current_phases", "PhaseStatus", "NormalPhases", "CurrentPhases"]


def normal_phases(terminal, core_num):
    return NormalPhases(terminal, core_num)


def current_phases(terminal, core_num):
    return CurrentPhases(terminal, core_num)


class PhaseStatus(ABC):

    @abstractmethod
    def phase(self):
        """
        :return: The phase added to this status
        """
        raise NotImplementedError()

    @abstractmethod
    def direction(self):
        """
        :return: The direction added to this status.
        """
        raise NotImplementedError()

    @abstractmethod
    def set(self, phase: SinglePhaseKind, direction: Direction):
        """
        Clears the phase and sets it to the specified phase and direction.
        If the passed in phase is NONE or the passed in direction is NONE, this should clear the phase status.
        :param phase: The new phase to be set.
        :param direction: The direction of the phase.
        """
        raise NotImplementedError()

    @abstractmethod
    def add(self, phase: SinglePhaseKind, direction: Direction):
        """
        Adds a phase to the status with the given direction.
        :param phase: The phase to be added.
        :param direction: The direction of the phase.
        :return: True if the phase or direction has been updated
        """
        raise NotImplementedError()

    @abstractmethod
    def remove(self, phase: SinglePhaseKind, direction: Direction = None):
        """
        Removes a phase from the status. If direction is supplied will remove phase matching the direction.
        :param phase: The phase to be removed.
        :param direction: The direction to match with the phase being removed.
        :return: True if the phase or direction has been removed.
        """
        raise NotImplementedError()


class NormalPhases(PhaseStatus):

    def __init__(self, terminal, core_num):
        self.terminal = terminal
        self.core_num = core_num

    def phase(self):
        return self.terminal.phases.phase_normal(self.core_num)

    def direction(self):
        return self.terminal.phases.direction_normal(self.core_num)

    def set(self, phase_kind: SinglePhaseKind, dir: Direction):
        return self.terminal.phases.set_normal(phase_kind, self.core_num, dir)

    def add(self, phase_kind: SinglePhaseKind, dir: Direction):
        return self.terminal.phases.add_normal(phase_kind, self.core_num, dir)

    def remove(self, phase_kind: SinglePhaseKind, dir: Direction = None):
        if dir is not None:
            return self.terminal.phases.remove_normal(phase_kind, self.core_num, dir)
        else:
            return self.terminal.phases.remove_normal(phase_kind, self.core_num)


class CurrentPhases(PhaseStatus):

    def __init__(self, terminal, core_num):
        self.terminal = terminal
        self.core_num = core_num

    def phase(self):
        return self.terminal.phases.phase_current(self.core_num)

    def direction(self):
        return self.terminal.phases.direction_current(self.core_num)

    def set(self, phase_kind: SinglePhaseKind, dir: Direction):
        return self.terminal.phases.set_current(phase_kind, self.core_num, dir)

    def add(self, phase_kind: SinglePhaseKind, dir: Direction):
        return self.terminal.phases.add_current(phase_kind, self.core_num, dir)

    def remove(self, phase_kind: SinglePhaseKind, dir: Direction = None):
        if dir is not None:
            return self.terminal.phases.remove_current(phase_kind, self.core_num, dir)
        else:
            return self.terminal.phases.remove_current(phase_kind, self.core_num)

