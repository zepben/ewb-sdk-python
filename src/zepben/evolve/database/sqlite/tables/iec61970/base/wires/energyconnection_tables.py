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
        self.column_index += 1
        self.energy_consumer_mrid = Column(self.column_index, "energy_consumer_mrid", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.phase = Column(self.column_index, "phase", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.p = Column(self.column_index, "p", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.q = Column(self.column_index, "q", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.p_fixed = Column(self.column_index, "p_fixed", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.q_fixed = Column(self.column_index, "q_fixed", "NUMBER", Nullable.NOT_NULL)

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
        self.column_index += 1
        self.customer_count = Column(self.column_index, "customer_count", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.grounded = Column(self.column_index, "phase", "BOOLEAN", Nullable.NOT_NULL)
        self.column_index += 1
        self.p = Column(self.column_index, "p", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.q = Column(self.column_index, "q", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.p_fixed = Column(self.column_index, "p_fixed", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.q_fixed = Column(self.column_index, "q_fixed", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.phase_connection = Column(self.column_index, "phase_connection", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "energy_consumers"


class TableEnergySourcePhases(TablePowerSystemResources):
    energy_source_mrid: Column = None
    phase: Column = None

    def __init__(self):
        super(TableEnergySourcePhases, self).__init__()
        self.column_index += 1
        self.energy_source_mrid = Column(self.column_index, "energy_source_mrid", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.phase = Column(self.column_index, "phase", "TEXT", Nullable.NOT_NULL)

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

    def __init__(self):
        super(TableEnergySources, self).__init__()
        self.column_index += 1
        self.active_power = Column(self.column_index, "active_power", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.reactive_power = Column(self.column_index, "reactive_power", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.voltage_angle = Column(self.column_index, "voltage_angle", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.voltage_magnitude = Column(self.column_index, "voltage_magnitude", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.p_max = Column(self.column_index, "p_max", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.p_min = Column(self.column_index, "p_min", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.r = Column(self.column_index, "r", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.r0 = Column(self.column_index, "r0", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.rn = Column(self.column_index, "rn", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.x = Column(self.column_index, "x", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.x0 = Column(self.column_index, "x0", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.xn = Column(self.column_index, "xn", "NUMBER", Nullable.NOT_NULL)

    def name(self) -> str:
        return "energy_sources"


class TableRegulatingCondEq(TableEnergyConnections):
    control_enabled: Column = None

    def __init__(self):
        super(TableRegulatingCondEq, self).__init__()
        self.column_index += 1
        self.control_enabled = Column(self.column_index, "control_enbaled", "BOOLEAN", Nullable.NOT_NULL)


class TableShuntCompensators(TableRegulatingCondEq):
    grounded: Column = None
    nom_u: Column = None
    phase_connection: Column = None
    sections: Column = None

    def __init__(self):
        super(TableShuntCompensators, self).__init__()
        self.column_index += 1
        self.grounded = Column(self.column_index, "grounded", "BOOLEAN", Nullable.NOT_NULL)
        self.column_index += 1
        self.nom_u = Column(self.column_index, "nom_u", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.phase_connection = Column(self.column_index, "phase_connection", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.sections = Column(self.column_index, "sections", "NUMBER", Nullable.NOT_NULL)


class TableLinearShuntCompensators(TableShuntCompensators):
    b0_per_section: Column = None
    b_per_section: Column = None
    g0_per_section: Column = None
    g_per_section: Column = None

    def __init__(self):
        super(TableShuntCompensators, self).__init__()
        self.column_index += 1
        self.b0_per_section = Column(self.column_index, "b0_per_section", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.b_per_section = Column(self.column_index, "b_per_section", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.g0_per_section = Column(self.column_index, "g0_per_section", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.g_per_section = Column(self.column_index, "g_per_section", "NUMBER", Nullable.NOT_NULL)

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
        self.column_index += 1
        self.max_i_fault = Column(self.column_index, "max_i_fault", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.max_q = Column(self.column_index, "max_q", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.min_q = Column(self.column_index, "min_q", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.p = Column(self.column_index, "p", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.q = Column(self.column_index, "q", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.rated_s = Column(self.column_index, "rated_s", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.rated_u = Column(self.column_index, "rated_u", "NUMBER", Nullable.NOT_NULL)

    def name(self) -> str:
        return "power_electronics_connection"


class TablePowerElectronicsConnectionPhases(TablePowerSystemResources):
    power_electronics_connection_mrid: Column = None
    p: Column = None
    phase: Column = None
    q: Column = None

    def __init__(self):
        super(TablePowerElectronicsConnectionPhases, self).__init__()
        self.column_index += 1
        self.power_electronics_connection_mrid = Column(self.column_index, "power_electronics_connection_mrid", "TEXT", Nullable.NULL)
        self.column_index += 1
        self.p = Column(self.column_index, "p", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.phase = Column(self.column_index, "phase", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.q = Column(self.column_index, "q", "NUMBER", Nullable.NOT_NULL)

    def name(self) -> str:
        return "power_electronics_connection_phase"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TablePowerElectronicsConnectionPhases, self).unique_index_columns()
        cols.append([self.power_electronics_connection_mrid])
        return cols
