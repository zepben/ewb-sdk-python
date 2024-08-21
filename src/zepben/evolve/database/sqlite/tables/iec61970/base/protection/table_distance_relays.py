#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_protection_relay_functions import TableProtectionRelayFunctions

__all__ = ["TableDistanceRelays"]


class TableDistanceRelays(TableProtectionRelayFunctions):

    def __init__(self):
        super().__init__()
        self.backward_blind: Column = self._create_column("backward_blind", "NUMBER", Nullable.NULL)
        self.backward_reach: Column = self._create_column("backward_reach", "NUMBER", Nullable.NULL)
        self.backward_reactance: Column = self._create_column("backward_reactance", "NUMBER", Nullable.NULL)
        self.forward_blind: Column = self._create_column("forward_blind", "NUMBER", Nullable.NULL)
        self.forward_reach: Column = self._create_column("forward_reach", "NUMBER", Nullable.NULL)
        self.forward_reactance: Column = self._create_column("forward_reactance", "NUMBER", Nullable.NULL)
        self.operation_phase_angle1: Column = self._create_column("operation_phase_angle1", "NUMBER", Nullable.NULL)
        self.operation_phase_angle2: Column = self._create_column("operation_phase_angle2", "NUMBER", Nullable.NULL)
        self.operation_phase_angle3: Column = self._create_column("operation_phase_angle3", "NUMBER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "distance_relays"
