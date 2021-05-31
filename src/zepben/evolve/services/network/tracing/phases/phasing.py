#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import copy
import logging
from enum import Enum
from typing import TYPE_CHECKING

from dataclassy import dataclass

if TYPE_CHECKING:
    from zepben.evolve import Terminal, ConductingEquipment, NetworkService
from zepben.evolve.model.cim.iec61970.base.wires.energy_source import EnergySource
from zepben.evolve.model.cim.iec61970.base.wires.switch import Breaker
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.model.phasedirection import PhaseDirection
from zepben.evolve.exceptions import PhaseException
from zepben.evolve.services.network.tracing.connectivity import get_connectivity
from zepben.evolve.exceptions import TracingException
from zepben.evolve.services.network.tracing.phases.phase_status import normal_phases, current_phases
from zepben.evolve.services.network.tracing.queuing_functions import queue_next_terminal
from zepben.evolve.services.network.tracing.traversals.queue import PriorityQueue
from zepben.evolve.services.network.tracing.traversals.tracing import Traversal
from zepben.evolve.services.network.tracing.phases.phase_status import PhaseStatus
from zepben.evolve.services.network.tracing.traversals.branch_recursive_tracing import BranchRecursiveTraversal
from zepben.evolve.services.network.tracing.util import normally_open, currently_open
from typing import Set, Callable, List, Iterable, Optional

__all__ = ["FeederProcessingStatus", "SetPhases", "FeederCbTerminalPhasesByStatus", "DelayedFeederTrace",
           "set_phases_and_queue_next", "set_current_phases_and_queue_next", "set_normal_phases_and_queue_next"]

logger = logging.getLogger("phasing.py")


class FeederProcessingStatus(Enum):
    COMPLETE = 0,
    PARTIAL = 1,
    NONE = 2


@dataclass(slots=True)
class FeederCbTerminalPhasesByStatus:
    terminal: Terminal
    in_phases: Set[SinglePhaseKind] = set()
    none_phases: Set[SinglePhaseKind] = set()
    phases_to_flow: Set[SinglePhaseKind] = set()


@dataclass(slots=True)
class DelayedFeederTrace:
    out_terminal: Terminal
    phases_to_flow: Set[SinglePhaseKind]


class SetPhases(object):
    def __init__(self):
        self.normal_traversal = BranchRecursiveTraversal(queue_next=set_normal_phases_and_queue_next,
                                                         process_queue=PriorityQueue(),
                                                         branch_queue=PriorityQueue())
        self.current_traversal = BranchRecursiveTraversal(queue_next=set_current_phases_and_queue_next,
                                                          process_queue=PriorityQueue(),
                                                          branch_queue=PriorityQueue())

    async def run(self, network: NetworkService):
        # terminals = await _apply_phases_from_feeder_cbs(network)
        await _apply_phases_from_sources(network)
        terminals = [term for es in network.objects(EnergySource) if es.num_phases() > 0 for term in es.terminals]
        if not terminals:
            raise TracingException("No feeder sources were found, tracing cannot be performed.")
        breakers = network.objects(Breaker)
        await self.run_complete(terminals, breakers)

    async def run_complete(self, terminals: Iterable[Terminal], breakers: Iterable[Breaker]):
        feeder_cbs = [br for br in breakers if br.is_substation_breaker()]
        await self._run_normal(terminals, feeder_cbs)
        await self._run_current(terminals, feeder_cbs)

    async def _run_normal(self, terminals, feeder_cbs):
        await run_set_phasing(terminals, feeder_cbs, self.normal_traversal, normally_open, normal_phases)

    async def _run_current(self, terminals, feeder_cbs):
        await run_set_phasing(terminals, feeder_cbs, self.current_traversal, currently_open, current_phases)

    async def run_ce(self, ce: ConductingEquipment, breakers: Iterable[Breaker]):
        if ce.num_terminals() == 0:
            return
        for in_term in ce.terminals:
            normal_phases_to_flow = _get_phases_to_flow(in_term, normally_open, normal_phases)
            current_phases_to_flow = _get_phases_to_flow(in_term, currently_open, current_phases)

            for out_term in ce.terminals:
                if out_term is not in_term:
                    _flow_through_equipment(self.normal_traversal, in_term, out_term, normal_phases_to_flow, normal_phases)
                    _flow_through_equipment(self.current_traversal, in_term, out_term, current_phases_to_flow, current_phases)

        self.normal_traversal.tracker.clear()
        self.current_traversal.tracker.clear()

        await self.run_complete(ce.terminals, breakers)


async def find_es_breaker_terminal(es):
    """
    From an EnergySource finds the closest connected Feeder CB (Breaker that is part of a substation). At the moment we assume that all EnergySource's with
    EnergySourcePhase's will be associated with at least a single feeder circuit breaker, and thus this function given an `EnergySource` will perform a trace
    that returns the first `zepben.evolve.iec61970.base.core.terminal.Terminal` encountered from that `EnergySource` that belongs to a `Breaker`. This
    `zepben.evolve.iec61970.base.core.terminal.Terminal` should always be the most downstream `zepben.evolve.iec61970.base.core.terminal.Terminal` on the
    `Breaker`, and thus can then be used for setting `Direction` downstream and away from this `Breaker`.
    TODO: check how ES are normally connected to feeder CB's.
    """
    out_terminals = set()

    async def stop_on_sub_breaker(term, exc=None):
        if out_terminals:  # stop as soon as we find a substation breaker.
            return True
        try:
            if term.conducting_equipment.is_substation_breaker():
                out_terminals.add(term)
                return True
        except AttributeError:
            return False
        return False

    t = Traversal(queue_next=queue_next_terminal, start_item=es.terminals[0], process_queue=PriorityQueue(), stop_conditions=[stop_on_sub_breaker])
    await t.trace()

    return out_terminals


async def _apply_phases_from_feeder_cbs(network):
    """
    Apply phase and direction on all Feeder Circuit Breakers. Will make all phases on the outgoing Terminal of a
    `Breaker` that is part of a substation have a `Direction` of `OUT`.
    `network` `zepben.evolve.network.Network` to apply phasing on.
    """
    start_terms = []
    # TODO: check if below assumption is correct
    # We find the substation breaker from the networks energy sources as we assume that the ES will be wired below
    # the breaker, and thus we can determine which terminal of the breaker to flow out from and apply phases.
    for es in network.energy_sources.values():
        esp = es.energy_source_phases
        if esp:
            if len(esp) != es.num_cores:
                # TODO: java network phases doesn't throw here, but would throw in the below for loop if num_phases > len(esp). why does java silently handle
                #  less cores?
                logger.error(f"Energy source {es.name} [{es.mrid}] is a source with {len(esp)} and {es.num_phases}. "
                             f"Number of phases should match number of cores. Phasing cannot be applied")
                raise TracingException(f"Energy source {es.name} [{es.mrid}] is a source with {len(esp)} and {es.num_cores}. "
                                       f"Number of phases should match number of cores. Phasing cannot be applied")
            breaker_terms = await find_es_breaker_terminal(es)
            for terminal in breaker_terms:
                for phase in terminal.phases.single_phases:
                    normal_phases(terminal, phase).add(esp[phase].phase, PhaseDirection.OUT)
                    current_phases(terminal, phase).add(esp[phase].phase, PhaseDirection.OUT)
                logger.debug(f"Set {terminal.conducting_equipment.mrid} as Feeder Circuit Breaker with phases {terminal.phases.phase}")
            start_terms.extend(breaker_terms)
    return start_terms


async def _apply_phases_from_sources(network: NetworkService):
    """
    Apply phase and direction on all Feeder Circuit Breakers. Will make all phases on the outgoing Terminal of a
    `Breaker` that is part of a substation have a `Direction` of `OUT`.
    `network` `zepben.evolve.network.Network` to apply phasing on.
    """
    for es in network.objects(EnergySource):
        if es.num_phases() > 0:
            await _apply_phases_from_source(es)


async def _apply_phases_from_source(energy_source: EnergySource):
    if energy_source.num_terminals() == 0:
        return
    es_phases = set()
    for phase in energy_source.phases:
        es_phases.add(phase)

    nominal_phases = set()
    for terminal in energy_source.terminals:
        nominal_phases.update(terminal.phases.single_phases)

    if len(es_phases) != len(nominal_phases):
        logger.warning((f"Energy source {str(energy_source)} is a source with {len(es_phases)} phases and {len(nominal_phases)} nominal phases. "
                        f"Number of phases should match the number of nominal phases!"))

    for term in energy_source.terminals:
        for phase in term.phases.single_phases:
            normal_phases(term, phase).add(phase, PhaseDirection.OUT)
            current_phases(term, phase).add(phase, PhaseDirection.OUT)


# TODO: pass through visited and be smart with it
def set_normal_phases_and_queue_next(terminal, traversal, visited):
    set_phases_and_queue_next(terminal, traversal, normally_open, normal_phases)


def set_current_phases_and_queue_next(terminal, traversal, visited):
    set_phases_and_queue_next(terminal, traversal, currently_open, current_phases)


def set_phases_and_queue_next(current: Terminal,
                              traversal: BranchRecursiveTraversal,
                              open_test: Callable[[ConductingEquipment, SinglePhaseKind], bool],
                              phase_selector: Callable[[Terminal, SinglePhaseKind], PhaseStatus]):
    phases_to_flow = _get_phases_to_flow(current, open_test, phase_selector)

    if current.conducting_equipment:
        for out_terminal in current.conducting_equipment.terminals:
            if out_terminal != current and _flow_through_equipment(traversal, current, out_terminal, phases_to_flow, phase_selector):
                _flow_out_to_connected_terminals_and_queue(traversal, out_terminal, phases_to_flow, phase_selector)


async def run_set_phasing(start_terminals: List[Terminal],
                          process_feeder_cbs: List[Breaker],
                          traversal: BranchRecursiveTraversal,
                          open_test: Callable[[ConductingEquipment, Optional[SinglePhaseKind]], bool],
                          phase_selector: Callable[[Terminal, Optional[SinglePhaseKind]], PhaseStatus]):
    for terminal in start_terminals:
        await _run_terminal(terminal, traversal, phase_selector)

    # We take a copy of the feeder CB's as we will modify the list while processing them.
    process_feeder_cbs = copy.copy(process_feeder_cbs)
    keep_processing = True
    while keep_processing:
        delayed_feeder_traces = []
        for feeder_cb in process_feeder_cbs:
            status = _run_feeder_breaker(feeder_cb, traversal, open_test, phase_selector, delayed_feeder_traces)
            if status == FeederProcessingStatus.COMPLETE:
                process_feeder_cbs.remove(feeder_cb)

        for trace in delayed_feeder_traces:
            await _run_from_out_terminal(traversal, trace.out_terminal, trace.phases_to_flow, phase_selector)
        keep_processing = len(delayed_feeder_traces) > 0


async def _run_terminal(start: Terminal, traversal: BranchRecursiveTraversal, phase_selector: Callable[[Terminal, SinglePhaseKind], PhaseStatus]):
    phases_to_flow = {phase for phase in start.phases.single_phases if phase_selector(start, phase).direction().has(PhaseDirection.OUT)}
    await _run_from_out_terminal(traversal, start, phases_to_flow, phase_selector)


async def _run_from_out_terminal(traversal: BranchRecursiveTraversal, out_terminal: Terminal, phases_to_flow: Set[SinglePhaseKind],
                                 phase_selector: Callable[[Terminal, SinglePhaseKind], PhaseStatus]):
    traversal.reset()
    traversal.tracker.visit(out_terminal)
    _flow_out_to_connected_terminals_and_queue(traversal, out_terminal, phases_to_flow, phase_selector)
    await traversal.trace()


def _flow_out_to_connected_terminals_and_queue(traversal: BranchRecursiveTraversal, out_terminal: Terminal, phases_to_flow: Set[SinglePhaseKind],
                                               phase_selector: Callable[[Terminal, SinglePhaseKind], PhaseStatus]):
    connectivity_results = get_connectivity(out_terminal, phases_to_flow)
    for cr in connectivity_results:
        in_term = cr.to_terminal
        has_added = False
        for oi in cr.nominal_phase_paths:
            out_core = oi.from_phase
            in_core = oi.to_phase
            out_phase = phase_selector(out_terminal, out_core).phase()
            in_phase = phase_selector(in_term, in_core)
            try:
                if in_phase.add(out_phase, PhaseDirection.IN):
                    has_added = True
            except PhaseException as ex:
                raise PhaseException(
                    (f"Attempted to apply more than one phase to [{in_term.conducting_equipment.mrid if in_term.conducting_equipment else in_term.mrid}"
                     f" on nominal phase {oi.to_phase}. Attempted to apply phase {out_phase} to {in_phase.phase()}."), ex)

        if has_added and not traversal.has_visited(in_term):
            if len(connectivity_results) > 1 or (out_terminal.conducting_equipment is not None and out_terminal.conducting_equipment.num_terminals() > 2):
                branch = traversal.create_branch()
                branch.start_item = in_term
                traversal.branch_queue.put(branch)
            else:
                traversal.process_queue.put(in_term)


def _get_phases_to_flow(terminal: Terminal,
                        open_test: Callable[[ConductingEquipment, Optional[SinglePhaseKind]], bool],
                        phase_selector: Callable[[Terminal, SinglePhaseKind], PhaseStatus]):
    phases_to_flow = set()
    if terminal.conducting_equipment is None:
        return phases_to_flow

    if isinstance(terminal.conducting_equipment, Breaker):
        if terminal.conducting_equipment.is_substation_breaker():
            return phases_to_flow

    equip = terminal.conducting_equipment
    for phase in terminal.phases.single_phases:
        if not open_test(equip, phase) and phase_selector(terminal, phase).direction().has(PhaseDirection.IN):
            phases_to_flow.add(phase)
    return phases_to_flow


def _flow_through_equipment(traversal: BranchRecursiveTraversal, in_terminal: Terminal, out_terminal: Terminal, phases_to_flow: Set[SinglePhaseKind],
                            phase_selector: Callable[[Terminal, SinglePhaseKind], PhaseStatus]):
    traversal.tracker.visit(out_terminal)
    has_changes = False

    for phase in phases_to_flow:
        out_phase_status = phase_selector(out_terminal, phase)
        in_phase = phase_selector(in_terminal, phase).phase()
        try:
            applied = out_phase_status.add(in_phase, PhaseDirection.OUT)
            has_changes = applied or has_changes
        except PhaseException as ex:
            raise PhaseException((
                f"Attempted to apply more than one phase to {out_terminal.conducting_equipment.mrid if out_terminal.conducting_equipment else in_terminal.mrid}"
                f" on nominal phase {phase}. Detected phases {out_phase_status.phase()} and {in_phase}. Underlying error was {str(ex)}"),
                ex)
    return has_changes


def _get_feeder_cb_terminal_cores_by_status(feeder_cb: Breaker,
                                            open_test: Callable[[ConductingEquipment, Optional[SinglePhaseKind]], bool],
                                            phase_selector: Callable[[Terminal, SinglePhaseKind], PhaseStatus]):
    res = []
    for terminal in feeder_cb.terminals:
        status = FeederCbTerminalPhasesByStatus(terminal=terminal)
        res.append(status)

        for phase in terminal.phases.single_phases:
            phase_status = phase_selector(terminal, phase)
            if phase_status.direction() == PhaseDirection.IN:
                status.in_phases.add(phase)
                if not open_test(feeder_cb, phase):
                    status.phases_to_flow.add(phase)
            elif phase_status.direction() == PhaseDirection.BOTH:
                status.in_phases.add(phase)
            elif phase_status.direction() == PhaseDirection.NONE:
                status.none_phases.add(phase)
    return res


def _flow_through_feeder_cb_and_queue(in_terminal: FeederCbTerminalPhasesByStatus,
                                      out_terminal: FeederCbTerminalPhasesByStatus,
                                      traversal: BranchRecursiveTraversal,
                                      phase_selector: Callable[[Terminal, SinglePhaseKind], PhaseStatus],
                                      delayed_traces: List,
                                      processed_phases: Set[SinglePhaseKind]):
    if not in_terminal.in_phases:
        return

    phases_to_flow = copy.copy(in_terminal.phases_to_flow)
    for phase in in_terminal.terminal.phases.single_phases:
        if phase in in_terminal.in_phases:
            processed_phases.add(phase)

            # Remove any phases that have already been processed from the other side
            if phase not in out_terminal.none_phases:
                phases_to_flow.remove(phase)

    if _flow_through_equipment(traversal, in_terminal.terminal, out_terminal.terminal, phases_to_flow, phase_selector):
        delayed_traces.append(DelayedFeederTrace(out_terminal.terminal, phases_to_flow))


def _run_feeder_breaker(feeder_cb: Breaker,
                        traversal: BranchRecursiveTraversal,
                        open_test: Callable[[ConductingEquipment, Optional[SinglePhaseKind]], bool],
                        phase_selector: Callable[[Terminal, SinglePhaseKind], PhaseStatus],
                        delayed_traces: List):
    if feeder_cb.num_terminals() not in (1, 2):
        logger.warning(f"Ignoring feeder CB {str(feeder_cb)} with {feeder_cb.num_terminals()} terminals, expected 1 or 2 terminals")
        return FeederProcessingStatus.COMPLETE

    if feeder_cb.num_terminals() == 1:
        set_phases_and_queue_next(next(feeder_cb.terminals), traversal, open_test, phase_selector)
        return FeederProcessingStatus.COMPLETE

    processed_phases = set()
    statuses = _get_feeder_cb_terminal_cores_by_status(feeder_cb, open_test, phase_selector)
    _flow_through_feeder_cb_and_queue(statuses[0], statuses[1], traversal, phase_selector, delayed_traces, processed_phases)
    _flow_through_feeder_cb_and_queue(statuses[1], statuses[0], traversal, phase_selector, delayed_traces, processed_phases)

    nominal_phases = {phase for term in feeder_cb.terminals for phase in term.phases.single_phases}
    if len(processed_phases) == len(nominal_phases):
        return FeederProcessingStatus.COMPLETE
    elif processed_phases:
        return FeederProcessingStatus.PARTIAL
    else:
        return FeederProcessingStatus.NONE
