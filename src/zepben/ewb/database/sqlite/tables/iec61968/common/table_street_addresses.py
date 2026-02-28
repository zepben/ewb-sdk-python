#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableStreetAddresses"]

from abc import ABC

from zepben.ewb.database.sql.column import Column, Nullable, Type
from zepben.ewb.database.sqlite.tables.iec61968.common.table_town_details import TableTownDetails


class TableStreetAddresses(TableTownDetails, ABC):
    """
    A class representing the ElectronicAddress columns required for the database table.

    :var postal_code: A column storing the postal code for the address.
    :var po_box: A column storing the post office box.
    :var building_name: A column storing the name of a building.
    :var floor_identification: A column storing the identification by name or number, expressed as text, of the floor in the building as part of this address.
    :var street_name: A column storing the name of the street.
    :var number: A column storing the designator of the specific location on the street.
    :var suite_number: A column storing the number of the apartment or suite.
    :var type: A column storing the type of street. Examples include: street, circle, boulevard, avenue, road, drive, etc.
    :var display_address: A column storing the address as it should be displayed to a user.
    :var building_number: A column storing the number of the building.
    """

    def __init__(self):
        super().__init__()
        self.postal_code: Column = self._create_column("postal_code", Type.STRING , Nullable.NULL)
        self.po_box: Column = self._create_column("po_box", Type.STRING, Nullable.NULL)
        self.building_name: Column = self._create_column("building_name", Type.STRING, Nullable.NULL)
        self.floor_identification: Column = self._create_column("floor_identification", Type.STRING, Nullable.NULL)
        self.street_name: Column = self._create_column("name", Type.STRING, Nullable.NULL)
        self.number: Column = self._create_column("number", Type.STRING, Nullable.NULL)
        self.suite_number: Column = self._create_column("suite_number", Type.STRING, Nullable.NULL)
        self.type: Column = self._create_column("type", Type.STRING, Nullable.NULL)
        self.display_address: Column = self._create_column("display_address", Type.STRING, Nullable.NULL)
        self.building_number: Column = self._create_column("building_number", Type.STRING, Nullable.NULL)
