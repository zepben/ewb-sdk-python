#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_regulating_cond_eq import TableRegulatingCondEq

__all__ = ["TablePowerElectronicsConnections"]


class TablePowerElectronicsConnections(TableRegulatingCondEq):

    def __init__(self):
        super().__init__()
        self.max_i_fault: Column = self._create_column("max_i_fault", "INTEGER", Nullable.NULL)
        self.max_q: Column = self._create_column("max_q", "NUMBER", Nullable.NULL)
        self.min_q: Column = self._create_column("min_q", "NUMBER", Nullable.NULL)
        self.p: Column = self._create_column("p", "NUMBER", Nullable.NULL)
        self.q: Column = self._create_column("q", "NUMBER", Nullable.NULL)
        self.rated_s: Column = self._create_column("rated_s", "INTEGER", Nullable.NULL)
        self.rated_u: Column = self._create_column("rated_u", "INTEGER", Nullable.NULL)
        self.inverter_standard: Column = self._create_column("inverter_standard", "TEXT", Nullable.NULL)
        self.sustain_op_overvolt_limit: Column = self._create_column("sustain_op_overvolt_limit", "INTEGER", Nullable.NULL)
        self.stop_at_over_freq: Column = self._create_column("stop_at_over_freq", "NUMBER", Nullable.NULL)
        self.stop_at_under_freq: Column = self._create_column("stop_at_under_freq", "NUMBER", Nullable.NULL)
        self.inv_volt_watt_resp_mode: Column = self._create_column("inv_volt_watt_resp_mode", "BOOLEAN", Nullable.NULL)
        self.inv_watt_resp_v1: Column = self._create_column("inv_watt_resp_v1", "INTEGER", Nullable.NULL)
        self.inv_watt_resp_v2: Column = self._create_column("inv_watt_resp_v2", "INTEGER", Nullable.NULL)
        self.inv_watt_resp_v3: Column = self._create_column("inv_watt_resp_v3", "INTEGER", Nullable.NULL)
        self.inv_watt_resp_v4: Column = self._create_column("inv_watt_resp_v4", "INTEGER", Nullable.NULL)
        self.inv_watt_resp_p_at_v1: Column = self._create_column("inv_watt_resp_p_at_v1", "NUMBER", Nullable.NULL)
        self.inv_watt_resp_p_at_v2: Column = self._create_column("inv_watt_resp_p_at_v2", "NUMBER", Nullable.NULL)
        self.inv_watt_resp_p_at_v3: Column = self._create_column("inv_watt_resp_p_at_v3", "NUMBER", Nullable.NULL)
        self.inv_watt_resp_p_at_v4: Column = self._create_column("inv_watt_resp_p_at_v4", "NUMBER", Nullable.NULL)
        self.inv_volt_var_resp_mode: Column = self._create_column("inv_volt_var_resp_mode", "BOOLEAN", Nullable.NULL)
        self.inv_var_resp_v1: Column = self._create_column("inv_var_resp_v1", "INTEGER", Nullable.NULL)
        self.inv_var_resp_v2: Column = self._create_column("inv_var_resp_v2", "INTEGER", Nullable.NULL)
        self.inv_var_resp_v3: Column = self._create_column("inv_var_resp_v3", "INTEGER", Nullable.NULL)
        self.inv_var_resp_v4: Column = self._create_column("inv_var_resp_v4", "INTEGER", Nullable.NULL)
        self.inv_var_resp_q_at_v1: Column = self._create_column("inv_var_resp_q_at_v1", "NUMBER", Nullable.NULL)
        self.inv_var_resp_q_at_v2: Column = self._create_column("inv_var_resp_q_at_v2", "NUMBER", Nullable.NULL)
        self.inv_var_resp_q_at_v3: Column = self._create_column("inv_var_resp_q_at_v3", "NUMBER", Nullable.NULL)
        self.inv_var_resp_q_at_v4: Column = self._create_column("inv_var_resp_q_at_v4", "NUMBER", Nullable.NULL)
        self.inv_reactive_power_mode: Column = self._create_column("inv_reactive_power_mode", "BOOLEAN", Nullable.NULL)
        self.inv_fix_reactive_power: Column = self._create_column("inv_fix_reactive_power", "NUMBER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "power_electronics_connections"
