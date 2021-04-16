#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from test.database.sqlite.tables.table_test_utils import verify_column
from zepben.evolve import TableAuxiliaryEquipment, Nullable, TableFaultIndicators


def test_table_auxiliary_equipment():
    t = TableAuxiliaryEquipment()
    verify_column(t.terminal_mrid, 9, "terminal_mrid", "TEXT", Nullable.NULL)


def test_table_fault_indicators():
    t = TableFaultIndicators()
    assert t.name() == "fault_indicators"
