#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_info import TableAssetInfo

__all__ = ["TableCurrentTransformerInfo"]


class TableCurrentTransformerInfo(TableAssetInfo):

    def __init__(self):
        super().__init__()
        self.accuracy_class: Column = self._create_column("accuracy_class", "TEXT", Nullable.NULL)
        self.accuracy_limit: Column = self._create_column("accuracy_limit", "NUMBER", Nullable.NULL)
        self.core_count: Column = self._create_column("core_count", "INTEGER", Nullable.NULL)
        self.ct_class: Column = self._create_column("ct_class", "TEXT", Nullable.NULL)
        self.knee_point_voltage: Column = self._create_column("knee_point_voltage", "INTEGER", Nullable.NULL)
        self.max_ratio_denominator: Column = self._create_column("max_ratio_denominator", "NUMBER", Nullable.NULL)
        self.max_ratio_numerator: Column = self._create_column("max_ratio_numerator", "NUMBER", Nullable.NULL)
        self.nominal_ratio_denominator: Column = self._create_column("nominal_ratio_denominator", "NUMBER", Nullable.NULL)
        self.nominal_ratio_numerator: Column = self._create_column("nominal_ratio_numerator", "NUMBER", Nullable.NULL)
        self.primary_ratio: Column = self._create_column("primary_ratio", "NUMBER", Nullable.NULL)
        self.rated_current: Column = self._create_column("rated_current", "INTEGER", Nullable.NULL)
        self.secondary_fls_rating: Column = self._create_column("secondary_fls_rating", "INTEGER", Nullable.NULL)
        self.secondary_ratio: Column = self._create_column("secondary_ratio", "NUMBER", Nullable.NULL)
        self.usage: Column = self._create_column("usage", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "current_transformer_info"
