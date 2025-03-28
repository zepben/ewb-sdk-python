#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import ConductingEquipment, Tracing

__all__ = ["log_directions"]

from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep


async def log_directions(*conducting_equipment: NetworkTraceStep):
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
        trace.run(cond_equip, False)


async def _step(step: NetworkTraceStep, _: bool):
    for term in step.conducting_equipment.terminals:
        print(f"{step.conducting_equipment.mrid}-T{term.sequence_number}: {{n:{term.normal_feeder_direction}, c:{term.current_feeder_direction}}}")
