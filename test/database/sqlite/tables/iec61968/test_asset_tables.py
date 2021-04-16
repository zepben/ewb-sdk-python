#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from test.database.sqlite.tables.table_test_utils import verify_column
from zepben.evolve import Nullable, TableAssets, TableAssetOwners, TablePoles, TableStreetlights


def test_table_assets():
    t = TableAssets()
    verify_column(t.location_mrid, 5, "location_mrid", "TEXT", Nullable.NULL)


def test_table_asset_owners():
    t = TableAssetOwners()
    assert t.name() == "asset_owners"


def test_table_poles():
    t = TablePoles()
    verify_column(t.classification, 6, "classification", "TEXT", Nullable.NOT_NULL)
    assert t.name() == "poles"


def test_table_streetlights():
    t = TableStreetlights()
    verify_column(t.pole_mrid, 6, "pole_mrid", "TEXT", Nullable.NULL)
    verify_column(t.lamp_kind, 7, "lamp_kind", "TEXT", Nullable.NOT_NULL)
    verify_column(t.light_rating, 8, "light_rating", "INTEGER", Nullable.NOT_NULL)
    assert t.name() == "streetlights"
