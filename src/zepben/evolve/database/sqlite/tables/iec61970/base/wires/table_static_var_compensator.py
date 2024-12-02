#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import TableRegulatingCondEq
from zepben.evolve.database.sqlite.tables.column import Column, Nullable

__all__ = ["TableStaticVarCompensators"]


class TableStaticVarCompensators(TableRegulatingCondEq):

    def __init__(self):
        super().__init__()
        self.capacitive_rating: Column = self._create_column("capacitive_rating", "NUMBER", Nullable.NULL)
        self.inductive_rating: Column = self._create_column("inductive_rating", "NUMBER", Nullable.NULL)
        self.q: Column = self._create_column("q", "NUMBER", Nullable.NULL)
        self.svc_control_mode: Column = self._create_column("svc_control_mode", "TEXT", Nullable.NOT_NULL)
        self.voltage_set_point: Column = self._create_column("voltage_set_point", "INTEGER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "static_var_compensators"
