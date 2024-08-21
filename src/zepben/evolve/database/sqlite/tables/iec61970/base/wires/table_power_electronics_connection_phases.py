#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_power_system_resources import TablePowerSystemResources

__all__ = ["TablePowerElectronicsConnectionPhases"]


class TablePowerElectronicsConnectionPhases(TablePowerSystemResources):

    def __init__(self):
        super().__init__()
        self.power_electronics_connection_mrid: Column = self._create_column("power_electronics_connection_mrid", "TEXT", Nullable.NULL)
        self.p: Column = self._create_column("p", "NUMBER", Nullable.NULL)
        self.phase: Column = self._create_column("phase", "TEXT", Nullable.NOT_NULL)
        self.q: Column = self._create_column("q", "NUMBER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "power_electronics_connection_phases"

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.power_electronics_connection_mrid]
