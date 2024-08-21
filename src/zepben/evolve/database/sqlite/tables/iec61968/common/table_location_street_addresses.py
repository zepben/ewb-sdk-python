#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.common.table_street_addresses import TableStreetAddresses

__all__ = ["TableLocationStreetAddresses"]


class TableLocationStreetAddresses(TableStreetAddresses):

    def __init__(self):
        super().__init__()
        self.location_mrid: Column = self._create_column("location_mrid", "TEXT", Nullable.NOT_NULL)
        self.address_field: Column = self._create_column("address_field", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "location_street_addresses"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.location_mrid, self.address_field]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.location_mrid]
