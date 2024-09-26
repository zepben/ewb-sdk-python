#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["TableEarthFaultCompensators"]

from abc import ABC

from zepben.evolve import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_conducting_equipment import TableConductingEquipment


class TableEarthFaultCompensators(TableConductingEquipment, ABC):
    """
    A class representing the EarthFaultCompensator columns required for the database table.
    """

    def __init__(self):
        super().__init__()
        self.r: Column = self._create_column("r", "NUMBER", Nullable.NULL)
        """A column storing the Nominal resistance of device in ohms."""
