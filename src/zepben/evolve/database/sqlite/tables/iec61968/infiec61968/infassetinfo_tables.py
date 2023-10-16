#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

from zepben.evolve import SqliteTable
from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.asset_tables import TableAssetInfo

__all__ = ["TableCurrentRelayInfo", "TableCurrentTransformerInfo", "TablePotentialTransformerInfo", "TableRecloseDelays"]


class TableRecloseDelays(SqliteTable):
    current_relay_info_mrid: Column = None
    reclose_delay: Column = None
    sequence_number: Column = None

    def __init__(self):
        super(TableRecloseDelays, self).__init__()
        self.current_relay_info_mrid = self._create_column("current_relay_info_mrid", "TEXT", Nullable.NOT_NULL)
        self.reclose_delay = self._create_column("reclose_delay", "NUMBER", Nullable.NOT_NULL)
        self.sequence_number = self._create_column("sequence_number", "INTEGER", Nullable.NOT_NULL)

    def name(self) -> str:
        return "reclose_delays"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableRecloseDelays, self).unique_index_columns()
        cols.append([self.current_relay_info_mrid, self.sequence_number])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableRecloseDelays, self).non_unique_index_columns()
        cols.append([self.current_relay_info_mrid])
        return cols

    def select_sql(self):
        return super(TableRecloseDelays, self).select_sql() + " ORDER BY current_relay_info_mrid, sequence_number ASC;"


class TableCurrentRelayInfo(TableAssetInfo):
    curve_setting: Column = None

    def __init__(self):
        super(TableCurrentRelayInfo, self).__init__()
        self.curve_setting = self._create_column("curve_setting", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "current_relay_info"


class TableCurrentTransformerInfo(TableAssetInfo):
    accuracy_class: Column = None
    accuracy_limit: Column = None
    core_count: Column = None
    ct_class: Column = None
    knee_point_voltage: Column = None
    max_ratio_denominator: Column = None
    max_ratio_numerator: Column = None
    nominal_ratio_denominator: Column = None
    nominal_ratio_numerator: Column = None
    primary_ratio: Column = None
    rated_current: Column = None
    secondary_fls_rating: Column = None
    secondary_ratio: Column = None
    usage: Column = None

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

    def name(self) -> str:
        return "current_transformer_info"


class TablePotentialTransformerInfo(TableAssetInfo):
    accuracy_class: Column = None
    nominal_ratio_denominator: Column = None
    nominal_ratio_numerator: Column = None
    primary_ratio: Column = None
    pt_class: Column = None
    rated_voltage: Column = None
    secondary_ratio: Column = None

    def __init__(self):
        super(TablePotentialTransformerInfo, self).__init__()
        self.accuracy_class = self._create_column("accuracy_class", "TEXT", Nullable.NULL)
        self.nominal_ratio_denominator = self._create_column("nominal_ratio_denominator", "NUMBER", Nullable.NULL)
        self.nominal_ratio_numerator = self._create_column("nominal_ratio_numerator", "NUMBER", Nullable.NULL)
        self.primary_ratio = self._create_column("primary_ratio", "NUMBER", Nullable.NULL)
        self.pt_class = self._create_column("pt_class", "TEXT", Nullable.NULL)
        self.rated_voltage = self._create_column("rated_voltage", "INTEGER", Nullable.NULL)
        self.secondary_ratio = self._create_column("secondary_ratio", "NUMBER", Nullable.NULL)

    def name(self) -> str:
        return "potential_transformer_info"
