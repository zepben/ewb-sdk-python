#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


__all__ = ["TableProtectionRelaySchemesProtectionRelayFunctions"]


class TableProtectionRelaySchemesProtectionRelayFunctions(SqliteTable):
    """
    A class representing the association between ProtectionRelaySchemes and ProtectionRelayFunctions.
    """

    def __init__(self):
        super().__init__()
        self.protection_relay_scheme_mrid: Column = self._create_column("protection_relay_scheme_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of ProtectionRelaySchemes."""

        self.protection_relay_function_mrid: Column = self._create_column("protection_relay_function_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of ProtectionRelayFunctions."""

    @property
    def name(self) -> str:
        return "protection_relay_schemes_protection_relay_functions"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.protection_relay_scheme_mrid, self.protection_relay_function_mrid]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.protection_relay_scheme_mrid]
        yield [self.protection_relay_function_mrid]
