#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Type, TYPE_CHECKING


if TYPE_CHECKING:
    from zepben.ewb import Identifiable
    from zepben.ewb.database.sqlite.network.network_cim_writer import TSqlTable


# TODO: after 3.10 support is dropped, the quoted typevars below can be unquoted.
def using_table(table: "Type[TSqlTable]"):
    def wrapper(func):
        def _inner(self, io: "Identifiable", *args, **kwargs):
            _table: TSqlTable = self._database_tables.get_table(table)
            _insert = self._database_tables.get_insert(table)
            return func(self, io, *args, table=_table, insert=_insert, **kwargs)

        return _inner

    return wrapper


