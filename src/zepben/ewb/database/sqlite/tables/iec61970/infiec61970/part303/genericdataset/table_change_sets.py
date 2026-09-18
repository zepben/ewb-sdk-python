#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableChangeSets"]

from zepben.ewb.database.sql.column import Column, Nullable, Type
from zepben.ewb.database.sqlite.tables.iec61970.infiec61970.part303.genericdataset.table_data_sets import TableDataSets


class TableChangeSets(TableDataSets):

    def __init__(self):
        super().__init__()
        self.network_model_project_stage_mrid: Column = self._create_column(
            "network_model_project_stage_mrid", Type.STRING, Nullable.NULL)

    @property
    def name(self) -> str:
        return "change_sets"
