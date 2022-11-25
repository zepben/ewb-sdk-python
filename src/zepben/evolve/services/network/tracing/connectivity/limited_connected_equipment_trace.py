#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Callable, List, Dict, Optional

from dataclassy import dataclass

from zepben.evolve import Terminal, FeederDirection, ConductingEquipment, ConductingEquipmentStep
from zepben.evolve.services.network.tracing.connectivity.connected_equipment_traversal import ConnectedEquipmentTraversal


@dataclass(slots=True)
class LimitedConnectedEquipmentTrace:
    """
    A class for finding the connected equipment.
    """

    create_traversal: Callable[[], ConnectedEquipmentTraversal]
    """
    Get the `ConnectedEquipmentTraversal` used to traverse the network. Should be either `tracing.normal_connected_equipment_trace` or
    `tracing.current_connected_equipment_trace`, depending on the network state you want to trace.
    """

    get_terminal_direction: Callable[[Terminal], FeederDirection]
    """
    Used to get the `FeederDirection` of a `Terminal`. Should be either `lambda it: it.normal_feeder_direction` or
    `lambda it: it.current_feeder_direction`, depending on the network state you want to trace.
    """

    async def run(
        self,
        starting_equipment: List[ConductingEquipment],
        maximum_steps: int = 1,
        feeder_direction: Optional[FeederDirection] = None
    ) -> Dict[ConductingEquipment, int]:
        """
        Run the trace from the `starting_equipment`.

        :param starting_equipment: The `ConductingEquipment` to start tracing from.
        :param maximum_steps: The maximum number of steps to trace out [1..100]. Defaults to 1.
        :param feeder_direction: The optional [FeederDirection] of the connected equipment you want to return. Default null (all).
        :return:
        """
        check_steps = maximum_steps if maximum_steps > 1 else 1
        check_steps = check_steps if check_steps < 100 else 100

        matching_equipment = await (self._run_with_direction(starting_equipment, check_steps, feeder_direction) if feeder_direction else
                                    self._run_without_direction(starting_equipment, check_steps))

        equipment_steps = {}
        for me in matching_equipment:
            dict.setdefault(equipment_steps, me.conducting_equipment, []).append(me.step)

        return {k: min(v) for k, v in equipment_steps.items()}

    async def _run_with_direction(
        self,
        starting_equipment: List[ConductingEquipment],
        maximum_steps: int,
        feeder_direction: FeederDirection
    ) -> List[ConductingEquipmentStep]:
        # noinspection PyArgumentList
        matching_equipment = [ConductingEquipmentStep(it) for it in starting_equipment]

        to_process = [t for it in starting_equipment for t in it.terminals if self.get_terminal_direction(t) == feeder_direction]
        to_process = [t.conducting_equipment for it in to_process for t in it.connected_terminals() if t.conducting_equipment is not None]

        async def reached_last_step(it: ConductingEquipmentStep):
            return it.step >= maximum_steps - 1

        async def found_starting_equipment(it: ConductingEquipmentStep):
            return it.conducting_equipment in starting_equipment

        async def has_no_valid_terminals(it: ConductingEquipmentStep):
            return not any(self.get_terminal_direction(t) == feeder_direction for t in it.conducting_equipment.terminals)

        async def add_matching_equipment(it: ConductingEquipmentStep, _: bool):
            # noinspection PyArgumentList
            matching_equipment.append(ConductingEquipmentStep(it.conducting_equipment, it.step + 1))

        for start in to_process:
            traversal = self.create_traversal()

            traversal.add_stop_condition(reached_last_step)
            traversal.add_stop_condition(found_starting_equipment)
            traversal.add_stop_condition(has_no_valid_terminals)
            traversal.add_step_action(add_matching_equipment)

            await traversal.run_from(start)

        if feeder_direction in (FeederDirection.BOTH, FeederDirection.NONE):
            return [it for it in matching_equipment if any(self.get_terminal_direction(t) == feeder_direction for t in it.conducting_equipment.terminals)]
        else:
            return matching_equipment

    async def _run_without_direction(self, starting_equipment: List[ConductingEquipment], maximum_steps: int) -> List[ConductingEquipmentStep]:
        matching_equipment = []

        async def reached_last_step(it: ConductingEquipmentStep):
            return it.step >= maximum_steps

        async def add_matching_equipment(it: ConductingEquipmentStep, _: bool):
            matching_equipment.append(it)

        for start in starting_equipment:
            traversal = self.create_traversal()

            traversal.add_stop_condition(reached_last_step)
            traversal.add_step_action(add_matching_equipment)

            await traversal.run_from(start, False)

        return matching_equipment
