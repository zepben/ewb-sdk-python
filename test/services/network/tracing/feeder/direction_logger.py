#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["log_directions"]

from typing import TypeVar

from zepben.ewb import ConductingEquipment, Tracing

T = TypeVar('T')

from zepben.ewb.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep


async def log_directions(*conducting_equipment: ConductingEquipment):
    """
    Logs all the feeder directions of terminals. Useful for debugging.
    """
    for cond_equip in conducting_equipment:
        print()
        print("###############################")
        print(f"Tracing directions from: {cond_equip}")
        print()

        trace = Tracing.network_trace()
        trace.add_step_action(_step)
        trace.add_queue_condition(lambda *args: True)
        await trace.run(cond_equip, False)


def _step(step: NetworkTraceStep[T], _: None):
    for term in step.path.to_equipment.terminals:
        print(
            f"{step.path.to_terminal.conducting_equipment.mrid}-T{term.sequence_number}: {{n:{term.normal_feeder_direction}, c:{term.current_feeder_direction}}}")
