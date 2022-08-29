#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Set, Callable, Optional, Awaitable, Any

from zepben.evolve import BasicTraversal
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.equipment_container import Feeder, EquipmentContainer
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.power_transformer import PowerTransformer
from zepben.evolve.services.network.network_service import NetworkService
from zepben.evolve.services.network.tracing.feeder.associated_terminal_trace import new_normal_trace, new_current_trace, get_associated_terminals

__all__ = ["AssignToFeeders"]


class AssignToFeeders:
    """
    Convenience class that provides methods for assigning HV/MV feeders on a `NetworkService`.
    Requires that a Feeder have a normalHeadTerminal with associated ConductingEquipment.
    This class is backed by a `BasicTraversal`.
    """

    def __init__(self, _normal_traversal: Optional[BasicTraversal[Terminal]] = None, _current_traversal: Optional[BasicTraversal[Terminal]] = None):
        self._normal_traversal: BasicTraversal[Terminal] = _normal_traversal if _normal_traversal is not None else new_normal_trace()
        """
        The traversal used to trace the network in its normal state of the network.
        """

        self._current_traversal: BasicTraversal[Terminal] = _current_traversal if _current_traversal is not None else new_current_trace()
        """
        The traversal used to trace the network in its current state of the network.
        """

        self._active_feeder: Optional[Feeder] = None  # This will never be optional by the time it is used.
        """
        The feeder that is currently being processed.
        """

        self._normal_traversal.add_step_action(self._process_normal)
        self._current_traversal.add_step_action(self._process_current)

    async def run(self, network: NetworkService):
        """
        Assign equipment to each feeder in the specified network.

        :param network: The network containing the feeders to process
        """
        feeder_start_points = set()
        for feeder in network.objects(Feeder):
            if feeder.normal_head_terminal:
                if feeder.normal_head_terminal.conducting_equipment:
                    feeder_start_points.add(feeder.normal_head_terminal.conducting_equipment)
        self._configure_stop_conditions(self._normal_traversal, feeder_start_points)
        self._configure_stop_conditions(self._current_traversal, feeder_start_points)

        for feeder in network.objects(Feeder):
            await self.run_feeder(feeder)

    async def run_feeder(self, feeder: Feeder):
        """
        Assign equipment to the specified feeders by tracing from the head terminal.

        :param feeder: The feeder to trace.
        """
        self._active_feeder = feeder
        if not feeder.normal_head_terminal:
            return

        await self._run_from_head_terminal(self._normal_traversal, feeder.normal_head_terminal)
        await self._run_from_head_terminal(self._current_traversal, feeder.normal_head_terminal)

    @staticmethod
    async def _run_from_head_terminal(traversal: BasicTraversal, head_terminal: Terminal):
        traversal.reset()

        traversal.tracker.visit(head_terminal)
        await traversal.apply_step_actions(head_terminal, False)
        traversal.process_queue.extend(get_associated_terminals(head_terminal))

        await traversal.run()

    def _configure_stop_conditions(self, traversal: BasicTraversal, feeder_start_points: Set[ConductingEquipment]):
        traversal.clear_stop_conditions()
        traversal.add_stop_condition(self._reached_equipment(feeder_start_points))
        traversal.add_stop_condition(self._reached_substation_transformer)
        traversal.add_stop_condition(self._reached_lv)

    @staticmethod
    def _reached_equipment(ce: Set[ConductingEquipment]) -> Callable[[Terminal], Awaitable[bool]]:
        async def check_reached(t: Terminal) -> bool:
            return t.conducting_equipment in ce

        return check_reached

    @staticmethod
    async def _reached_substation_transformer(t: Terminal) -> bool:
        return isinstance(t.conducting_equipment, PowerTransformer) and t.conducting_equipment.num_substations()

    @staticmethod
    async def _reached_lv(t: Terminal) -> bool:
        ce = t.conducting_equipment
        nominal_voltage = ce and ce.base_voltage and ce.base_voltage.nominal_voltage
        return nominal_voltage is not None and nominal_voltage < 1000

    async def _process_normal(self, terminal: Terminal, is_stopping: bool):
        # noinspection PyTypeChecker
        self._process(terminal, ConductingEquipment.add_container, Feeder.add_equipment, is_stopping)

    async def _process_current(self, terminal: Terminal, is_stopping: bool):
        # noinspection PyTypeChecker
        self._process(terminal, ConductingEquipment.add_current_container, Feeder.add_current_equipment, is_stopping)

    def _process(
        self,
        terminal: Optional[Terminal],
        assign_feeder_to_equip: Callable[[ConductingEquipment, EquipmentContainer], Any],
        assign_equip_to_feeder: Callable[[EquipmentContainer, ConductingEquipment], Any],
        is_stopping: bool
    ):
        if is_stopping and (self._reached_lv(terminal) or self._reached_substation_transformer(terminal)):
            return

        if terminal.conducting_equipment:
            assign_feeder_to_equip(terminal.conducting_equipment, self._active_feeder)
            assign_equip_to_feeder(self._active_feeder, terminal.conducting_equipment)
