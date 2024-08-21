#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["CustomerServiceWriter"]

from zepben.evolve.database.sqlite.common.base_service_writer import BaseServiceWriter
from zepben.evolve.database.sqlite.customer.customer_cim_writer import CustomerCimWriter
from zepben.evolve.database.sqlite.customer.customer_database_tables import CustomerDatabaseTables
from zepben.evolve.model.cim.iec61968.common.organisation import Organisation
from zepben.evolve.model.cim.iec61968.customers.customer import Customer
from zepben.evolve.model.cim.iec61968.customers.customer_agreement import CustomerAgreement
from zepben.evolve.model.cim.iec61968.customers.pricing_structure import PricingStructure
from zepben.evolve.model.cim.iec61968.customers.tariff import Tariff
from zepben.evolve.services.customer.customers import CustomerService


class CustomerServiceWriter(BaseServiceWriter):
    """
    A class for writing a `CustomerService` into the database.

    :param service: The `CustomerService` to save to the database.
    :param database_tables: The `CustomerDatabaseTables` to add to the database.
    """

    def __init__(
        self,
        service: CustomerService,
        database_tables: CustomerDatabaseTables,
        writer: CustomerCimWriter = None
    ):
        writer = writer if writer is not None else CustomerCimWriter(database_tables)
        super().__init__(service, writer)

        # This is not strictly necessary, it is just to update the type of the writer. It could be done with a generic
        # on the base class which looks like it works, but that actually silently breaks code insight and completion
        self._writer = writer

    def _do_save(self) -> bool:
        return all([
            self._save_each_object(Organisation, self._writer.save_organisation),
            self._save_each_object(Customer, self._writer.save_customer),
            self._save_each_object(CustomerAgreement, self._writer.save_customer_agreement),
            self._save_each_object(PricingStructure, self._writer.save_pricing_structure),
            self._save_each_object(Tariff, self._writer.save_tariff)
        ])
