#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import TYPE_CHECKING, Callable, TypeVar

from zepben.protobuf.cim.iec61970.base.core.Terminal_pb2 import Terminal

from zepben.evolve.services.network.tracing.feeder.feeder_direction import FeederDirection


from abc import abstractmethod

__all__ = ['FeederDirectionStateOperations', 'NormalFeederDirectionStateOperations', 'CurrentFeederDirectionStateOperations']

from zepben.evolve.services.network.tracing.networktrace.conditions.direction_condition import DirectionCondition
from zepben.evolve.services.network.tracing.networktrace.network_trace_queue_condition import NetworkTraceQueueCondition
from zepben.evolve.services.network.tracing.networktrace.operators import StateOperator

T = TypeVar('T')

class FeederDirectionStateOperations(StateOperator):
    """
    Interface for accessing and managing the [FeederDirection] associated with [Terminal]s.
    """

    @abstractmethod
    def get_direction(self, terminal: Terminal) -> FeederDirection:
        """
        Retrieves the feeder direction for the specified terminal.

        `terminal` The terminal for which to retrieve the feeder direction.
        Returns The current feeder direction associated with the specified terminal.
        """
        pass

    @abstractmethod
    def set_direction(self, terminal: Terminal, direction: FeederDirection) -> bool:
        """
        Sets the feeder direction for the specified terminal.

        `terminal` The terminal for which to set the feeder direction.
        `direction` The new feeder direction to assign to the terminal.
        Returns `true` if the direction was changed; `false` if the direction was already set to the specified value.
        """
        pass

    @abstractmethod
    def add_direction(self, terminal: Terminal, direction: FeederDirection) -> bool:
        """
        Adds the specified feeder direction to the terminal, preserving existing directions.

        `terminal` The terminal for which to add the feeder direction.
        `direction` The feeder direction to add.
        Returns `true` if the direction was added successfully; `false` if the direction was already present.
        """
        pass


    @abstractmethod
    def remove_direction(self, terminal: Terminal, direction: FeederDirection) -> bool:
        """
        Removes the specified feeder direction from the terminal.

        `terminal` The terminal for which to remove the feeder direction.
        `direction` The feeder direction to remove.
        Returns `true` if the direction was removed; `false` if the direction was not present.
        """
        pass

    @classmethod
    def upstream(cls, get_direction: Callable[[Terminal], FeederDirection]) -> NetworkTraceQueueCondition[T]:
        return cls.with_direction(FeederDirection.UPSTREAM, get_direction)

    @classmethod
    def downstream(cls, get_direction: Callable[[Terminal], FeederDirection]) -> NetworkTraceQueueCondition[T]:
        return cls.with_direction(FeederDirection.DOWNSTREAM, get_direction)

    @staticmethod
    def with_direction(direction: FeederDirection, get_direction: Callable[[Terminal], FeederDirection]) -> NetworkTraceQueueCondition[T]:
        return DirectionCondition(direction, get_direction)

class NormalFeederDirectionStateOperations(FeederDirectionStateOperations):
    def get_direction(self, terminal: Terminal) -> FeederDirection:
        return terminal.normal_feeder_direction

    def set_direction(self, terminal: Terminal, direction: FeederDirection) -> bool:
        if terminal.normal_feeder_direction == direction:
            return False

        terminal.normal_feeder_direction = direction
        return True

    def add_direction(self, terminal: Terminal, direction: FeederDirection) -> bool:
        previous = terminal.normal_feeder_direction
        new = previous + direction
        if new == previous:
            return False

        terminal.normal_feeder_direction = new
        return True

    def remove_direction(self, terminal: Terminal, direction: FeederDirection) -> bool:
        previous = terminal.normal_feeder_direction
        new = previous - direction
        if new == previous:
            return False

        terminal.normal_feeder_direction = new
        return True


class CurrentFeederDirectionStateOperations(FeederDirectionStateOperations):
    def get_direction(self, terminal: Terminal) -> FeederDirection:
        return terminal.current_feeder_direction

    def set_direction(self, terminal: Terminal, direction: FeederDirection) -> bool:
        if terminal.current_feeder_direction == direction:
            return False

        terminal.current_feeder_direction = direction
        return True

    def add_direction(self, terminal: Terminal, direction: FeederDirection) -> bool:
        previous = terminal.current_feeder_direction
        new = previous + direction
        if new == previous:
            return False

        terminal.current_feeder_direction = new
        return True

    def remove_direction(self, terminal: Terminal, direction: FeederDirection) -> bool:
        previous = terminal.current_feeder_direction
        new = previous - direction
        if new == previous:
            return False

        terminal.current_feeder_direction = new
        return True

FeederDirectionStateOperations.NORMAL = NormalFeederDirectionStateOperations()
FeederDirectionStateOperations.CURRENT = CurrentFeederDirectionStateOperations()
