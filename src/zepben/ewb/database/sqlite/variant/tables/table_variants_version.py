#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableVariantsVersion"]

from zepben.ewb.database.sqlite.tables.table_version import TableVersion


class TableVariantsVersion(TableVersion):
    """
    The `version` table in the variant database.

    This is the Python equivalent of the JVM `tableVariantsVersion: TableVersion = TableVersion(1)`. The Python
    `TableVersion` uses a class-level `SUPPORTED_VERSION` attribute rather than a per-instance constructor value,
    so the variant database's own (separate, v1) schema version is expressed here as a subclass overriding
    `SUPPORTED_VERSION`.
    """

    SUPPORTED_VERSION = 1
