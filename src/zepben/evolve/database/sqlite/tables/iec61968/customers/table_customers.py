#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.common.table_organisation_roles import TableOrganisationRoles

__all__ = ["TableCustomers"]


class TableCustomers(TableOrganisationRoles):

    def __init__(self):
        super().__init__()
        self.kind: Column = self._create_column("kind", "TEXT", Nullable.NOT_NULL)
        self.num_end_devices: Column = self._create_column("num_end_devices", "INTEGER", Nullable.NOT_NULL)
        self.special_need: Column = self._create_column("special_need", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "customers"
