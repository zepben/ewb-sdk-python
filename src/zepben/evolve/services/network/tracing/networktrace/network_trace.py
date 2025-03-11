#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import TypeVar

from zepben.evolve import Traversal, ConductingEquipment, Terminal, PhaseCode, NominalPhasePath, SinglePhaseKind
from zepben.evolve.services.network.tracing.networktrace.compute_data import ComputeData, ComputeDataWithPaths
from zepben.evolve.services.network.tracing.networktrace.network_trace_action_type import NetworkTraceActionType
from zepben.evolve.services.network.tracing.networktrace.network_trace_queue_condition import NetworkTraceQueueCondition
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.networktrace.network_trace_tracker import NetworkTraceTracker
from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.evolve.services.network.tracing.traversal.queue_condition import QueueCondition
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext
from zepben.evolve.services.network.tracing.traversal.traversal import QueueType, BasicQueueType, BranchingQueueType, D
from zepben.evolve.services.network.tracing.traversal.traversal_condition import TraversalCondition

T = TypeVar('T')

# TODO: Document this
# TODO: implement the other constructors

class NetworkTrace[T](Traversal[NetworkTraceStep[T], 'NetworkTrace[T]']):
    network_state_operators: NetworkStateOperators
    queue_type: QueueType[NetworkTraceStep[T], 'NetworkTrace']
    parent: 'NetworkTrace[T]' = None
    _action_type: NetworkTraceActionType

    def __init__(self,
                 queue_type: QueueType[NetworkTraceStep[T], "NetworkTrace[T]"],
                 parent: 'NetworkTrace[T]',
                 action_type: NetworkTraceActionType):

        self.tracker: NetworkTraceTracker
        if isinstance(queue_type, BasicQueueType):
            self.tracker = NetworkTraceTracker(256)
        if isinstance(queue_type, BranchingQueueType):
            self.tracker = NetworkTraceTracker(16)

    def add_start_item(self, start: [Terminal, ConductingEquipment], data: T, phases: PhaseCode=None) -> "NetworkTrace[T]":
        if isinstance(start, Terminal):
            start_path = NetworkTraceStep.Path(start, start, self.start_nominal_phase_path(phases))
            super().add_start_item(NetworkTraceStep(start_path, 0, 0, data))
            return self
        if isinstance(start, ConductingEquipment):
            for it in start.terminals:
                self.add_start_item(it, data, phases)
            return self

    def run(self, start: ConductingEquipment, Terminal, data: T, phases: PhaseCode=None, can_stop_on_start_item: bool=True) -> "NetworkTrace[T]":
        self.add_start_item(start, data, phases)
        super().run(can_stop_on_start_item)
        return self

    def add_condition(self, condition: TraversalCondition[T]) -> "NetworkTrace[T]":
        super().add_condition(self.network_state_operators.condition())
        return self

    def add_queue_condition(self, condition: QueueCondition[NetworkTraceStep[T]], step_type:NetworkTraceStep.Type=None) -> "NetworkTrace[T]":
        if step_type is None:
            return super().add_queue_condition(condition.to_network_trace_queue_condition(self._action_type.default_queue_condition_step_type(), False))
        else:
            return super().add_queue_condition(condition.to_network_trace_queue_condition(step_type, True))

    def can_action_item(self, item: T, context: StepContext) -> bool:
        return self._action_type.can_action_item(item, context, self.has_visited)  # TODO: WHAT IS THIS MAGIC ::hasVisited ??

    def on_reset(self):
        self.tracker.clear()

    def can_visit_item(self, item: T, context: StepContext) -> bool:
        return self.visit(item.path.to_terminal, item.path.nominal_phase_paths.to_phase_set())

    def get_derived_this(self) -> 'NetworkTrace[T]':
        return self

    def create_new_this(self) -> 'NetworkTrace[T]':
        return NetworkTrace(self.network_state_operators, self.queue_type, self, self._action_type)

    def start_nominal_phase_path(self, phases: PhaseCode) -> list[NominalPhasePath]:
        return [NominalPhasePath(it, it) for it in phases.single_phases] if phases and phases.single_phases else []

    def has_visited(self, terminal: Terminal, phases: set[SinglePhaseKind]) -> bool:
        parent = self.parent
        while parent is not None:
            if parent.tracker.has_visited(terminal, phases):
                return True
            parent = parent.parent

        return self.tracker.has_visited(terminal, phases)

    def visit(self, terminal: Terminal, phases: set[SinglePhaseKind]) -> bool:
        parent = self.parent
        while parent is not None:
            if parent.tracker.has_visited(terminal, phases):
                return False
            parent = parent.parent

        return self.tracker.visit(terminal, phases)

# TODO: this hurts every part of my soul.
def to_network_trace_queue_condition(self, step_type: NetworkTraceStep.Type, override_step_type: bool):
    if isinstance(self, NetworkTraceQueueCondition[T] and not override_step_type):
        return self
    else:
        return NetworkTraceQueueCondition.delegate_to(step_type, self)

QueueCondition[NetworkTraceStep[T]].to_network_trace_queue_condition = to_network_trace_queue_condition

def default_queue_condition_step_type(self):
    if self == NetworkTraceActionType.ALL_STEPS:
        return NetworkTraceStep.Type.ALL
    elif self == NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT:
        return NetworkTraceStep.Type.EXTERNAL

NetworkTraceActionType.default_queue_condition_step_type = default_queue_condition_step_type

# FIXME: this is wrong
def with_action_type(self, action_type: NetworkTraceActionType) -> ComputeData[T]:
    if action_type == NetworkTraceActionType.ALL_STEPS:
        return self
    elif action_type == NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT:
        return ComputeData(lambda current_step, current_context, next_path: 
            current_step.data if next_path.traced_internally else self.compute_next(current_step, current_context, next_path)
        )
ComputeData[T].with_action_type = with_action_type

# FIXME: this is wrong also
def with_paths_with_action_type(self, action_type: NetworkTraceActionType) -> ComputeData[T]:
    if action_type == NetworkTraceActionType.ALL_STEPS:
        return self
    elif action_type == NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT:
        return ComputeDataWithPaths(lambda current_step, current_context, next_path, next_paths:
            current_step.data if next_path.traced_internally else self.compute_next(current_step, current_context, next_path, next_paths)
        )
ComputeDataWithPaths[T].with_action_type = with_paths_with_action_type
