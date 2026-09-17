#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["EWBDatabaseTables"]

from typing import Generator

from zepben.ewb.database.sqlite.common.base_database_tables import BaseDatabaseTables
from zepben.ewb.database.sqlite.tables.extensions.iec61970.infpart303.networkmodelprojects.table_network_model_projects import \
    TableNetworkModelProjects
from zepben.ewb.database.sqlite.tables.iec61970.infiec61970.infpart303.networkmodelprojects.table_annotated_project_dependencies import \
    TableAnnotatedProjectDependencies
from zepben.ewb.database.sqlite.tables.iec61970.infiec61970.infpart303.networkmodelprojects.table_network_model_project_stage_equipment_containers import \
    TableNetworkModelProjectStageEquipmentContainers
from zepben.ewb.database.sqlite.tables.iec61970.infiec61970.infpart303.networkmodelprojects.table_network_model_project_stages import \
    TableNetworkModelProjectStages
from zepben.ewb.database.sqlite.tables.sqlite_table import SqliteTable


class EWBDatabaseTables(BaseDatabaseTables):
    """
    The collection of tables for our EWB databases.
    """

    @property
    def _included_tables(self) -> Generator[SqliteTable, None, None]:
        yield from super()._included_tables

        yield TableNetworkModelProjectStages()
        yield TableNetworkModelProjects()
        yield TableAnnotatedProjectDependencies()
        yield TableNetworkModelProjectStageEquipmentContainers()
