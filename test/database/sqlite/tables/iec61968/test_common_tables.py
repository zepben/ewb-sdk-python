#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from test.database.sqlite.tables.table_test_utils import verify_column
from zepben.evolve import Nullable, TableDocuments, TableLocations, TableTownDetails, TableStreetAddresses, TableLocationStreetAddresses, TableOrganisations, \
    TablePositionPoints


def test_table_documents():
    t = TableDocuments()
    verify_column(t.title, 5, "title", "TEXT", Nullable.NOT_NULL)
    verify_column(t.created_date_time, 6, "created_date_time", "TEXT", Nullable.NULL)
    verify_column(t.author_name, 7, "author_name", "TEXT", Nullable.NOT_NULL)
    verify_column(t.type, 8, "type", "TEXT", Nullable.NOT_NULL)
    verify_column(t.status, 9, "status", "TEXT", Nullable.NOT_NULL)
    verify_column(t.comment, 10, "comment", "TEXT", Nullable.NOT_NULL)


def test_table_locations():
    t = TableLocations()
    assert t.name() == "locations"


def test_table_town_details():
    t = TableTownDetails()
    verify_column(t.town_name, 1, "town_name", "TEXT", Nullable.NULL)
    verify_column(t.state_or_province, 2, "state_or_province", "TEXT", Nullable.NULL)


def test_table_street_addresses():
    t = TableStreetAddresses()
    verify_column(t.postal_code, 3, "postal_code", "TEXT", Nullable.NOT_NULL)


def test_table_location_street_addresses():
    t = TableLocationStreetAddresses()
    verify_column(t.location_mrid, 4, "location_mrid", "TEXT", Nullable.NOT_NULL)
    verify_column(t.address_field, 5, "address_field", "TEXT", Nullable.NOT_NULL)
    assert t.unique_index_columns() == [*super(TableLocationStreetAddresses, t).unique_index_columns(), [t.location_mrid, t.address_field]]
    assert t.non_unique_index_columns() == [*super(TableLocationStreetAddresses, t).non_unique_index_columns(), [t.location_mrid]]
    assert t.name() == "location_street_addresses"


def test_table_organisations():
    t = TableOrganisations()
    assert t.name() == "organisations"


def test_table_position_points():
    t = TablePositionPoints()
    verify_column(t.location_mrid, 1, "location_mrid", "TEXT", Nullable.NOT_NULL)
    verify_column(t.sequence_number, 2, "sequence_number", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.x_position, 3, "x_position", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.y_position, 4, "y_position", "NUMBER", Nullable.NOT_NULL)
    assert t.unique_index_columns() == [*super(TablePositionPoints, t).unique_index_columns(), [t.location_mrid, t.sequence_number]]
    assert t.name() == "position_points"
