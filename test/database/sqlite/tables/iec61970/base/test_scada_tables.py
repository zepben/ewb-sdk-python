#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from test.database.sqlite.tables.table_test_utils import verify_column
from zepben.evolve import Nullable, TableRemoteControls, TableRemoteSources


def test_table_remote_controls():
    t = TableRemoteControls()
    verify_column(t.control_mrid, 5, "control_mrid", "TEXT", Nullable.NULL)
    assert t.name() == "remote_controls"


def test_table_remote_sources():
    t = TableRemoteSources()
    verify_column(t.measurement_mrid, 5, "measurement_mrid", "TEXT", Nullable.NULL)
    assert t.name() == "remote_sources"
