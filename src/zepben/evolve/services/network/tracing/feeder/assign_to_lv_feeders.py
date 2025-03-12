#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Set, Callable, Optional, Awaitable, Any

from zepben.evolve import AssignToFeeders
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.equipment_container import EquipmentContainer, Feeder
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.lv_feeder import LvFeeder
from zepben.evolve.services.common.resolver import normal_head_terminal
from zepben.evolve.services.network.network_service import NetworkService
from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.evolve.services.network.tracing.traversal.traversal import Traversal

__all__ = ["AssignToLvFeeders"]


class AssignToLvFeeders(AssignToFeeders):
    """
    Convenience class that provides methods for assigning LV feeders on a `NetworkService`.
    Requires that a Feeder have a normalHeadTerminal with associated ConductingEquipment.
    This class is backed by a `BasicTraversal`.
    """

    network_state_operators = NetworkStateOperators.NORMAL

    async def run(self,
                  network: NetworkService,
                  network_state_operators: NetworkStateOperators = NetworkStateOperators.NORMAL,
                  start_terminal: Terminal=None):
        """
        Assign equipment to each feeder in the specified network.

        :param network: The network containing the feeders to process
        """
        self.network_state_operators = network_state_operators

        lv_feeder_start_points = network.lv_feeder_start_points
        terminal_to_aux_equipment = network.aux_equipment_by_terminal

        if start_terminal is None:
            for lv_feeder in list(it for it in network if isinstance(it, LvFeeder)):
                head_equipment = lv_feeder.normal_head_terminal.conducting_equipment
                for feeder in head_equipment.get_filtered_containers(Feeder, self.network_state_operators):
                    self.network_state_operators.associate_energizing_feeder(feeder, lv_feeder)
                await self.run_with_feeders(lv_feeder.normal_head_terminal, lv_feeder_start_points, terminal_to_aux_equipment, [lv_feeder])

        else:
            await self.run_with_feeders(normal_head_terminal, lv_feeder_start_points, terminal_to_aux_equipment, self._lv_feeders_from_terminal(start_terminal))


    def _lv_feeders_from_terminal(self, terminal: Terminal):
        return terminal.conducting_equipment.get_filtered_containers(LvFeeder)(self.network_state_operators)

