#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from test.database.sqlite.tables.table_test_utils import verify_column
from zepben.evolve import Nullable, TableSwitches, TableBreakers, TableDisconnectors, TableFuses, TableJumpers, TableLoadBreakSwitches, TableReclosers


def test_table_switches():
    t = TableSwitches()
    verify_column(t.normal_open, 10, "normal_open", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.open, 11, "open", "INTEGER", Nullable.NOT_NULL)


def test_table_breakers():
    t = TableBreakers()
    assert t.name() == "breakers"


def test_table_disconnectors():
    t = TableDisconnectors()
    assert t.name() == "disconnectors"


def test_table_fuses():
    t = TableFuses()
    assert t.name() == "fuses"


def test_table_jumpers():
    t = TableJumpers()
    assert t.name() == "jumpers"


def test_table_load_break_switches():
    t = TableLoadBreakSwitches()
    assert t.name() == "load_break_switches"


def test_table_reclosers():
    t = TableReclosers()
    assert t.name() == "reclosers"
