#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableEquipment

__all__ = ["TablePowerElectronicsUnit", "TablePowerElectronicsWindUnit", "TablePhotoVoltaicUnit", "TablePowerElectronicsWindUnit"]


class TablePowerElectronicsUnit(TableEquipment):
    power_electronics_connection_mrid: Column = None
    max_p: Column = None
    min_p: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.power_electronics_connection_mrid = Column(self.column_index, "power_electronics_connection_mrid", "TEXT", Nullable.NULL)
        self.column_index += 1
        self.max_p = Column(self.column_index, "max_p", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.min_p = Column(self.column_index, "min_p", "INTEGER", Nullable.NOT_NULL)

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super().unique_index_columns()
        cols.append([self.power_electronics_connection_mrid])
        return cols


class TableBatteryUnit(TablePowerElectronicsUnit):
    battery_state: Column = None
    rated_e: Column = None
    stored_e: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.battery_state = Column(self.column_index, "battery_state", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.rated_e = Column(self.column_index, "rated_e", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.stored_e = Column(self.column_index, "stored_e", "INTEGER", Nullable.NOT_NULL)

    def name(self) -> str:
        return "battery_unit"


class TablePhotoVoltaicUnit(TablePowerElectronicsUnit):
    def name(self) -> str:
        return "photo_voltaic_unit"


class TablePowerElectronicsWindUnit(TablePowerElectronicsUnit):
    def name(self) -> str:
        return "power_electronics_wind_unit"
