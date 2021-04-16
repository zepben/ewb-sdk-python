#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from test.database.sqlite.tables.table_test_utils import verify_column
from zepben.evolve import Nullable, TableEndDevices, TableMeters, TableUsagePoints


def test_table_end_devices():
    t = TableEndDevices()
    verify_column(t.customer_mrid, 6, "customer_mrid", "TEXT", Nullable.NULL)
    verify_column(t.service_location_mrid, 7, "service_location_mrid", "TEXT", Nullable.NULL)


def test_table_meters():
    t = TableMeters()
    assert t.name() == "meters"


def test_table_usage_points():
    t = TableUsagePoints()
    verify_column(t.location_mrid, 5, "location_mrid", "TEXT", Nullable.NULL)
    assert t.name() == "usage_points"
