#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.associations.customeragreements_association_tables import TableCustomerAgreementsPricingStructures
from zepben.evolve.database.sqlite.tables.associations.pricingstructure_association_tables import TablePricingStructuresTariffs
from zepben.evolve.database.sqlite.tables.database_tables import PreparedStatement
from zepben.evolve.database.sqlite.tables.iec61968.common_tables import TableAgreements
from zepben.evolve.database.sqlite.tables.iec61968.customer_tables import TableCustomers, TableCustomerAgreements, TablePricingStructures, TableTariffs
from zepben.evolve.database.sqlite.writers.base_cim_writer import BaseCIMWriter
from zepben.evolve.model.cim.iec61968.common.document import Agreement
from zepben.evolve.model.cim.iec61968.customers.customer import Customer
from zepben.evolve.model.cim.iec61968.customers.customer_agreement import CustomerAgreement
from zepben.evolve.model.cim.iec61968.customers.pricing_structure import PricingStructure
from zepben.evolve.model.cim.iec61968.customers.tariff import Tariff

__all__ = ["CustomerCIMWriter"]


class CustomerCIMWriter(BaseCIMWriter):

    def save_agreement(self, table: TableAgreements, insert: PreparedStatement, agreement: Agreement, description: str) -> bool:
        return self._save_document(table, insert, agreement, description)

    def save_customer(self, customer: Customer) -> bool:
        table = self.database_tables.get_table(TableCustomers)
        insert = self.database_tables.get_insert(TableCustomers)

        insert.add_value(table.kind.query_index, customer.kind.name)
        insert.add_value(table.num_end_devices.query_index, 0)  # Currently unused

        return self.save_organisation_role(table, insert, customer, "Customer")

    def save_customer_agreement(self, customer_agreement: CustomerAgreement) -> bool:
        table = self.database_tables.get_table(TableCustomerAgreements)
        insert = self.database_tables.get_insert(TableCustomerAgreements)

        status = True
        for ps in customer_agreement.pricing_structures:
            status = status and self.save_customer_agreement_to_pricing_structure_association(customer_agreement, ps)

        insert.add_value(table.customer_mrid.query_index, self._mrid_or_none(customer_agreement.customer))

        return status and self.save_agreement(table, insert, customer_agreement, "CustomerAgreement")

    def save_pricing_structure(self, pricing_structure: PricingStructure) -> bool:
        table = self.database_tables.get_table(TablePricingStructures)
        insert = self.database_tables.get_insert(TablePricingStructures)

        status = True
        for tariff in pricing_structure.tariffs:
            status = status and self.save_pricing_structure_to_tariff_association(pricing_structure, tariff)

        return status and self._save_document(table, insert, pricing_structure, "PricingStructure")

    def save_tariff(self, tariff: Tariff) -> bool:
        table = self.database_tables.get_table(TableTariffs)
        insert = self.database_tables.get_insert(TableTariffs)

        return self._save_document(table, insert, tariff, "tariff")

    # Associations #
    def save_customer_agreement_to_pricing_structure_association(self, customer_agreement: CustomerAgreement, pricing_structure: PricingStructure) -> bool:
        table = self.database_tables.get_table(TableCustomerAgreementsPricingStructures)
        insert = self.database_tables.get_insert(TableCustomerAgreementsPricingStructures)

        insert.add_value(table.customer_agreement_mrid.query_index, customer_agreement.mrid)
        insert.add_value(table.pricing_structure_mrid.query_index, pricing_structure.mrid)

        return self.try_execute_single_update(insert, f"{customer_agreement.mrid}-to-{pricing_structure.mrid}",
                                              "CustomerAgreement to PricingStructure association")

    def save_pricing_structure_to_tariff_association(self, pricing_structure: PricingStructure, tariff: Tariff) -> bool:
        table = self.database_tables.get_table(TablePricingStructuresTariffs)
        insert = self.database_tables.get_insert(TablePricingStructuresTariffs)

        insert.add_value(table.pricing_structure_mrid.query_index, pricing_structure.mrid)
        insert.add_value(table.tariff_mrid.query_index, tariff.mrid)

        return self.try_execute_single_update(insert, f"{pricing_structure.mrid}-to-{tariff.mrid}", "PricingStructure to Tariff association")
