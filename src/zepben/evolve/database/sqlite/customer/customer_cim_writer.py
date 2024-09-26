#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["CustomerCimWriter"]

from zepben.evolve.database.sqlite.common.base_cim_writer import BaseCimWriter
from zepben.evolve.database.sqlite.customer.customer_database_tables import CustomerDatabaseTables
from zepben.evolve.database.sqlite.extensions.prepared_statement import PreparedStatement
from zepben.evolve.database.sqlite.tables.associations.table_customer_agreements_pricing_structures import TableCustomerAgreementsPricingStructures
from zepben.evolve.database.sqlite.tables.associations.table_pricing_structures_tariffs import TablePricingStructuresTariffs
from zepben.evolve.database.sqlite.tables.iec61968.common.table_agreements import TableAgreements
from zepben.evolve.database.sqlite.tables.iec61968.customers.table_customer_agreements import TableCustomerAgreements
from zepben.evolve.database.sqlite.tables.iec61968.customers.table_customers import TableCustomers
from zepben.evolve.database.sqlite.tables.iec61968.customers.table_pricing_structures import TablePricingStructures
from zepben.evolve.database.sqlite.tables.iec61968.customers.table_tariffs import TableTariffs
from zepben.evolve.model.cim.iec61968.common.document import Agreement
from zepben.evolve.model.cim.iec61968.customers.customer import Customer
from zepben.evolve.model.cim.iec61968.customers.customer_agreement import CustomerAgreement
from zepben.evolve.model.cim.iec61968.customers.pricing_structure import PricingStructure
from zepben.evolve.model.cim.iec61968.customers.tariff import Tariff


class CustomerCimWriter(BaseCimWriter):
    """
    A class for writing the `CustomerService` tables to the database.

    :param database_tables: The tables available in the database.
    """

    def __init__(self, database_tables: CustomerDatabaseTables):
        super().__init__(database_tables)
        self._database_tables: CustomerDatabaseTables

    ###################
    # IEC61968 Common #
    ###################

    def _save_agreement(self, table: TableAgreements, insert: PreparedStatement, agreement: Agreement, description: str) -> bool:
        return self._save_document(table, insert, agreement, description)

    ######################
    # IEC61968 Customers #
    ######################

    def save_customer(self, customer: Customer) -> bool:
        """
        Save the `Customer` fields to `TableCustomers`.

        :param customer: The `Customer` instance to write to the database.

        :return: True if the `Customer` was successfully written to the database, otherwise False.
        :raises SQLException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableCustomers)
        insert = self._database_tables.get_insert(TableCustomers)

        insert.add_value(table.kind.query_index, customer.kind.name)
        insert.add_value(table.num_end_devices.query_index, 0)  # Currently unused
        insert.add_value(table.special_need.query_index, customer.special_need)

        return self._save_organisation_role(table, insert, customer, "customer")

    def save_customer_agreement(self, customer_agreement: CustomerAgreement) -> bool:
        """
        Save the `CustomerAgreement` fields to `TableCustomerAgreements`.

        :param customer_agreement: The `CustomerAgreement` instance to write to the database.

        :return: True if the `CustomerAgreement` was successfully written to the database, otherwise False.
        :raises SQLException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableCustomerAgreements)
        insert = self._database_tables.get_insert(TableCustomerAgreements)

        status = True
        for it in customer_agreement.pricing_structures:
            status = all([status, self._save_customer_agreement_to_pricing_structure_association(customer_agreement, it)])

        insert.add_value(table.customer_mrid.query_index, self._mrid_or_none(customer_agreement.customer))

        return all([status, self._save_agreement(table, insert, customer_agreement, "customer agreement")])

    def save_pricing_structure(self, pricing_structure: PricingStructure) -> bool:
        """
        Save the `PricingStructure` fields to `TablePricingStructures`.

        :param pricing_structure: The `PricingStructure` instance to write to the database.

        :return: True if the `PricingStructure` was successfully written to the database, otherwise False.
        :raises SQLException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TablePricingStructures)
        insert = self._database_tables.get_insert(TablePricingStructures)

        status = True
        for it in pricing_structure.tariffs:
            status = all([status, self._save_pricing_structure_to_tariff_association(pricing_structure, it)])

        return all([status, self._save_document(table, insert, pricing_structure, "pricing structure")])

    def save_tariff(self, tariff: Tariff) -> bool:
        """
        Save the `Tariff` fields to `TableTariffs`.

        :param tariff: The `Tariff` instance to write to the database.

        :return: True if the `Tariff` was successfully written to the database, otherwise False.
        :raises SQLException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableTariffs)
        insert = self._database_tables.get_insert(TableTariffs)

        return self._save_document(table, insert, tariff, "tariff")

    ################
    # Associations #
    ################

    def _save_customer_agreement_to_pricing_structure_association(self, customer_agreement: CustomerAgreement, pricing_structure: PricingStructure) -> bool:
        table = self._database_tables.get_table(TableCustomerAgreementsPricingStructures)
        insert = self._database_tables.get_insert(TableCustomerAgreementsPricingStructures)

        insert.add_value(table.customer_agreement_mrid.query_index, customer_agreement.mrid)
        insert.add_value(table.pricing_structure_mrid.query_index, pricing_structure.mrid)

        return self._try_execute_single_update(insert, "customer agreement to pricing structure association")

    def _save_pricing_structure_to_tariff_association(self, pricing_structure: PricingStructure, tariff: Tariff) -> bool:
        table = self._database_tables.get_table(TablePricingStructuresTariffs)
        insert = self._database_tables.get_insert(TablePricingStructuresTariffs)

        insert.add_value(table.pricing_structure_mrid.query_index, pricing_structure.mrid)
        insert.add_value(table.tariff_mrid.query_index, tariff.mrid)

        return self._try_execute_single_update(insert, "pricing structure to tariff association")
