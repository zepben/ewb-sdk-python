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


import logging
from zepben.model.equipment import Equipment
from zepben.model.tracing.tracing import Traversal, SearchType
phase_logger = logging.getLogger("phase_logger")
tracing_logger = logging.getLogger("queue_next")


def normally_open(equip: Equipment, core=None):
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


def currently_open(equip: Equipment, core=None):
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
        tracing_logger.debug(f"Queuing {to_terms[0].mrid} from single terminal equipment {item.mrid}")
        return to_terms

    crs = []
    for term in other_terms:
        crs.extend(term.get_connectivity(exclude=exclude))

    to_terms = [cr.to_terminal for cr in crs]
    tracing_logger.debug(f"Queuing terminals: [{', '.join(t.mrid for t in to_terms)}] from {item.mrid}")
    return to_terms


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
