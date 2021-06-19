#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import BaseServiceComparator, ObjectDifference, Customer, CustomerAgreement, PricingStructure, Tariff


#
# NOTE: The functions below are accessed by reflection rather than directly. Make sure you check the code coverage
#       to ensure they are covered correctly.
#
class CustomerServiceComparator(BaseServiceComparator):
    """
    Compare the objects supported by the customer service.
    """

    def _compare_agreement(self, diff: ObjectDifference) -> ObjectDifference:
        return self._compare_document(diff)

    def _compare_customer(self, source: Customer, target: Customer) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(diff, Customer.kind)
        self._compare_id_reference_collections(diff, Customer.agreements)

        return self._compare_organisation_role(diff)

    def _compare_customer_agreement(self, source: CustomerAgreement, target: CustomerAgreement) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_references(diff, CustomerAgreement.customer)
        self._compare_id_reference_collections(diff, CustomerAgreement.pricing_structures)

        return self._compare_agreement(diff)

    def _compare_pricing_structure(self, source: PricingStructure, target: PricingStructure) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_reference_collections(diff, PricingStructure.tariffs)

        return self._compare_document(diff)

    def _compare_tariff(self, source: Tariff, target: Tariff) -> ObjectDifference:
        return self._compare_document(ObjectDifference(source, target))
