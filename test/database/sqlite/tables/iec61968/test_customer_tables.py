#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from test.database.sqlite.tables.table_test_utils import verify_column
from zepben.evolve import Nullable, TableCustomerAgreements, TableCustomers, TablePricingStructures, TableTariffs


def test_table_customer_agreements():
    t = TableCustomerAgreements()
    verify_column(t.customer_mrid, 11, "customer_mrid", "TEXT", Nullable.NULL)
    assert t.non_unique_index_columns() == [*super(TableCustomerAgreements, t).non_unique_index_columns(), [t.customer_mrid]]
    assert t.name() == "customer_agreements"


def test_table_customers():
    t = TableCustomers()
    verify_column(t.kind, 6, "kind", "TEXT", Nullable.NOT_NULL)
    verify_column(t.num_end_devices, 7, "num_end_devices", "INTEGER", Nullable.NOT_NULL)
    assert t.name() == "customers"


def test_table_pricing_structures():
    t = TablePricingStructures()
    assert t.name() == "pricing_structures"


def test_table_tariffs():
    t = TableTariffs()
    assert t.name() == "tariffs"
