#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.common.table_town_details import TableTownDetails

__all__ = ["TableStreetAddresses"]


class TableStreetAddresses(TableTownDetails, ABC):

    def __init__(self):
        super().__init__()
        self.postal_code: Column = self._create_column("postal_code", "TEXT", Nullable.NOT_NULL)
        self.po_box: Column = self._create_column("po_box", "TEXT", Nullable.NULL)
        self.building_name: Column = self._create_column("building_name", "TEXT", Nullable.NULL)
        self.floor_identification: Column = self._create_column("floor_identification", "TEXT", Nullable.NULL)
        self.street_name: Column = self._create_column("name", "TEXT", Nullable.NULL)
        self.number: Column = self._create_column("number", "TEXT", Nullable.NULL)
        self.suite_number: Column = self._create_column("suite_number", "TEXT", Nullable.NULL)
        self.type: Column = self._create_column("type", "TEXT", Nullable.NULL)
        self.display_address: Column = self._create_column("display_address", "TEXT", Nullable.NULL)
