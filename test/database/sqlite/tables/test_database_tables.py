#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pytest import raises

from zepben.evolve import SqliteTable, DatabaseTables, MissingTableConfigException


def test_database_tables():
    class NotATable(SqliteTable):
        pass

    d = DatabaseTables()
    assert len(list(d.tables)) > 0
    for t in d.tables:
        assert t == d.get_table(type(t))
        assert d.get_insert(type(t)) == t.prepared_insert_sql()

    with raises(MissingTableConfigException):
        d.get_table(NotATable)

    with raises(MissingTableConfigException):
        d.get_insert(NotATable)
