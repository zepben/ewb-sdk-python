#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import ConductingEquipment, connected_equipment_trace

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

        await connected_equipment_trace() \
            .add_step_action(_step) \
            .run(cond_equip)


async def _step(conducting_equipment: ConductingEquipment, _: bool):
    for term in conducting_equipment.terminals:
        print(f"{conducting_equipment.mrid}-T{term.sequence_number}: {{n:{term.normal_feeder_direction}, c:{term.current_feeder_direction}}}")
