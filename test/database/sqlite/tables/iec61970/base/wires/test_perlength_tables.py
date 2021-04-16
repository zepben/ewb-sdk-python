#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from test.database.sqlite.tables.table_test_utils import verify_column
from zepben.evolve import Nullable, TablePerLengthSequenceImpedances


def test_table_per_length_sequence_impedances():
    t = TablePerLengthSequenceImpedances()
    verify_column(t.r, 5, "r", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.x, 6, "x", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.r0, 7, "r0", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.x0, 8, "x0", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.bch, 9, "bch", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.gch, 10, "gch", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.b0ch, 11, "b0ch", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.g0ch, 12, "g0ch", "NUMBER", Nullable.NOT_NULL)
    assert t.name() == "per_length_sequence_impedances"
