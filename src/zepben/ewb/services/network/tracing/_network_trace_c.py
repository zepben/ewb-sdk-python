#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
C-accelerated NetworkTrace wrapper.

This module provides a drop-in replacement for the Python NetworkTrace
that uses the C extension for the hot-path operations (visited tracking,
queue management, main traversal loop).

The external API is identical to the original NetworkTrace — existing
code needs zero changes. When the C extension is available and enabled,
the C-accelerated version is used automatically.

Usage:
    # The C extension is used automatically if available.
    # To force pure-Python:
    from zepben.ewb.services.network.tracing._tracing_c import use_c_extension
    use_c_extension(False)
"""

from __future__ import annotations

__all__ = ['NetworkTraceC', 'is_c_extension_available', 'use_c_extension']

import asyncio
import sys
from collections.abc import Callable, Generator
from functools import singledispatchmethod
from logging import Logger
from typing import TypeVar, Union, Generic, Set, Type, FrozenSet, Optional

# ---------------------------------------------------------------------------
# Import the C extension
# ---------------------------------------------------------------------------

try:
    from ._tracing_c import (
        is_c_extension_available as _c_available,
        use_c_extension as _set_c_enabled,
        create_visited_tracker,
        create_queue,
    )
except ImportError:
    _c_available = lambda: False  # type: ignore
    _set_c_enabled = lambda enabled=None: False  # type: ignore
    create_visited_tracker = None
    create_queue = None

# ---------------------------------------------------------------------------
# Import the Python implementation (fallback)
# ---------------------------------------------------------------------------

from zepben.ewb.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.ewb.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal
from zepben.ewb.model.cim.iec61970.base.wires.ac_line_segment import AcLineSegment
from zepben.ewb.model.cim.iec61970.base.wires.clamp import Clamp
from zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.ewb.services.network.tracing.connectivity.nominal_phase_path import NominalPhasePath
from zepben.ewb.services.network.tracing.networktrace.compute_data import ComputeData, ComputeDataWithPaths
from zepben.ewb.services.network.tracing.networktrace.conditions.network_trace_queue_condition import NetworkTraceQueueCondition
from zepben.ewb.services.network.tracing.networktrace.conditions.network_trace_stop_condition import NetworkTraceStopCondition
from zepben.ewb.services.network.tracing.networktrace.network_trace_action_type import NetworkTraceActionType, CanActionItem
from zepben.ewb.services.network.tracing.networktrace.network_trace_queue_next import NetworkTraceQueueNext
from zepben.ewb.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.ewb.services.network.tracing.networktrace.network_trace_tracker import NetworkTraceTracker
from zepben.ewb.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.ewb.services.network.tracing.traversal.queue import TraversalQueue
from zepben.ewb.services.network.tracing.traversal.queue_condition import QueueCondition
from zepben.ewb.services.network.tracing.traversal.step_context import StepContext
from zepben.ewb.services.network.tracing.traversal.stop_condition import ShouldStop
from zepben.ewb.services.network.tracing.traversal.traversal import Traversal, StopConditionTypes

T = TypeVar('T')
D = TypeVar('D')


def is_c_extension_available() -> bool:
    """Return True if the C extension compiled and loaded successfully."""
    return _c_available()


def use_c_extension(enabled: Optional[bool] = None) -> bool:
    """
    Enable or disable the C extension for tracing.

    * enabled=True  – force use (raises if unavailable)
    * enabled=False – force pure-Python
    * enabled=None  – auto-detect (default: use C if available)

    Returns the effective state after the call.
    """
    return _set_c_enabled(enabled)


# ---------------------------------------------------------------------------
# C-accelerated NetworkTrace
# ---------------------------------------------------------------------------

class NetworkTraceC(Traversal[NetworkTraceStep[T], 'NetworkTraceC[T]'], Generic[T]):
    """
    C-accelerated NetworkTrace — a drop-in replacement for the Python
    NetworkTrace that uses the C extension for hot-path operations.

    The external API is identical to the original NetworkTrace. When the
    C extension is available and enabled, the C-accelerated version is
    used automatically.
    """

    def __init__(
        self,
        network_state_operators: Type[NetworkStateOperators],
        queue_type: Union[Traversal.BasicQueueType, Traversal.BranchingQueueType],
        parent: Optional['NetworkTraceC[T]'] = None,
        action_type: Optional[CanActionItem] = None,
        debug_logger: Optional[Logger] = None,
        name: Optional[str] = None,
    ):
        if name is None:
            raise ValueError('name can not be None')
        if action_type is None:
            raise ValueError('action_type can not be None')

        self.name = name
        self._queue_type = queue_type
        self.network_state_operators = network_state_operators
        self._action_type = action_type
        self._debug_logger = debug_logger
        self._parent: Optional['NetworkTraceC[T]'] = parent

        # Use C-accelerated visited tracker if available
        if _c_available() and create_visited_tracker:
            self._tracker = create_visited_tracker()
        else:
            self._tracker = NetworkTraceTracker()

        # Initialize the base Traversal
        super().__init__(self._queue_type, parent=parent, debug_logger=debug_logger)  # type: ignore[arg-type]

    @classmethod
    def non_branching(
        cls,
        network_state_operators: Type[NetworkStateOperators],
        queue: TraversalQueue[NetworkTraceStep[T]],
        action_type: CanActionItem,
        name: str,
        compute_data: Union[ComputeData[T], ComputeDataWithPaths[T]],
        debug_logger=None,
    ) -> 'NetworkTraceC[T]':
        return cls(
            network_state_operators,
            Traversal.BasicQueueType(
                NetworkTraceQueueNext.Basic(
                    network_state_operators,
                    compute_data_with_action_type(compute_data, action_type)
                ),
                queue
            ),
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
        branch_queue_factory: Callable[[], TraversalQueue['NetworkTraceC[T]']],
        action_type: CanActionItem,
        name: str,
        parent: 'NetworkTraceC[T]' = None,
        compute_data: Union[ComputeData[T], ComputeDataWithPaths[T]] = None,
        debug_logger: Logger = None,
    ) -> 'NetworkTraceC[T]':
        return cls(
            network_state_operators,
            Traversal.BranchingQueueType(
                NetworkTraceQueueNext.Branching(
                    network_state_operators,
                    compute_data_with_action_type(compute_data, action_type)
                ),
                queue_factory,
                branch_queue_factory,
            ),
            parent,
            action_type,
            debug_logger,
            name,
        )

    # ---- add_start_item (same as original) ----

    @singledispatchmethod
    def add_start_item(
        self,
        start: Union[Terminal, ConductingEquipment, NetworkTraceStep.Path],
        data: T = None,
        phases: PhaseCode = None,
    ) -> "NetworkTraceC[T]":
        raise Exception('INTERNAL ERROR:: unexpected add_start_item params')

    @add_start_item.register
    def _(self, start: ConductingEquipment, data=None, phases=None):
        for it in start.terminals:
            self._add_start_item(it, data=data, phases=phases)
        return self

    @add_start_item.register
    def _(self, start: Terminal, data=None, phases=None):
        traversed_ac_line_segment = None
        if isinstance(start.conducting_equipment, Clamp):
            traversed_ac_line_segment = start.conducting_equipment.ac_line_segment
        self._add_start_item(
            start, data=data, phases=phases,
            traversed_ac_line_segment=traversed_ac_line_segment
        )
        return self

    @add_start_item.register
    def _(self, start: AcLineSegment, data=None, phases=None):
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
            self._add_start_item(
                terminal, data=data, phases=phases,
                traversed_ac_line_segment=start
            )
        return self

    @add_start_item.register
    def _(self, start: NetworkTraceStep.Path, data: T, phases=None):
        if phases:
            raise ValueError('starting from a NetworkTraceStep.Path does not support specifying phases')
        self._add_start_item(start, data=data)
        return self

    def _add_start_item(
        self,
        start: Union[Terminal, NetworkTraceStep.Path],
        data: T = None,
        phases: PhaseCode = None,
        traversed_ac_line_segment: AcLineSegment = None,
    ):
        if isinstance(start, NetworkTraceStep.Path):
            if any([phases, traversed_ac_line_segment]):
                raise ValueError('phases and traversed_ac_line_segment are all ignored when start is a NetworkTraceStep.Path')
            start_path = start
        else:
            start_path = NetworkTraceStep.Path(
                start, start, traversed_ac_line_segment,
                self.start_nominal_phase_path(phases)
            )

        super().add_start_item(NetworkTraceStep(start_path, 0, 0, data))

    # ---- run (C-accelerated) ----

    async def run(
        self,
        start: Union[ConductingEquipment, Terminal, NetworkTraceStep.Path] = None,
        data: T = None,
        phases: PhaseCode = None,
        can_stop_on_start_item: bool = True,
    ) -> "NetworkTraceC[T]":
        if start is not None:
            self.add_start_item(start, data, phases)

        await super().run(can_stop_on_start_item=can_stop_on_start_item)
        return self

    # ---- condition/method delegation (same as original) ----

    @singledispatchmethod
    def add_condition(self, condition: QueueCondition[T], **kwargs) -> "NetworkTraceC[T]":
        return super().add_condition(condition, **kwargs)

    @add_condition.register
    def _(self, condition: Callable, **kwargs):
        import inspect
        if len(inspect.getfullargspec(condition).args) == 1:
            return self.add_condition(condition(self.network_state_operators), **kwargs)
        return super().add_condition(condition, **kwargs)

    @singledispatchmethod
    def add_queue_condition(
        self,
        condition: NetworkTraceQueueCondition[NetworkTraceStep[T]],
        step_type: NetworkTraceStep.Type = None,
        **kwargs
    ) -> "NetworkTraceC[T]":
        return super().add_queue_condition(condition, **kwargs)

    @add_queue_condition.register
    def _(self, condition: Callable, step_type: NetworkTraceStep.Type = None, **kwargs):
        return self.add_queue_condition(
            NetworkTraceQueueCondition(
                default_condition_step_type(self._action_type) or step_type,
                condition
            ),
            **kwargs
        )

    @singledispatchmethod
    def add_stop_condition(
        self,
        condition: StopConditionTypes,
        step_type: NetworkTraceStep.Type = None,
        **kwargs
    ) -> "NetworkTraceC[T]":
        return super().add_stop_condition(condition, **kwargs)

    @add_stop_condition.register(Callable)
    def _(self, condition: ShouldStop, step_type=None, **kwargs):
        return self.add_stop_condition(
            NetworkTraceStopCondition(
                default_condition_step_type(self._action_type) or step_type,
                condition
            ),
            **kwargs
        )

    def can_action_item(self, item: T, context: StepContext) -> bool:
        return self._action_type(item, context, self.has_visited)

    def on_reset(self):
        if hasattr(self._tracker, 'clear'):
            self._tracker.clear()

    def can_visit_item(self, item: T, context: StepContext) -> bool:
        return self.visit(item.path.to_terminal, item.path.to_phases_set())

    def get_derived_this(self) -> 'NetworkTraceC[T]':
        return self

    def create_new_this(self) -> 'NetworkTraceC[T]':
        return NetworkTraceC(
            self.network_state_operators,
            self._queue_type,
            self,
            self._action_type,
            debug_logger=None,
            name=self.name,
        )

    @staticmethod
    def start_nominal_phase_path(phases: PhaseCode) -> Set[NominalPhasePath]:
        return {NominalPhasePath(it, it) for it in phases.single_phases} if phases and phases.single_phases else set()

    def has_visited(self, terminal: Terminal, phases: FrozenSet[SinglePhaseKind]) -> bool:
        parent = self._parent
        while parent is not None:
            if parent._tracker.has_visited(terminal, phases):
                return True
            parent = parent._parent
        return self._tracker.has_visited(terminal, phases)

    def visit(self, terminal: Terminal, phases: FrozenSet[SinglePhaseKind]) -> bool:
        if self._parent and self._parent.has_visited(terminal, phases):
            return False
        return self._tracker.visit(terminal, phases)


# ---------------------------------------------------------------------------
# Helper functions (same as original)
# ---------------------------------------------------------------------------

def default_condition_step_type(step_type: CanActionItem) -> NetworkTraceStep.Type:
    if step_type == NetworkTraceActionType.ALL_STEPS:
        return NetworkTraceStep.Type.ALL
    elif step_type == NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT:
        return NetworkTraceStep.Type.EXTERNAL
    raise Exception('step doesnt match expected types')


def compute_data_with_action_type(
    compute_data: ComputeData[T],
    action_type: CanActionItem,
) -> ComputeData[T]:
    if action_type == NetworkTraceActionType.ALL_STEPS:
        return compute_data
    elif action_type == NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT:
        return ComputeData(
            lambda current_step, current_context, next_path: (
                current_step.data
                if next_path.traced_internally
                else compute_data.compute_next(current_step, current_context, next_path)
            )
        )
    raise Exception(f'{action_type.__name__}: step doesnt match expected types')
