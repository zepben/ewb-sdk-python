#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableAgreements"]

from abc import ABC

from zepben.ewb import Column, Nullable
from zepben.ewb.database.sqlite.tables.iec61968.common.table_documents import TableDocuments


class TableAgreements(TableDocuments, ABC):
    def __init__(self):
        super().__init__()
        self.validity_interval_start: Column = self._create_column("validity_interval_start", "TEXT", Nullable.NULL)
        self.validity_interval_end: Column = self._create_column("validity_interval_end", "TEXT", Nullable.NULL)
