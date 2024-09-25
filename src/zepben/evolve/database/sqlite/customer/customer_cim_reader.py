#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["CustomerCimReader"]

from typing import Callable

from zepben.evolve.database.sqlite.common.base_cim_reader import BaseCimReader
from zepben.evolve.database.sqlite.extensions.result_set import ResultSet
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
from zepben.evolve.model.cim.iec61968.customers.customer_kind import CustomerKind
from zepben.evolve.model.cim.iec61968.customers.pricing_structure import PricingStructure
from zepben.evolve.model.cim.iec61968.customers.tariff import Tariff
from zepben.evolve.services.customer.customers import CustomerService

class CustomerCimReader(BaseCimReader):
    """
    A class for reading the `CustomerService` tables from the database.

    :param service: The `CustomerService` to populate from the database.
    """

    def __init__(self, service: CustomerService):
        super().__init__(service)
        self._service: CustomerService

    ###################
    # IEC61968 Common #
    ###################

    def _load_agreement(self, agreement: Agreement, table: TableAgreements, result_set: ResultSet) -> bool:
        return self._load_document(agreement, table, result_set)

    ######################
    # IEC61968 Customers #
    ######################

    def load_customers(self, table: TableCustomers, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `Customer` and populate its fields from `TableCustomers`.

        :param table: The database table to read the `Customer` fields from.
        :param result_set: The record in the database table containing the fields for this `Customer`.
        :param set_identifier: A callback to register the mRID of this `Customer` for logging purposes.

        :return: True if the `Customer` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        customer = Customer(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        customer.kind = CustomerKind[result_set.get_string(table.kind.query_index)]
        # Currently unused customer.num_end_devices = rs.get_int(table.num_end_devices.query_index, None)
        customer.special_need = result_set.get_string(table.special_need.query_index, on_none=None)

        return self._load_organisation_role(customer, table, result_set) and self._add_or_throw(customer)

    def load_customer_agreements(self, table: TableCustomerAgreements, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `CustomerAgreement` and populate its fields from `TableCustomerAgreements`.

        :param table: The database table to read the `CustomerAgreement` fields from.
        :param result_set: The record in the database table containing the fields for this `CustomerAgreement`.
        :param set_identifier: A callback to register the mRID of this `CustomerAgreement` for logging purposes.

        :return: True if the `CustomerAgreement` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        customer_agreement = CustomerAgreement(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        customer_agreement.customer = self._ensure_get(
            result_set.get_string(table.customer_mrid.query_index, on_none=None),
            Customer
        )
        if customer_agreement.customer is not None:
            customer_agreement.customer.add_agreement(customer_agreement)

        return self._load_agreement(customer_agreement, table, result_set) and self._add_or_throw(customer_agreement)

    def load_pricing_structures(self, table: TablePricingStructures, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `PricingStructure` and populate its fields from `TablePricingStructures`.

        :param table: The database table to read the `PricingStructure` fields from.
        :param result_set: The record in the database table containing the fields for this `PricingStructure`.
        :param set_identifier: A callback to register the mRID of this `PricingStructure` for logging purposes.

        :return: True if the `PricingStructure` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        pricing_structure = PricingStructure(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_document(pricing_structure, table, result_set) and self._add_or_throw(pricing_structure)

    def load_tariffs(self, table: TableTariffs, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `Tariff` and populate its fields from `TableTariffs`.

        :param table: The database table to read the `Tariff` fields from.
        :param result_set: The record in the database table containing the fields for this `Tariff`.
        :param set_identifier: A callback to register the mRID of this `Tariff` for logging purposes.

        :return: True if the `Tariff` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        tariff = Tariff(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_document(tariff, table, result_set) and self._add_or_throw(tariff)

    ################
    # Associations #
    ################

    def load_customer_agreements_pricing_structures(self, table: TableCustomerAgreementsPricingStructures, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `CustomerAgreement` to `PricingStructure` association from `TableCustomerAgreementsPricingStructures`.

        :param table: The database table to read the association from.
        :param result_set: The record in the database table containing the fields for this association.
        :param set_identifier: A callback to register the identifier of this association for logging purposes.

        :return: True if the association was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        customer_agreement_mrid = set_identifier(result_set.get_string(table.customer_agreement_mrid.query_index))
        set_identifier(f"{customer_agreement_mrid}-to-UNKNOWN")

        pricing_structure_mrid = result_set.get_string(table.pricing_structure_mrid.query_index)
        set_identifier(f"{customer_agreement_mrid}-to-{pricing_structure_mrid}")

        customer_agreement = self._ensure_get(customer_agreement_mrid, CustomerAgreement)
        pricing_structure = self._ensure_get(pricing_structure_mrid, PricingStructure)

        customer_agreement.add_pricing_structure(pricing_structure)

        return True

    def load_pricing_structures_tariffs(self, table: TablePricingStructuresTariffs, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `PricingStructure` to `Tariff` association from `TablePricingStructuresTariffs`.

        :param table: The database table to read the association from.
        :param result_set: The record in the database table containing the fields for this association.
        :param set_identifier: A callback to register the identifier of this association for logging purposes.

        :return: True if the association was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        pricing_structure_mrid = set_identifier(result_set.get_string(table.pricing_structure_mrid.query_index))
        set_identifier(f"{pricing_structure_mrid}-to-UNKNOWN")

        tariff_mrid = result_set.get_string(table.tariff_mrid.query_index)

        pricing_structure = self._ensure_get(pricing_structure_mrid, PricingStructure)
        tariff = self._ensure_get(tariff_mrid, Tariff)

        pricing_structure.add_tariff(tariff)

        return True
