#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC
from enum import Enum
from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.core_tables import TableIdentifiedObjects
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


class TableDocuments(TableIdentifiedObjects):
    title: Column = None
    created_date_time: Column = None
    author_name: Column = None
    type: Column = None
    status: Column = None
    comment: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.title = Column(self.column_index, "title", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.created_date_time = Column(self.column_index, "created_date_time", "TEXT", Nullable.null)
        self.column_index += 1
        self.author_name = Column(self.column_index, "author_name", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.type = Column(self.column_index, "type", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.status = Column(self.column_index, "status", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.comment = Column(self.column_index, "comment", "TEXT", Nullable.NOT_NULL)


class TableAgreements(TableDocuments):
    pass


class TableLocations(TableIdentifiedObjects):

    def name(self) -> str:
        return "locations"


class TableTownDetails(SqliteTable, ABC):
    town_name: Column = None
    state_or_province: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.town_name = Column(self.column_index, "town_name", "TEXT", Nullable.NULL)
        self.column_index += 1
        self.state_or_province = Column(self.column_index, "state_or_province", "TEXT", Nullable.NULL)


class TableStreetAddresses(TableTownDetails, ABC):
    postal_code: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.postal_code = Column(self.column_index, "postal_code", "TEXT", Nullable.NOT_NULL)


class TableLocationStreetAddresses(TableStreetAddresses):
    location_mrid: Column = None
    address_field: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.location_mrid = Column(self.column_index, "location_mrid", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.address_field = Column(self.column_index, "address_field", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "location_street_addresses"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super().unique_index_columns()
        cols.append([self.location_mrid, self.address_field])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super().non_unique_index_columns()
        cols.append([self.location_mrid])
        return cols


class TableLocationStreetAddressField(Enum):
    mainAddress = 0
#     secondaryAddress = 1


class TableOrganisationRoles(TableIdentifiedObjects):
    organisation_mrid: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.organisation_mrid = Column(self.column_index, "organisation_mrid", "TEXT", Nullable.NULL)


class TablePositionPoints(SqliteTable):
    location_mrid: Column = None
    sequence_number: Column = None
    x_position: Column = None
    y_position: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.location_mrid = Column(self.column_index, "location_mrid", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.sequence_number = Column(self.column_index, "sequence_number", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.x_position = Column(self.column_index, "x_position", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.y_position = Column(self.column_index, "y_position", "NUMBER", Nullable.NOT_NULL)

    def name(self) -> str:
        return "position_points"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super().unique_index_columns()
        cols.append([self.location_mrid, self.sequence_number])
        return cols
