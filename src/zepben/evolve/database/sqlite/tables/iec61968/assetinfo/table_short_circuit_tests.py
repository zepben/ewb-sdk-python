#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_transformer_test import TableTransformerTest

__all__ = ["TableShortCircuitTests"]


class TableShortCircuitTests(TableTransformerTest):

    def __init__(self):
        super().__init__()
        self.current: Column = self._create_column("current", "NUMBER", Nullable.NULL)
        self.energised_end_step: Column = self._create_column("energised_end_step", "INTEGER", Nullable.NULL)
        self.grounded_end_step: Column = self._create_column("grounded_end_step", "INTEGER", Nullable.NULL)
        self.leakage_impedance: Column = self._create_column("leakage_impedance", "NUMBER", Nullable.NULL)
        self.leakage_impedance_zero: Column = self._create_column("leakage_impedance_zero", "NUMBER", Nullable.NULL)
        self.loss: Column = self._create_column("loss", "INTEGER", Nullable.NULL)
        self.loss_zero: Column = self._create_column("loss_zero", "INTEGER", Nullable.NULL)
        self.power: Column = self._create_column("power", "NUMBER", Nullable.NULL)
        self.voltage: Column = self._create_column("voltage", "NUMBER", Nullable.NULL)
        self.voltage_ohmic_part: Column = self._create_column("voltage_ohmic_part", "NUMBER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "short_circuit_tests"
