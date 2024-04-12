#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_power_system_resources import TablePowerSystemResources

__all__ = ["TableEquipment"]


class TableEquipment(TablePowerSystemResources, ABC):

    def __init__(self):
        super().__init__()
        self.normally_in_service: Column = self._create_column("normally_in_service", "BOOLEAN")
        self.in_service: Column = self._create_column("in_service", "BOOLEAN")
        self.commissioned_date: Column = self._create_column("commissioned_date", "TEXT", Nullable.NULL)
