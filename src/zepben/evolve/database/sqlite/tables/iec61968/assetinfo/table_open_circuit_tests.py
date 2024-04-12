#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_transformer_test import TableTransformerTest

__all__ = ["TableOpenCircuitTests"]


class TableOpenCircuitTests(TableTransformerTest):

    def __init__(self):
        super().__init__()
        self.energised_end_voltage: Column = self._create_column("energised_end_step", "INTEGER", Nullable.NULL)
        self.energised_end_step: Column = self._create_column("energised_end_voltage", "INTEGER", Nullable.NULL)
        self.open_end_step: Column = self._create_column("open_end_step", "INTEGER", Nullable.NULL)
        self.open_end_voltage: Column = self._create_column("open_end_voltage", "INTEGER", Nullable.NULL)
        self.phase_shift: Column = self._create_column("phase_shift", "NUMBER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "open_circuit_tests"
