#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC

from zepben.ewb.database.sqlite.tables.sqlite_table import SqliteTable
from zepben.ewb.database.sql.column import Type, Column, Nullable


class TableTelephoneNumbers(SqliteTable, ABC):
    """
    A class representing the TelephoneNumber columns required for the database table.

    :var area_code: A column storing the area or region code.
    :var city_code: A column storing the city code.
    :var country_code: A column storing the country code.
    :var dial_out: A column storing the dial out code, for instance to call outside an enterprise.
    :var extension: A column storing the extension for this telephone number.
    :var international_prefix: A column storing the prefix used when calling an international number.
    :var local_number: A column storing the main (local) part of this telephone number.
    :var is_primary: A column storing indicating if this phone number is the primary number.
    :var description: A column storing the description for phone number, e.g: home, work, mobile.
    """
    def __init__(self):
        super().__init__()
        self.area_code: Column = self._create_column('area_code', Type.STRING, Nullable.NULL)
        self.city_code: Column = self._create_column('city_code', Type.STRING, Nullable.NULL)
        self.country_code: Column = self._create_column('country_code', Type.STRING, Nullable.NULL)
        self.dial_out: Column = self._create_column('dial_out', Type.STRING, Nullable.NULL)
        self.extension: Column = self._create_column('extension', Type.STRING, Nullable.NULL)
        self.international_prefix: Column = self._create_column('international_prefix', Type.STRING, Nullable.NULL)
        self.local_number: Column = self._create_column('local_number', Type.STRING, Nullable.NULL)
        self.is_primary: Column = self._create_column('is_primary', Type.BOOLEAN, Nullable.NULL)
        self.description: Column = self._create_column('description', Type.STRING, Nullable.NULL)
