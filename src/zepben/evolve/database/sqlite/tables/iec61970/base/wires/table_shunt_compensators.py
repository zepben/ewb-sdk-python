#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_regulating_cond_eq import TableRegulatingCondEq

__all__ = ["TableShuntCompensators"]


class TableShuntCompensators(TableRegulatingCondEq, ABC):

    def __init__(self):
        super().__init__()
        self.shunt_compensator_info_mrid: Column = self._create_column("shunt_compensator_info_mrid", "TEXT", Nullable.NULL)
        self.grounded: Column = self._create_column("grounded", "BOOLEAN", Nullable.NOT_NULL)
        self.nom_u: Column = self._create_column("nom_u", "INTEGER", Nullable.NULL)
        self.phase_connection: Column = self._create_column("phase_connection", "TEXT", Nullable.NOT_NULL)
        self.sections: Column = self._create_column("sections", "NUMBER", Nullable.NULL)
