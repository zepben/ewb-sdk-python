#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableNetworkModelProjectStageEquipmentContainers"]

from zepben.ewb.database.sql.column import Column, Nullable, Type
from zepben.ewb.database.sqlite.tables.sqlite_table import SqliteTable


class TableNetworkModelProjectStageEquipmentContainers(SqliteTable):
    """
    A class representing the association between NetworkModelProjectStage and EquipmentContainers.
    """

    def __init__(self):
        super().__init__()
        self.network_model_project_stage_mrid: Column = self._create_column(
            "network_model_project_stage_mrid", Type.STRING, Nullable.NOT_NULL)
        self.equipment_container_mrid: Column = self._create_column("equipment_container_mrid", Type.STRING, Nullable.NOT_NULL)
        self.base_model_version: Column = self._create_column("base_model_version", Type.STRING, Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "network_model_project_stage_equipment_containers"

    @property
    def unique_index_columns(self):
        yield [self.network_model_project_stage_mrid, self.equipment_container_mrid]

    @property
    def non_unique_index_columns(self):
        yield [self.network_model_project_stage_mrid]
        yield [self.equipment_container_mrid]
