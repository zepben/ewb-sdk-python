#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["TablePetersenCoils"]

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_earth_fault_compensators import TableEarthFaultCompensators


class TablePetersenCoils(TableEarthFaultCompensators):
    """
    A class representing the PetersenCoil columns required for the database table.
    """

    @property
    def name(self) -> str:
        return "petersen_coils"

    def __init__(self):
        super().__init__()
        self.x_ground_nominal: Column = self._create_column("x_ground_nominal", "NUMBER", Nullable.NULL)
        """
        A column storing the nominal reactance in ohms. This is the operating point (normally over compensation) that is defined based
        on the resonance point in the healthy network condition. The impedance is calculated based on nominal voltage divided by position current.
        """
