#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from logging import Logger
from typing import TypeVar, Union, Callable, Type

from zepben.evolve.services.network.tracing.networktrace.compute_data import ComputeData, ComputeDataWithPaths
from zepben.evolve.services.network.tracing.networktrace.network_trace import NetworkTrace
from zepben.evolve.services.network.tracing.networktrace.network_trace_action_type import NetworkTraceActionType, CanActionItem
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.evolve.services.network.tracing.traversal.queue import TraversalQueue

T = TypeVar('T')


class Tracing:
    @staticmethod
    def network_trace(
        network_state_operators: Type[NetworkStateOperators] = NetworkStateOperators.NORMAL,
        action_step_type: CanActionItem = NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT,
        debug_logger: Logger = None,
        name: str = 'NetworkTrace',
        queue: TraversalQueue[NetworkTraceStep[T]] = TraversalQueue.depth_first(),
        compute_data: Union[ComputeData[T], Callable] = None
    ) -> NetworkTrace[T]:
        """
        Creates a `NetworkTrace` that computes contextual data for every step.

        :param network_state_operators: The state operators to make the NetworkTrace state aware. Defaults to `NetworkStateOperators.NORMAL`.
        :param action_step_type: The action step type to be applied when the trace steps. Defaults to `NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT`.
        :param queue: The traversal queue the trace is backed by. Defaults to a depth first queue.
        :param debug_logger: An optional logger to add information about how the trace is processing items.
        :param name: An optional name for your trace that can be used for logging purposes.
        :param compute_data: The computer that provides the `NetworkTraceStep.data` contextual step data for each step in the trace.

        :returns: a new `NetworkTrace`
        """

        if not isinstance(compute_data, ComputeData):
            compute_data = ComputeData(compute_data or (lambda *args: None))

        return NetworkTrace.non_branching(
            network_state_operators,
            queue,
            action_step_type,
            name,
            compute_data,
            debug_logger=debug_logger
        )

    @staticmethod
    def network_trace_branching(
        network_state_operators: Type[NetworkStateOperators] = NetworkStateOperators.NORMAL,
        action_step_type: CanActionItem = NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT,
        debug_logger: Logger = None,
        name: str = 'NetworkTrace',
        queue_factory: Callable[[], TraversalQueue[NetworkTraceStep[T]]] = lambda: TraversalQueue.depth_first(),
        branch_queue_factory: Callable[[], TraversalQueue[NetworkTrace[NetworkTraceStep[T]]]] = lambda: TraversalQueue.breadth_first(),
        compute_data: Union[ComputeData[T], ComputeDataWithPaths[T]] = None
    ) -> NetworkTrace[T]:
        """
        Creates a branching `NetworkTrace` that computes contextual data for every step. A new 'branch' will be created for each terminal
        where the current terminal in the trace will step to two or more terminals.

        :param network_state_operators: The state operators to make the NetworkTrace state aware. Defaults to `NetworkStateOperators.NORMAL`.
        :param action_step_type: The action step type to be applied when the trace steps. Defaults to `NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT`.
        :param queue_factory: A factory that will produce [TraversalQueue]s used by each branch in the trace to queue steps. Defaults to a factory
          the creates depth first queues.
        :param branch_queue_factory: A factory that will produce `TraversalQueue`s used by each branch in the trace to queue branches. Defaults
          to a factory that creates breadth first queues.
        :param debug_logger: An optional logger to add information about how the trace is processing items.
        :param name: An optional name for your trace that can be used for logging purposes.
        :param compute_data: The computer that provides the `NetworkTraceStep.data` contextual step data for each step in the trace.

        :returns: a new `NetworkTrace`
        """

        if not isinstance(compute_data, ComputeData):
            compute_data = ComputeData(compute_data or (lambda *args: None))

        return NetworkTrace.branching(
            network_state_operators,
            queue_factory,
            branch_queue_factory,
            action_step_type,
            name,
            None,
            compute_data,
            debug_logger=debug_logger
        )

    @staticmethod
    def set_direction(debug_logger: Logger = None):
        from zepben.evolve.services.network.tracing.feeder.set_direction import SetDirection
        return SetDirection(debug_logger=debug_logger)

    @staticmethod
    def clear_direction(debug_logger: Logger = None):
        from zepben.evolve.services.network.tracing.feeder.clear_direction import ClearDirection
        return ClearDirection(debug_logger=debug_logger)

    @staticmethod
    def assign_equipment_to_feeders(debug_logger: Logger = None):
        from zepben.evolve.services.network.tracing.feeder.assign_to_feeders import AssignToFeeders
        return AssignToFeeders(debug_logger=debug_logger)

    @staticmethod
    def assign_equipment_to_lv_feeders(debug_logger: Logger = None):
        from zepben.evolve.services.network.tracing.feeder.assign_to_lv_feeders import AssignToLvFeeders
        return AssignToLvFeeders(debug_logger=debug_logger)

    @staticmethod
    def set_phases(debug_logger: Logger = None):
        from zepben.evolve.services.network.tracing.phases.set_phases import SetPhases
        return SetPhases(debug_logger=debug_logger)

    @staticmethod
    def remove_phases(debug_logger: Logger = None):
        from zepben.evolve.services.network.tracing.phases.remove_phases import RemovePhases
        return RemovePhases(debug_logger=debug_logger)

    @staticmethod
    def phase_inferrer(debug_logger: Logger = None):
        from zepben.evolve.services.network.tracing.phases.phase_inferrer import PhaseInferrer
        return PhaseInferrer(debug_logger=debug_logger)

    @staticmethod
    def find_swer_equipment(debug_logger: Logger = None):
        from zepben.evolve.services.network.tracing.find_swer_equipment import FindSwerEquipment
        return FindSwerEquipment(debug_logger=debug_logger)
