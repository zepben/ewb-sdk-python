#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Set, Callable, Optional, Awaitable

from dataclassy import dataclass
from zepben.evolve import Equipment
from zepben.evolve.model.cim.iec61970.base.wires.power_transformer import PowerTransformer
from zepben.evolve.services.network.network import NetworkService
from zepben.evolve.model.cim.iec61970.base.core.equipment_container import Feeder, EquipmentContainer
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.services.network.tracing.feeder.associated_terminal_trace import new_normal_trace, new_current_trace, get_associated_terminals
from zepben.evolve.services.network.tracing.traversals.tracing import Traversal

__all__ = ["AssignToFeeders"]


def configure_stop_conditions(traversal: Traversal, feeder_start_points: Set[ConductingEquipment]):
    traversal.clear_stop_conditions()
    traversal.add_stop_condition(reached_equipment(feeder_start_points))
    traversal.add_stop_condition(reached_substation_transformer)


def reached_equipment(ce: Set[ConductingEquipment]) -> Callable[[Terminal], Awaitable[bool]]:
    async def r(t: Terminal) -> bool:
        return t.conducting_equipment in ce
    return r


async def reached_substation_transformer(t: Terminal) -> bool:
    return isinstance(t.conducting_equipment, PowerTransformer) and t.conducting_equipment.num_substations()


@dataclass(slots=True)
class AssignToFeeders(object):
    normal_traversal: Traversal = None
    current_traversal: Traversal = None
    active_feeder: Feeder = None

    def __init__(self, normal_traversal: Traversal = None, current_traversal: Traversal = None):
        self.normal_traversal = normal_traversal if normal_traversal is not None else new_normal_trace()
        self.current_traversal = current_traversal if current_traversal is not None else new_current_trace()
        self.normal_traversal.add_step_action(self.process_normal)
        self.current_traversal.add_step_action(self.process_current)

    async def run(self, network: NetworkService):
        feeder_start_points = set()
        for feeder in network.objects(Feeder):
            if feeder.normal_head_terminal:
                if feeder.normal_head_terminal.conducting_equipment:
                    feeder_start_points.add(feeder.normal_head_terminal.conducting_equipment)
        configure_stop_conditions(self.normal_traversal, feeder_start_points)
        configure_stop_conditions(self.current_traversal, feeder_start_points)

        for feeder in network.objects(Feeder):
            await self.assign_to_feeder(feeder)

    async def assign_to_feeder(self, feeder: Feeder):
        self.active_feeder = feeder
        if not feeder.normal_head_terminal:
            return

        await self._traverse(self.normal_traversal, feeder.normal_head_terminal)
        await self._traverse(self.current_traversal, feeder.normal_head_terminal)

    async def _traverse(self, traversal: Traversal, head_terminal: Terminal):
        traversal.reset()
        traversal.tracker.visit(head_terminal)
        await traversal.apply_step_actions(head_terminal, False)
        traversal.process_queue.extend(get_associated_terminals(head_terminal))

        await traversal.trace()

    async def process_normal(self, terminal: Terminal, is_stopping: bool):
        self.process(terminal.conducting_equipment, terminal.conducting_equipment.add_container, self.active_feeder.add_equipment, is_stopping)

    async def process_current(self, terminal: Terminal, is_stopping: bool):
        self.process(terminal.conducting_equipment, terminal.conducting_equipment.add_current_feeder, self.active_feeder.add_current_equipment, is_stopping)

    def process(self, ce: Optional[ConductingEquipment],
                assign_feeder_to_equip: Callable[[EquipmentContainer], Equipment],
                assign_equip_to_feeder: Callable[[ConductingEquipment], EquipmentContainer],
                is_stopping: bool):
        if is_stopping and isinstance(ce, PowerTransformer):
            return

        if ce:
            assign_feeder_to_equip(self.active_feeder)
            assign_equip_to_feeder(ce)









