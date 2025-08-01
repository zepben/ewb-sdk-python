#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableProtectionRelayFunctionThresholds"]

from typing import List, Generator

from zepben.ewb.database.sqlite.tables.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.sqlite_table import SqliteTable


class TableProtectionRelayFunctionThresholds(SqliteTable):

    def __init__(self):
        super().__init__()
        self.protection_relay_function_mrid: Column = self._create_column("protection_relay_function_mrid", "TEXT", Nullable.NOT_NULL)
        self.sequence_number: Column = self._create_column("sequence_number", "INTEGER", Nullable.NOT_NULL)
        self.unit_symbol: Column = self._create_column("unit_symbol", "TEXT", Nullable.NOT_NULL)
        self.value: Column = self._create_column("value", "NUMBER", Nullable.NOT_NULL)
        self.name_: Column = self._create_column("name", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "protection_relay_function_thresholds"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.protection_relay_function_mrid, self.sequence_number]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.protection_relay_function_mrid]
