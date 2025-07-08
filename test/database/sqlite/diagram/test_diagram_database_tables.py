#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.ewb import DiagramDatabaseTables
from zepben.ewb.database.sqlite.common.base_database_tables import BaseDatabaseTables


def test_contains_base_tables():
    tables = map(lambda it: it.__class__.__name__, DiagramDatabaseTables().tables)
    base_tables = map(lambda it: it.__class__.__name__, BaseDatabaseTables().tables)

    assert all([it in tables for it in base_tables]), "should contain all base tables"
