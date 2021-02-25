#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import Column, TableConductingEquipment, Nullable

__all__ = ["TableEquivalentBranches", "TableEquivalentEquipment"]


# noinspection PyAbstractClass
class TableEquivalentEquipment(TableConductingEquipment):
    pass


class TableEquivalentBranches(TableEquivalentEquipment):
    negative_r12: Column = None
    negative_r21: Column = None
    negative_x12: Column = None
    negative_x21: Column = None
    positive_r12: Column = None
    positive_r21: Column = None
    positive_x12: Column = None
    positive_x21: Column = None
    r: Column = None
    r21: Column = None
    x: Column = None
    x21: Column = None
    zero_r12: Column = None
    zero_r21: Column = None
    zero_x12: Column = None
    zero_x21: Column = None

    def __init__(self):
        super(TableEquivalentBranches, self).__init__()
        self.negative_r12 = self._create_column("negative_r12", "NUMBER", Nullable.NULL)
        self.negative_r21 = self._create_column("negative_r21", "NUMBER", Nullable.NULL)
        self.negative_x12 = self._create_column("negative_x12", "NUMBER", Nullable.NULL)
        self.negative_x21 = self._create_column("negative_x21", "NUMBER", Nullable.NULL)
        self.positive_r12 = self._create_column("positive_r12", "NUMBER", Nullable.NULL)
        self.positive_r21 = self._create_column("positive_r21", "NUMBER", Nullable.NULL)
        self.positive_x12 = self._create_column("positive_x12", "NUMBER", Nullable.NULL)
        self.positive_x21 = self._create_column("positive_x21", "NUMBER", Nullable.NULL)
        self.r = self._create_column("r", "NUMBER", Nullable.NULL)
        self.r21 = self._create_column("r21", "NUMBER", Nullable.NULL)
        self.x = self._create_column("x", "NUMBER", Nullable.NULL)
        self.x21 = self._create_column("x21", "NUMBER", Nullable.NULL)
        self.zero_r12 = self._create_column("zero_r12", "NUMBER", Nullable.NULL)
        self.zero_r21 = self._create_column("zero_r21", "NUMBER", Nullable.NULL)
        self.zero_x12 = self._create_column("zero_x12", "NUMBER", Nullable.NULL)
        self.zero_x21 = self._create_column("zero_x21", "NUMBER", Nullable.NULL)

    def name(self) -> str:
        return "equivalent_branches"
