#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.ewb.database.sqlite.tables.iec61970.base.core.table_equipment_containers import TableEquipmentContainers
from zepben.ewb.model.cim.extensions.zbex import zbex


@zbex
class TableLvSubstations(TableEquipmentContainers):
    """
    [ZBEX] A collection of equipment for purposes other than generation or utilization, through which electric energy in bulk is passed for the distribution of
    energy to low voltage network.
    """

    @property
    def name(self) -> str:
        return "lv_substations"
