#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections.abc import Callable
from typing import TypeVar, Union, Generic

from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

from zepben.evolve.services.network.tracing.networktrace.compute_data import ComputeData, ComputeDataWithPaths
from zepben.evolve.services.network.tracing.networktrace.network_trace_action_type import NetworkTraceActionType
from zepben.evolve.services.network.tracing.networktrace.network_trace_queue_condition import NetworkTraceQueueCondition
from zepben.evolve.services.network.tracing.networktrace.network_trace_queue_next import NetworkTraceQueueNext
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.networktrace.network_trace_tracker import NetworkTraceTracker
from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.evolve.services.network.tracing.traversal.queue_condition import QueueCondition
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext
from zepben.evolve.services.network.tracing.traversal.traversal import Traversal
from zepben.evolve.services.network.tracing.traversal.queue import TraversalQueue
from zepben.evolve.services.network.tracing.connectivity.nominal_phase_path import NominalPhasePath

T = TypeVar('T')
D = TypeVar('D')


class NetworkTrace(Traversal[NetworkTraceStep[T], 'NetworkTrace[T]'], Generic[T]):
    """
    A [Traversal] implementation specifically designed to trace connected [Terminal]s of [ConductingEquipment] in a network.

    This trace manages the complexity of network connectivity, especially in cases where connectivity is not straightforward,
    such as with [BusbarSection]s and [Clamp]s. It checks the in service flag of equipment and only steps to equipment that is marked as in service.
    It also provides the optional ability to trace only specific phases.

    Steps are represented by a [NetworkTraceStep], which contains a [NetworkTraceStep.Path] and allows associating arbitrary data with each step.
    The arbitrary data for each step is computed via a [ComputeData] or [ComputeDataWithPaths] function provided at construction.
    The trace invokes these functions when queueing each item and stores the result with the next step.

    When traversing, this trace will step on every connected terminal, as long as they match all the traversal conditions.
    Each step is classified as either an external step or an internal step:

    - **External Step**: Moves from one terminal to another with different [Terminal.conductingEquipment].
    - **Internal Step**: Moves between terminals within the same [Terminal.conductingEquipment].

    Often, you may want to act upon a [ConductingEquipment] only once, rather than multiple times for each internal and external terminal step.
    To achieve this, set [actionType] to [NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT]. With this type, the trace will only call step actions and
    conditions once for each [ConductingEquipment], regardless of how many terminals it has. However, queue conditions can be configured to be called
    differently for each condition as continuing the trace can rely on different conditions based on an external or internal step. For example, not
    queuing past open switches should happen on an internal step, thus if the trace is configured with FIRST_STEP_ON_EQUIPMENT, it will by default only
    action the first external step to each equipment, and thus the provided [Conditions.stopAtOpen] condition overrides the default behaviour such that
    it is called on all internal steps.

    The network trace is state-aware by requiring an instance of [NetworkStateOperators].
    This allows traversal conditions and step actions to query and act upon state-based properties and functions of equipment in the network when required.

    'Branching' traversals are also supported allowing tracing both ways around loops in the network. When using a branching instance, a new 'branch'
    is created for each terminal when a step has two or more terminals it can step to. That is on an internal step, if the equipment has more than 2 terminals
    and more than 2 terminals will be queued, a branch will be created for each terminal. On an external step, if 2 or more terminals are to be queued,
    a branch will be created for each terminal.
    If you do not need to trace loops both ways or have no loops, do not use a branching instance as it is less efficient than the non-branching one.

    To create instances of this class, use the factory methods provided in the [Tracing] object.
    """

    def __init__(self,
                 network_state_operators: NetworkStateOperators,
                 queue_type: Union[Traversal.BasicQueueType, Traversal.BranchingQueueType],
                 parent: 'NetworkTrace[T]'=None,
                 action_type: NetworkTraceActionType=None
                 ):

        self._queue_type = queue_type
        self.network_state_operators = network_state_operators
        self._action_type = action_type

        self._tracker = NetworkTraceTracker()

        super().__init__(self._queue_type, parent)

    @classmethod
    def non_branching(cls,
                      network_state_operators: NetworkStateOperators,
                      queue: TraversalQueue[NetworkTraceStep[T]],
                      action_type: NetworkTraceActionType,
                      compute_data: Union[ComputeData[T], ComputeDataWithPaths[T]]
                      ):
        return cls(network_state_operators,
                   Traversal.BasicQueueType(NetworkTraceQueueNext().basic(
                       network_state_operators.is_in_service,
                       compute_data_with_action_type(compute_data, action_type)
                   ), queue),
                   None,
                   action_type)

    @classmethod
    def branching(cls,
                  network_state_operators: NetworkStateOperators,
                  queue_factory: Callable[[], TraversalQueue[T]],
                  branch_queue_factory: Callable[[], TraversalQueue['NetworkTrace[T]']],
                  action_type: NetworkTraceActionType,
                  parent: 'NetworkTrace[T]'=None,
                  compute_data: Union[ComputeData[T], ComputeDataWithPaths[T]]=None,
                  ):

        return cls(network_state_operators,
                   Traversal.BranchingQueueType(NetworkTraceQueueNext().branching(
                       network_state_operators.is_in_service, compute_data_with_action_type(compute_data, action_type)
                   ), queue_factory, branch_queue_factory),
                   parent,
                   action_type)

    def add_start_item(self, start: Union[Terminal, ConductingEquipment], data: T= None, phases: PhaseCode=None) -> "NetworkTrace[T]":
        """
        Depending on the type of `start`, adds either:
          - A starting [Terminal] to the trace with the associated step data.
          - All terminals of the given [ConductingEquipment] as starting points in the trace, with the associated data.

        Tracing will be only external from this terminal and not trace internally back through its conducting equipment.

        :param start: The starting [Terminal] or [ConductingEquipment] for the trace.
        :param data: The data associated with the start step.
        :param phases: Phases to trace; `None` to ignore phases.
        """
        if isinstance(start, Terminal):
            start_path = NetworkTraceStep.Path(start, start, self.start_nominal_phase_path(phases))
            super().add_start_item(NetworkTraceStep(start_path, 0, 0, data))
            return self

        if issubclass(start.__class__, ConductingEquipment) or isinstance(start, ConductingEquipment):
            for it in start.terminals:
                self.add_start_item(it, data, phases)
            return self

        super().add_start_item(start)
        return self

    async def run(self, start: Union[ConductingEquipment, Terminal]=None, data: T=None, phases: PhaseCode=None, can_stop_on_start_item: bool=True) -> "NetworkTrace[T]":
        """
        Runs the network trace starting from `start`

        Depending on the type of `start`, this will either start from:
          - A starting [Terminal] to the trace with the associated step data.
          - All terminals of the given [ConductingEquipment] as starting points in the trace, with the associated data.

        :param start: The starting [Terminal] or [ConductingEquipment] for the trace.
        :param data: The data associated with the start step.
        :param phases: Phases to trace; `None` to ignore phases.
        :param can_stop_on_start_item: indicates whether the trace should check stop conditions on start items.
        """
        if start is not None:
            self.add_start_item(start, data, phases)

        await super().run(can_stop_on_start_item=can_stop_on_start_item)
        return self

    def add_condition(self, condition: QueueCondition[T]) -> "NetworkTrace[T]":
        """
        Adds a traversal condition to the trace using the trace's [NetworkStateOperators] as the receiver.

        This overload primarily exists to enable a DSL-like syntax for adding predefined traversal conditions to the trace.
        For example, to configure the trace to stop at open points using the [Conditions.stopAtOpen] factory, you can use:

        >>> NetworkTrace().add_condition(NetworkStateOperators.NORMAL.stop_at_open())

        :param condition: A lambda function that returns a traversal condition.
        :returns: This [NetworkTrace] instance
        """
        super().add_condition(condition)
        return self

    def add_queue_condition(self, condition: Union[Callable, QueueCondition[NetworkTraceStep[T]]], step_type:NetworkTraceStep.Type=None) -> "NetworkTrace[T]":
        if callable(condition):
            return self.add_queue_condition(QueueCondition(condition))

        if step_type is None:
            return super().add_queue_condition(to_network_trace_queue_condition(condition, default_queue_condition_step_type(self._action_type), False))
        else:
            return super().add_queue_condition(to_network_trace_queue_condition(condition, step_type, True))

    def can_action_item(self, item: T, context: StepContext) -> bool:
        return self._action_type(item, context, self.has_visited)

    def on_reset(self):
        self._tracker.clear()

    def can_visit_item(self, item: T, context: StepContext) -> bool:
        return self.visit(item.path.to_terminal, item.path.to_phases_set())

    def get_derived_this(self) -> 'NetworkTrace[T]':
        return self

    def create_new_this(self) -> 'NetworkTrace[T]':
        return NetworkTrace(self.network_state_operators, self._queue_type, self, self._action_type)

    @staticmethod
    def start_nominal_phase_path(phases: PhaseCode) -> list[NominalPhasePath]:
        return [NominalPhasePath(it, it) for it in phases.single_phases] if phases and phases.single_phases else []

    def has_visited(self, terminal: Terminal, phases: set[SinglePhaseKind]) -> bool:
        parent = self.parent
        while parent is not None:
            if parent._tracker.has_visited(terminal, phases):
                return True
            parent = parent.parent

        return self._tracker.has_visited(terminal, phases)

    def visit(self, terminal: Terminal, phases: set[SinglePhaseKind]) -> bool:
        parent = self.parent
        while parent is not None:
            if parent._tracker.has_visited(terminal, phases):
                return False
            parent = parent.parent

        return self._tracker.visit(terminal, phases)


def to_network_trace_queue_condition(queue_condition: QueueCondition[NetworkTraceStep[T]], step_type: NetworkTraceStep.Type, override_step_type: bool):
    if isinstance(queue_condition, NetworkTraceQueueCondition) and not override_step_type:
        return queue_condition
    else:
        return NetworkTraceQueueCondition.delegate_to(step_type, queue_condition)


def default_queue_condition_step_type(step_type):
    if step_type == NetworkTraceActionType.ALL_STEPS:
        return NetworkTraceStep.Type.ALL
    elif step_type == NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT:
        return NetworkTraceStep.Type.EXTERNAL
    raise Exception('step doesnt match expected types')


def compute_data_with_action_type(compute_data: ComputeData[T], action_type: NetworkTraceActionType) -> ComputeData[T]:
    if action_type == NetworkTraceActionType.ALL_STEPS:
        return compute_data
    elif action_type == NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT:
        return ComputeData(lambda current_step, current_context, next_path: 
            current_step.data if next_path.traced_internally else compute_data.compute_next(current_step, current_context, next_path)
        )
    raise Exception(f'{action_type.__class__}: step doesnt match expected types')

def with_paths_with_action_type(self, action_type: NetworkTraceActionType) -> ComputeDataWithPaths[T]:
    if action_type == NetworkTraceActionType.ALL_STEPS:
        return self
    elif action_type == NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT:
        return ComputeDataWithPaths(lambda current_step, current_context, next_path, next_paths:
            current_step.data if next_path.traced_internally else self.compute_next(current_step, current_context, next_path, next_paths)
        )
    raise Exception('step doesnt match expected types')

ComputeDataWithPaths[T].with_action_type = with_paths_with_action_type
