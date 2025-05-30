#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Type, Callable

from zepben.evolve.services.network.tracing.feeder.feeder_direction import FeederDirection
from zepben.evolve.services.network.tracing.networktrace.conditions.direction_condition import DirectionCondition
from zepben.evolve.services.network.tracing.networktrace.conditions.equipment_step_limit_condition import EquipmentStepLimitCondition
from zepben.evolve.services.network.tracing.networktrace.conditions.equipment_type_step_limit_condition import EquipmentTypeStepLimitCondition

T = TypeVar('T')

if TYPE_CHECKING:
    from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
    from zepben.evolve.services.network.tracing.traversal.queue_condition import QueueCondition
    from zepben.evolve.services.network.tracing.traversal.stop_condition import StopCondition
    from zepben.evolve import ConductingEquipment, NetworkStateOperators

    DSLLambda = Callable[[NetworkStateOperators], QueueCondition[NetworkTraceStep[T]]]

__all__ = ['upstream', 'downstream', 'with_direction', 'limit_equipment_steps', 'stop_at_open']


def upstream() -> DSLLambda:
    """
    Creates a [NetworkTrace] condition that will cause tracing a feeder upstream (towards the head terminal).
    This uses [FeederDirectionStateOperations.get_direction] receiver instance method within the condition.

    :return: [NetworkTraceQueueCondition] that results in upstream tracing.
    """
    return lambda state_operator: state_operator.with_direction(FeederDirection.UPSTREAM)

def downstream() -> DSLLambda:
    """
    Creates a [NetworkTrace] condition that will cause tracing a feeder downstream (away from the head terminal).
    This uses [FeederDirectionStateOperations.get_direction] receiver instance method within the condition.

    :return: [NetworkTraceQueueCondition] that results in downstream tracing.
    """
    return lambda state_operator: state_operator.with_direction(FeederDirection.DOWNSTREAM)

def with_direction(direction: FeederDirection) -> DSLLambda:
    """
    Creates a [NetworkTrace] condition that will cause tracing only terminals with directions that match [direction].
    This uses [FeederDirectionStateOperations.get_direction] receiver instance method within the condition.

    :return: [NetworkTraceQueueCondition] that results in upstream tracing.
    """
    return lambda state_operator: DirectionCondition(direction, state_operator)

def limit_equipment_steps(limit: int, equipment_type: Type[ConductingEquipment]=None) -> StopCondition[NetworkTraceStep[T]]:
    """
    Creates a [NetworkTrace] condition that stops tracing a path once a specified number of equipment steps have been reached.

    :param limit: The maximum number of equipment steps allowed before stopping.
    :param equipment_type: The class of the equipment type to track against the limit

    :return: A [NetworkTraceStopCondition] that stops tracing the path once the step limit is reached.
    """
    if equipment_type is not None:
        return EquipmentTypeStepLimitCondition(limit, equipment_type)
    return EquipmentStepLimitCondition(limit)

def stop_at_open():
    return lambda state_operator: state_operator.stop_at_open()

