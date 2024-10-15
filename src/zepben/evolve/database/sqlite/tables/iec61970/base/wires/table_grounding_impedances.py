#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["TableGroundingImpedances"]

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_earth_fault_compensators import TableEarthFaultCompensators


class TableGroundingImpedances(TableEarthFaultCompensators):
    """
    A class representing the GroundingImpedance columns required for the database table.
    """

    @property
    def name(self) -> str:
        return "grounding_impedances"

    def __init__(self):
        super().__init__()
        self.x: Column = self._create_column("x", "NUMBER", Nullable.NULL)
        """A column storing the Reactance of device in ohms."""
