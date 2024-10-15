#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_conducting_equipment import TableConductingEquipment

__all__ = ["TableConductors"]


class TableConductors(TableConductingEquipment, ABC):

    def __init__(self):
        super().__init__()
        self.length: Column = self._create_column("length", "NUMBER", Nullable.NULL)
        self.design_temperature: Column = self._create_column("design_temperature", "INTEGER", Nullable.NULL)
        self.design_rating: Column = self._create_column("design_rating", "NUMBER", Nullable.NULL)
        self.wire_info_mrid: Column = self._create_column("wire_info_mrid", "TEXT", Nullable.NULL)
