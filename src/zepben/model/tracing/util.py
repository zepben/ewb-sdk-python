"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""


from __future__ import annotations
import logging
from zepben.model.tracing.connectivity import ConductingEquipmentToCores
from zepben.model.direction import Direction
from zepben.model.tracing.tracing import Traversal, SearchType
from zepben.model.tracing.phase_status import normal_phases, current_phases
from typing import Callable

__all__ = ["normally_open", "currently_open", "queue_next_equipment", "queue_next_terminal", "normal_downstream_trace",
           "current_downstream_trace", "get_cores_with_direction", "phase_log"]
phase_logger = logging.getLogger("phase_logger")
tracing_logger = logging.getLogger("queue_next")


def normally_open(equip: Equipment, core: int = None):
    """
    Test if a given core on an equipment is normally open.
    :param equip: The equipment to test
    :param core: The core to test. If None tests all cores.
    :return: True if the equipment is open (de-energised), False otherwise
    """
    try:
        if core is None:
            ret = not equip.normally_in_service
            for core in range(0, equip.num_cores()):
                ret &= equip.normally_open(core)
            return ret
        else:
            return equip.normally_open(core) or not equip.normally_in_service
    except AttributeError:
        # This should only be reachable if equip is normally in service but didn't define normally_open, in which case
        # it's not normally open.
        return not equip.normally_in_service


def currently_open(equip: Equipment, core: int = None):
    """
    Test if a given core on an equipment is open.
    :param equip: The equipment to test
    :param core: The core to test. If None tests all cores.
    :return: True if the equipment is open (de-energised), False otherwise
    """
    try:
        if core is None:
            ret = not equip.in_service
            for core in range(0, equip.num_cores()):
                ret &= equip.is_open(core)
            return ret
        else:
            return not equip.in_service or equip.is_open(core)
    except AttributeError:
        # This should only be reachable if equip is normally in service but didn't define normally_open, in which case
        # it's not normally open.
        return not equip.in_service


def queue_next_equipment(item, exclude=None):
    connected_equips = item.get_connected_equipment(exclude=exclude)
    tracing_logger.debug(f"Queuing connections [{', '.join(e.mrid for e in connected_equips)}] from {item.mrid}")
    return connected_equips


def queue_next_terminal(item, exclude=None):
    """
    Wrapper tracing queue function for queuing terminals via their connectivity
    TODO: CoreTrace: queue_next that allows specifying cores to trace
    :param item:
    :param exclude:
    :return:
    """
    other_terms = item.get_other_terminals()
    if not other_terms:
        # If there are no other terminals we get connectivity for this one and return that. Note that this will
        # also return connections for EnergyConsumer's, but upstream will be covered by the exclude parameter and thus
        # should yield an empty list.
        to_terms = [cr.to_terminal for cr in item.get_connectivity(exclude=exclude)]
        if len(to_terms) > 0:
            tracing_logger.debug(f"Queuing {to_terms[0].mrid} from single terminal equipment {item.mrid}")
        return to_terms

    crs = []
    for term in other_terms:
        crs.extend(term.get_connectivity(exclude=exclude))

    to_terms = [cr.to_terminal for cr in crs]
    tracing_logger.debug(f"Queuing terminals: [{', '.join(t.mrid for t in to_terms)}] from {item.mrid}")
    return to_terms


def normal_downstream_trace(search_type: SearchType = SearchType.PRIORITY, **kwargs):
    """
    Create a downstream trace over nominal phases.
    :param search_type: Search type to perform for this traversal. Defaults to priority traversal based on number of
                        cores.
    :param kwargs: Args to be passed to :class:`zepben.model.tracing.tracing.Traversal`
    :return: A :class:`zepben.model.tracing.tracing.Traversal`
    """
    return Traversal(queue_next=_create_downstream_queue_next(normally_open, normal_phases), search_type=search_type,
                     **kwargs)


def current_downstream_trace(search_type: SearchType = SearchType.PRIORITY, **kwargs):
    """
    Create a downstream trace over current phases
    :param search_type: Search type to perform for this traversal. Defaults to priority traversal based on number of
                        cores.
    :param kwargs: Args to be passed to :class:`zepben.model.tracing.tracing.Traversal`
    :return: A :class:`zepben.model.tracing.tracing.Traversal`
    """
    return Traversal(queue_next=_create_downstream_queue_next(currently_open, current_phases), search_type=search_type,
                     **kwargs)


def _create_downstream_queue_next(open_test: Callable[[Equipment, int], bool], active_phases: Callable[[Terminal, int], PhaseStatus]):
    """
    Creates a queue_next function from the given open test and phase selector for use with tracing
    :param open_test: Function that takes a ConductingEquipment and a core (int) and returns whether the core on the
                      equipment is open (True) or closed (False).
    :param active_phases: A :class:`zepben.model.tracing.phase_status.PhaseStatus`
    :return: A queue_next function for use with :class:`zepben.model.tracing.tracing.BaseTraversal` classes
    """
    def qn(cetc, visited):
        connected_terms = []
        if not cetc:
            return connected_terms
        for term in cetc.equipment.terminals:
            out_cores = get_cores_with_direction(open_test, active_phases, term, cetc.cores, Direction.OUT)
            if out_cores:
                crs = term.get_connectivity(out_cores)
                for cr in crs:
                    if cr.to_equip in visited:
                        continue
                    connected_terms.append(ConductingEquipmentToCores(cr.to_equip, cr.to_cores, cr.from_equip))
        return connected_terms
    return qn


def get_cores_with_direction(open_test, active_phases, terminal, filter_cores, direction):
    """
    Gets the closed cores from terminal in a specified :class:`zepben.model.direction.Direction`
    :param open_test: Function that takes a ConductingEquipment and a core (int) and returns whether the core on the
                      equipment is open (True) or closed (False).
    :param active_phases: A :class:`zepben.model.tracing.phase_status.PhaseStatus`
    :param terminal: :class:`zepben.model.terminal.Terminal` to retrieve cores for
    :param filter_cores: The cores for `terminal` to test. May be a subset of `terminal`'s available cores.
    :param direction: The direction to check against.
    :return: Set of cores that are closed in the specified `Direction`.
    """
    return_cores = set()
    for core in filter_cores:
        if not open_test(terminal.equipment, core):
            if active_phases(terminal, core).direction().has(direction):
                return_cores.add(core)
    return return_cores


async def phase_log(cond_equip):
    msg = ""
    try:
        for e in cond_equip:
            msg = await _phase_log_trace(e)
    except:
        msg = await _phase_log_trace(cond_equip)
    phase_logger.debug(msg)


async def _phase_log_trace(cond_equip):
    log_msg = []

    async def log(e, exc):
        equip_msgs = []
        for i, term in enumerate(e.terminals):
            e_msg = f"{e.mrid}-T{i}:"
            for n in range(term.num_cores):
                ps_n = term.normal_phases(i)
                phase_n_msg = f"n: {ps_n.phase().short_name}:{ps_n.direction().short_name}"
                ps_c = term.current_phases(i)
                phase_c_msg = f"c: {ps_c.phase().short_name}:{ps_c.direction().short_name}"
                e_msg = f"{e_msg} {{core {n}: {phase_n_msg} {phase_c_msg}}}"
            equip_msgs.append(e_msg)
        log_msg.append(equip_msgs)

    trace = Traversal(queue_next=queue_next_equipment, start_item=cond_equip, search_type=SearchType.DEPTH, step_actions=[log])
    await trace.trace()
    return "\n".join([", ".join(x) for x in log_msg])
