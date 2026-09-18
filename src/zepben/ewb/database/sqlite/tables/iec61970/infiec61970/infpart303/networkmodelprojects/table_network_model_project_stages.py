#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableNetworkModelProjectStages"]

from zepben.ewb.database.sql.column import Column, Nullable, Type
from zepben.ewb.database.sqlite.tables.extensions.iec61970.infpart303.networkmodelprojects.table_network_model_project_components import \
    TableNetworkModelProjectComponents


class TableNetworkModelProjectStages(TableNetworkModelProjectComponents):
    """
    A class representing the NetworkModelProjectStage columns required for the database table.
    """

    def __init__(self):
        super().__init__()
        self.planned_commission_date: Column = self._create_column("planned_commission_date", Type.TIMESTAMP, Nullable.NULL)
        self.commissioned_date: Column = self._create_column("commissioned_date", Type.TIMESTAMP, Nullable.NULL)
        self.confidence_level: Column = self._create_column("confidence_level", Type.INTEGER, Nullable.NULL)
        self.base_model_version: Column = self._create_column("base_model_version", Type.STRING, Nullable.NULL)
        self.last_conflict_checked_at: Column = self._create_column("last_conflict_checked_at", Type.TIMESTAMP, Nullable.NULL)
        self.user_comments: Column = self._create_column("user_comments", Type.STRING, Nullable.NULL)
        self.change_set_mrid: Column = self._create_column("change_set_mrid", Type.STRING, Nullable.NULL)

    @property
    def name(self) -> str:
        return "network_model_project_stages"

    @property
    def unique_index_columns(self):
        yield from super().unique_index_columns
        yield [self.base_model_version, self.change_set_mrid]

    @property
    def non_unique_index_columns(self):
        yield from super().non_unique_index_columns
        yield [self.base_model_version, self.mrid]
        yield [self.change_set_mrid, self.mrid]
