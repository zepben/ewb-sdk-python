#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import inspect
from collections.abc import Callable
from functools import singledispatchmethod
from logging import Logger
from typing import TypeVar, Union, Generic, Set, Type, Generator, FrozenSet

from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.aclinesegment import AcLineSegment
from zepben.evolve.model.cim.iec61970.base.wires.clamp import Clamp
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.services.network.tracing.connectivity.nominal_phase_path import NominalPhasePath
from zepben.evolve.services.network.tracing.networktrace.compute_data import ComputeData, ComputeDataWithPaths
from zepben.evolve.services.network.tracing.networktrace.conditions.network_trace_queue_condition import NetworkTraceQueueCondition
from zepben.evolve.services.network.tracing.networktrace.conditions.network_trace_stop_condition import NetworkTraceStopCondition, ShouldStop
from zepben.evolve.services.network.tracing.networktrace.network_trace_action_type import NetworkTraceActionType, CanActionItem
from zepben.evolve.services.network.tracing.networktrace.network_trace_queue_next import NetworkTraceQueueNext
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.networktrace.network_trace_tracker import NetworkTraceTracker
from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.evolve.services.network.tracing.traversal.queue import TraversalQueue
from zepben.evolve.services.network.tracing.traversal.queue_condition import QueueCondition
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext
from zepben.evolve.services.network.tracing.traversal.traversal import Traversal, StopConditionTypes

T = TypeVar('T')
D = TypeVar('D')

__all__ = ['NetworkTrace']


class NetworkTrace(Traversal[NetworkTraceStep[T], 'NetworkTrace[T]'], Generic[T]):
    """
    A :class:`Traversal` implementation specifically designed to trace connected :class:`Terminal`s of :class:`ConductingEquipment` in a network.

    This trace manages the complexity of network connectivity, especially in cases where connectivity is not straightforward,
    such as with :class:`BusbarSection`s and :class:`Clamp`s. It checks the in service flag of equipment and only steps to equipment that is marked as in service.
    It also provides the optional ability to trace only specific phases.

    Steps are represented by a :class:`NetworkTraceStep`, which contains a :class:`NetworkTraceStep.Path` and allows associating arbitrary data with each step.
    The arbitrary data for each step is computed via a :class:`ComputeData` or :class:`ComputeDataWithPaths` function provided at construction.
    The trace invokes these functions when queueing each item and stores the result with the next step.

    When traversing, this trace will step on every connected terminal, as long as they match all the traversal conditions.
    Each step is classified as either an external step or an internal step:

        - **External Step**: Moves from one terminal to another with different ``Terminal.conducting_equipment``.
        - **Internal Step**: Moves between terminals within the same ``Terminal.conducting_equipment``.

    Often, you may want to act upon a :class:`ConductingEquipment` only once, rather than multiple times for each internal and external terminal step.
    To achieve this, set ``action_type`` to ``NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT``. With this type, the trace will only call step actions and
    conditions once for each :class:`ConductingEquipment`, regardless of how many terminals it has. However, queue conditions can be configured to be called
    differently for each condition as continuing the trace can rely on different conditions based on an external or internal step. For example, not
    queuing past open switches should happen on an internal step, thus if the trace is configured with ``FIRST_STEP_ON_EQUIPMENT``, it will by default only
    action the first external step to each equipment, and thus the provided `Conditions.stopAtOpen` condition overrides the default behaviour such that
    it is called on all internal steps.

    The network trace is state-aware by requiring an instance of :class:`NetworkStateOperators`.
    This allows traversal conditions and step actions to query and act upon state-based properties and functions of equipment in the network when required.

    'Branching' traversals are also supported allowing tracing both ways around loops in the network. When using a branching instance, a new 'branch'
    is created for each terminal when a step has two or more terminals it can step to. That is on an internal step, if the equipment has more than 2 terminals
    and more than 2 terminals will be queued, a branch will be created for each terminal. On an external step, if 2 or more terminals are to be queued,
    a branch will be created for each terminal.
    If you do not need to trace loops both ways or have no loops, do not use a branching instance as it is less efficient than the non-branching one.

    To create instances of this class, use the factory methods provided in the :class:`Tracing` object.
    """

    def __init__(
        self,
        network_state_operators: Type[NetworkStateOperators],
        queue_type: Union[Traversal.BasicQueueType, Traversal.BranchingQueueType],
        parent: 'NetworkTrace[T]' = None,
        action_type: CanActionItem = None,
        debug_logger: Logger = None,
        name: str = None,
    ):

        if name is None:
            raise ValueError('name can not be None')
        self.name = name
        if action_type is None:
            raise ValueError('action_type can not be None')

        self._queue_type = queue_type
        self.network_state_operators = network_state_operators
        self._action_type = action_type

        self._tracker = NetworkTraceTracker()

        super().__init__(self._queue_type, parent=parent, debug_logger=debug_logger)

    @classmethod
    def non_branching(
        cls,
        network_state_operators: Type[NetworkStateOperators],
        queue: TraversalQueue[NetworkTraceStep[T]],
        action_type: CanActionItem,
        name: str,
        compute_data: Union[ComputeData[T], ComputeDataWithPaths[T]],
        debug_logger=None,
    ) -> 'NetworkTrace[T]':

        return cls(
            network_state_operators,
            Traversal.BasicQueueType(NetworkTraceQueueNext.Basic(network_state_operators, compute_data_with_action_type(compute_data, action_type)), queue),
            None,
            action_type,
            debug_logger,
            name,
        )

    @classmethod
    def branching(
        cls,
        network_state_operators: Type[NetworkStateOperators],
        queue_factory: Callable[[], TraversalQueue[T]],
        branch_queue_factory: Callable[[], TraversalQueue['NetworkTrace[T]']],
        action_type: CanActionItem,
        name: str,
        parent: 'NetworkTrace[T]' = None,
        compute_data: Union[ComputeData[T], ComputeDataWithPaths[T]] = None,
        debug_logger: Logger = None,
    ) -> 'NetworkTrace[T]':

        return cls(
            network_state_operators,
            Traversal.BranchingQueueType(
                NetworkTraceQueueNext.Branching(network_state_operators, compute_data_with_action_type(compute_data, action_type)),
                queue_factory,
                branch_queue_factory,
            ),
            parent,
            action_type,
            debug_logger,
            name,
        )

    @singledispatchmethod
    def add_start_item(self, start: Union[Terminal, ConductingEquipment, NetworkTraceStep.Path], data: T = None, phases: PhaseCode = None) -> "NetworkTrace[T]":
        """
        Depending on the type of `start` adds one of the following as starting points in the trace, along
        with the associated data:

          - A starting `Terminal`
          - All terminals of the given :class:`ConductingEquipment`.
          - All terminals of the given :class:`AcLineSegment`.
          - The :class:`NetworkTraceStep.Path` passed in.

        Tracing will be only external from this terminal and not trace internally back through its conducting equipment.

        :param start: The starting item for the trace.
        :param data: The data associated with the start step.
        :param phases: Phases to trace; `None` to ignore phases.

        :returns: This `NetworkTrace` instance
        """

        raise Exception('INTERNAL ERROR:: unexpected add_start_item params')

    @add_start_item.register
    def _(self, start: ConductingEquipment, data=None, phases=None):
        """
        Adds all terminals of the given :class:`ConductingEquipment` as starting points in the trace, with the associated data.
        Tracing will be only external from each terminal and not trace internally back through the conducting equipment.

        :param start: The starting equipment whose terminals will be added to the trace
        :param data: The data associated with the start step.
        :param phases: Phases to trace; `None` to ignore phases.

        :returns: This :class:`NetworkTrace` instance
        """

        # We don't have a special case for Clamp here because we say if you start from the whole Clamp rather than its terminal specifically,
        # we want to trace externally from it and traverse its segment.
        for it in start.terminals:
            self._add_start_item(it, data=data, phases=phases)
        return self

    @add_start_item.register
    def _(self, start: Terminal, data=None, phases=None):
        """
        Adds a starting :class:`Terminal` to the trace with the associated step data. Tracing will be only external from this
        terminal and not trace internally back through its conducting equipment.

        :param start: The starting `Terminal` for the trace.
        :param data: The data associated with the start step.
        :param phases: Phases to trace; `None` to ignore phases.

        :returns: This :class:`NetworkTrace` instance
        """

        # We have a special case when starting specifically on a clamp terminal that we mark it as having traversed the segment such that it
        # will only trace externally from the clamp terminal. This behaves differently to when the whole Clamp is added as a start item.
        traversed_ac_line_segment = None
        if isinstance(start.conducting_equipment, Clamp):
            traversed_ac_line_segment = start.conducting_equipment.ac_line_segment
        self._add_start_item(start, data=data, phases=phases, traversed_ac_line_segment=traversed_ac_line_segment)
        return self

    @add_start_item.register
    def _(self, start: AcLineSegment, data=None, phases=None):
        """
        Adds all terminals of the given :class:`AcLineSegment` as starting points in the trace, with the associated data.
        Tracing will be only external from each terminal and not trace internally back through the `AcLineSegment`.

        :param start: The starting `AcLineSegment` whose terminals will be added to the trace
        :param data: The data associated with the start step.
        :param phases: Phases to trace; `None` to ignore phases.

        :returns: This :class:`NetworkTrace` instance
        """

        # If we start on an AcLineSegment, we queue the segments terminals, and all its Cut and Clamp terminals as if we have traversed the segment,
        # so the next steps will be external from all the terminals "belonging" to the segment.
        def start_terminals() -> Generator[Terminal, None, None]:
            for _terminal in start.terminals:
                yield _terminal
            for clamp in start.clamps:
                for _terminal in clamp.terminals:
                    yield _terminal
                    break
            for cut in start.cuts:
                for _terminal in cut.terminals:
                    yield _terminal

        for terminal in start_terminals():
            self._add_start_item(terminal, data=data, phases=phases, traversed_ac_line_segment=start)
        return self

    @add_start_item.register
    def _(self, start: NetworkTraceStep.Path, data: T, phases=None):
        if phases:
            raise ValueError('starting from a NetworkTraceStep.Path does not support specifying phases')
        self._add_start_item(start, data=data)
        return self

    def _add_start_item(
        self, start: Union[Terminal, NetworkTraceStep.Path], data: T = None, phases: PhaseCode = None, traversed_ac_line_segment: AcLineSegment = None
    ):
        """
        To be called by self.add_start_item(), this method builds the start :class:`NetworkTraceStep.Path`s for the start item
        and adds it to the :class:`Traversal`

        If `start` is a `NetworkTraceStep.Path`, [`phases`, `traversed_ac_line_segment`] will all be ignored.

        :param start: The starting :class:`Terminal` or `NetworkTraceStep.Path` to be added to the trace
        :param data: The data associated with the start `Terminal`.
        :param phases: Phases to trace; `None` to ignore phases.
        :param traversed_ac_line_segment: The :class:`AcLineSegment` that was just traversed

        :returns: This `NetworkTrace` instance
        """

        if isinstance(start, NetworkTraceStep.Path):
            if any([phases, traversed_ac_line_segment]):
                raise ValueError('phases and traversed_ac_line_segment are all ignored when start is a NetworkTraceStep.Path')
            start_path = start
        else:
            start_path = NetworkTraceStep.Path(start, start, traversed_ac_line_segment, self.start_nominal_phase_path(phases))

        super().add_start_item(NetworkTraceStep(start_path, 0, 0, data))

    async def run(
        self,
        start: Union[ConductingEquipment, Terminal, NetworkTraceStep.Path] = None,
        data: T = None,
        phases: PhaseCode = None,
        can_stop_on_start_item: bool = True,
    ) -> "NetworkTrace[T]":
        """
        Runs the network trace starting from ``start``

        Depending on the type of ``start``, this will either start from::

            - A starting Terminal to the trace with the associated step data.
            - All terminals of the given ConductingEquipment as starting points in the trace, with the associated data.

        :param start: The starting :class:`Terminal` or :class:`ConductingEquipment` for the trace.
        :param data: The data associated with the start step.
        :param phases: Phases to trace; ``None`` to ignore phases.
        :param can_stop_on_start_item: indicates whether the trace should check stop conditions on start items.
        """

        if start is not None:
            self.add_start_item(start, data, phases)

        await super().run(can_stop_on_start_item=can_stop_on_start_item)
        return self

    @singledispatchmethod
    def add_condition(self, condition: QueueCondition[T], **kwargs) -> "NetworkTrace[T]":
        """
        Adds a traversal condition to the trace.

        Valid types for ``condition`` are::

            - A predefined traversal condition (eg: Conditions.stop_at_open())
            - A function implementing ShouldQueue or ShouldStop signature.
            - A class subclassing StopCondition or QueueCondition

        :param condition: The condition to be added
        :keyword allow_re_wrapping: Allow rewrapping of :class:`StopCondition`s with debug logging
        :returns: This :class:`NetworkTrace` instance
        """

        return super().add_condition(condition, **kwargs)

    @add_condition.register
    def _(self, condition: Callable, **kwargs):
        """
        Adds a traversal condition to the trace using the trace's :class:`NetworkStateOperators` as the receiver.

        This overload primarily exists to enable a DSL-like syntax for adding predefined traversal conditions to the trace.
        For example, to configure the trace to stop at open points using the :meth:`Conditions.stop_at_open` factory, you can use:

        .. code-block::

            from zepben.evolve import stop_at_open
            NetworkTrace().add_condition(stop_at_open())
        """

        if len(inspect.getfullargspec(condition).args) == 1:  # Catches DSL Style lambda conditions from zepben.evolve.Conditions
            return self.add_condition(condition(self.network_state_operators), **kwargs)
        return super().add_condition(condition, **kwargs)

    @singledispatchmethod
    def add_queue_condition(
        self, condition: NetworkTraceQueueCondition[NetworkTraceStep[T]], step_type: NetworkTraceStep.Type = None, **kwargs
    ) -> "NetworkTrace[T]":
        """
        Adds a :class:`QueueCondition` to the traversal. However, before registering it with the traversal, it will make sure that the queue condition
        is only checked on step types relevant to the `NetworkTraceActionType` assigned to this instance. That is when:

            - ``step_type`` is ``NetworkTraceActionType.ALL_STEPS`` the condition will be checked on all steps.
            - ``step_type`` is ``NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT`` the condition will be checked on external steps.

        However, if the `condition` is an instance of :class:`NetworkTraceQueueCondition` the ``NetworkTraceQueueCondition.step_type`` will be honoured.

        :param condition: The queue condition to add.
        :param step_type: `NetworkTraceStepType` value.
        :keyword allow_re_wrapping: Allow rewrapping of :class:`QueueCondition`s with debug logging
        :returns: This :class:`NetworkTrace` instance
        """

        return super().add_queue_condition(condition, **kwargs)

    @add_queue_condition.register
    def _(self, condition: Callable, step_type: NetworkTraceStep.Type = None, **kwargs):
        return self.add_queue_condition(NetworkTraceQueueCondition(default_condition_step_type(self._action_type) or step_type, condition), **kwargs)

    @singledispatchmethod
    def add_stop_condition(self, condition: StopConditionTypes, step_type: NetworkTraceStep.Type = None, **kwargs) -> "NetworkTrace[T]":
        """
        Adds a :class:`StopCondition` to the traversal. However, before registering it with the traversal, it will make sure that the queue condition
        is only checked on step types relevant to the `NetworkTraceActionType` assigned to this instance. That is when:

            - ``step_type`` is ``NetworkTraceActionType.ALL_STEPS`` the condition will be checked on all steps.
            - ``step_type`` is ``NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT`` the condition will be checked on external steps.

        However, if the `condition` is an instance of :class:`NetworkTraceStopCondition` the ``NetworkTraceStopCondition.step_type`` will be honoured.

        :param condition: The stop condition to add.
        :param step_type: `NetworkTraceStepType` value.
        :keyword allow_re_wrapping: Allow rewrapping of :class:`StopCondition`s with debug logging
        :returns: This :class:`NetworkTrace` instance
        """

        return super().add_stop_condition(condition, **kwargs)

    @add_stop_condition.register(Callable)
    def _(self, condition: ShouldStop, step_type=None, **kwargs):
        return self.add_stop_condition(NetworkTraceStopCondition(default_condition_step_type(self._action_type) or step_type, condition), **kwargs)

    def can_action_item(self, item: T, context: StepContext) -> bool:
        return self._action_type(item, context, self.has_visited)

    def on_reset(self):
        self._tracker.clear()

    def can_visit_item(self, item: T, context: StepContext) -> bool:
        return self.visit(item.path.to_terminal, item.path.to_phases_set())

    def get_derived_this(self) -> 'NetworkTrace[T]':
        return self

    def create_new_this(self) -> 'NetworkTrace[T]':
        return NetworkTrace(self.network_state_operators, self._queue_type, self, self._action_type, debug_logger=None, name=self.name)

    @staticmethod
    def start_nominal_phase_path(phases: PhaseCode) -> Set[NominalPhasePath]:
        return {NominalPhasePath(it, it) for it in phases.single_phases} if phases and phases.single_phases else set()

    def has_visited(self, terminal: Terminal, phases: FrozenSet[SinglePhaseKind]) -> bool:
        parent = self.parent
        while parent is not None:
            if parent._tracker.has_visited(terminal, phases):
                return True
            parent = parent.parent
        return self._tracker.has_visited(terminal, phases)

    def visit(self, terminal: Terminal, phases: FrozenSet[SinglePhaseKind]) -> bool:
        if self.parent and self.parent.has_visited(terminal, phases):
            return False
        return self._tracker.visit(terminal, phases)


def default_condition_step_type(step_type: CanActionItem):
    if step_type is None:
        return False
    if step_type == NetworkTraceActionType.ALL_STEPS:
        return NetworkTraceStep.Type.ALL
    elif step_type == NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT:
        return NetworkTraceStep.Type.EXTERNAL
    raise Exception('step doesnt match expected types')


def compute_data_with_action_type(compute_data: ComputeData[T], action_type: CanActionItem) -> ComputeData[T]:
    if action_type == NetworkTraceActionType.ALL_STEPS:
        return compute_data
    elif action_type == NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT:
        return ComputeData(
            lambda current_step, current_context, next_path: (
                current_step.data if next_path.traced_internally else compute_data.compute_next(current_step, current_context, next_path)
            )
        )
    raise Exception(f'{action_type.__class__}: step doesnt match expected types')


def with_paths_with_action_type(self, action_type: NetworkTraceActionType) -> ComputeDataWithPaths[T]:
    if action_type == NetworkTraceActionType.ALL_STEPS:
        return self
    elif action_type == NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT:
        return ComputeDataWithPaths(
            lambda current_step, current_context, next_path, next_paths: (
                current_step.data if next_path.traced_internally else self.compute_next(current_step, current_context, next_path, next_paths)
            )
        )
    raise Exception('step doesnt match expected types')


ComputeDataWithPaths[T].with_action_type = with_paths_with_action_type
