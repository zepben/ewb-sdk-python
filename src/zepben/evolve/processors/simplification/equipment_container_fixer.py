#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve.processors.simplification.reshape import Reshape

from zepben.evolve import NetworkService, EquipmentContainer, Equipment
from zepben.evolve.processors.simplification.reshape_post_processor import ReshapePostProcessor


class EquipmentContainerFixer(ReshapePostProcessor):

    def process(self, service: NetworkService, cumulativeReshapes: Reshape):
        original_container_list = service.objects(EquipmentContainer)
        for container in original_container_list:
            original_equipment_list = list(container.equipment)
            for eq in original_equipment_list:
                if eq.mrid in cumulativeReshapes.originalToNew and cumulativeReshapes.originalToNew[eq.mrid] is not None:
                    container.remove_equipment(eq)
                    for newIO in cumulativeReshapes.originalToNew[eq.mrid]:
                        if isinstance(newIO, Equipment):
                            container.add_equipment(newIO)

            original_current_equipment_list = list(container.current_equipment)
            for eq in original_current_equipment_list:
                if eq.mrid in cumulativeReshapes.originalToNew and cumulativeReshapes.originalToNew[eq.mrid] is not None:
                    container.remove_current_equipment(eq)
                    for newIO in cumulativeReshapes.originalToNew[eq.mrid]:
                        if isinstance(newIO, Equipment):
                            container.add_current_equipment(newIO)
