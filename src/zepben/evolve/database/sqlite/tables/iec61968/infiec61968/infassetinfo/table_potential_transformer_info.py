#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_info import TableAssetInfo

__all__ = ["TablePotentialTransformerInfo"]


class TablePotentialTransformerInfo(TableAssetInfo):

    def __init__(self):
        super().__init__()
        self.accuracy_class: Column = self._create_column("accuracy_class", "TEXT", Nullable.NULL)
        self.nominal_ratio_denominator: Column = self._create_column("nominal_ratio_denominator", "NUMBER", Nullable.NULL)
        self.nominal_ratio_numerator: Column = self._create_column("nominal_ratio_numerator", "NUMBER", Nullable.NULL)
        self.primary_ratio: Column = self._create_column("primary_ratio", "NUMBER", Nullable.NULL)
        self.pt_class: Column = self._create_column("pt_class", "TEXT", Nullable.NULL)
        self.rated_voltage: Column = self._create_column("rated_voltage", "INTEGER", Nullable.NULL)
        self.secondary_ratio: Column = self._create_column("secondary_ratio", "NUMBER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "potential_transformer_info"
