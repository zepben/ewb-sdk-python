#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["TableSynchronousMachinesReactiveCapabilityCurves"]

from typing import Generator, List

from zepben.evolve import SqliteTable, Column, Nullable


class TableSynchronousMachinesReactiveCapabilityCurves(SqliteTable):
    """
    A class representing the association between SynchronousMachines and ReactiveCapabilityCurves.
    """

    def __init__(self):
        super().__init__()
        self.synchronous_machine_mrid: Column = self._create_column("synchronous_machine_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of SynchronousMachines."""

        self.reactive_capability_curve_mrid: Column = self._create_column("reactive_capability_curve_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of ReactiveCapabilityCurves."""

    @property
    def name(self) -> str:
        return "synchronous_machines_reactive_capability_curves"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.synchronous_machine_mrid, self.reactive_capability_curve_mrid]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.synchronous_machine_mrid]
        yield [self.reactive_capability_curve_mrid]
