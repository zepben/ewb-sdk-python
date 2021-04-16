#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from test.database.sqlite.tables.table_test_utils import verify_column
from zepben.evolve import Nullable, TableEnergyConsumerPhases, TableEnergyConsumers, TableEnergySourcePhases, TableEnergySources, TableRegulatingCondEq, \
    TableShuntCompensators, TableLinearShuntCompensators, TablePowerElectronicsConnection, TablePowerElectronicsConnectionPhases


def test_table_energy_consumer_phases():
    t = TableEnergyConsumerPhases()
    verify_column(t.energy_consumer_mrid, 7, "energy_consumer_mrid", "TEXT", Nullable.NOT_NULL)
    verify_column(t.phase, 8, "phase", "TEXT", Nullable.NOT_NULL)
    verify_column(t.p, 9, "p", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.q, 10, "q", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.p_fixed, 11, "p_fixed", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.q_fixed, 12, "q_fixed", "NUMBER", Nullable.NOT_NULL)
    assert t.unique_index_columns() == [*super(TableEnergyConsumerPhases, t).unique_index_columns(), [t.energy_consumer_mrid, t.phase]]
    assert t.non_unique_index_columns() == [*super(TableEnergyConsumerPhases, t).non_unique_index_columns(), [t.energy_consumer_mrid]]
    assert t.name() == "energy_consumer_phases"


def test_table_energy_consumers():
    t = TableEnergyConsumers()
    verify_column(t.customer_count, 10, "customer_count", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.grounded, 11, "grounded", "BOOLEAN", Nullable.NOT_NULL)
    verify_column(t.p, 12, "p", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.q, 13, "q", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.p_fixed, 14, "p_fixed", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.q_fixed, 15, "q_fixed", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.phase_connection, 16, "phase_connection", "TEXT", Nullable.NOT_NULL)
    assert t.name() == "energy_consumers"


def test_table_energy_source_phases():
    t = TableEnergySourcePhases()
    verify_column(t.energy_source_mrid, 7, "energy_source_mrid", "TEXT", Nullable.NOT_NULL)
    verify_column(t.phase, 8, "phase", "TEXT", Nullable.NOT_NULL)
    assert t.unique_index_columns() == [*super(TableEnergySourcePhases, t).unique_index_columns(), [t.energy_source_mrid, t.phase]]
    assert t.non_unique_index_columns() == [*super(TableEnergySourcePhases, t).non_unique_index_columns(), [t.energy_source_mrid]]
    assert t.name() == "energy_source_phases"


def test_table_energy_sources():
    t = TableEnergySources()
    verify_column(t.active_power, 10, "active_power", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.reactive_power, 11, "reactive_power", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.voltage_angle, 12, "voltage_angle", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.voltage_magnitude, 13, "voltage_magnitude", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.p_max, 14, "p_max", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.p_min, 15, "p_min", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.r, 16, "r", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.r0, 17, "r0", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.rn, 18, "rn", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.x, 19, "x", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.x0, 20, "x0", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.xn, 21, "xn", "NUMBER", Nullable.NOT_NULL)
    assert t.name() == "energy_sources"


def test_table_regulating_cond_eq():
    t = TableRegulatingCondEq()
    verify_column(t.control_enabled, 10, "control_enabled", "BOOLEAN", Nullable.NOT_NULL)


def test_table_shunt_compensators():
    t = TableShuntCompensators()
    verify_column(t.grounded, 11, "grounded", "BOOLEAN", Nullable.NOT_NULL)
    verify_column(t.nom_u, 12, "nom_u", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.phase_connection, 13, "phase_connection", "TEXT", Nullable.NOT_NULL)
    verify_column(t.sections, 14, "sections", "NUMBER", Nullable.NOT_NULL)


def test_table_linear_shunt_compensators():
    t = TableLinearShuntCompensators()
    verify_column(t.b0_per_section, 15, "b0_per_section", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.b_per_section, 16, "b_per_section", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.g0_per_section, 17, "g0_per_section", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.g_per_section, 18, "g_per_section", "NUMBER", Nullable.NOT_NULL)
    assert t.name() == "linear_shunt_compensators"


def test_table_power_electronics_connection():
    t = TablePowerElectronicsConnection()
    verify_column(t.max_i_fault, 11, "max_i_fault", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.max_q, 12, "max_q", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.min_q, 13, "min_q", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.p, 14, "p", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.q, 15, "q", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.rated_s, 16, "rated_s", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.rated_u, 17, "rated_u", "INTEGER", Nullable.NOT_NULL)
    assert t.name() == "power_electronics_connection"


def test_table_power_electronics_connection_phases():
    t = TablePowerElectronicsConnectionPhases()
    verify_column(t.power_electronics_connection_mrid, 7, "power_electronics_connection_mrid", "TEXT", Nullable.NULL)
    verify_column(t.p, 8, "p", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.phase, 9, "phase", "TEXT", Nullable.NOT_NULL)
    verify_column(t.q, 10, "q", "NUMBER", Nullable.NOT_NULL)
    assert t.name() == "power_electronics_connection_phase"
    assert t.unique_index_columns() == [*super(TablePowerElectronicsConnectionPhases, t).unique_index_columns(), [t.power_electronics_connection_mrid]]

