#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_info import TableAssetInfo

__all__ = ["TableTransformerEndInfo"]


class TableTransformerEndInfo(TableAssetInfo):

    def __init__(self):
        super().__init__()
        self.connection_kind: Column = self._create_column("connection_kind", "TEXT", Nullable.NOT_NULL)
        self.emergency_s: Column = self._create_column("emergency_s", "INTEGER", Nullable.NULL)
        self.end_number: Column = self._create_column("end_number", "INTEGER", Nullable.NOT_NULL)
        self.insulation_u: Column = self._create_column("insulation_u", "INTEGER", Nullable.NULL)
        self.phase_angle_clock: Column = self._create_column("phase_angle_clock", "INTEGER", Nullable.NULL)
        self.r: Column = self._create_column("r", "NUMBER", Nullable.NULL)
        self.rated_s: Column = self._create_column("rated_s", "INTEGER", Nullable.NULL)
        self.rated_u: Column = self._create_column("rated_u", "INTEGER", Nullable.NULL)
        self.short_term_s: Column = self._create_column("short_term_s", "INTEGER", Nullable.NULL)
        self.transformer_tank_info_mrid: Column = self._create_column("transformer_tank_info_mrid", "TEXT", Nullable.NULL)
        self.energised_end_no_load_tests: Column = self._create_column("energised_end_no_load_tests", "TEXT", Nullable.NULL)
        self.energised_end_short_circuit_tests: Column = self._create_column("energised_end_short_circuit_tests", "TEXT", Nullable.NULL)
        self.grounded_end_short_circuit_tests: Column = self._create_column("grounded_end_short_circuit_tests", "TEXT", Nullable.NULL)
        self.open_end_open_circuit_tests: Column = self._create_column("open_end_open_circuit_tests", "TEXT", Nullable.NULL)
        self.energised_end_open_circuit_tests: Column = self._create_column("energised_end_open_circuit_tests", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "transformer_end_info"

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.transformer_tank_info_mrid]
        yield [self.energised_end_no_load_tests]
        yield [self.energised_end_short_circuit_tests]
        yield [self.grounded_end_short_circuit_tests]
        yield [self.open_end_open_circuit_tests]
        yield [self.energised_end_open_circuit_tests]
