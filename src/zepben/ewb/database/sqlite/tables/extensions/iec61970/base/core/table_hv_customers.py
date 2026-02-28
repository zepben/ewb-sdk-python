#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.ewb.database.sqlite.tables.iec61970.base.core.table_equipment_containers import TableEquipmentContainers
from zepben.ewb.model.cim.extensions.zbex import zbex


@zbex
class TableHvCustomers(TableEquipmentContainers):
    """
    [ZBEX] A collection of equipment for organizational purposes, used for grouping distribution resources located at a HV customer site.
    """

    @property
    def name(self) -> str:
        return "hv_customers"
