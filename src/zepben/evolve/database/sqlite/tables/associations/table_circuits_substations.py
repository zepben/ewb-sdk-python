#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


__all__ = ["TableCircuitsSubstations"]


class TableCircuitsSubstations(SqliteTable):
    """
    A class representing the association between Circuits and Substations.
    """

    def __init__(self):
        super().__init__()
        self.circuit_mrid: Column = self._create_column("circuit_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of Circuits."""

        self.substation_mrid: Column = self._create_column("substation_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of Substations."""

    @property
    def name(self) -> str:
        return "circuits_substations"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.circuit_mrid, self.substation_mrid]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.circuit_mrid]
        yield [self.substation_mrid]
