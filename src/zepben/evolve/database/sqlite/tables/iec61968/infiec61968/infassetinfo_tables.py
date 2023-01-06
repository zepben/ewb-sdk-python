#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.asset_tables import TableAssetInfo

__all__ = ["TableCurrentTransformerInfo", "TablePotentialTransformerInfo"]


class TableCurrentTransformerInfo(TableAssetInfo):
    accuracy_class: Column
    accuracy_limit: Column
    core_count: Column
    ct_class: Column
    knee_point_voltage: Column
    max_ratio_denominator: Column
    max_ratio_numerator: Column
    nominal_ratio_denominator: Column
    nominal_ratio_numerator: Column
    primary_ratio: Column
    rated_current: Column
    secondary_fls_rating: Column
    secondary_ratio: Column
    usage: Column

    def name(self) -> str:
        return "current_transformer_info"

    def __init__(self):
        super(TableCurrentTransformerInfo, self).__init__()
        self.accuracy_class = self._create_column("accuracy_class", "TEXT", Nullable.NULL)
        self.accuracy_limit = self._create_column("accuracy_limit", "NUMBER", Nullable.NULL)
        self.core_count = self._create_column("core_count", "INTEGER", Nullable.NULL)
        self.ct_class = self._create_column("ct_class", "TEXT", Nullable.NULL)
        self.knee_point_voltage = self._create_column("knee_point_voltage", "INTEGER", Nullable.NULL)
        self.max_ratio_denominator = self._create_column("max_ratio_denominator", "NUMBER", Nullable.NULL)
        self.max_ratio_numerator = self._create_column("max_ratio_numerator", "NUMBER", Nullable.NULL)
        self.nominal_ratio_denominator = self._create_column("nominal_ratio_denominator", "NUMBER", Nullable.NULL)
        self.nominal_ratio_numerator = self._create_column("nominal_ratio_numerator", "NUMBER", Nullable.NULL)
        self.primary_ratio = self._create_column("primary_ratio", "NUMBER", Nullable.NULL)
        self.rated_current = self._create_column("rated_current", "INTEGER", Nullable.NULL)
        self.secondary_fls_rating = self._create_column("secondary_fls_rating", "INTEGER", Nullable.NULL)
        self.secondary_ratio = self._create_column("secondary_ratio", "NUMBER", Nullable.NULL)
        self.usage = self._create_column("usage", "TEXT", Nullable.NULL)


class TablePotentialTransformerInfo(TableAssetInfo):
    accuracy_class: Column
    nominal_ratio_denominator: Column
    nominal_ratio_numerator: Column
    primary_ratio: Column
    pt_class: Column
    rated_voltage: Column
    secondary_ratio: Column

    def name(self) -> str:
        return "potential_transformer_info"

    def __init__(self):
        super(TablePotentialTransformerInfo, self).__init__()
        self.accuracy_class = self._create_column("accuracy_class", "TEXT", Nullable.NULL)
        self.nominal_ratio_denominator = self._create_column("nominal_ratio_denominator", "NUMBER", Nullable.NULL)
        self.nominal_ratio_numerator = self._create_column("nominal_ratio_numerator", "NUMBER", Nullable.NULL)
        self.primary_ratio = self._create_column("primary_ratio", "NUMBER", Nullable.NULL)
        self.pt_class = self._create_column("pt_class", "TEXT", Nullable.NULL)
        self.rated_voltage = self._create_column("rated_voltage", "INTEGER", Nullable.NULL)
        self.secondary_ratio = self._create_column("secondary_ratio", "NUMBER", Nullable.NULL)
