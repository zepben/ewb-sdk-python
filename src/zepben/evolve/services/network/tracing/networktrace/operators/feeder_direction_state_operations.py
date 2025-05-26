#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, TypeVar

from zepben.evolve.services.network.tracing.feeder.feeder_direction import FeederDirection

if TYPE_CHECKING:
    from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
    from zepben.evolve.services.network.tracing.networktrace.conditions.network_trace_queue_condition import NetworkTraceQueueCondition

__all__ = ['FeederDirectionStateOperations', 'NormalFeederDirectionStateOperations', 'CurrentFeederDirectionStateOperations']

from zepben.evolve.services.network.tracing.networktrace.conditions.direction_condition import DirectionCondition
from zepben.evolve.services.network.tracing.networktrace.operators import StateOperator

T = TypeVar('T')

class FeederDirectionStateOperations(StateOperator):
    """
    Interface for accessing and managing the [FeederDirection] associated with [Terminal]s.
    """

    @staticmethod
    @abstractmethod
    def get_direction(terminal: Terminal) -> FeederDirection:
        """
        Retrieves the feeder direction for the specified terminal.

        :param terminal: The terminal for which to retrieve the feeder direction.

        :return: The current feeder direction associated with the specified terminal.
        """
        pass

    @staticmethod
    @abstractmethod
    def set_direction(terminal: Terminal, direction: FeederDirection) -> bool:
        """
        Sets the feeder direction for the specified terminal.

        :param terminal: The terminal for which to set the feeder direction.
        :param direction: The new feeder direction to assign to the terminal.

        :return: `True` if the direction was changed; `false` if the direction was already set to the specified value.
        """
        pass

    @staticmethod
    @abstractmethod
    def add_direction(terminal: Terminal, direction: FeederDirection) -> bool:
        """
        Adds the specified feeder direction to the terminal, preserving existing directions.

        :param terminal: The terminal for which to add the feeder direction.
        :param direction: The feeder direction to add.

        :return: `True` if the direction was added successfully; `false` if the direction was already present.
        """
        pass


    @staticmethod
    @abstractmethod
    def remove_direction(terminal: Terminal, direction: FeederDirection) -> bool:
        """
        Removes the specified feeder direction from the terminal.

        :param terminal: The terminal for which to remove the feeder direction.
        :param direction: The feeder direction to remove.

        :return: `true` if the direction was removed; `false` if the direction was not present.
        """
        pass

    @classmethod
    def upstream(cls) -> NetworkTraceQueueCondition[T]:
        """
        Creates a [NetworkTrace] condition that will cause tracing a feeder upstream (towards the head terminal).
        This uses [FeederDirectionStateOperations.get_direction] receiver instance method within the condition.

        :return: [NetworkTraceQueueCondition] that results in upstream tracing.
        """
        return cls.with_direction(FeederDirection.UPSTREAM)

    @classmethod
    def downstream(cls) -> NetworkTraceQueueCondition[T]:
        """
        Creates a [NetworkTrace] condition that will cause tracing a feeder downstream (away from the head terminal).
        This uses [FeederDirectionStateOperations.get_direction] receiver instance method within the condition.

        :return: [NetworkTraceQueueCondition] that results in downstream tracing.
        """
        return cls.with_direction(FeederDirection.DOWNSTREAM)

    @classmethod
    def with_direction(cls, direction: FeederDirection) -> NetworkTraceQueueCondition[T]:
        """
        Creates a [NetworkTrace] condition that will cause tracing only terminals with directions that match [direction].
        This uses [FeederDirectionStateOperations.get_direction] receiver instance method within the condition.

        :return: [NetworkTraceQueueCondition] that results in upstream tracing.
        """
        return DirectionCondition(direction, cls)

class NormalFeederDirectionStateOperations(FeederDirectionStateOperations):
    @staticmethod
    def get_direction(terminal: Terminal) -> FeederDirection:
        return terminal.normal_feeder_direction

    @staticmethod
    def set_direction(terminal: Terminal, direction: FeederDirection) -> bool:
        if terminal.normal_feeder_direction == direction:
            return False

        terminal.normal_feeder_direction = direction
        return True

    @staticmethod
    def add_direction(terminal: Terminal, direction: FeederDirection) -> bool:
        previous = terminal.normal_feeder_direction
        new = previous + direction
        if new == previous:
            return False

        terminal.normal_feeder_direction = new
        return True

    @staticmethod
    def remove_direction(terminal: Terminal, direction: FeederDirection) -> bool:
        previous = terminal.normal_feeder_direction
        new = previous - direction
        if new == previous:
            return False

        terminal.normal_feeder_direction = new
        return True


class CurrentFeederDirectionStateOperations(FeederDirectionStateOperations):
    @staticmethod
    def get_direction(terminal: Terminal) -> FeederDirection:
        return terminal.current_feeder_direction

    @staticmethod
    def set_direction(terminal: Terminal, direction: FeederDirection) -> bool:
        if terminal.current_feeder_direction == direction:
            return False

        terminal.current_feeder_direction = direction
        return True

    @staticmethod
    def add_direction(terminal: Terminal, direction: FeederDirection) -> bool:
        previous = terminal.current_feeder_direction
        new = previous + direction
        if new == previous:
            return False

        terminal.current_feeder_direction = new
        return True

    @staticmethod
    def remove_direction(terminal: Terminal, direction: FeederDirection) -> bool:
        previous = terminal.current_feeder_direction
        new = previous - direction
        if new == previous:
            return False

        terminal.current_feeder_direction = new
        return True

FeederDirectionStateOperations.NORMAL = NormalFeederDirectionStateOperations
FeederDirectionStateOperations.CURRENT = CurrentFeederDirectionStateOperations
