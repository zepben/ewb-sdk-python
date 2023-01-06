#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableConductingEquipment

__all__ = ["TableConductors", "TableAcLineSegments"]


# noinspection PyAbstractClass
class TableConductors(TableConductingEquipment):
    length: Column = None
    wire_info_mrid: Column = None

    def __init__(self):
        super(TableConductors, self).__init__()
        self.length = self._create_column("length", "NUMBER", Nullable.NULL)
        self.wire_info_mrid = self._create_column("wire_info_mrid", "TEXT", Nullable.NULL)


class TableAcLineSegments(TableConductors):
    per_length_sequence_impedance_mrid: Column = None

    def __init__(self):
        super(TableAcLineSegments, self).__init__()
        self.per_length_sequence_impedance_mrid = self._create_column("per_length_sequence_impedance_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "ac_line_segments"
