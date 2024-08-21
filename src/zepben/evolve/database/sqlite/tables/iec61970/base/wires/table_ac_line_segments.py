#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_conductors import TableConductors

__all__ = ["TableAcLineSegments"]


class TableAcLineSegments(TableConductors):

    def __init__(self):
        super().__init__()
        self.per_length_sequence_impedance_mrid: Column = self._create_column("per_length_sequence_impedance_mrid", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "ac_line_segments"
