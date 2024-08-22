#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["TableRotatingMachines"]

from zepben.evolve import TableRegulatingCondEq
from zepben.evolve.database.sqlite.tables.column import Column, Nullable


class TableRotatingMachines(TableRegulatingCondEq):
    """
    A class representing the RotatingMachine columns required for the database table.
    """

    @property
    def name(self) -> str:
        return "rotating_machines"

    def __init__(self):
        super().__init__()
        self.rated_power_factor: Column = self._create_column("rated_power_factor", "NUMBER", Nullable.NULL)
        """Power factor (nameplate data). It is primarily used for short circuit data exchange according to IEC 60909. The attribute cannot be a negative value."""

        self.rated_s: Column = self._create_column("rated_s", "NUMBER", Nullable.NULL)
        """Nameplate apparent power rating for the unit in volt-amperes (VA). The attribute shall have a positive value."""

        self.rated_u: Column = self._create_column("rated_u", "INTEGER", Nullable.NULL)
        """Rated voltage in volts (nameplate data, Ur in IEC 60909-0). It is primarily used for short circuit data exchange according to IEC 60909. The attribute shall be a positive value."""

        self.p: Column = self._create_column("p", "NUMBER", Nullable.NULL)
        """Active power injection in watts. Load sign convention is used, i.e. positive sign means flow out from a node. Starting value for a steady state solution."""

        self.q: Column = self._create_column("q", "NUMBER", Nullable.NULL)
        """Reactive power injection in VAr. Load sign convention is used, i.e. positive sign means flow out from a node. Starting value for a steady state solution."""
