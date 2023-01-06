#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableConductingEquipment, TablePowerSystemResources

__all__ = ["TableEnergyConnections", "TableEnergyConsumerPhases", "TableEnergyConsumers", "TableEnergySources", "TableEnergySourcePhases",
           "TableRegulatingCondEq", "TableShuntCompensators", "TableLinearShuntCompensators", "TablePowerElectronicsConnection",
           "TablePowerElectronicsConnectionPhases"]


# noinspection PyAbstractClass
class TableEnergyConnections(TableConductingEquipment):
    pass


class TableEnergyConsumerPhases(TablePowerSystemResources):
    energy_consumer_mrid: Column = None
    phase: Column = None
    p: Column = None
    q: Column = None
    p_fixed: Column = None
    q_fixed: Column = None

    def __init__(self):
        super(TableEnergyConsumerPhases, self).__init__()
        self.energy_consumer_mrid = self._create_column("energy_consumer_mrid", "TEXT", Nullable.NOT_NULL)
        self.phase = self._create_column("phase", "TEXT", Nullable.NOT_NULL)
        self.p = self._create_column("p", "NUMBER", Nullable.NULL)
        self.q = self._create_column("q", "NUMBER", Nullable.NULL)
        self.p_fixed = self._create_column("p_fixed", "NUMBER", Nullable.NULL)
        self.q_fixed = self._create_column("q_fixed", "NUMBER", Nullable.NULL)

    def name(self) -> str:
        return "energy_consumer_phases"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableEnergyConsumerPhases, self).unique_index_columns()
        cols.append([self.energy_consumer_mrid, self.phase])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableEnergyConsumerPhases, self).non_unique_index_columns()
        cols.append([self.energy_consumer_mrid])
        return cols


class TableEnergyConsumers(TableEnergyConnections):
    customer_count: Column = None
    grounded: Column = None
    p: Column = None
    q: Column = None
    p_fixed: Column = None
    q_fixed: Column = None
    phase_connection: Column = None

    def __init__(self):
        super(TableEnergyConsumers, self).__init__()
        self.customer_count = self._create_column("customer_count", "INTEGER", Nullable.NULL)
        self.grounded = self._create_column("grounded", "BOOLEAN", Nullable.NOT_NULL)
        self.p = self._create_column("p", "NUMBER", Nullable.NULL)
        self.q = self._create_column("q", "NUMBER", Nullable.NULL)
        self.p_fixed = self._create_column("p_fixed", "NUMBER", Nullable.NULL)
        self.q_fixed = self._create_column("q_fixed", "NUMBER", Nullable.NULL)
        self.phase_connection = self._create_column("phase_connection", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "energy_consumers"


class TableEnergySourcePhases(TablePowerSystemResources):
    energy_source_mrid: Column = None
    phase: Column = None

    def __init__(self):
        super(TableEnergySourcePhases, self).__init__()
        self.energy_source_mrid = self._create_column("energy_source_mrid", "TEXT", Nullable.NOT_NULL)
        self.phase = self._create_column("phase", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "energy_source_phases"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableEnergySourcePhases, self).unique_index_columns()
        cols.append([self.energy_source_mrid, self.phase])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableEnergySourcePhases, self).non_unique_index_columns()
        cols.append([self.energy_source_mrid])
        return cols


class TableEnergySources(TableEnergyConnections):
    active_power: Column = None
    reactive_power: Column = None
    voltage_angle: Column = None
    voltage_magnitude: Column = None
    p_max: Column = None
    p_min: Column = None
    r: Column = None
    r0: Column = None
    rn: Column = None
    x: Column = None
    x0: Column = None
    xn: Column = None
    is_external_grid: Column = None
    r_min: Column = None
    rn_min: Column = None
    r0_min: Column = None
    x_min: Column = None
    xn_min: Column = None
    x0_min: Column = None
    r_max: Column = None
    rn_max: Column = None
    r0_max: Column = None
    x_max: Column = None
    xn_max: Column = None
    x0_max: Column = None

    def __init__(self):
        super(TableEnergySources, self).__init__()
        self.active_power = self._create_column("active_power", "NUMBER", Nullable.NULL)
        self.reactive_power = self._create_column("reactive_power", "NUMBER", Nullable.NULL)
        self.voltage_angle = self._create_column("voltage_angle", "NUMBER", Nullable.NULL)
        self.voltage_magnitude = self._create_column("voltage_magnitude", "NUMBER", Nullable.NULL)
        self.p_max = self._create_column("p_max", "NUMBER", Nullable.NULL)
        self.p_min = self._create_column("p_min", "NUMBER", Nullable.NULL)
        self.r = self._create_column("r", "NUMBER", Nullable.NULL)
        self.r0 = self._create_column("r0", "NUMBER", Nullable.NULL)
        self.rn = self._create_column("rn", "NUMBER", Nullable.NULL)
        self.x = self._create_column("x", "NUMBER", Nullable.NULL)
        self.x0 = self._create_column("x0", "NUMBER", Nullable.NULL)
        self.xn = self._create_column("xn", "NUMBER", Nullable.NULL)
        self.is_external_grid = self._create_column("is_external_grid", "BOOLEAN", Nullable.NOT_NULL)
        self.r_min = self._create_column("r_min", "NUMBER", Nullable.NULL)
        self.rn_min = self._create_column("rn_min", "NUMBER", Nullable.NULL)
        self.r0_min = self._create_column("r0_min", "NUMBER", Nullable.NULL)
        self.x_min = self._create_column("x_min", "NUMBER", Nullable.NULL)
        self.xn_min = self._create_column("xn_min", "NUMBER", Nullable.NULL)
        self.x0_min = self._create_column("x0_min", "NUMBER", Nullable.NULL)
        self.r_max = self._create_column("r_max", "NUMBER", Nullable.NULL)
        self.rn_max = self._create_column("rn_max", "NUMBER", Nullable.NULL)
        self.r0_max = self._create_column("r0_max", "NUMBER", Nullable.NULL)
        self.x_max = self._create_column("x_max", "NUMBER", Nullable.NULL)
        self.xn_max = self._create_column("xn_max", "NUMBER", Nullable.NULL)
        self.x0_max = self._create_column("x0_max", "NUMBER", Nullable.NULL)

    def name(self) -> str:
        return "energy_sources"


# noinspection PyAbstractClass
class TableRegulatingCondEq(TableEnergyConnections):
    control_enabled: Column = None

    def __init__(self):
        super(TableRegulatingCondEq, self).__init__()
        self.control_enabled = self._create_column("control_enabled", "BOOLEAN", Nullable.NOT_NULL)


# noinspection PyAbstractClass
class TableShuntCompensators(TableRegulatingCondEq):
    shunt_compensator_info_mrid: Column = None
    grounded: Column = None
    nom_u: Column = None
    phase_connection: Column = None
    sections: Column = None

    def __init__(self):
        super(TableShuntCompensators, self).__init__()
        self.shunt_compensator_info_mrid = self._create_column("shunt_compensator_info_mrid", "TEXT", Nullable.NULL)
        self.grounded = self._create_column("grounded", "BOOLEAN", Nullable.NOT_NULL)
        self.nom_u = self._create_column("nom_u", "INTEGER", Nullable.NULL)
        self.phase_connection = self._create_column("phase_connection", "TEXT", Nullable.NOT_NULL)
        self.sections = self._create_column("sections", "NUMBER", Nullable.NULL)


class TableLinearShuntCompensators(TableShuntCompensators):
    b0_per_section: Column = None
    b_per_section: Column = None
    g0_per_section: Column = None
    g_per_section: Column = None

    def __init__(self):
        super(TableLinearShuntCompensators, self).__init__()
        self.b0_per_section = self._create_column("b0_per_section", "NUMBER", Nullable.NULL)
        self.b_per_section = self._create_column("b_per_section", "NUMBER", Nullable.NULL)
        self.g0_per_section = self._create_column("g0_per_section", "NUMBER", Nullable.NULL)
        self.g_per_section = self._create_column("g_per_section", "NUMBER", Nullable.NULL)

    def name(self) -> str:
        return "linear_shunt_compensators"


class TablePowerElectronicsConnection(TableRegulatingCondEq):
    max_i_fault: Column = None
    max_q: Column = None
    min_q: Column = None
    p: Column = None
    q: Column = None
    rated_s: Column = None
    rated_u: Column = None

    def __init__(self):
        super(TablePowerElectronicsConnection, self).__init__()
        self.max_i_fault = self._create_column("max_i_fault", "INTEGER", Nullable.NULL)
        self.max_q = self._create_column("max_q", "NUMBER", Nullable.NULL)
        self.min_q = self._create_column("min_q", "NUMBER", Nullable.NULL)
        self.p = self._create_column("p", "NUMBER", Nullable.NULL)
        self.q = self._create_column("q", "NUMBER", Nullable.NULL)
        self.rated_s = self._create_column("rated_s", "INTEGER", Nullable.NULL)
        self.rated_u = self._create_column("rated_u", "INTEGER", Nullable.NULL)

    def name(self) -> str:
        return "power_electronics_connection"


class TablePowerElectronicsConnectionPhases(TablePowerSystemResources):
    power_electronics_connection_mrid: Column = None
    p: Column = None
    phase: Column = None
    q: Column = None

    def __init__(self):
        super(TablePowerElectronicsConnectionPhases, self).__init__()
        self.power_electronics_connection_mrid = self._create_column("power_electronics_connection_mrid", "TEXT", Nullable.NULL)
        self.p = self._create_column("p", "NUMBER", Nullable.NULL)
        self.phase = self._create_column("phase", "TEXT", Nullable.NOT_NULL)
        self.q = self._create_column("q", "NUMBER", Nullable.NULL)

    def name(self) -> str:
        return "power_electronics_connection_phase"

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TablePowerElectronicsConnectionPhases, self).non_unique_index_columns()
        cols.append([self.power_electronics_connection_mrid])
        return cols
