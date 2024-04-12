#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Generator

from zepben.evolve.database.sqlite.common.base_database_tables import BaseDatabaseTables
from zepben.evolve.database.sqlite.tables.associations.table_customer_agreements_pricing_structures import *
from zepben.evolve.database.sqlite.tables.associations.table_pricing_structures_tariffs import *
from zepben.evolve.database.sqlite.tables.iec61968.common.table_organisations import *
from zepben.evolve.database.sqlite.tables.iec61968.customers.table_customer_agreements import *
from zepben.evolve.database.sqlite.tables.iec61968.customers.table_customers import *
from zepben.evolve.database.sqlite.tables.iec61968.customers.table_pricing_structures import *
from zepben.evolve.database.sqlite.tables.iec61968.customers.table_tariffs import *
from zepben.evolve.database.sqlite.tables.sqlite_table import *

__all__ = ["CustomerDatabaseTables"]


class CustomerDatabaseTables(BaseDatabaseTables):
    """
    The collection of tables for our customer databases.
    """

    @property
    def _included_tables(self) -> Generator[SqliteTable, None, None]:
        for table in super()._included_tables:
            yield table

        yield TableCustomerAgreements()
        yield TableCustomerAgreementsPricingStructures()
        yield TableCustomers()
        yield TableOrganisations()
        yield TablePricingStructures()
        yield TablePricingStructuresTariffs()
        yield TableTariffs()
