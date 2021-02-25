#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Callable

from zepben.evolve import BaseCIMReader, CustomerService, Agreement, TableAgreements, ResultSet, TableCustomers, Customer, CustomerKind, \
    TableCustomerAgreements, CustomerAgreement, TablePricingStructures, PricingStructure, TableTariffs, Tariff, TableCustomerAgreementsPricingStructures, \
    TablePricingStructuresTariffs

__all__ = ["CustomerCIMReader"]


class CustomerCIMReader(BaseCIMReader):
    _customer_service: CustomerService

    def __init__(self, customer_service: CustomerService):
        super().__init__(customer_service)
        self._customer_service = customer_service

    # ************ IEC61968 COMMON ************

    def _load_agreement(self, agreement: Agreement, table: TableAgreements, rs: ResultSet) -> bool:
        return self._load_document(agreement, table, rs)

    # ************ IEC61968 CUSTOMERS ************

    def load_customer(self, table: TableCustomers, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        customer = Customer(mrid=set_last_mrid(rs.get_string(table.mrid.query_index, ValueError)))

        customer.kind = CustomerKind[rs.get_string(table.kind.query_index)]
        # Currently unused customer.num_end_devices = rs.get_int(table.num_end_devices.query_index, None)

        return self._load_organisation_role(customer, table, rs) and self._add_or_throw(customer)

    def load_customer_agreement(self, table: TableCustomerAgreements, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        customer_agreement = CustomerAgreement(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        customer_agreement.customer = self._ensure_get(rs.get_string(table.customer_mrid.query_index, None), Customer)
        if customer_agreement.customer is not None:
            customer_agreement.customer.add_agreement(customer_agreement)

        return self._load_agreement(customer_agreement, table, rs) and self._add_or_throw(customer_agreement)

    def load_pricing_structure(self, table: TablePricingStructures, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        pricing_structure = PricingStructure(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_document(pricing_structure, table, rs) and self._add_or_throw(pricing_structure)

    def load_tariff(self, table: TableTariffs, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        tariff = Tariff(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_document(tariff, table, rs) and self._add_or_throw(tariff)

    # ************ ASSOCIATIONS ************

    def load_customer_agreement_pricing_structure(
        self,
        table: TableCustomerAgreementsPricingStructures,
        rs: ResultSet,
        set_last_mrid: Callable[[str], str]
    ) -> bool:
        customer_agreement_mrid = set_last_mrid(rs.get_string(table.customer_agreement_mrid.query_index))
        set_last_mrid(f"{customer_agreement_mrid}-to-UNKNOWN")

        pricing_structure_mrid = rs.get_string(table.pricing_structure_mrid.query_index)
        set_last_mrid(f"{customer_agreement_mrid}-to-{pricing_structure_mrid}")

        customer_agreement = self._ensure_get(customer_agreement_mrid, CustomerAgreement)
        pricing_structure = self._ensure_get(pricing_structure_mrid, PricingStructure)

        if (customer_agreement is not None) and (pricing_structure is not None):
            customer_agreement.add_pricing_structure(pricing_structure)

        return True

    def load_pricing_structure_tariff(self, table: TablePricingStructuresTariffs, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        pricing_structure_mrid = set_last_mrid(rs.get_string(table.pricing_structure_mrid.query_index))
        set_last_mrid(f"{pricing_structure_mrid}-to-UNKNOWN")

        tariff_mrid = rs.get_string(table.tariff_mrid.query_index)
        set_last_mrid(f"{pricing_structure_mrid}-to-{tariff_mrid}")

        pricing_structure = self._ensure_get(pricing_structure_mrid, PricingStructure)
        tariff = self._ensure_get(tariff_mrid, Tariff)

        if (pricing_structure is not None) and (tariff is not None):
            pricing_structure.add_tariff(tariff)

        return True
