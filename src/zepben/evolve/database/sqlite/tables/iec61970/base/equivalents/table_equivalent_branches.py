#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.equivalents.table_equivalent_equipment import TableEquivalentEquipment

__all__ = ["TableEquivalentBranches"]


class TableEquivalentBranches(TableEquivalentEquipment):

    def __init__(self):
        super().__init__()
        self.negative_r12: Column = self._create_column("negative_r12", "NUMBER", Nullable.NULL)
        self.negative_r21: Column = self._create_column("negative_r21", "NUMBER", Nullable.NULL)
        self.negative_x12: Column = self._create_column("negative_x12", "NUMBER", Nullable.NULL)
        self.negative_x21: Column = self._create_column("negative_x21", "NUMBER", Nullable.NULL)
        self.positive_r12: Column = self._create_column("positive_r12", "NUMBER", Nullable.NULL)
        self.positive_r21: Column = self._create_column("positive_r21", "NUMBER", Nullable.NULL)
        self.positive_x12: Column = self._create_column("positive_x12", "NUMBER", Nullable.NULL)
        self.positive_x21: Column = self._create_column("positive_x21", "NUMBER", Nullable.NULL)
        self.r: Column = self._create_column("r", "NUMBER", Nullable.NULL)
        self.r21: Column = self._create_column("r21", "NUMBER", Nullable.NULL)
        self.x: Column = self._create_column("x", "NUMBER", Nullable.NULL)
        self.x21: Column = self._create_column("x21", "NUMBER", Nullable.NULL)
        self.zero_r12: Column = self._create_column("zero_r12", "NUMBER", Nullable.NULL)
        self.zero_r21: Column = self._create_column("zero_r21", "NUMBER", Nullable.NULL)
        self.zero_x12: Column = self._create_column("zero_x12", "NUMBER", Nullable.NULL)
        self.zero_x21: Column = self._create_column("zero_x21", "NUMBER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "equivalent_branches"
