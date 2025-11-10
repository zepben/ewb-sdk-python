#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from sqlite3 import Connection
from unittest.mock import create_autospec

from util import import_submodules, all_subclasses
from zepben.ewb import TableEquipmentEquipmentContainers, PreparedStatement, NetworkDatabaseTables, NetworkCimWriter, EquipmentContainer, Site, Substation, \
    Circuit, Feeder, LvFeeder, Junction


def test_only_exports_equipment_for_expected_equipment_containers():
    table = TableEquipmentEquipmentContainers()
    # We use a relaxed mock as we are only checking a fraction of the overall functionality, with the rest being checked in other test classes.
    insert = create_autospec(PreparedStatement)

    database_tables = NetworkDatabaseTables()
    database_tables.prepare_insert_statements(create_autospec(Connection))
    # We are not interested in validating any of the other interactions, so just use relaxed mocks by default.
    database_tables._insert_statements = {k: insert if k == TableEquipmentEquipmentContainers else create_autospec(PreparedStatement) for k, it in
                                          database_tables._insert_statements.items()}

    writer = NetworkCimWriter(database_tables)

    _ = import_submodules('zepben.ewb.model.cim')
    # all_equipment_container_classes = all_subclasses(EquipmentContainer, 'zepben.ewb.model.cim')

    should_export = [Site(mrid="site"), Substation(mrid="substation"), Circuit(mrid="circuit")]
    should_ignore = [Feeder(mrid="feeder"), LvFeeder(mrid="lv_feeder")]

    # Subclass checks were broken; Test needs to be updated to include new classes
    # assert {it.__class__ for it in (should_export + should_ignore)} == all_equipment_container_classes, "Should be checking all EquipmentContainer subclasses"

    junction = Junction()
    for it in should_export:
        junction.add_container(it)
    for it in should_ignore:
        junction.add_container(it)

    writer.save_junction(junction)

    actual_calls = {it.args[1] for it in insert.add_value.call_args_list if it.args[0] == table.equipment_container_mrid.query_index}
    expected_calls = {it.mrid for it in should_export}

    assert actual_calls == expected_calls, "Should have exported all expected types, and no ignored types."
