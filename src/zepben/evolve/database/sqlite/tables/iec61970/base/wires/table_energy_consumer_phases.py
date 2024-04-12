#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_power_system_resources import TablePowerSystemResources

__all__ = ["TableEnergyConsumerPhases"]


class TableEnergyConsumerPhases(TablePowerSystemResources):

    def __init__(self):
        super().__init__()
        self.energy_consumer_mrid: Column = self._create_column("energy_consumer_mrid", "TEXT", Nullable.NOT_NULL)
        self.phase: Column = self._create_column("phase", "TEXT", Nullable.NOT_NULL)
        self.p: Column = self._create_column("p", "NUMBER", Nullable.NULL)
        self.q: Column = self._create_column("q", "NUMBER", Nullable.NULL)
        self.p_fixed: Column = self._create_column("p_fixed", "NUMBER", Nullable.NULL)
        self.q_fixed: Column = self._create_column("q_fixed", "NUMBER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "energy_consumer_phases"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.energy_consumer_mrid, self.phase]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.energy_consumer_mrid]
