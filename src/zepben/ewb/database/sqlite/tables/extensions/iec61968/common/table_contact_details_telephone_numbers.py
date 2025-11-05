#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Generator, List

from zepben.ewb.database.sql.column import Type, Column, Nullable
from zepben.ewb.database.sqlite.tables.iec61968.common.table_telephone_numbers import TableTelephoneNumbers


class TableContactDetailsTelephoneNumbers(TableTelephoneNumbers):
    """
     A class representing the `ContactDetails` to `TelephoneNumber` association columns required for the database table.

    :var contact_details_id: A column that stores the identifier of the contact details associated with the street address.
    """
    def __init__(self):
        super().__init__()
        self.contact_details_id: Column = self._create_column('contact_details_id', Type.STRING, Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return 'contact_details_telephone_numbers'

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield [self.contact_details_id]
