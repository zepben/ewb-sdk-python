#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from abc import ABC
from sqlite3 import Connection
from unittest.mock import create_autospec

from pytest import raises

from util import import_submodules, all_subclasses
from zepben.ewb import CustomerDatabaseTables, DiagramDatabaseTables, NetworkDatabaseTables
from zepben.ewb.database.sqlite.common.base_database_tables import BaseDatabaseTables
from zepben.ewb.database.sqlite.tables.exceptions import MissingTableConfigException
from zepben.ewb.database.sqlite.tables.sqlite_table import SqliteTable


def test_has_all_tables():
    """
    This test detects if a Table class has been added under zepben.ewb.database.sqlite.tables however hasn't been added to
    DatabaseTables
    """
    _ = import_submodules('zepben.ewb.database.sqlite.tables')
    all_final_tables = all_subclasses(SqliteTable, 'zepben.ewb.database.sqlite.tables')

    table_collections = [CustomerDatabaseTables(), DiagramDatabaseTables(), NetworkDatabaseTables()]
    used_tables = {type(it) for collection in table_collections for it in collection.tables}

    misplaced = used_tables.difference(all_final_tables)
    assert not misplaced, (
        "Using tables that aren't defined under `zepben.ewb.database.sqlite.tables`: "
        f"{', '.join([it.__name__ for it in misplaced])}"
    )

    unused = all_final_tables.difference(used_tables)
    assert not unused, (
        "Not using tables defined under `zepben.ewb.database.sqlite.tables`: "
        f"{', '.join([it.__name__ for it in unused])}"
    )


def test_database_tables():
    class MissingTable(SqliteTable, ABC):
        pass

    d = BaseDatabaseTables()

    with raises(MissingTableConfigException):
        d.get_table(MissingTable)

    expected_error = "INTERNAL ERROR: Statements have not been prepared. You must call `prepare_insert_statements` first."
    with raises(MissingTableConfigException, match=expected_error):
        d.get_insert(MissingTable)

    d.prepare_insert_statements(create_autospec(Connection))

    expected_error = f"INTERNAL ERROR: No prepared statement has been registered for {MissingTable}. You might want to consider fixing that."
    with raises(MissingTableConfigException, match=expected_error):
        d.get_insert(MissingTable)
