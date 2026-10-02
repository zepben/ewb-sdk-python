#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableAnnotatedProjectDependencies"]

from zepben.ewb.database.sql.column import Column, Nullable, Type
from zepben.ewb.database.sqlite.tables.sqlite_table import SqliteTable


class TableAnnotatedProjectDependencies(SqliteTable):
    """
    A class representing the AnnotatedProjectDependency columns required for the database table.
    """

    def __init__(self):
        super().__init__()
        self.mrid_: Column = self._create_column("mrid", Type.STRING, Nullable.NOT_NULL)
        self.dependency_type: Column = self._create_column("dependency_type", Type.STRING, Nullable.NOT_NULL)
        self.dependency_dependent_on_stage_mrid: Column = self._create_column(
            "dependency_dependent_on_stage_mrid", Type.STRING, Nullable.NOT_NULL)
        self.dependency_depending_stage_mrid: Column = self._create_column(
            "dependency_depending_stage_mrid", Type.STRING, Nullable.NOT_NULL)
        self.base_model_version: Column = self._create_column("base_model_version", Type.STRING, Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "annotated_project_dependencies"

    @property
    def unique_index_columns(self):
        yield [self.mrid_]
        yield [
            self.dependency_dependent_on_stage_mrid,
            self.dependency_depending_stage_mrid,
            self.dependency_type,
            self.base_model_version,
        ]

    @property
    def non_unique_index_columns(self):
        yield [self.dependency_depending_stage_mrid]
        yield [self.dependency_dependent_on_stage_mrid]
