#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["TableReactiveCapabilityCurves"]

from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_curves import TableCurves


class TableReactiveCapabilityCurves(TableCurves):
    """
    A class representing the ReactiveCapabilityCurve columns required for the database table.
    """

    @property
    def name(self) -> str:
        return "reactive_capability_curves"
