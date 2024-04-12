#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_per_length_impedances import TablePerLengthImpedances

__all__ = ["TablePerLengthSequenceImpedances"]


class TablePerLengthSequenceImpedances(TablePerLengthImpedances):

    def __init__(self):
        super().__init__()
        self.r: Column = self._create_column("r", "NUMBER", Nullable.NULL)
        self.x: Column = self._create_column("x", "NUMBER", Nullable.NULL)
        self.r0: Column = self._create_column("r0", "NUMBER", Nullable.NULL)
        self.x0: Column = self._create_column("x0", "NUMBER", Nullable.NULL)
        self.bch: Column = self._create_column("bch", "NUMBER", Nullable.NULL)
        self.gch: Column = self._create_column("gch", "NUMBER", Nullable.NULL)
        self.b0ch: Column = self._create_column("b0ch", "NUMBER", Nullable.NULL)
        self.g0ch: Column = self._create_column("g0ch", "NUMBER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "per_length_sequence_impedances"
