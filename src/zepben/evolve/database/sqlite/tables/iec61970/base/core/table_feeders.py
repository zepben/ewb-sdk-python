#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_equipment_containers import TableEquipmentContainers

__all__ = ["TableFeeders"]


class TableFeeders(TableEquipmentContainers):

    def __init__(self):
        super().__init__()
        self.normal_head_terminal_mrid: Column = self._create_column("normal_head_terminal_mrid", "TEXT", Nullable.NULL)
        self.normal_energizing_substation_mrid: Column = self._create_column("normal_energizing_substation_mrid", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "feeders"

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.normal_energizing_substation_mrid]
