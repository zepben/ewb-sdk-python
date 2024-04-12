#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_tap_changers import TableTapChangers

__all__ = ["TableRatioTapChangers"]


class TableRatioTapChangers(TableTapChangers):

    def __init__(self):
        super().__init__()
        self.transformer_end_mrid: Column = self._create_column("transformer_end_mrid", "TEXT", Nullable.NULL)
        self.step_voltage_increment: Column = self._create_column("step_voltage_increment", "NUMBER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "ratio_tap_changers"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.transformer_end_mrid]
