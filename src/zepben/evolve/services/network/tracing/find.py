#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations
from dataclassy import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from zepben.evolve import ConductingEquipment, Traversal
from zepben.evolve.services.network.tracing.phases.phase_step import PhaseStep
from zepben.evolve.services.network.tracing.tracing import normal_downstream_trace, current_downstream_trace
from typing import Callable, List, Optional, Dict
from enum import Enum

__all__ = ["Status", "Result", "find_current", "find_normal"]


class Status(Enum):
    SUCCESS = 1,
    NO_PATH = 2,
    MISMATCHED_FROM_TO = 3


@dataclass(slots=True)
class Result(object):
    status: Status = Status.SUCCESS
    equipment: Optional[Dict[str, ConductingEquipment]] = dict()


async def _trace(traversal_supplier: Callable[[], Traversal], from_: ConductingEquipment, to: Optional[ConductingEquipment]):
    if from_.num_terminals() == 0:
        if to is not None:
            return Result(status=Status.NO_PATH)
        elif from_.num_usage_points() != 0:
            return Result(equipment={from_.mrid: from_})
        else:
            return Result(status=Status.SUCCESS)

    extent_ids = {ce.mrid for ce in (from_, to) if ce is not None}
    path_found = [to is None]
    with_usage_points = {}

    async def stop_contains(phase_step):
        return phase_step.conducting_equipment.mrid in extent_ids

    async def step(phase_step, is_stopping):
        if is_stopping:
            path_found[0] = True

        if phase_step.conducting_equipment.num_usage_points() != 0:
            with_usage_points[phase_step.conducting_equipment.mrid] = phase_step.conducting_equipment

    traversal = traversal_supplier()
    traversal.add_stop_condition(stop_contains)
    traversal.add_step_action(step)
    traversal.reset()
    # noinspection PyArgumentList
    await traversal.run(PhaseStep(from_, frozenset(next(from_.terminals).phases.single_phases)), can_stop_on_start_item=False)
    # this works off a downstream trace, so if we didn't find a path try reverse from and to in case the "to" point was higher up in the network.
    if to is not None and not path_found[0]:
        if to.num_terminals() == 0:
            return Result(status=Status.NO_PATH)
        with_usage_points.clear()
        traversal.reset()
        # noinspection PyArgumentList
        await traversal.run(PhaseStep(to, frozenset(next(to.terminals).phases.single_phases)), can_stop_on_start_item=False)

    if path_found[0]:
        return Result(conducting_equipment=with_usage_points)
    else:
        return Result(status=Status.NO_PATH)


async def _find(traversal_supplier: Callable[[...], Traversal], froms: List[ConductingEquipment], tos: List[ConductingEquipment]) -> List[Result]:
    if len(froms) != len(tos):
        return [Result(status=Status.MISMATCHED_FROM_TO)] * min(len(froms), len(tos))

    res = []
    for f, t in zip(froms, tos):
        if t is not None and f.mrid == t.mrid:
            res.append(Result(equipment={f.mrid: f} if f.num_usage_points() != 0 else None))
        else:
            res.append(_trace(traversal_supplier, f, t))
    return res


def find_normal(from_: ConductingEquipment, to: ConductingEquipment):
    return _find(normal_downstream_trace, froms=[from_], tos=[to])


def find_current(from_: ConductingEquipment, to: ConductingEquipment):
    return _find(current_downstream_trace, froms=[from_], tos=[to])
