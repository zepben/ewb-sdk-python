#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableEquipment

__all__ = ["TablePowerElectronicsUnit", "TablePowerElectronicsWindUnit", "TablePhotoVoltaicUnit", "TableBatteryUnit"]


# noinspection PyAbstractClass
class TablePowerElectronicsUnit(TableEquipment):
    power_electronics_connection_mrid: Column = None
    max_p: Column = None
    min_p: Column = None

    def __init__(self):
        super(TablePowerElectronicsUnit, self).__init__()
        self.power_electronics_connection_mrid = self._create_column("power_electronics_connection_mrid", "TEXT", Nullable.NULL)
        self.max_p = self._create_column("max_p", "INTEGER", Nullable.NULL)
        self.min_p = self._create_column("min_p", "INTEGER", Nullable.NULL)

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TablePowerElectronicsUnit, self).non_unique_index_columns()
        cols.append([self.power_electronics_connection_mrid])
        return cols


class TableBatteryUnit(TablePowerElectronicsUnit):
    battery_state: Column = None
    rated_e: Column = None
    stored_e: Column = None

    def __init__(self):
        super(TableBatteryUnit, self).__init__()
        self.battery_state = self._create_column("battery_state", "TEXT", Nullable.NOT_NULL)
        self.rated_e = self._create_column("rated_e", "INTEGER", Nullable.NULL)
        self.stored_e = self._create_column("stored_e", "INTEGER", Nullable.NULL)

    def name(self) -> str:
        return "battery_unit"


class TablePhotoVoltaicUnit(TablePowerElectronicsUnit):
    def name(self) -> str:
        return "photo_voltaic_unit"


class TablePowerElectronicsWindUnit(TablePowerElectronicsUnit):
    def name(self) -> str:
        return "power_electronics_wind_unit"
