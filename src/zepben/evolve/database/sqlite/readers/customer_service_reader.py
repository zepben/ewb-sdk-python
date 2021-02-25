#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import BaseServiceReader, TableOrganisations, TableCustomers, TableCustomerAgreements, TablePricingStructures, TableTariffs, \
    TableCustomerAgreementsPricingStructures, TablePricingStructuresTariffs, CustomerCIMReader

__all__ = ["CustomerServiceReader"]


class CustomerServiceReader(BaseServiceReader):
    """
    Class for reading a `CustomerService` from the database.
    """

    def load(self, reader: CustomerCIMReader) -> bool:
        status = self.load_name_types(reader)

        status = status and self._load_each(TableOrganisations, "organisations", reader.load_organisation)
        status = status and self._load_each(TableCustomers, "customers", reader.load_customer)
        status = status and self._load_each(TableCustomerAgreements, "customer agreements", reader.load_customer_agreement)
        status = status and self._load_each(TablePricingStructures, "pricing structures", reader.load_pricing_structure)
        status = status and self._load_each(TableTariffs, "tariffs", reader.load_tariff)
        status = status and self._load_each(
            TableCustomerAgreementsPricingStructures,
            "customer agreement to pricing structure associations",
            reader.load_customer_agreement_pricing_structure
        )
        status = status and self._load_each(TablePricingStructuresTariffs, "pricing structure to tariff associations", reader.load_pricing_structure_tariff)

        status = status and self.load_names(reader)

        return status
