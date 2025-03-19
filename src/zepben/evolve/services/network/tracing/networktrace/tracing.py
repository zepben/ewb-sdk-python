#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import TypeVar, Union

from zepben.evolve import require
from zepben.evolve.services.network.tracing.networktrace.compute_data import ComputeData, ComputeDataWithPaths
from zepben.evolve.services.network.tracing.networktrace.network_trace import BranchingNetworkTrace, NetworkTrace
from zepben.evolve.services.network.tracing.networktrace.network_trace_action_type import NetworkTraceActionType
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.evolve.services.network.tracing.traversal.traversal_queue import TraversalQueue

T = TypeVar('T')


class Tracing:
    @staticmethod
    def network_trace(network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL,
                      action_step_type: NetworkTraceActionType=NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT,
                      queue: TraversalQueue[NetworkTraceStep[T]]=TraversalQueue.depth_first,
                      compute_data: ComputeData[T]=None
                      ) -> NetworkTrace[T]:
        """
        Creates a `NetworkTrace` that computes contextual data for every step.

        :param network_state_operators: The state operators to make the NetworkTrace state aware. Defaults to `NetworkStateOperators.NORMAL`.
        :param action_step_type: The action step type to be applied when the trace steps. Defaults to `NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT`.
        :param queue: The traversal queue the trace is backed by. Defaults to a depth first queue.
        :param compute_data: The computer that provides the [NetworkTraceStep.data] contextual step data for each step in the trace.

        :returns: a new `NetworkTrace`
        """
        return NetworkTrace(network_state_operators, queue, action_step_type, compute_data or (lambda: None))

    @staticmethod
    def network_trace_branching(network_state_operators: NetworkStateOperators,
                                action_step_type: NetworkTraceActionType=NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT,
                                queue_factory: TraversalQueue[NetworkTraceStep[T]]=TraversalQueue.depth_first,
                                branch_queue_factory: TraversalQueue[NetworkTraceStep[T]]=TraversalQueue.breadth_first,
                                compute_data: Union[ComputeData[T], ComputeDataWithPaths[T]]=None
                                ) -> NetworkTrace[T]:


        return BranchingNetworkTrace(network_state_operators, queue_factory, branch_queue_factory, action_step_type, None, (compute_data or (lambda: None)))

    @staticmethod
    def set_direction():
        from zepben.evolve.services.network.tracing.feeder.set_direction import SetDirection
        return SetDirection()

    @staticmethod
    def clear_direction():
        return ClearDirection()

    @staticmethod
    def assign_equipment_to_feeders():
        from zepben.evolve import AssignToFeeders
        return AssignToFeeders()

    @staticmethod
    def assign_equipment_to_lv_feeders():
        from zepben.evolve import AssignToLvFeeders
        return AssignToLvFeeders()

    @staticmethod
    def set_phases():
        from zepben.evolve import SetPhases
        return SetPhases()

    @staticmethod
    def remove_phases():
        from zepben.evolve import RemovePhases
        return RemovePhases()

    @staticmethod
    def phase_inferrer():
        from zepben.evolve import PhaseInferrer
        return PhaseInferrer()

    @staticmethod
    def find_swer_equipment():
        from zepben.evolve import FindSwerEquipment
        return FindSwerEquipment()
