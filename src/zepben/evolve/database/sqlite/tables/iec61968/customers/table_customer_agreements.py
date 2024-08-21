#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.common.table_agreements import TableAgreements

__all__ = ["TableCustomerAgreements"]


class TableCustomerAgreements(TableAgreements):

    def __init__(self):
        super().__init__()
        self.customer_mrid: Column = self._create_column("customer_mrid", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "customer_agreements"

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.customer_mrid]
