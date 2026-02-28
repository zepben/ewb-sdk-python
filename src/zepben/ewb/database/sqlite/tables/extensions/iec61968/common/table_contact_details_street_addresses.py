#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Generator, List

from zepben.ewb.database.sqlite.tables.iec61968.common.table_street_addresses import TableStreetAddresses
from zepben.ewb.database.sql.column import Type, Column, Nullable


class TableContactDetailsStreetAddresses(TableStreetAddresses):
    """
    A class representing the `ContactDetails` to `StreetAddress` association columns required for the database table.

    :var contact_details_id: A column that stores the identifier of the contact details associated with the street address.
    """

    def __init__(self):
        super().__init__()
        self.contact_details_id: Column = self._create_column('contact_details_id', Type.STRING, Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return 'contact_details_street_addresses'

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.contact_details_id]