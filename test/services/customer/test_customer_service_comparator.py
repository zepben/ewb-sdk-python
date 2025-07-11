#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Type

from services.common.service_comparator_validator import ServiceComparatorValidator
from services.common.test_base_service_comparator import TestBaseServiceComparator
from zepben.ewb import CustomerService, Customer, CustomerKind, CustomerAgreement, PricingStructure, Tariff
from zepben.ewb.model.cim.iec61968.common.agreement import Agreement
from zepben.ewb.services.customer.customer_service_comparator import CustomerServiceComparator


class TestCustomerServiceComparator(TestBaseServiceComparator):
    validator = ServiceComparatorValidator(lambda: CustomerService(), lambda _: CustomerServiceComparator())

    def test_compare_customer(self):
        self._compare_organisation_role(Customer)

        self.validator.validate_property(Customer.kind, Customer, lambda _: CustomerKind.residential, lambda _: CustomerKind.commercialIndustrial)
        self.validator.validate_collection(
            Customer.agreements,
            Customer.add_agreement,
            Customer,
            lambda it: CustomerAgreement(mrid="1", customer=it),
            lambda it: CustomerAgreement(mrid="2", customer=it))
        # self.validator.validate_property(Customer.num_end_devices, Customer, lambda _: 1, lambda _: 2)  # Currently unused
        self.validator.validate_property(Customer.special_need, Customer, lambda _: "1", lambda _: "2")

    def test_compare_customer_agreement(self):
        self._compare_agreement(CustomerAgreement)

        self.validator.validate_property(CustomerAgreement.customer, CustomerAgreement, lambda _: Customer(mrid="1"), lambda _: Customer(mrid="2"))
        self.validator.validate_collection(
            CustomerAgreement.pricing_structures,
            CustomerAgreement.add_pricing_structure,
            CustomerAgreement,
            lambda _: PricingStructure(mrid="1"),
            lambda _: PricingStructure(mrid="2"))

    def test_compare_pricing_structure(self):
        self._compare_document(PricingStructure)

        self.validator.validate_collection(
            PricingStructure.tariffs,
            PricingStructure.add_tariff,
            PricingStructure,
            lambda _: Tariff(mrid="1"),
            lambda _: Tariff(mrid="2"))

    def test_compare_tariff(self):
        self._compare_document(Tariff)

    def _compare_agreement(self, creator: Type[Agreement]):
        self._compare_document(creator)
