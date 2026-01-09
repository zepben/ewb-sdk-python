#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from unittest.mock import create_autospec, call

from capture_mock_sequence import CaptureMockSequence
from zepben.ewb import CustomerService, CustomerCimWriter, Customer, CustomerServiceWriter, CustomerDatabaseTables, generate_id


class TestCustomerServiceWriter:

    #
    # NOTE: We don't do an exhaustive test of saving objects as this is done via the schema test.
    #

    def setup_method(self):
        self.customer_service = CustomerService()
        self.cim_writer = create_autospec(CustomerCimWriter)
        self.customer_service_writer = CustomerServiceWriter(self.customer_service, create_autospec(CustomerDatabaseTables), self.cim_writer)

        self.cim_writer.save_customer.return_value = True

        self.mock_sequence = CaptureMockSequence(
            cim_writer=self.cim_writer,
        )

    def test_passes_objects_through_to_the_cim_writer(self):
        customer = Customer(mrid=generate_id())
        self.customer_service.add(customer)

        # NOTE: the save method will fail due to the relaxed mock returning false for all save operations,
        #       but a save should still be attempted on every object
        self.customer_service_writer.save()

        self.mock_sequence.verify_sequence([call.cim_writer.save_customer(customer)])
