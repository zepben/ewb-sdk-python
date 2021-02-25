#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableIdentifiedObjects

__all__ = ["TablePerLengthLineImpedances", "TablePerLengthLineParameters", "TablePerLengthSequenceImpedances", "TablePerLengthImpedances"]


# noinspection PyAbstractClass
class TablePerLengthLineParameters(TableIdentifiedObjects):
    pass


# noinspection PyAbstractClass
class TablePerLengthLineImpedances(TablePerLengthLineParameters):
    pass


# noinspection PyAbstractClass
class TablePerLengthImpedances(TablePerLengthLineParameters):
    pass


class TablePerLengthSequenceImpedances(TablePerLengthImpedances):
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
        self.r = self._create_column("r", "NUMBER", Nullable.NULL)
        self.x = self._create_column("x", "NUMBER", Nullable.NULL)
        self.r0 = self._create_column("r0", "NUMBER", Nullable.NULL)
        self.x0 = self._create_column("x0", "NUMBER", Nullable.NULL)
        self.bch = self._create_column("bch", "NUMBER", Nullable.NULL)
        self.gch = self._create_column("gch", "NUMBER", Nullable.NULL)
        self.b0ch = self._create_column("b0ch", "NUMBER", Nullable.NULL)
        self.g0ch = self._create_column("g0ch", "NUMBER", Nullable.NULL)

    def name(self) -> str:
        return "per_length_sequence_impedances"
