#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC
from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_identified_objects import TableIdentifiedObjects

__all__ = ["TableMeasurements"]


class TableMeasurements(TableIdentifiedObjects, ABC):

    def __init__(self):
        super().__init__()
        self.power_system_resource_mrid: Column = self._create_column("power_system_resource_mrid", "TEXT", Nullable.NULL)
        self.remote_source_mrid: Column = self._create_column("remote_source_mrid", "TEXT", Nullable.NULL)
        self.terminal_mrid: Column = self._create_column("terminal_mrid", "TEXT", Nullable.NULL)
        self.phases: Column = self._create_column("phases", "TEXT", Nullable.NOT_NULL)
        self.unit_symbol: Column = self._create_column("unit_symbol", "TEXT", Nullable.NOT_NULL)

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.power_system_resource_mrid]
        yield [self.remote_source_mrid]
        yield [self.terminal_mrid]
