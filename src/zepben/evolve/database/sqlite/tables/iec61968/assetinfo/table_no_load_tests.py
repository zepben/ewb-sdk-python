#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_transformer_test import TableTransformerTest

__all__ = ["TableNoLoadTests"]


class TableNoLoadTests(TableTransformerTest):

    def __init__(self):
        super().__init__()
        self.energised_end_voltage: Column = self._create_column("energised_end_voltage", "INTEGER", Nullable.NULL)
        self.exciting_current: Column = self._create_column("exciting_current", "NUMBER", Nullable.NULL)
        self.exciting_current_zero: Column = self._create_column("exciting_current_zero", "NUMBER", Nullable.NULL)
        self.loss: Column = self._create_column("loss", "INTEGER", Nullable.NULL)
        self.loss_zero: Column = self._create_column("loss_zero", "INTEGER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "no_load_tests"
