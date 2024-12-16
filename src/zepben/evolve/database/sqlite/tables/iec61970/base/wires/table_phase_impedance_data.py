#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["TablePhaseImpedanceData"]

from typing import List, Generator

from zepben.evolve import SqliteTable
from zepben.evolve.database.sqlite.tables.column import Column, Nullable


class TablePhaseImpedanceData(SqliteTable):
    """A class representing the PhaseImpedanceData columns required for the database table."""

    def __init__(self):
        super().__init__()
        self.per_length_phase_impedance_mrid: Column = self._create_column("per_length_phase_impedance_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the per_length_phase_impedance mRID."""

        self.from_phase: Column = self._create_column("from_phase", "TEXT", Nullable.NOT_NULL)
        """A column storing the from_phase of this per_length_phase_impedance data point."""

        self.to_phase: Column = self._create_column("to_phase", "TEXT", Nullable.NOT_NULL)
        """A column storing the to_phase of this per_length_phase_impedance data point."""

        self.b: Column = self._create_column("b", "NUMBER", Nullable.NULL)
        """A column storing the b of this per_length_phase_impedance data point."""

        self.g: Column = self._create_column("g", "NUMBER", Nullable.NULL)
        """A column storing the g of this per_length_phase_impedance data point."""

        self.r: Column = self._create_column("r", "NUMBER", Nullable.NULL)
        """A column storing the r of this per_length_phase_impedance data point."""

        self.x: Column = self._create_column("x", "NUMBER", Nullable.NULL)
        """A column storing the x of this per_length_phase_impedance data point."""

    @property
    def name(self) -> str:
        return "phase_impedance_data"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.per_length_phase_impedance_mrid, self.from_phase, self.to_phase]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.per_length_phase_impedance_mrid]
