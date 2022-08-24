#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import BasicTraversal, ConductingEquipmentStep, ConductingEquipment


class ConnectedEquipmentTraversal(BasicTraversal[ConductingEquipmentStep]):
    """
    Traversal of `ConductingEquipmentStep` which wraps `BasicTraversal` for the purposes of starting directly from `ConductingEquipment`.
    """

    async def run_from(self, conducting_equipment: ConductingEquipment, can_stop_on_start_item: bool = True):
        """
        Helper function to start the traversal from a [ConductingEquipment] without needing to explicitly creating the [ConductingEquipmentStep].

        :param conducting_equipment: The [ConductingEquipment] to start from.
        :param can_stop_on_start_item: Indicates if the stop conditions should be run on the start item.
        """
        # noinspection PyArgumentList
        await self.run(ConductingEquipmentStep(conducting_equipment), can_stop_on_start_item)
