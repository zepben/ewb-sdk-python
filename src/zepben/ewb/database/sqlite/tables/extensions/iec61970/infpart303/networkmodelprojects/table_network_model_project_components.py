#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableNetworkModelProjectComponents"]

from abc import ABC

from zepben.ewb.database.sql.column import Column, Nullable, Type
from zepben.ewb.database.sqlite.tables.iec61970.base.core.table_identified_objects import TableIdentifiedObjects


class TableNetworkModelProjectComponents(TableIdentifiedObjects, ABC):
    """
    A class representing the NetworkModelProjectComponent columns required for the database table.
    """

    def __init__(self):
        super().__init__()
        self.created: Column = self._create_column("created", Type.TIMESTAMP, Nullable.NULL)
        self.updated: Column = self._create_column("updated", Type.TIMESTAMP, Nullable.NULL)
        self.closed: Column = self._create_column("closed", Type.TIMESTAMP, Nullable.NULL)
        self.parent_mrid: Column = self._create_column("parent_mrid", Type.STRING, Nullable.NULL)

    @property
    def non_unique_index_columns(self):
        yield from super().non_unique_index_columns
        yield [self.parent_mrid]
