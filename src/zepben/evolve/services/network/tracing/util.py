#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations
import logging
from typing import Optional

from zepben.evolve import Switch, ConductingEquipment, SinglePhaseKind
from zepben.evolve.services.network.tracing.queuing_functions import tracing_logger
from zepben.evolve.services.network.tracing.traversals.tracing import Traversal
from zepben.evolve.services.network.tracing.traversals.queue import LifoQueue
from zepben.evolve.services.network.tracing.phases.phase_status import normal_phases, current_phases

__all__ = ["normally_open", "currently_open", "ignore_open", "phase_log"]
phase_logger = logging.getLogger("phase_logger")


def normally_open(equip: ConductingEquipment, phase: Optional[SinglePhaseKind] = None):
    """
    Test if a given phase on an equipment is normally open.
    `equip` The equipment to test
    `phase` The Phase to test. If None tests all phases.
    Returns True if the equipment is open (de-energised), False otherwise
    """
    if isinstance(equip, Switch):
        # noinspection PyUnresolvedReferences
        return not equip.normally_in_service or equip.is_normally_open(phase)
    else:
        return not equip.normally_in_service


def currently_open(equip: ConductingEquipment, phase: Optional[SinglePhaseKind] = None):
    """
    Test if a given phase on an equipment is open.
    `equip` The equipment to test
    `phase` The phase to test. If None tests all phases.
    Returns True if the equipment is open (de-energised), False otherwise
    """
    if isinstance(equip, Switch):
        # noinspection PyUnresolvedReferences
        return not equip.in_service or equip.is_open(phase)
    else:
        return not equip.in_service


def ignore_open(ce: ConductingEquipment, phase: Optional[SinglePhaseKind] = None):
    """
    Test that always returns that the phase is closed.
    `equip` The equipment to test
    `phase` The phase to test. If None tests all cores.
    Returns False 
    """
    return False


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
        for term in e.terminals:
            e_msg = f"{e.mrid}-T{term.sequence_number}:"
            for n in term.phases.single_phases:
                ps_n = normal_phases(term, n)
                phase_n_msg = f"n: {ps_n.phase().short_name}:{ps_n.direction().short_name}"
                ps_c = current_phases(term, n)
                phase_c_msg = f"c: {ps_c.phase().short_name}:{ps_c.direction().short_name}"
                e_msg = f"{e_msg} {{core {n}: {phase_n_msg} {phase_c_msg}}}"
            equip_msgs.append(e_msg)
        log_msg.append(equip_msgs)

    trace = Traversal(queue_next=queue_next_equipment, start_item=cond_equip, process_queue=LifoQueue(), step_actions=[log])
    await trace.trace()
    return "\n".join([", ".join(x) for x in log_msg])


def queue_next_equipment(item, exclude=None):
    connected_equips = item.get_connected_equipment(exclude=exclude)
    tracing_logger.debug(f"Queuing connections [{', '.join(e.mrid for e in connected_equips)}] from {item.mrid}")
    return connected_equips
