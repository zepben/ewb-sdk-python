#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_switches import TableSwitches

__all__ = ["TableCuts"]


class TableCuts(TableSwitches, ABC):

    def __init__(self):
        super().__init__()
        self.length_from_terminal_1: Column = self._create_column("length_from_terminal_1", "NUMBER", Nullable.NULL)
        self.ac_line_segment_mrid: Column = self._create_column("ac_line_segment_mrid", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "cuts"
