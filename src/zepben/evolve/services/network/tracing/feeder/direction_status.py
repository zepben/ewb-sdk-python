#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["normal_direction", "current_direction", "DirectionStatus", "NormalDirection", "CurrentDirection"]

from abc import ABC, abstractmethod

from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.services.network.tracing.feeder.feeder_direction import FeederDirection


def normal_direction(terminal: Terminal):
    return NormalDirection(terminal)


def current_direction(terminal: Terminal):
    return CurrentDirection(terminal)


class DirectionStatus(ABC):
    """
    Interface to query or set the `FeederDirection` for a `Terminal`.
    """

    @abstractmethod
    def value(self) -> FeederDirection:
        """
        Returns The direction added to this status.
        """
        raise NotImplementedError()

    @abstractmethod
    def set(self, direction: FeederDirection) -> bool:
        """
        Clears the existing direction and sets it to the specified direction.

        `direction` The direction of the `Terminal`.

        Returns True if the direction has been updated, otherwise False.
        """
        raise NotImplementedError

    @abstractmethod
    def add(self, direction: FeederDirection) -> bool:
        """
        Adds the given direction to the `Terminal`.

        `direction` The direction to add to the `Terminal`.

        Returns True if the direction has been updated, otherwise False.
        """
        raise NotImplementedError

    @abstractmethod
    def remove(self, direction: FeederDirection) -> bool:
        """
        Removes the given direction from the `Terminal`.

        `direction` The direction to remove from the `Terminal`.

        Returns True if the direction has been updated, otherwise False.
        """
        raise NotImplementedError


class NormalDirection(DirectionStatus):

    def __init__(self, terminal: Terminal):
        self.terminal = terminal

    def value(self) -> FeederDirection:
        return self.terminal.normal_feeder_direction

    def set(self, direction: FeederDirection) -> bool:
        if self.terminal.normal_feeder_direction == direction:
            return False

        self.terminal.normal_feeder_direction = direction
        return True

    def add(self, direction: FeederDirection) -> bool:
        previous = self.terminal.normal_feeder_direction
        new = previous + direction
        if new == previous:
            return False

        self.terminal.normal_feeder_direction = new
        return True

    def remove(self, direction: FeederDirection) -> bool:
        previous = self.terminal.normal_feeder_direction
        new = previous - direction
        if new == previous:
            return False

        self.terminal.normal_feeder_direction = new
        return True


class CurrentDirection(DirectionStatus):

    def __init__(self, terminal: Terminal):
        self.terminal = terminal

    def value(self) -> FeederDirection:
        return self.terminal.current_feeder_direction

    def set(self, direction: FeederDirection) -> bool:
        if self.terminal.current_feeder_direction == direction:
            return False

        self.terminal.current_feeder_direction = direction
        return True

    def add(self, direction: FeederDirection) -> bool:
        previous = self.terminal.current_feeder_direction
        new = previous + direction
        if new == previous:
            return False

        self.terminal.current_feeder_direction = new
        return True

    def remove(self, direction: FeederDirection) -> bool:
        previous = self.terminal.current_feeder_direction
        new = previous - direction
        if new == previous:
            return False

        self.terminal.current_feeder_direction = new
        return True
