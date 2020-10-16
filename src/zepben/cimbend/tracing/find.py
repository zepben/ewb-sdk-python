

#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations
from dataclasses import dataclass
from zepben.cimbend.tracing.connectivity import ConductingEquipmentToCores
from zepben.cimbend.tracing.util import normal_downstream_trace, current_downstream_trace
from zepben.cimbend.tracing.exceptions import TracingException
from zepben.cimbend.cores import from_count
from typing import Callable, List
from enum import Enum

__all__ = ["Status", "Result", "find_current", "find_normal"]


class Status(Enum):
    SUCCESS = 1,
    NO_PATH = 2



class Result(object):
    status: Status = Status.SUCCESS
    equipment: List[ConductingEquipment] = None


async def _trace(traversal: Traversal, from_: ConductingEquipment, to: ConductingEquipment):
    extent_ids = (from_.mrid, to.mrid)
    path_found = [to is None]
    equip = []

    async def stop_contains(cetc):
        return cetc.conducting_equipment.mrid in extent_ids

    async def step(cetc, is_stopping):
        if is_stopping:
            path_found[0] = True

        equip.append(cetc.conducting_equipment)

    traversal.add_stop_condition(stop_contains)
    traversal.add_step_action(step)
    traversal.reset()
    await traversal.trace(ConductingEquipmentToCores(from_, from_count(from_.num_cores)), can_stop_on_start_item=False)
    # this works off a downstream trace, so if we didn't find a path try reverse from and to in case the "to" point
    # was higher up in the network.
    if not path_found[0]:
        equip = []
        traversal.reset()
        traversal.trace(ConductingEquipmentToCores(to, from_count(to.num_cores)), can_stop_on_start_item=False)

    if path_found[0]:
        return Result(equipment=equip)
    else:
        return Result(status=Status.NO_PATH)


async def _find(traversal_supplier: Callable[[SearchType, ...], Traversal], froms: List[ConductingEquipment],
                tos: List[ConductingEquipment]):
    if len(froms) != len(tos):
        raise TracingException("There must be a From equipment for each To equipment.")

    res = []
    for f, t in zip(froms, tos):
        if f.mrid == t.mrid:
            res.append(Result(equipment={f.mrid: f}))
        else:
            res.append(_trace(traversal_supplier, f, t))
    return res


def find_normal(from_: ConductingEquipment, to: ConductingEquipment):
    return _find(normal_downstream_trace, froms=[from_], tos=[to])


def find_current(from_: ConductingEquipment, to: ConductingEquipment):
    return _find(current_downstream_trace, froms=[from_], tos=[to])
