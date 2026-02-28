#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TablePricingStructures"]

from zepben.ewb.database.sql.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.iec61968.common.table_documents import TableDocuments


class TablePricingStructures(TableDocuments):

    def __init__(self):
        super().__init__()
        self.code: Column = self._create_column("code", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "pricing_structures"
