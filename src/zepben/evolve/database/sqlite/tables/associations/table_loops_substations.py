#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


__all__ = ["TableLoopsSubstations"]


class TableLoopsSubstations(SqliteTable):
    """
    A class representing the association between Loops and Substations.
    """

    def __init__(self):
        super().__init__()
        self.loop_mrid: Column = self._create_column("loop_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of Loops."""

        self.substation_mrid: Column = self._create_column("substation_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of Substations."""

        self.relationship: Column = self._create_column("relationship", "TEXT", Nullable.NOT_NULL)
        """A column storing the type of relationships between the Loop and the Substation."""

    @property
    def name(self) -> str:
        return "loops_substations"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.loop_mrid, self.substation_mrid]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.loop_mrid]
        yield [self.substation_mrid]
