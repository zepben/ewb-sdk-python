#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableObjectCreations"]

from zepben.ewb.database.sqlite.tables.iec61970.infiec61970.part303.genericdataset.table_change_set_members import \
    TableChangeSetMembers


class TableObjectCreations(TableChangeSetMembers):
    """
    A class representing the ObjectCreation columns required for the database table.
    """

    @property
    def name(self) -> str:
        return "object_creations"
