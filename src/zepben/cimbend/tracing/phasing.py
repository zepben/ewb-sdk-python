#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import copy
import logging
from dataclasses import field
from enum import Enum
from zepben.cimbend.model.phasedirection import PhaseDirection
from zepben.cimbend.exceptions import CoreException, PhaseException
from zepben.cimbend.tracing.exceptions import TracingException
from zepben.cimbend.tracing.phase_status import normal_phases, current_phases
from zepben.cimbend.tracing.util import queue_next_terminal
from zepben.cimbend.tracing.queue import PriorityQueue
from zepben.cimbend.traversals.tracing import SearchType, Traversal
from zepben.cimbend.tracing.phase_status import PhaseStatus
from zepben.cimbend.traversals.branch_recursive_tracing import BranchRecursiveTraversal
from zepben.cimbend.tracing.util import normally_open, currently_open
from typing import Set, Callable, List

__all__ = ["FeederProcessingStatus", "SetPhases", "FeederCbTerminalCoresByStatus", "DelayedFeederTrace",
           "set_phases_and_queue_next", "set_current_phases_and_queue_next", "set_normal_phases_and_queue_next"]

logger = logging.getLogger("phasing.py")


class FeederProcessingStatus(Enum):
    COMPLETE = 0,
    PARTIAL = 1,
    NONE = 2



class FeederCbTerminalCoresByStatus:
    #__slots__ = ("terminal", "in_cores", "none_cores", "cores_to_flow")
    terminal: Terminal
    in_cores: Set[int] = field(default_factory=set)
    none_cores: Set[int] = field(default_factory=set)
    cores_to_flow: Set[int] = field(default_factory=set)



class DelayedFeederTrace:
    __slots__ = ("out_terminal", "cores_to_flow")
    out_terminal: Terminal
    cores_to_flow: Set[int]


class SetPhases(object):
    def __init__(self):
        self.normal_traversal = BranchRecursiveTraversal(queue_next=set_normal_phases_and_queue_next,
                                                         search_type=SearchType.PRIORITY,
                                                         branch_queue=PriorityQueue())
        self.current_traversal = BranchRecursiveTraversal(queue_next=set_current_phases_and_queue_next,
                                                          search_type=SearchType.PRIORITY,
                                                          branch_queue=PriorityQueue())

    async def run(self, network):
        terminals = await _apply_phases_from_feeder_cbs(network)
        if not terminals:
            raise TracingException("No feeder circuit breakers were found, tracing cannot be performed.")
        await self.run_complete(terminals, network.breakers.values())

    async def run_complete(self, terminals: list, breakers: List[Breaker]):
        feeder_cbs = [br for br in breakers if br.is_substation_breaker()]
        await self._run_normal(terminals, feeder_cbs)
        await self._run_current(terminals, feeder_cbs)

    async def _run_normal(self, terminals, feeder_cbs):
        await run_set_phasing(terminals, feeder_cbs, self.normal_traversal, normally_open, normal_phases)

    async def _run_current(self, terminals, feeder_cbs):
        await run_set_phasing(terminals, feeder_cbs, self.current_traversal, currently_open, current_phases)


async def find_es_breaker_terminal(es):
    """
    From an EnergySource finds the closest connected Feeder CB (Breaker that is part of a substation).
    At the moment we assume that all EnergySource's with EnergySourcePhase's will be associated with at least a
    single feeder circuit breaker, and thus this function given an `EnergySource` will perform a trace that returns
    the first `zepben.cimbend.iec61970.base.core.terminal.Terminal` encountered from that `EnergySource` that belongs to a `Breaker`. This `zepben.cimbend.iec61970.base.core.terminal.Terminal` should always
    be the most downstream `zepben.cimbend.iec61970.base.core.terminal.Terminal` on the `Breaker`, and thus can then be used for setting `Direction` downstream and
    away from this `Breaker`.
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

    t = Traversal(queue_next=queue_next_terminal, start_item=es.terminals[0], search_type=SearchType.BREADTH, stop_conditions=[stop_on_sub_breaker])
    await t.trace()

    return out_terminals


async def _apply_phases_from_feeder_cbs(network):
    """
    Apply phase and direction on all Feeder Circuit Breakers. Will make all phases on the outgoing Terminal of a
    `Breaker` that is part of a substation have a `Direction` of `OUT`.
    `network` `zepben.cimbend.network.Network` to apply phasing on.
    """
    start_terms = []
    # TODO: check if below assumption is correct
    # We find the substation breaker from the networks energy sources as we assume that the ES will be wired below
    # the breaker, and thus we can determine which terminal of the breaker to flow out from and apply phases.
    for es in network.energy_sources.values():
        esp = es.energy_source_phases
        if esp:
            if len(esp) != es.num_cores:
                # TODO: java network phases doesn't throw here, but would throw in the below for loop if num_cores > len(esp). why does java silently handle less cores?
                logger.error(f"Energy source {es.name} [{es.mrid}] is a source with {len(esp)} and {es.num_cores}. Number of phases should match number of cores. Phasing cannot be applied")
                raise TracingException(f"Energy source {es.name} [{es.mrid}] is a source with {len(esp)} and {es.num_cores}. Number of phases should match number of cores. Phasing cannot be applied")
            breaker_terms = await find_es_breaker_terminal(es)
            for terminal in breaker_terms:
                for i in range(terminal.num_cores):
                    terminal.normal_phases(i).add(esp[i].phase, PhaseDirection.OUT)
                    terminal.current_phases(i).add(esp[i].phase, PhaseDirection.OUT)
                logger.debug(f"Set {terminal.conducting_equipment.mrid} as Feeder Circuit Breaker with phases {terminal.phases.phase}")
            start_terms.extend(breaker_terms)
    return start_terms


# TODO: pass through visited and be smart with it
def set_normal_phases_and_queue_next(terminal, traversal, visited):
    set_phases_and_queue_next(terminal, traversal, normally_open, normal_phases)


def set_current_phases_and_queue_next(terminal, traversal, visited):
    set_phases_and_queue_next(terminal, traversal, currently_open, current_phases)


def set_phases_and_queue_next(current: Terminal,
                              traversal: BranchRecursiveTraversal,
                              open_test: Callable[[Equipment, int], bool],
                              phase_selector: Callable[[Terminal, int], PhaseStatus]):
    cores_to_flow = _get_cores_to_flow(current, open_test, phase_selector)

    for out_terminal in current.conducting_equipment.terminals:
        if out_terminal != current and _flow_through_equipment(traversal, current, out_terminal, cores_to_flow, phase_selector):
            _flow_out_to_connected_terminals_and_queue(traversal, out_terminal, cores_to_flow, phase_selector)


async def run_set_phasing(start_terminals: List[Terminal],
                          feeder_cbs_: List[Breaker],
                          traversal: BranchRecursiveTraversal,
                          open_test: Callable[[Equipment, int], bool],
                          phase_selector: Callable[[Terminal, int], PhaseStatus]):
    for terminal in start_terminals:
        await _run_terminal(terminal, traversal, phase_selector)

    processing = True
    while processing:
        feeder_cbs_ = copy.copy(feeder_cbs_)
        delayed_feeder_traces = []
        for feeder_cb in feeder_cbs_:
            status = _run_feeder_breaker(feeder_cb, traversal, open_test, phase_selector, delayed_feeder_traces)
            if status == FeederProcessingStatus.COMPLETE:
                feeder_cbs_.remove(feeder_cb)

        for trace in delayed_feeder_traces:
            await _run_from_out_terminal(traversal, trace.out_terminal, trace.cores_to_flow, phase_selector)
        processing = not len(delayed_feeder_traces) == 0


async def _run_terminal(start: Terminal, traversal: BranchRecursiveTraversal, phase_selector: Callable[[Terminal, int], PhaseStatus]):
    cores_to_flow = set()
    for core in range(start.num_cores):
        if phase_selector(start, core).direction().has(PhaseDirection.OUT):
            cores_to_flow.add(core)
    await _run_from_out_terminal(traversal, start, cores_to_flow, phase_selector)


async def _run_from_out_terminal(traversal: BranchRecursiveTraversal, out_terminal: Terminal, cores_to_flow: set,
                                 phase_selector: Callable[[Terminal, int], PhaseStatus]):
    traversal.reset()
    traversal.tracker.visit(out_terminal)
    _flow_out_to_connected_terminals_and_queue(traversal, out_terminal, cores_to_flow, phase_selector)
    await traversal.trace()


def _flow_out_to_connected_terminals_and_queue(traversal: BranchRecursiveTraversal, out_terminal: Terminal,
                                               cores_to_flow: Set[int], phase_selector: Callable[[Terminal, int], PhaseStatus]):
    """

    `traversal`
    `out_terminal`
    `cores_to_flow`
    `phase_selector`
    Returns
    Raises PhaseException, CoreException if phasing couldn't be added.
    """
    connectivity_results = out_terminal.get_connectivity(cores_to_flow)
    for cr in connectivity_results:
        in_term = cr.to_terminal
        has_added = False
        for oi in cr.core_paths:
            out_core = oi.from_core
            in_core = oi.to_core
            out_phase = phase_selector(out_terminal, out_core).phase()
            in_phase = phase_selector(in_term, in_core)
            try:
                if in_phase.add(out_phase, PhaseDirection.IN):
                    has_added = True
                    if in_phase.direction() == PhaseDirection.BOTH:
                        logger.debug(f"Applied {PhaseDirection.BOTH} to phase {out_phase} on core {in_core} for {in_term.mrid}")
                    else:
                        logger.debug(f"Applied {PhaseDirection.IN} to phase {out_phase} on core {in_core} for {in_term.mrid}")
            except (PhaseException, CoreException) as ex:
                raise PhaseException((f"Attempted to apply more than one phase to [{in_term.conducting_equipment.mrid}|"
                                      f"{in_term.conducting_equipment.name}] on core {in_core}."
                                      f" Current phase was {out_phase} and applied was {in_phase.phase()}."), ex)
        if has_added and not traversal.has_visited(in_term):
            if len(connectivity_results) > 1 or len(out_terminal.conducting_equipment.terminals) > 2:
                branch = traversal.create_branch()
                branch.start_item = in_term
                traversal.branch_queue.put(branch)
            else:
                traversal.process_queue.put(in_term)


def _get_cores_to_flow(terminal: Terminal, open_test: Callable[[Equipment, int], bool], phase_selector: Callable[[Terminal, int], PhaseStatus]):
    cores = set()
    try:
        if terminal.conducting_equipment.is_substation_breaker():
            return cores
    except AttributeError:
        pass

    equip = terminal.conducting_equipment
    for core in range(equip.num_cores):
        if not open_test(equip, core) and phase_selector(terminal, core).direction().has(PhaseDirection.IN):
            cores.add(core)
    return cores


def _flow_through_equipment(traversal: BranchRecursiveTraversal, in_terminal: Terminal, out_terminal: Terminal,
                            cores_to_flow: Set[int], phase_selector: Callable[[Terminal, int], PhaseStatus]):
    has_changes = False
    traversal.tracker.visit(out_terminal)
    for core in cores_to_flow:
        out_phase_status = phase_selector(out_terminal, core)
        try:
            in_phase = phase_selector(in_terminal, core).phase()
            applied = out_phase_status.add(in_phase, PhaseDirection.OUT)
            has_changes = applied or has_changes
            if applied:
                if out_phase_status.direction() == PhaseDirection.BOTH:
                    logger.debug(f"Applied {PhaseDirection.BOTH} to phase {in_phase} on core {core} for {out_terminal.mrid}")
                else:
                    logger.debug(f"Applied {PhaseDirection.OUT} to phase {in_phase} on core {core} for {out_terminal.mrid}")
        except (PhaseException, CoreException) as ex:
            raise PhaseException((f"Attempted to apply more than one phase to {out_terminal.conducting_equipment.mrid} "
                                  f"[{out_terminal.mrid}] on core {core}." 
                                  f" Current phase was {out_phase_status.phase()} and applied was {in_phase}."), ex)
    return has_changes


def _get_feeder_cb_terminal_cores_by_status(feeder_cb: Breaker, open_test: Callable[[Equipment, int], bool],
                                            phase_selector: Callable[[Terminal, int], PhaseStatus]):
    res = []
    for terminal in feeder_cb.terminals:
        status = FeederCbTerminalCoresByStatus(terminal=terminal)
        res.append(status)

        for core in range(terminal.num_cores):
            phase_status = phase_selector(terminal, core)
            if phase_status.direction() == PhaseDirection.IN:
                status.in_cores.add(core)
            if not open_test(feeder_cb, core):
                status.cores_to_flow.add(core)
            elif phase_status.direction() == PhaseDirection.BOTH:
                status.in_cores.add(core)
            elif phase_status.direction() == PhaseDirection.NONE:
                status.none_cores.add(core)
    return res


def _flow_through_feeder_cb_and_queue(in_terminal: FeederCbTerminalCoresByStatus,
                                      out_terminal: FeederCbTerminalCoresByStatus, traversal: BranchRecursiveTraversal,
                                      phase_selector: Callable[[Terminal, int], PhaseStatus], delayed_traces: List,
                                      processed_cores: Set[int]):
    if not in_terminal.in_cores:
        return

    cores_to_flow = copy.copy(in_terminal.cores_to_flow)
    for core in range(in_terminal.terminal.num_cores):
        if core in in_terminal.in_cores:
            processed_cores.add(core)

            if core not in out_terminal.none_cores:
                cores_to_flow.remove(core)
    if _flow_through_equipment(traversal, in_terminal.terminal, out_terminal.terminal, cores_to_flow, phase_selector):
        delayed_traces.append(DelayedFeederTrace(out_terminal.terminal, cores_to_flow))


def _run_feeder_breaker(feeder_cb: Breaker,
                        traversal: BranchRecursiveTraversal,
                        open_test: Callable[[Equipment, int], bool],
                        phase_selector: Callable[[Terminal, int], PhaseStatus],
                        delayed_traces: List ):
    if len(feeder_cb.terminals) not in (1, 2):
        logger.warning(f"Ignoring feeder CB {feeder_cb.name} [{feeder_cb.mrid}] with {len(feeder_cb.terminals)} terminals, expected one or two terminals")
        return FeederProcessingStatus.COMPLETE

    if len(feeder_cb.terminals) == 1:
        set_phases_and_queue_next(feeder_cb.terminals[0], traversal, open_test, phase_selector)
        return FeederProcessingStatus.COMPLETE

    processed_cores = set()
    feeder_cb_terminal_cores_by_status = _get_feeder_cb_terminal_cores_by_status(feeder_cb, open_test, phase_selector)
    _flow_through_feeder_cb_and_queue(feeder_cb_terminal_cores_by_status[0], feeder_cb_terminal_cores_by_status[1], traversal, phase_selector, delayed_traces, processed_cores)
    _flow_through_feeder_cb_and_queue(feeder_cb_terminal_cores_by_status[1], feeder_cb_terminal_cores_by_status[0], traversal, phase_selector, delayed_traces, processed_cores)

    if len(processed_cores) == feeder_cb.num_cores:
        return FeederProcessingStatus.COMPLETE
    elif not processed_cores:
        return FeederProcessingStatus.PARTIAL
    else:
        return FeederProcessingStatus.NONE

