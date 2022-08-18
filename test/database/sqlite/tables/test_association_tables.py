#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from database.sqlite.tables.table_test_utils import verify_column
from zepben.evolve import Nullable, TableAssetOrganisationRolesAssets, TableCircuitsSubstations, TableCircuitsTerminals, \
    TableCustomerAgreementsPricingStructures, TableEquipmentEquipmentContainers, TableEquipmentOperationalRestrictions, TableEquipmentUsagePoints, \
    TableLoopsSubstations, TablePricingStructuresTariffs, TableUsagePointsEndDevices


def test_table_asset_organisation_roles_assets():
    t = TableAssetOrganisationRolesAssets()
    verify_column(t.asset_organisation_role_mrid, 1, "asset_organisation_role_mrid", "TEXT", Nullable.NOT_NULL)
    verify_column(t.asset_mrid, 2, "asset_mrid", "TEXT", Nullable.NOT_NULL)
    assert t.unique_index_columns() == [*super(TableAssetOrganisationRolesAssets, t).unique_index_columns(), [t.asset_organisation_role_mrid, t.asset_mrid]]
    assert t.non_unique_index_columns() == [*super(TableAssetOrganisationRolesAssets, t).non_unique_index_columns(), [t.asset_organisation_role_mrid], [t.asset_mrid]]
    assert t.name() == "asset_organisation_roles_assets"


def test_table_circuits_substations():
    t = TableCircuitsSubstations()
    verify_column(t.circuit_mrid, 1, "circuit_mrid", "TEXT", Nullable.NOT_NULL)
    verify_column(t.substation_mrid, 2, "substation_mrid", "TEXT", Nullable.NOT_NULL)
    assert t.unique_index_columns() == [*super(TableCircuitsSubstations, t).unique_index_columns(), [t.circuit_mrid, t.substation_mrid]]
    assert t.non_unique_index_columns() == [*super(TableCircuitsSubstations, t).non_unique_index_columns(), [t.circuit_mrid], [t.substation_mrid]]
    assert t.name() == "circuits_substations"


def test_table_circuits_terminals():
    t = TableCircuitsTerminals()
    verify_column(t.circuit_mrid, 1, "circuit_mrid", "TEXT", Nullable.NOT_NULL)
    verify_column(t.terminal_mrid, 2, "terminal_mrid", "TEXT", Nullable.NOT_NULL)
    assert t.unique_index_columns() == [*super(TableCircuitsTerminals, t).unique_index_columns(), [t.circuit_mrid, t.terminal_mrid]]
    assert t.non_unique_index_columns() == [*super(TableCircuitsTerminals, t).non_unique_index_columns(), [t.circuit_mrid], [t.terminal_mrid]]
    assert t.name() == "circuits_terminals"


def test_table_customer_agreements_pricing_structures():
    t = TableCustomerAgreementsPricingStructures()
    verify_column(t.customer_agreement_mrid, 1, "customer_agreement_mrid", "TEXT", Nullable.NOT_NULL)
    verify_column(t.pricing_structure_mrid, 2, "pricing_structure_mrid", "TEXT", Nullable.NOT_NULL)
    assert t.unique_index_columns() == [*super(TableCustomerAgreementsPricingStructures, t).unique_index_columns(), [t.customer_agreement_mrid, t.pricing_structure_mrid]]
    assert t.non_unique_index_columns() == [*super(TableCustomerAgreementsPricingStructures, t).non_unique_index_columns(), [t.customer_agreement_mrid], [t.pricing_structure_mrid]]
    assert t.name() == "customer_agreements_pricing_structures"


def test_table_equipment_equipment_containers():
    t = TableEquipmentEquipmentContainers()
    verify_column(t.equipment_mrid, 1, "equipment_mrid", "TEXT", Nullable.NOT_NULL)
    verify_column(t.equipment_container_mrid, 2, "equipment_container_mrid", "TEXT", Nullable.NOT_NULL)
    assert t.unique_index_columns() == [*super(TableEquipmentEquipmentContainers, t).unique_index_columns(), [t.equipment_mrid, t.equipment_container_mrid]]
    assert t.non_unique_index_columns() == [*super(TableEquipmentEquipmentContainers, t).non_unique_index_columns(), [t.equipment_mrid], [t.equipment_container_mrid]]
    assert t.name() == "equipment_equipment_containers"


def test_table_equipment_operational_restrictions():
    t = TableEquipmentOperationalRestrictions()
    verify_column(t.equipment_mrid, 1, "equipment_mrid", "TEXT", Nullable.NOT_NULL)
    verify_column(t.operational_restriction_mrid, 2, "operational_restriction_mrid", "TEXT", Nullable.NOT_NULL)
    assert t.unique_index_columns() == [*super(TableEquipmentOperationalRestrictions, t).unique_index_columns(), [t.equipment_mrid, t.operational_restriction_mrid]]
    assert t.non_unique_index_columns() == [*super(TableEquipmentOperationalRestrictions, t).non_unique_index_columns(), [t.equipment_mrid], [t.operational_restriction_mrid]]
    assert t.name() == "equipment_operational_restrictions"


def test_table_equipment_usage_points():
    t = TableEquipmentUsagePoints()
    verify_column(t.equipment_mrid, 1, "equipment_mrid", "TEXT", Nullable.NOT_NULL)
    verify_column(t.usage_point_mrid, 2, "usage_point_mrid", "TEXT", Nullable.NOT_NULL)
    assert t.unique_index_columns() == [*super(TableEquipmentUsagePoints, t).unique_index_columns(), [t.equipment_mrid, t.usage_point_mrid]]
    assert t.non_unique_index_columns() == [*super(TableEquipmentUsagePoints, t).non_unique_index_columns(), [t.equipment_mrid], [t.usage_point_mrid]]
    assert t.name() == "equipment_usage_points"


def test_table_loops_substations():
    t = TableLoopsSubstations()
    verify_column(t.loop_mrid, 1, "loop_mrid", "TEXT", Nullable.NOT_NULL)
    verify_column(t.substation_mrid, 2, "substation_mrid", "TEXT", Nullable.NOT_NULL)
    assert t.unique_index_columns() == [*super(TableLoopsSubstations, t).unique_index_columns(), [t.loop_mrid, t.substation_mrid]]
    assert t.non_unique_index_columns() == [*super(TableLoopsSubstations, t).non_unique_index_columns(), [t.loop_mrid], [t.substation_mrid]]
    assert t.name() == "loops_substations"


def test_table_pricing_structures_tariffs():
    t = TablePricingStructuresTariffs()
    verify_column(t.pricing_structure_mrid, 1, "pricing_structure_mrid", "TEXT", Nullable.NOT_NULL)
    verify_column(t.tariff_mrid, 2, "tariff_mrid", "TEXT", Nullable.NOT_NULL)
    assert t.unique_index_columns() == [*super(TablePricingStructuresTariffs, t).unique_index_columns(), [t.pricing_structure_mrid, t.tariff_mrid]]
    assert t.non_unique_index_columns() == [*super(TablePricingStructuresTariffs, t).non_unique_index_columns(), [t.pricing_structure_mrid], [t.tariff_mrid]]
    assert t.name() == "pricing_structures_tariffs"


def test_table_usage_points_end_devices():
    t = TableUsagePointsEndDevices()
    verify_column(t.usage_point_mrid, 1, "usage_point_mrid", "TEXT", Nullable.NOT_NULL)
    verify_column(t.end_device_mrid, 2, "end_device_mrid", "TEXT", Nullable.NOT_NULL)
    assert t.unique_index_columns() == [*super(TableUsagePointsEndDevices, t).unique_index_columns(), [t.usage_point_mrid, t.end_device_mrid]]
    assert t.non_unique_index_columns() == [*super(TableUsagePointsEndDevices, t).non_unique_index_columns(), [t.usage_point_mrid], [t.end_device_mrid]]
    assert t.name() == "usage_points_end_devices"
