#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


__all__ = ["TableProtectionRelayFunctionsProtectedSwitches"]


class TableProtectionRelayFunctionsProtectedSwitches(SqliteTable):
    """
    A class representing the association between ProtectionRelayFunctions and ProtectedSwitches.
    """

    def __init__(self):
        super().__init__()
        self.protection_relay_function_mrid: Column = self._create_column("protection_relay_function_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of ProtectionRelayFunctions."""

        self.protected_switch_mrid: Column = self._create_column("protected_switch_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of ProtectedSwitches."""

    @property
    def name(self) -> str:
        return "protection_relay_functions_protected_switches"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.protection_relay_function_mrid, self.protected_switch_mrid]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.protection_relay_function_mrid]
        yield [self.protected_switch_mrid]
