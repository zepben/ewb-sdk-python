#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableDocuments"]

from abc import ABC

from zepben.ewb.database.sql.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.iec61970.base.core.table_identified_objects import TableIdentifiedObjects


class TableDocuments(TableIdentifiedObjects, ABC):

    def __init__(self):
        super().__init__()
        self.title: Column = self._create_column("title", "TEXT", Nullable.NULL)
        self.created_date_time: Column = self._create_column("created_date_time", "TEXT", Nullable.NULL)
        self.author_name: Column = self._create_column("author_name", "TEXT", Nullable.NULL)
        self.type: Column = self._create_column("type", "TEXT", Nullable.NULL)
        self.status: Column = self._create_column("status", "TEXT", Nullable.NULL)
        self.comment: Column = self._create_column("comment", "TEXT", Nullable.NULL)
