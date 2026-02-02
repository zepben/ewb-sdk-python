#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableElectronicAddresses"]

from abc import ABC

from zepben.ewb.database.sqlite.tables.sqlite_table import SqliteTable
from zepben.ewb.database.sql.column import Column, Type, Nullable


class TableElectronicAddresses(SqliteTable, ABC):
    """
    A class representing the ElectronicAddress columns required for the database table.

    :var email_1: A column storing the primary email address.
    :var is_primary: A column storing whether this email is the primary email address of the contact.
    :var description: A column storing a description for this email, e.g: work, personal.
    """
    def __init__(self):
        super().__init__()
        self.email_1: Column = self._create_column("email_1", Type.STRING, Nullable.NULL)
        self.is_primary: Column = self._create_column("is_primary", Type.STRING)
        self.description: Column = self._create_column("description", Type.STRING, Nullable.NULL)