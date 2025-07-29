#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TablePricingStructuresTariffs"]

from typing import List, Generator

from zepben.ewb.database.sql.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.sqlite_table import SqliteTable


class TablePricingStructuresTariffs(SqliteTable):
    """
    A class representing the association between PricingStructures and Tariffs.
    """

    def __init__(self):
        super().__init__()
        self.pricing_structure_mrid: Column = self._create_column("pricing_structure_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of PricingStructures."""

        self.tariff_mrid: Column = self._create_column("tariff_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of Tariffs."""

    @property
    def name(self) -> str:
        return "pricing_structures_tariffs"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.pricing_structure_mrid, self.tariff_mrid]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.pricing_structure_mrid]
        yield [self.tariff_mrid]
