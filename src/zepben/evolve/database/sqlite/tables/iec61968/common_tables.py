#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from enum import Enum
from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableIdentifiedObjects
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable

__all__ = ["TableDocuments", "TableAgreements", "TableLocations", "TableTownDetails", "TableStreetAddresses", "TableLocationStreetAddresses",
           "TableLocationStreetAddressField", "TableOrganisationRoles", "TablePositionPoints", "TableOrganisations"]


# noinspection PyAbstractClass
class TableDocuments(TableIdentifiedObjects):
    title: Column = None
    created_date_time: Column = None
    author_name: Column = None
    type: Column = None
    status: Column = None
    comment: Column = None

    def __init__(self):
        super(TableDocuments, self).__init__()
        self.title = self._create_column("title", "TEXT", Nullable.NOT_NULL)
        self.created_date_time = self._create_column("created_date_time", "TEXT", Nullable.NULL)
        self.author_name = self._create_column("author_name", "TEXT", Nullable.NOT_NULL)
        self.type = self._create_column("type", "TEXT", Nullable.NOT_NULL)
        self.status = self._create_column("status", "TEXT", Nullable.NOT_NULL)
        self.comment = self._create_column("comment", "TEXT", Nullable.NOT_NULL)


# noinspection PyAbstractClass
class TableAgreements(TableDocuments):
    pass


class TableLocations(TableIdentifiedObjects):

    def name(self) -> str:
        return "locations"


# noinspection PyAbstractClass
class TableTownDetails(SqliteTable):
    town_name: Column = None
    state_or_province: Column = None

    def __init__(self):
        super(TableTownDetails, self).__init__()
        self.town_name = self._create_column("town_name", "TEXT", Nullable.NULL)
        self.state_or_province = self._create_column("state_or_province", "TEXT", Nullable.NULL)


# noinspection PyAbstractClass
class TableStreetAddresses(TableTownDetails):
    postal_code: Column = None
    po_box: Column = None
    building_name: Column = None
    floor_identification: Column = None
    street_name: Column = None
    number: Column = None
    suite_number: Column = None
    type: Column = None
    display_address: Column = None

    def __init__(self):
        super(TableStreetAddresses, self).__init__()
        self.postal_code = self._create_column("postal_code", "TEXT", Nullable.NOT_NULL)
        self.po_box = self._create_column("po_box", "TEXT", Nullable.NULL)
        self.building_name = self._create_column("building_name", "TEXT", Nullable.NULL)
        self.floor_identification = self._create_column("floor_identification", "TEXT", Nullable.NULL)
        self.street_name = self._create_column("name", "TEXT", Nullable.NULL)
        self.number = self._create_column("number", "TEXT", Nullable.NULL)
        self.suite_number = self._create_column("suite_number", "TEXT", Nullable.NULL)
        self.type = self._create_column("type", "TEXT", Nullable.NULL)
        self.display_address = self._create_column("display_address", "TEXT", Nullable.NULL)


class TableLocationStreetAddresses(TableStreetAddresses):
    location_mrid: Column = None
    address_field: Column = None

    def __init__(self):
        super(TableLocationStreetAddresses, self).__init__()
        self.location_mrid = self._create_column("location_mrid", "TEXT", Nullable.NOT_NULL)
        self.address_field = self._create_column("address_field", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "location_street_addresses"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableLocationStreetAddresses, self).unique_index_columns()
        cols.append([self.location_mrid, self.address_field])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableLocationStreetAddresses, self).non_unique_index_columns()
        cols.append([self.location_mrid])
        return cols


class TableLocationStreetAddressField(Enum):
    mainAddress = 0
#     secondaryAddress = 1


# noinspection PyAbstractClass
class TableOrganisationRoles(TableIdentifiedObjects):
    organisation_mrid: Column = None

    def __init__(self):
        super(TableOrganisationRoles, self).__init__()
        self.organisation_mrid = self._create_column("organisation_mrid", "TEXT", Nullable.NULL)


class TableOrganisations(TableIdentifiedObjects):

    def name(self) -> str:
        return "organisations"


class TablePositionPoints(SqliteTable):
    location_mrid: Column = None
    sequence_number: Column = None
    x_position: Column = None
    y_position: Column = None

    def __init__(self):
        super(TablePositionPoints, self).__init__()
        self.location_mrid = self._create_column("location_mrid", "TEXT", Nullable.NOT_NULL)
        self.sequence_number = self._create_column("sequence_number", "INTEGER", Nullable.NOT_NULL)
        self.x_position = self._create_column("x_position", "NUMBER", Nullable.NOT_NULL)
        self.y_position = self._create_column("y_position", "NUMBER", Nullable.NOT_NULL)

    def name(self) -> str:
        return "position_points"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TablePositionPoints, self).unique_index_columns()
        cols.append([self.location_mrid, self.sequence_number])
        return cols
