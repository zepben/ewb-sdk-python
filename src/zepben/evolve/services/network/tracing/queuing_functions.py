#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
from typing import Optional, Iterable, Set

from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.services.network.tracing.connectivity import get_connected_equipment


__all__ = ["conducting_equipment_queue_next", "queue_next_terminal", "tracing_logger"]


tracing_logger = logging.getLogger("queue_next")


def conducting_equipment_queue_next(conducting_equipment: Optional[ConductingEquipment], exclude: Optional[Set] = None) -> Iterable[ConductingEquipment]:
    """
    Get the next `ConductingEquipment` to queue next as determined by `conducting_equipment`s connectivity.
    `conducting_equipment` the `ConductingEquipment` to fetch connected equipment for.
    `exclude` Any `ConductingEquipment` that should be excluded from the result.
    Returns a list of `ConductingEquipment` that should be queued next.
    """
    if exclude is None:
        exclude = []

    if conducting_equipment:
        crs = get_connected_equipment(conducting_equipment, exclude)
        return [cr.to_equip for cr in crs if cr.to_equip and cr.to_equip not in exclude]
    return []


def queue_next_terminal(item, exclude: Optional[Set] = None):
    """
    Wrapper tracing queue function for fetching the terminals that should be queued based on their connectivity

    `item` The Terminal to fetch connected `zepben.evolve.iec61970.base.core.terminal.Terminal`s for.
    `exclude` set of `Terminal`s to be excluded from queuing.
    Returns a list of `zepben.evolve.iec61970.base.core.terminal.Terminal`s to be queued
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

