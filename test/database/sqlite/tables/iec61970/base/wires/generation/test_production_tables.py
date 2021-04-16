#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from test.database.sqlite.tables.table_test_utils import verify_column
from zepben.evolve import Nullable, TablePowerElectronicsUnit, TableBatteryUnit, TablePhotoVoltaicUnit, TablePowerElectronicsWindUnit


def test_table_power_electronics_unit():
    t = TablePowerElectronicsUnit()
    verify_column(t.power_electronics_connection_mrid, 9, "power_electronics_connection_mrid", "TEXT", Nullable.NULL)
    verify_column(t.max_p, 10, "max_p", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.min_p, 11, "min_p", "INTEGER", Nullable.NOT_NULL)
    assert t.unique_index_columns() == [*super(TablePowerElectronicsUnit, t).unique_index_columns(), [t.power_electronics_connection_mrid]]


def test_table_battery_unit():
    t = TableBatteryUnit()
    verify_column(t.battery_state, 12, "battery_state", "TEXT", Nullable.NOT_NULL)
    verify_column(t.rated_e, 13, "rated_e", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.stored_e, 14, "stored_e", "INTEGER", Nullable.NOT_NULL)
    assert t.name() == "battery_unit"


def test_table_photo_voltaic_unit():
    t = TablePhotoVoltaicUnit()
    assert t.name() == "photo_voltaic_unit"


def test_table_power_electronics_wind_unit():
    t = TablePowerElectronicsWindUnit()
    assert t.name() == "power_electronics_wind_unit"
