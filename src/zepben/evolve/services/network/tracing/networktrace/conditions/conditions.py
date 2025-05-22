#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Type

from zepben.evolve.services.network.tracing.feeder.feeder_direction import FeederDirection
from zepben.evolve.services.network.tracing.networktrace.conditions.direction_condition import DirectionCondition
from zepben.evolve.services.network.tracing.networktrace.conditions.equipment_step_limit_condition import EquipmentStepLimitCondition
from zepben.evolve.services.network.tracing.networktrace.conditions.equipment_type_step_limit_condition import EquipmentTypeStepLimitCondition

T = TypeVar('T')

if TYPE_CHECKING:
    from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
    from zepben.evolve.services.network.tracing.traversal.queue_condition import QueueCondition
    from zepben.evolve.services.network.tracing.traversal.stop_condition import StopCondition
    from zepben.evolve import ConductingEquipment

    NetworkTraceQueueCondition = QueueCondition[NetworkTraceStep[T]]
    NetworkTraceStopCondition = StopCondition[NetworkTraceStep[T]]


# FIXME: work out how to inject NetworkStateOperators into this from inside NetworkTrace
class Conditions:
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
        return DirectionCondition(direction, cls)  # FIXME: cls should be NetworkStateOperators, somehow need
                                                   #   to load these methods onto there after passing them to NetworkTrace

    @staticmethod
    def limit_equipment_steps(limit: int, equipment_type: Type[ConductingEquipment]=None) -> NetworkTraceStopCondition[T]:
        """
        Creates a [NetworkTrace] condition that stops tracing a path once a specified number of equipment steps have been reached.

        :param limit: The maximum number of equipment steps allowed before stopping.
        :param equipment_type: The class of the equipment type to track against the limit

        :return: A [NetworkTraceStopCondition] that stops tracing the path once the step limit is reached.
        """
        if equipment_type is not None:
            return EquipmentTypeStepLimitCondition(limit, equipment_type)
        return EquipmentStepLimitCondition(limit)

