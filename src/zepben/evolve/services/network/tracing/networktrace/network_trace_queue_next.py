#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import TypeVar, Callable, Sequence, Iterable, Generator

from zepben.evolve import TerminalConnectivityConnected
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.connectors import BusbarSection

from zepben.evolve.services.network.tracing.traversal.step_context import StepContext
from zepben.evolve.services.network.tracing.networktrace.compute_data import ComputeData
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.traversal.traversal import Traversal

T = TypeVar('T')

CheckInService = Callable[[ConductingEquipment], bool]


class NetworkTraceQueueNext:
    def basic(self, is_in_service: CheckInService, compute_data: ComputeData[T]) -> Traversal.QueueNext[NetworkTraceStep[T]]:
        return Traversal.QueueNext(lambda item, context, queue_item: list(map(queue_item ,self._next_trace_steps(is_in_service, item, context, compute_data))))

    def branching(self, is_in_service: CheckInService, compute_data: ComputeData[T]) -> Traversal.BranchingQueueNext[NetworkTraceStep[T]]:
        return Traversal.BranchingQueueNext(lambda item, context, queue_item, queue_branch: self._queue_next_steps_branching(list(self._next_trace_steps(is_in_service, item, context, compute_data)), queue_item, queue_branch))

    @staticmethod
    def _queue_next_steps_branching(next_steps: list[NetworkTraceStep[T]],
                                    queue_item: Callable[[NetworkTraceStep[T]], bool],
                                    queue_branch: Callable[[NetworkTraceStep[T]], bool]):
        if len(next_steps) == 1:
            return queue_item(next_steps[0])
        else:
            return [queue_branch(step) for step in next_steps]

    def _next_trace_steps(self,
                          is_in_service: CheckInService,
                          current_step: NetworkTraceStep[T],
                          current_context: StepContext,
                          compute_data: ComputeData[T]
                          ) -> Sequence[NetworkTraceStep[T]]:
        """ Builds a list of next `NetworkTraceStep` to add to the `NetworkTrace` queue """

        next_num_terminal_steps = current_step.next_num_terminal_steps()
        next_num_equipment_steps = current_step.next_num_equipment_steps()
        return list(NetworkTraceStep(
            path,
            next_num_terminal_steps,
            next_num_equipment_steps,
            compute_data.compute_next(current_step, current_context, path)
        ) for path in self._next_step_paths(is_in_service, current_step.path))

    def _next_step_paths(self, is_in_service: CheckInService, path: NetworkTraceStep.Path) -> Generator[NetworkTraceStep.Path, None, None]:
        next_terminals = self._next_terminals(is_in_service, path)

        if len(path.nominal_phase_paths) > 0:
            phase_paths = set(it.to_phase for it in path.nominal_phase_paths)

            for result in (TerminalConnectivityConnected().terminal_connectivity(path.to_terminal, t, phase_paths) for t in next_terminals):
                if result.nominal_phase_paths:
                    yield NetworkTraceStep.Path(path.to_terminal, result.to_terminal, result.nominal_phase_paths)

        else:
            for terminal in next_terminals:
                yield NetworkTraceStep.Path(path.to_terminal, terminal)

    @staticmethod
    def _next_terminals(is_in_service: CheckInService, path: NetworkTraceStep.Path) -> Iterable[Terminal]:
        def __next_terminals():
            if path.traced_internally:
                # We need to step externally to connected terminals. However:
                # Busbars are only modelled with a single terminal. So if we find any we need to step to them before the
                # other (non busbar) equipment connected to the same connectivity node. Once the busbar has been
                # visited we then step to the other non busbar terminals connected to the same connectivity node.
                if path.to_terminal.has_connected_busbars():
                    return (t for t in path.to_terminal.connected_terminals() if t.conducting_equipment is BusbarSection)
                else:
                    return path.to_terminal.connected_terminals()
            
            else:
                # If we just visited a busbar, we step to the other terminals that share the same connectivity node.
                # Otherwise, we internally step to the other terminals on the equipment
                if path.to_equipment is BusbarSection:
                    # We don't need to step to terminals that are busbars as they would have been queued at the same time this busbar step was.
                    # We also don't try and go back to the terminals we came from as we already visited it to get to this busbar.
                    return (t for t in path.to_terminal.connected_terminals() if t != path.from_terminal and t.conducting_equipment is not BusbarSection)
                else:
                    return path.to_terminal.other_terminals()
                    
        def _filter(it: Terminal) -> bool:
            if it.conducting_equipment:
                return is_in_service(it.conducting_equipment)
            return False

        return (t for t in __next_terminals() if _filter(t))
