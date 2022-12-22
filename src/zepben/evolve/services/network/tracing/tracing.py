#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from zepben.evolve.services.network.tracing.connectivity.connected_equipment_trace import new_connected_equipment_trace, \
    new_connected_equipment_breadth_trace, new_normal_connected_equipment_trace, new_current_connected_equipment_trace, \
    new_normal_limited_connected_equipment_trace, new_current_limited_connected_equipment_trace, new_normal_downstream_equipment_trace, \
    new_current_downstream_equipment_trace, new_normal_upstream_equipment_trace, new_current_upstream_equipment_trace
from zepben.evolve.services.network.tracing.connectivity.connected_equipment_traversal import ConnectedEquipmentTraversal
from zepben.evolve.services.network.tracing.connectivity.connectivity_trace import create_connectivity_traversal
from zepben.evolve.services.network.tracing.connectivity.limited_connected_equipment_trace import LimitedConnectedEquipmentTrace
from zepben.evolve.services.network.tracing.feeder.assign_to_feeders import AssignToFeeders
from zepben.evolve.services.network.tracing.feeder.assign_to_lv_feeders import AssignToLvFeeders
from zepben.evolve.services.network.tracing.feeder.direction_status import normal_direction, current_direction
from zepben.evolve.services.network.tracing.feeder.remove_direction import RemoveDirection
from zepben.evolve.services.network.tracing.feeder.set_direction import SetDirection
from zepben.evolve.services.network.tracing.find_swer_equipment import FindSwerEquipment
from zepben.evolve.services.network.tracing.phases.phase_inferrer import PhaseInferrer
from zepben.evolve.services.network.tracing.phases.phase_trace import new_phase_trace, new_downstream_phase_trace, new_upstream_phase_trace
from zepben.evolve.services.network.tracing.phases.remove_phases import RemovePhases
from zepben.evolve.services.network.tracing.phases.set_phases import SetPhases
from zepben.evolve.services.network.tracing.traversals.basic_traversal import BasicTraversal
from zepben.evolve.services.network.tracing.traversals.queue import breadth_first, Queue, depth_first
from zepben.evolve.services.network.tracing.tree.downstream_tree import DownstreamTree
from zepben.evolve.services.network.tracing.util import ignore_open, normally_open, currently_open
if TYPE_CHECKING:
    from zepben.evolve import ConnectivityResult, PhaseStep, ConductingEquipment
    from zepben.evolve.types import QueueNext
    T = TypeVar("T")

__all__ = ["create_basic_depth_trace", "create_basic_breadth_trace", "connected_equipment_trace", "connected_equipment_breadth_trace",
           "normal_connected_equipment_trace", "current_connected_equipment_trace", "normal_limited_connected_equipment_trace",
           "current_limited_connected_equipment_trace", "normal_downstream_equipment_trace", "current_downstream_equipment_trace",
           "normal_upstream_equipment_trace", "current_upstream_equipment_trace", "connectivity_trace", "connectivity_breadth_trace",
           "normal_connectivity_trace", "current_connectivity_trace", "phase_trace", "normal_phase_trace", "current_phase_trace", "normal_downstream_trace",
           "current_downstream_trace", "normal_upstream_trace", "current_upstream_trace", "normal_downstream_tree", "current_downstream_tree", "set_phases",
           "remove_phases", "set_direction", "remove_direction", "phase_inferrer", "assign_equipment_to_feeders", "assign_equipment_to_lv_feeders",
           "find_swer_equipment"]


# --- Helper functions that create depth-first/breadth-first traversals ---

def create_basic_depth_trace(queue_next: QueueNext[T]) -> BasicTraversal[T]:
    """
    Create a `BasicTraversal` using the `queue_next` function and a depth first queue (LIFO).

    :param queue_next: The function used to add items to the trace queue.
    :return: The `BasicTraversal`
    """
    # noinspection PyArgumentList
    return BasicTraversal(queue_next=queue_next)


def create_basic_breadth_trace(queue_next: QueueNext[T]) -> BasicTraversal[T]:
    """
    Create a `BasicTraversal` using the `queue_next` function and a breadth first queue (FIFO).

    :param queue_next: The function used to add items to the trace queue.
    :return: The `BasicTraversal`
    """
    # noinspection PyArgumentList
    return BasicTraversal(queue_next=queue_next, process_queue=breadth_first())


# --- Traversals for conducting equipment ---

def connected_equipment_trace() -> ConnectedEquipmentTraversal:
    """
    Creates a new traversal that traces equipment that are connected. This ignores phases, open status etc.
    It is purely to trace equipment that are connected in any way.

    :return: The new traversal instance.
    """
    return new_connected_equipment_trace()


def connected_equipment_breadth_trace() -> ConnectedEquipmentTraversal:
    """
    Creates a new traversal that traces equipment that are connected. This ignores phases, open status etc.
    It is purely to trace equipment that are connected in any way.

    :return: The new `ConnectedEquipmentTraversal` instance.
    """
    return new_connected_equipment_breadth_trace()


def normal_connected_equipment_trace() -> ConnectedEquipmentTraversal:
    """
    Creates a new traversal that traces equipment that are connected at normally open points.

    :return: The new `ConnectedEquipmentTraversal` instance.
    """
    return new_normal_connected_equipment_trace()


def current_connected_equipment_trace() -> ConnectedEquipmentTraversal:
    """
    Creates a new traversal that traces equipment that are connected at currently open points.

    :return: The new `ConnectedEquipmentTraversal` instance.
    """
    return new_current_connected_equipment_trace()


def normal_limited_connected_equipment_trace() -> LimitedConnectedEquipmentTrace:
    """
    Creates a new limited traversal that traces equipment that are connected stopping at normally open points. This ignores phases etc.
    It is purely to trace equipment that are connected in any way.

    The trace can be limited by the number of steps, or the feeder direction.

    :return: The new `LimitedConnectedEquipmentTrace` instance.
    """
    return new_normal_limited_connected_equipment_trace()


def current_limited_connected_equipment_trace() -> LimitedConnectedEquipmentTrace:
    """
    Creates a new limited traversal that traces equipment that are connected stopping at normally open points. This ignores phases etc.
    It is purely to trace equipment that are connected in any way.

    The trace can be limited by the number of steps, or the feeder direction.

    :return: The new `LimitedConnectedEquipmentTrace` instance.
    """
    return new_current_limited_connected_equipment_trace()


def normal_downstream_equipment_trace(queue: Queue[ConductingEquipment] = depth_first()) -> BasicTraversal[ConductingEquipment]:
    """
    Create a new `BasicTraversal` that traverses in the downstream direction using the normal state of the network. The trace works on `ConductingEquipment`,
    and ignores phase connectivity, instead considering things to be connected if they share a `ConnectivityNode`.

    :param queue: An optional parameter to allow you to change the queue being used for the traversal. The default value is a LIFO queue.
    :return: The `BasicTraversal`.
    """
    return new_normal_downstream_equipment_trace(queue)


def current_downstream_equipment_trace(queue: Queue[ConductingEquipment] = depth_first()) -> BasicTraversal[ConductingEquipment]:
    """
    Create a new `BasicTraversal` that traverses in the downstream direction using the current state of the network. The trace works on `ConductingEquipment`,
    and ignores phase connectivity, instead considering things to be connected if they share a `ConnectivityNode`.

    :param queue: An optional parameter to allow you to change the queue being used for the traversal. The default value is a LIFO queue.
    :return: The `BasicTraversal`.
    """
    return new_current_downstream_equipment_trace(queue)


def normal_upstream_equipment_trace(queue: Queue[ConductingEquipment] = depth_first()) -> BasicTraversal[ConductingEquipment]:
    """
    Create a new `BasicTraversal` that traverses in the upstream direction using the normal state of the network. The trace works on `ConductingEquipment`,
    and ignores phase connectivity, instead considering things to be connected if they share a `ConnectivityNode`.

    :param queue: An optional parameter to allow you to change the queue being used for the traversal. The default value is a LIFO queue.
    :return: The `BasicTraversal`.
    """
    return new_normal_upstream_equipment_trace(queue)


def current_upstream_equipment_trace(queue: Queue[ConductingEquipment] = depth_first()) -> BasicTraversal[ConductingEquipment]:
    """
    Create a new `BasicTraversal` that traverses in the upstream direction using the current state of the network. The trace works on `ConductingEquipment`,
    and ignores phase connectivity, instead considering things to be connected if they share a `ConnectivityNode`.

    :param queue: An optional parameter to allow you to change the queue being used for the traversal. The default value is a LIFO queue.
    :return: The `BasicTraversal`.
    """
    return new_current_upstream_equipment_trace(queue)


# Traversals for connectivity results

def connectivity_trace() -> BasicTraversal[ConnectivityResult]:
    """
    Creates a new traversal that traces equipment that are connected. This ignores phases, open status etc.
    It is purely to trace equipment that are connected in any way.

    :return: The new traversal instance.
    """
    return create_connectivity_traversal(ignore_open)


def connectivity_breadth_trace() -> BasicTraversal[ConnectivityResult]:
    """
    Creates a new traversal that traces equipment that are connected. This ignores phases, open status etc.
    It is purely to trace equipment that are connected in any way.

    :return: The new traversal instance.
    """
    return create_connectivity_traversal(ignore_open, breadth_first())


def normal_connectivity_trace() -> BasicTraversal[ConnectivityResult]:
    """
    Creates a new traversal that traces equipment that are normally connected.

    :return: The new traversal instance.
    """
    return create_connectivity_traversal(normally_open)


def current_connectivity_trace() -> BasicTraversal[ConnectivityResult]:
    """
    Creates a new traversal that traces equipment that are currently connected.

    :return: The new traversal instance.
    """
    return create_connectivity_traversal(currently_open)


# --- Traversals for phase steps ---

def phase_trace() -> BasicTraversal[PhaseStep]:
    """
    Creates a new phase-based trace ignoring the state of open phases

    :return: The new traversal instance.
    """
    return new_phase_trace(ignore_open)


def normal_phase_trace() -> BasicTraversal[PhaseStep]:
    """
    Creates a new phase-based trace stopping on normally open phases

    :return: The new traversal instance.
    """
    return new_phase_trace(normally_open)


def current_phase_trace() -> BasicTraversal[PhaseStep]:
    """
    Creates a new phase-based trace stopping on currently open phases

    :return: The new traversal instance.
    """
    return new_phase_trace(currently_open)


def normal_downstream_trace() -> BasicTraversal[PhaseStep]:
    """
    Creates a new downstream trace based on phases and the normal state of the network. Note that the phases
    need to be set on the network before a concept of downstream is known.

    :return: The new traversal instance.
    """
    return new_downstream_phase_trace(normally_open, normal_direction)


def current_downstream_trace() -> BasicTraversal[PhaseStep]:
    """
    Creates a new downstream trace based on phases and the current state of the network. Note that the phases
    need to be set on the network before a concept of downstream is known.

    :return: The new traversal instance.
    """
    return new_downstream_phase_trace(currently_open, current_direction)


def normal_upstream_trace() -> BasicTraversal[PhaseStep]:
    """
    Creates a new upstream trace based on phases and the normal state of the network. Note that the phases
    need to be set on the network before a concept of upstream is known.

    :return: The new traversal instance.
    """
    return new_upstream_phase_trace(normally_open, normal_direction)


def current_upstream_trace() -> BasicTraversal[PhaseStep]:
    """
    Creates a new upstream trace based on phases and the current state of the network. Note that the phases
    need to be set on the network before a concept of upstream is known.

    :return: The new traversal instance.
    """
    return new_upstream_phase_trace(currently_open, current_direction)


# --- Downstream trees ---

def normal_downstream_tree() -> DownstreamTree:
    """
    Returns an instance of `DownstreamTree` convenience class for tracing using the
    normal state of a network

    :return: A new traversal instance.
    """
    return DownstreamTree(normally_open, normal_direction)


def current_downstream_tree() -> DownstreamTree:
    """
    Returns an instance of `DownstreamTree` convenience class for tracing using the
    current state of a network

    :return: A new traversal instance.
    """
    return DownstreamTree(currently_open, current_direction)


# --- Convenience functions.  ---
#
# These are not really necessary, but can be useful if you want to use code completion to find the traces by importing this module under an alias. e.g.
#
# import zepben.evolve.services.network.tracing.tracing as tracing
# tracing.set_phases()
#

def set_phases() -> SetPhases:
    """
    Returns an instance of `SetPhases` convenience class for setting phases on a network.

    :return: A new `SetPhases` instance.
    """
    return SetPhases()


def remove_phases() -> RemovePhases:
    """
    Returns an instance of `RemovePhases` convenience class for removing phases from a network.

    :return: A new `RemovePhases` instance.
    """
    return RemovePhases()


def set_direction() -> SetDirection:
    """
    Returns an instance of `SetDirection` convenience class for setting feeder directions on a network.

    :return: A new `SetDirection` instance.
    """
    return SetDirection()


def remove_direction() -> RemoveDirection:
    """
    Returns an instance of `RemoveDirection` convenience class for removing feeder directions from a network.

    :return: A new `RemoveDirection` instance.
    """
    return RemoveDirection()


def phase_inferrer() -> PhaseInferrer:
    """
    Returns an instance of `PhaseInferrer` convenience class for inferring missing phases on a network.

    :return: A new `PhaseInferrer` instance.
    """
    return PhaseInferrer()


def assign_equipment_to_feeders() -> AssignToFeeders:
    """
    Returns an instance of `AssignToFeeders` convenience class for assigning equipment
    containers to feeders on a network.

    @return A new `AssignToFeeders` instance.
    """
    return AssignToFeeders()


def assign_equipment_to_lv_feeders() -> AssignToLvFeeders:
    """
    Returns an instance of `zepben.evolve.services.network.tracing.feeder.assign_to_lv_feeders.AssignToLvFeeders` convenience class for assigning equipment
    containers to feeders on a network.
    """
    return AssignToLvFeeders()


# TODO
# def find_with_usage_points() -> FindWithUsagePoints:
#     """
#     Returns an instance of `FindWithUsagePoints` convenience class for finding conducting equipment with attached usage points.
#
#     :return: A new `FindWithUsagePoints` instance.
#     """
#     return FindWithUsagePoints()


def find_swer_equipment() -> FindSwerEquipment:
    """
    Returns an instance of `FindSwerEquipment` convenience class for finding swer equipment on a feeders or network.
    """
    return FindSwerEquipment()
