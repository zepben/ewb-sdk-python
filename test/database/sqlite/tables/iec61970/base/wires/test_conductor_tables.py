#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from test.database.sqlite.tables.table_test_utils import verify_column
from zepben.evolve import Nullable, TableConductors, TableAcLineSegments


def test_table_conductors():
    t = TableConductors()
    verify_column(t.length, 10, "length", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.wire_info_mrid, 11, "wire_info_mrid", "TEXT", Nullable.NULL)


def test_table_aclinesegments():
    t = TableAcLineSegments()
    verify_column(t.per_length_sequence_impedance_mrid, 12, "per_length_sequence_impedance_mrid", "TEXT", Nullable.NULL)
    assert t.name() == "ac_line_segments"
