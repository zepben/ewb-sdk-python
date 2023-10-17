#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableConductingEquipment

__all__ = ["TableSwitches", "TableProtectedSwitches", "TableFuses", "TableLoadBreakSwitches", "TableBreakers", "TableReclosers", "TableJumpers",
           "TableDisconnectors"]


# noinspection PyAbstractClass
class TableSwitches(TableConductingEquipment):
    normal_open: Column = None
    open: Column = None
    rated_current: Column = None
    switch_info_mrid: Column = None

    def __init__(self):
        super(TableSwitches, self).__init__()
        self.normal_open = self._create_column("normal_open", "INTEGER", Nullable.NOT_NULL)
        self.open = self._create_column("open", "INTEGER", Nullable.NOT_NULL)
        self.rated_current = self._create_column("rated_current", "INTEGER", Nullable.NULL)
        self.switch_info_mrid = self._create_column("switch_info_mrid", "TEXT", Nullable.NULL)


# noinspection PyAbstractClass
class TableProtectedSwitches(TableSwitches):
    breaking_capacity: Column = None

    def __init__(self):
        super(TableProtectedSwitches, self).__init__()
        self.breaking_capacity = self._create_column("breaking_capacity", "INTEGER", Nullable.NULL)


class TableBreakers(TableProtectedSwitches):
    in_transit_time: Column = None

    def name(self) -> str:
        return "breakers"

    def __init__(self):
        super(TableBreakers, self).__init__()
        self.in_transit_time = self._create_column("in_transit_time", "NUMBER", Nullable.NULL)


class TableDisconnectors(TableSwitches):
    def name(self) -> str:
        return "disconnectors"


class TableFuses(TableSwitches):
    def name(self) -> str:
        return "fuses"


class TableJumpers(TableSwitches):
    def name(self) -> str:
        return "jumpers"


class TableLoadBreakSwitches(TableProtectedSwitches):
    def name(self) -> str:
        return "load_break_switches"


class TableReclosers(TableProtectedSwitches):
    def name(self) -> str:
        return "reclosers"

