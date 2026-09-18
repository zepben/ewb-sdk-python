#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableNetworkModelProjects"]

from zepben.ewb.database.sql.column import Column, Nullable, Type
from zepben.ewb.database.sqlite.tables.extensions.iec61970.infpart303.networkmodelprojects.table_network_model_project_components import \
    TableNetworkModelProjectComponents


class TableNetworkModelProjects(TableNetworkModelProjectComponents):
    """
    A class representing the NetworkModelProject columns required for the database table.
    """

    def __init__(self):
        super().__init__()
        self.external_status: Column = self._create_column("external_status", Type.STRING, Nullable.NULL)
        self.forecast_commission_date: Column = self._create_column("forecast_commission_date", Type.TIMESTAMP, Nullable.NULL)
        self.external_driver: Column = self._create_column("external_driver", Type.STRING, Nullable.NULL)

    @property
    def name(self) -> str:
        return "network_model_projects"
