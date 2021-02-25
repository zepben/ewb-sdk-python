#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import CustomerCIMWriter, Organisation, Customer, CustomerAgreement, PricingStructure, Tariff, CustomerService
from zepben.evolve.database.sqlite.writers.base_service_writer import BaseServiceWriter

__all__ = ["CustomerServiceWriter"]


class CustomerServiceWriter(BaseServiceWriter):

    def save(self, service: CustomerService, writer: CustomerCIMWriter) -> bool:
        status = super(CustomerServiceWriter, self).save(service, writer)

        for obj in service.objects(Organisation):
            status = status and self.try_save_common(obj, writer.save_organisation)
        for obj in service.objects(Customer):
            status = status and self.validate_save(obj, writer.save_customer)
        for obj in service.objects(CustomerAgreement):
            status = status and self.validate_save(obj, writer.save_customer_agreement)
        for obj in service.objects(PricingStructure):
            status = status and self.validate_save(obj, writer.save_pricing_structure)
        for obj in service.objects(Tariff):
            status = status and self.validate_save(obj, writer.save_tariff)

        return status
