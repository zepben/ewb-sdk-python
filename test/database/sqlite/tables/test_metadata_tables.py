#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from test.database.sqlite.tables.table_test_utils import verify_column
from zepben.evolve import Nullable
from zepben.evolve.database.sqlite.tables.metadata_tables import TableVersion, TableMetadataDataSources


def test_table_version():
    t = TableVersion()
    verify_column(t.version, 1, "version", "TEXT", Nullable.NOT_NULL)
    assert t.name() == "version"


def test_table_metadata_sources():
    t = TableMetadataDataSources()
    verify_column(t.source, 1, "source", "TEXT", Nullable.NOT_NULL)
    verify_column(t.version, 2, "version", "TEXT", Nullable.NOT_NULL)
    verify_column(t.timestamp, 3, "timestamp", "TEXT", Nullable.NOT_NULL)
