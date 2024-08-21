#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""
Helpers to simply print the database SQL statements
"""
from typing import Callable

from zepben.evolve import SqliteTable, CustomerDatabaseTables, DiagramDatabaseTables, NetworkDatabaseTables


def print_database_create_statements(table: SqliteTable):
    print_statement(table.create_table_sql)
    for it in table.create_indexes_sql:
        print_statement(it)
    print("")


def print_database_select_statements(table: SqliteTable):
    print_statement(table.select_sql)


def print_database_insert_statements(table: SqliteTable):
    print_statement(table.prepared_insert_sql)


def print_database_update_statements(table: SqliteTable):
    print_statement(table.prepared_update_sql)


def print_statements(action: Callable[[SqliteTable], None]):
    print("******** Customer Database ********")
    print("")
    CustomerDatabaseTables().for_each_table(action)
    print("")
    print("******** Diagram Database ********")
    print("")
    DiagramDatabaseTables().for_each_table(action)
    print("")
    print("******** Network Database ********")
    print("")
    NetworkDatabaseTables().for_each_table(action)
    print("")


def print_statement(sql: str):
    print(f"{sql};")


if __name__ == "__main__":
    print("#####################")
    print("# CREATE STATEMENTS #")
    print("#####################")
    print("")
    print_statements(print_database_create_statements)

    print("#####################")
    print("# SELECT STATEMENTS #")
    print("#####################")
    print("")
    print_statements(print_database_select_statements)

    print("#####################")
    print("# INSERT STATEMENTS #")
    print("#####################")
    print("")
    print_statements(print_database_insert_statements)

    print("#####################")
    print("# UPDATE STATEMENTS #")
    print("#####################")
    print("")
    print_statements(print_database_update_statements)
