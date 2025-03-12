#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List, Optional

from zepben.evolve import Terminal, NetworkService, Feeder, PowerTransformer, Switch, ConductingEquipment

__all__ = ["SetDirection"]


class SetDirection:
    """
    Convenience class that provides methods for setting feeder direction on a [NetworkService]
    This class is backed by a [BranchRecursiveTraversal].
    """

    async def run(self, network: NetworkService):
        """
         Apply feeder directions from all feeder head terminals in the network.

         :param network: The network in which to apply feeder directions.
         """
        await self._run_terminals(
            [f.normal_head_terminal for f in network.objects(Feeder) if
             f.normal_head_terminal and not self._is_normally_open_switch(f.normal_head_terminal.conducting_equipment)])

    async def run_terminal(self, terminal: Terminal):
        """
         Apply [FeederDirection.DOWNSTREAM] from the [terminal].

         :param terminal: The terminal to start applying feeder direction from.
         """
        await self._run_terminals([terminal])

    async def _run_terminals(self, start_terminals: List[Terminal]):
        self.normal_traversal.tracker.clear()
        self.current_traversal.tracker.clear()

        for t in start_terminals:
            await self.normal_traversal.reset().run(t)
            await self.current_traversal.reset().run(t)

    @staticmethod
    def _reached_substation_transformer(terminal: Terminal) -> bool:
        ce = terminal.conducting_equipment
        if not ce:
            return False

        return isinstance(ce, PowerTransformer) and ce.num_substations() > 0

    def _is_normally_open_switch(conducting_equipment: Optional[ConductingEquipment]):
        return isinstance(conducting_equipment, Switch) and conducting_equipment.is_normally_open()

