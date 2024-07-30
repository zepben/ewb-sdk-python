#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import ConductingEquipment, connected_equipment_trace, ConductingEquipmentStep

__all__ = ["log_directions"]


async def log_directions(*conducting_equipment: ConductingEquipment):
    """
    Logs all the feeder directions of terminals. Useful for debugging.
    """
    for cond_equip in conducting_equipment:
        print()
        print("###############################")
        print(f"Tracing directions from: {cond_equip}")
        print()

        trace = connected_equipment_trace()
        trace.add_step_action(_step)
        await trace.run_from(cond_equip)


async def _step(step: ConductingEquipmentStep, _: bool):
    for term in step.conducting_equipment.terminals:
        print(f"{step.conducting_equipment.mrid}-T{term.sequence_number}: {{n:{term.normal_feeder_direction}, c:{term.current_feeder_direction}}}")
