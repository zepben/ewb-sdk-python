#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.core_tables import TableConductingEquipment


class TableConductors(TableConductingEquipment):
    length: Column = None
    wire_info_mrid: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.length = Column(self.column_index, "length", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.wire_info_mrid = Column(self.column_index, "wire_info_mrid", "TEXT", Nullable.NOT_NULL)


class TableAcLineSegments(TableConductors):
    per_length_sequence_impedance_mrid: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.per_length_sequence_impedance_mrid = Column(self.column_index, "per_length_sequence_impedance_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "ac_line_segments"

