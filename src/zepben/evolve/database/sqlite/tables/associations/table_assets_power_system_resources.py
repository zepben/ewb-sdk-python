#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable

__all__ = ["TableAssetsPowerSystemResources"]


class TableAssetsPowerSystemResources(SqliteTable):
    """
    A class representing the association between AssetOrganisationRoles and Assets.
    """

    def __init__(self):
        super().__init__()

        self.asset_mrid: Column = self._create_column("asset_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of Assets."""

        self.power_system_resource_mrid: Column = self._create_column("power_system_resource_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of PowerSystemResources."""

    @property
    def name(self) -> str:
        return "assets_power_system_resources"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.asset_mrid, self.power_system_resource_mrid]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.asset_mrid]
        yield [self.power_system_resource_mrid]
