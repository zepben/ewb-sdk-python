#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableIdentifiedObjects

__all__ = ["TablePerLengthLineImpedances", "TablePerLengthLineParameters", "TablePerLengthSequenceImpedances", "TablePerLengthImpedances"]


class TablePerLengthLineParameters(TableIdentifiedObjects):
    pass


class TablePerLengthLineImpedances(TablePerLengthLineParameters):
    pass


class TablePerLengthImpedances(TablePerLengthLineParameters):
    pass


class TablePerLengthSequenceImpedances(TablePerLengthLineImpedances):
    r: Column = None
    x: Column = None
    r0: Column = None
    x0: Column = None
    bch: Column = None
    gch: Column = None
    b0ch: Column = None
    g0ch: Column = None

    def __init__(self):
        super(TablePerLengthSequenceImpedances, self).__init__()
        self.column_index += 1
        self.r = Column(self.column_index, "r", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.x = Column(self.column_index, "x", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.r0 = Column(self.column_index, "r0", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.x0 = Column(self.column_index, "x0", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.bch = Column(self.column_index, "bch", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.gch = Column(self.column_index, "gch", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.b0ch = Column(self.column_index, "b0ch", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.g0ch = Column(self.column_index, "g0ch", "NUMBER", Nullable.NOT_NULL)

    def name(self) -> str:
        return "per_length_sequence_impedances"
