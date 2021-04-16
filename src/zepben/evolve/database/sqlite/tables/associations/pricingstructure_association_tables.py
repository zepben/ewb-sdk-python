#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable

__all__ = ["TablePricingStructuresTariffs"]


class TablePricingStructuresTariffs(SqliteTable):
    pricing_structure_mrid: Column = None
    tariff_mrid: Column = None

    def __init__(self):
        super(TablePricingStructuresTariffs, self).__init__()
        self.column_index += 1
        self.pricing_structure_mrid = Column(self.column_index, "pricing_structure_mrid", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.tariff_mrid = Column(self.column_index, "tariff_mrid", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "pricing_structures_tariffs"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TablePricingStructuresTariffs, self).unique_index_columns()
        cols.append([self.pricing_structure_mrid, self.tariff_mrid])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TablePricingStructuresTariffs, self).non_unique_index_columns()
        cols.append([self.pricing_structure_mrid])
        cols.append([self.tariff_mrid])
        return cols

