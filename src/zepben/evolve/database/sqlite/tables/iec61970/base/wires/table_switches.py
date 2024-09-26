#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_conducting_equipment import TableConductingEquipment

__all__ = ["TableSwitches"]


class TableSwitches(TableConductingEquipment, ABC):

    def __init__(self):
        super().__init__()
        self.normal_open: Column = self._create_column("normal_open", "INTEGER", Nullable.NOT_NULL)
        self.open: Column = self._create_column("open", "INTEGER", Nullable.NOT_NULL)
        self.rated_current: Column = self._create_column("rated_current", "NUMBER", Nullable.NULL)
        self.switch_info_mrid: Column = self._create_column("switch_info_mrid", "TEXT", Nullable.NULL)
