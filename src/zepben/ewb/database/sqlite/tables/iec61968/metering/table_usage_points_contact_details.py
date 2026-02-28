#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Generator, List

from zepben.ewb.database.sql.column import Type, Nullable, Column
from zepben.ewb.database.sqlite.tables.extensions.iec61968.common.table_contact_details import TableContactDetails


class TableUsagePointsContactDetails(TableContactDetails):
    """
    A class representing the UsagePoint to ContactDetails association columns required for the database table.

    :var usage_point_mrid: A column that stores the identifier of the usage point associated with the contact details.
    """
    def __init__(self):
        super().__init__()
        self.usage_point_mrid: Column = self._create_column('usage_point_mrid', Type.STRING, Nullable.NULL)

    @property
    def name(self) -> str:
        return "usage_point_contact_details"

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield [self.usage_point_mrid]
