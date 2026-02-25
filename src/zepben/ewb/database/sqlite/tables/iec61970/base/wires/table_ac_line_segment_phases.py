#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Generator, List

from zepben.ewb.database.sqlite.tables.iec61970.base.core.table_power_system_resources import TablePowerSystemResources
from zepben.ewb.database.sql.column import Column, Nullable


class TableAcLineSegmentPhases(TablePowerSystemResources):

    def __init__(self):
        super().__init__()
        self.ac_line_segment_mrid: Column = self._create_column("ac_line_segment_mrid", "TEXT", Nullable.NULL)
        self.phase: Column = self._create_column("phase", "TEXT", Nullable.NOT_NULL)
        self.sequence_number: Column = self._create_column("sequence_number", "INTEGER", Nullable.NULL)
        self.wire_info_mrid: Column = self._create_column("wire_info_mrid", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "ac_line_segment_phases"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.ac_line_segment_mrid, self.phase]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.ac_line_segment_mrid]
        yield [self.wire_info_mrid]