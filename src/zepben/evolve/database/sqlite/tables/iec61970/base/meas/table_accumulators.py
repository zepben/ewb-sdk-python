#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_measurements import TableMeasurements

__all__ = ["TableAccumulators"]


class TableAccumulators(TableMeasurements):

    @property
    def name(self) -> str:
        return "accumulators"
