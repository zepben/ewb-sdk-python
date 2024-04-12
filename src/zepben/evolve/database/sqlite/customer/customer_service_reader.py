#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["CustomerServiceReader"]

from sqlite3 import Connection

from zepben.evolve.database.sqlite.common.base_service_reader import BaseServiceReader
from zepben.evolve.database.sqlite.customer.customer_cim_reader import CustomerCimReader
from zepben.evolve.database.sqlite.customer.customer_database_tables import CustomerDatabaseTables
from zepben.evolve.database.sqlite.tables.associations.table_customer_agreements_pricing_structures import TableCustomerAgreementsPricingStructures
from zepben.evolve.database.sqlite.tables.associations.table_pricing_structures_tariffs import TablePricingStructuresTariffs
from zepben.evolve.database.sqlite.tables.iec61968.common.table_organisations import TableOrganisations
from zepben.evolve.database.sqlite.tables.iec61968.customers.table_customer_agreements import TableCustomerAgreements
from zepben.evolve.database.sqlite.tables.iec61968.customers.table_customers import TableCustomers
from zepben.evolve.database.sqlite.tables.iec61968.customers.table_pricing_structures import TablePricingStructures
from zepben.evolve.database.sqlite.tables.iec61968.customers.table_tariffs import TableTariffs
from zepben.evolve.services.customer.customers import CustomerService


class CustomerServiceReader(BaseServiceReader):
    """
    A class for reading a [CustomerService] from the database.

    @param service The [CustomerService] to populate from the database.
    @param database_tables The tables available in the database.
    @param connection A connection to the database.

    @property reader The [CustomerCimReader] used to load the objects from the database.
    """

    def __init__(
        self,
        service: CustomerService,
        database_tables: CustomerDatabaseTables,
        connection: Connection,
        reader: CustomerCimReader = None
    ):
        reader = reader if reader is not None else CustomerCimReader(service)
        super().__init__(database_tables, connection, reader)

        # This is not strictly necessary, it is just to update the type of the reader. It could be done with a generic
        # on the base class which looks like it works, but that actually silently breaks code insight and completion
        self._reader = reader

    def _do_load(self) -> bool:
        return all([
            self._load_each(TableOrganisations, self._reader.load_organisations),
            self._load_each(TableCustomers, self._reader.load_customers),
            self._load_each(TableCustomerAgreements, self._reader.load_customer_agreements),
            self._load_each(TablePricingStructures, self._reader.load_pricing_structures),
            self._load_each(TableTariffs, self._reader.load_tariffs),
            self._load_each(TableCustomerAgreementsPricingStructures, self._reader.load_customer_agreements_pricing_structures),
            self._load_each(TablePricingStructuresTariffs, self._reader.load_pricing_structures_tariffs)
        ])
