#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from test.database.sqlite.tables.table_test_utils import verify_column
from zepben.evolve import Nullable, TableCircuits, TableLoops


def test_table_circuits():
    t = TableCircuits()
    verify_column(t.loop_mrid, 7, "loop_mrid", "TEXT", Nullable.NULL)
    assert t.non_unique_index_columns() == [*super(TableCircuits, t).non_unique_index_columns(), [t.loop_mrid]]
    assert t.name() == "circuits"


def test_table_loops():
    t = TableLoops()
    assert t.name() == "loops"
