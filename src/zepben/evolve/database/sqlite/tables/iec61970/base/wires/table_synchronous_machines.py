#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["TableSynchronousMachines"]

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_rotating_machines import TableRotatingMachines


class TableSynchronousMachines(TableRotatingMachines):
    """
    A class representing the SynchronousMachine columns required for the database table.
    """

    @property
    def name(self) -> str:
        return "synchronous_machines"

    def __init__(self):
        super().__init__()
        self.base_q: Column = self._create_column("base_q", "NUMBER", Nullable.NULL)
        """Default base reactive power value in VAr. This value represents the initial reactive power that can be used by any application function."""

        self.condenser_p: Column = self._create_column("condenser_p", "INTEGER", Nullable.NULL)
        """Active power consumed (watts) when in condenser mode operation."""

        self.earthing: Column = self._create_column("earthing", "BOOLEAN", Nullable.NULL)
        """Indicates whether the generator is earthed. Used for short circuit data exchange according to IEC 60909."""

        self.earthing_star_point_r: Column = self._create_column("earthing_star_point_r", "NUMBER", Nullable.NULL)
        """Generator star point earthing resistance in Ohms (Re). Used for short circuit data exchange according to IEC 60909."""

        self.earthing_star_point_x: Column = self._create_column("earthing_star_point_x", "NUMBER", Nullable.NULL)
        """Generator star point earthing reactance in Ohms (Xe). Used for short circuit data exchange according to IEC 60909."""

        self.ikk: Column = self._create_column("ikk", "NUMBER", Nullable.NULL)
        """
        Steady-state short-circuit current (in A for the profile) of generator with compound excitation during 3-phase short circuit.
        - Ikk=0: Generator with no compound excitation. - Ikk<>0: Generator with compound excitation.
        Ikk is used to calculate the minimum steady-state short-circuit current for generators with compound excitation. (4.6.1.2 in IEC 60909-0:2001).
        Used only for single fed short circuit on a generator. (4.3.4.2. in IEC 60909-0:2001).
        """

        self.max_q: Column = self._create_column("max_q", "NUMBER", Nullable.NULL)
        """Maximum reactive power limit in VAr. This is the maximum (nameplate) limit for the unit."""

        self.max_u: Column = self._create_column("max_u", "INTEGER", Nullable.NULL)
        """Maximum voltage limit for the unit in volts."""

        self.min_q: Column = self._create_column("min_q", "NUMBER", Nullable.NULL)
        """Minimum reactive power limit for the unit in VAr."""

        self.min_u: Column = self._create_column("min_u", "INTEGER", Nullable.NULL)
        """Minimum voltage limit for the unit in volts."""

        self.mu: Column = self._create_column("mu", "NUMBER", Nullable.NULL)
        """Factor to calculate the breaking current (Section 4.5.2.1 in IEC 60909-0). Used only for single fed short circuit on a generator (Section 4.3.4.2. in IEC 60909-0)."""

        self.r: Column = self._create_column("r", "NUMBER", Nullable.NULL)
        """
        Equivalent resistance (RG) of generator as a percentage. RG is considered for the calculation of all currents,
        except for the calculation of the peak current ip. Used for short circuit data exchange according to IEC 60909.
        """

        self.r0: Column = self._create_column("r0", "NUMBER", Nullable.NULL)
        """Zero sequence resistance of the synchronous machine as a percentage."""

        self.r2: Column = self._create_column("r2", "NUMBER", Nullable.NULL)
        """Negative sequence resistance as a percentage."""

        self.sat_direct_subtrans_x: Column = self._create_column("sat_direct_subtrans_x", "NUMBER", Nullable.NULL)
        """Direct-axis subtransient reactance saturated as a percentage, also known as Xd"sat."""

        self.sat_direct_sync_x: Column = self._create_column("sat_direct_sync_x", "NUMBER", Nullable.NULL)
        """
        Direct-axes saturated synchronous reactance (xdsat); reciprocal of short-circuit ration, as a percentage.
        Used for short circuit data exchange, only for single fed short circuit on a generator. (4.3.4.2. in IEC 60909-0:2001).
        """

        self.sat_direct_trans_x: Column = self._create_column("sat_direct_trans_x", "NUMBER", Nullable.NULL)
        """Saturated Direct-axis transient reactance as a percentage. The attribute is primarily used for short circuit calculations according to ANSI."""

        self.x0: Column = self._create_column("x0", "NUMBER", Nullable.NULL)
        """Zero sequence reactance of the synchronous machine as a percentage."""

        self.x2: Column = self._create_column("x2", "NUMBER", Nullable.NULL)
        """Negative sequence reactance as a percentage."""

        self.type: Column = self._create_column("type", "TEXT", Nullable.NOT_NULL)
        """Modes that this synchronous machine can operate in."""

        self.operating_mode: Column = self._create_column("operating_mode", "TEXT", Nullable.NOT_NULL)
        """Current mode of operation."""
