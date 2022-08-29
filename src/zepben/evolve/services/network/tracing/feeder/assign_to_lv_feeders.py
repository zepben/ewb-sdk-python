#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Set, Callable, Optional, Awaitable, Any

from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.equipment_container import EquipmentContainer
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.lv_feeder import LvFeeder
from zepben.evolve.services.network.network_service import NetworkService
from zepben.evolve.services.network.tracing.feeder.associated_terminal_trace import new_normal_trace, new_current_trace, get_associated_terminals
from zepben.evolve.services.network.tracing.traversals.traversal import Traversal

__all__ = ["AssignToLvFeeders"]


class AssignToLvFeeders:
    """
    Convenience class that provides methods for assigning LV feeders on a `NetworkService`.
    Requires that a Feeder have a normalHeadTerminal with associated ConductingEquipment.
    This class is backed by a `BasicTraversal`.
    """

    def __init__(self, _normal_traversal: Optional[Traversal[Terminal]] = None, _current_traversal: Optional[Traversal[Terminal]] = None):
        self._normal_traversal: Traversal[Terminal] = _normal_traversal if _normal_traversal is not None else new_normal_trace()
        """
        The traversal used to trace the network in its normal state of the network.
        """

        self._current_traversal: Traversal[Terminal] = _current_traversal if _current_traversal is not None else new_current_trace()
        """
        The traversal used to trace the network in its current state of the network.
        """

        self._active_lv_feeder: Optional[LvFeeder] = None  # This will never be optional by the time it is used.
        """
        The LV feeder that is currently being processed.
        """

        self._normal_traversal.add_step_action(self._process_normal)
        self._current_traversal.add_step_action(self._process_current)

    async def run(self, network: NetworkService):
        """
        Assign equipment to each LV feeder in the specified network.

        :param network: The network containing the feeders to process
        """
        lv_feeder_start_points = set()
        for lv_feeder in network.objects(LvFeeder):
            if lv_feeder.normal_head_terminal:
                head_equipment = lv_feeder.normal_head_terminal.conducting_equipment
                if head_equipment:
                    lv_feeder_start_points.add(head_equipment)
                    for feeder in head_equipment.normal_feeders:
                        lv_feeder.add_normal_energizing_feeder(feeder)
                        feeder.add_normal_energized_lv_feeder(lv_feeder)
        self._configure_stop_conditions(self._normal_traversal, lv_feeder_start_points)
        self._configure_stop_conditions(self._current_traversal, lv_feeder_start_points)

        for lv_feeder in network.objects(LvFeeder):
            await self.run_feeder(lv_feeder)

    async def run_feeder(self, lv_feeder: LvFeeder):
        """
        Assign equipment to the specified feeders by tracing from the head terminal.

        :param lv_feeder: The feeder to trace.
        """
        self._active_lv_feeder = lv_feeder
        if not lv_feeder.normal_head_terminal:
            return

        await self._run_from_head_terminal(self._normal_traversal, lv_feeder.normal_head_terminal)
        await self._run_from_head_terminal(self._current_traversal, lv_feeder.normal_head_terminal)

    @staticmethod
    async def _run_from_head_terminal(traversal: Traversal, head_terminal: Terminal):
        traversal.reset()

        traversal.tracker.visit(head_terminal)
        await traversal.apply_step_actions(head_terminal, False)
        traversal.process_queue.extend(get_associated_terminals(head_terminal))

        await traversal.run()

    def _configure_stop_conditions(self, traversal: Traversal, lv_feeder_start_points: Set[ConductingEquipment]):
        traversal.clear_stop_conditions()
        traversal.add_stop_condition(self._reached_equipment(lv_feeder_start_points))
        traversal.add_stop_condition(self._reached_hv)

    @staticmethod
    def _reached_equipment(ce: Set[ConductingEquipment]) -> Callable[[Terminal], Awaitable[bool]]:
        async def check_reached(t: Terminal) -> bool:
            return t.conducting_equipment in ce

        return check_reached

    @staticmethod
    async def _reached_hv(t: Terminal) -> bool:
        ce = t.conducting_equipment
        nominal_voltage = ce and ce.base_voltage and ce.base_voltage.nominal_voltage
        return nominal_voltage is not None and nominal_voltage >= 1000

    async def _process_normal(self, terminal: Terminal, is_stopping: bool):
        # noinspection PyTypeChecker
        self._process(terminal, ConductingEquipment.add_container, LvFeeder.add_equipment, is_stopping)

    async def _process_current(self, terminal: Terminal, is_stopping: bool):
        # noinspection PyTypeChecker
        self._process(terminal, ConductingEquipment.add_current_container, LvFeeder.add_current_equipment, is_stopping)

    def _process(
        self,
        terminal: Optional[Terminal],
        assign_lv_feeder_to_equip: Callable[[ConductingEquipment, EquipmentContainer], Any],
        assign_equip_to_lv_feeder: Callable[[EquipmentContainer, ConductingEquipment], Any],
        is_stopping: bool
    ):
        if is_stopping and self._reached_hv(terminal):
            return

        if terminal.conducting_equipment:
            assign_lv_feeder_to_equip(terminal.conducting_equipment, self._active_lv_feeder)
            assign_equip_to_lv_feeder(self._active_lv_feeder, terminal.conducting_equipment)
