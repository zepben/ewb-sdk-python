#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given

from cim_creators import *
from services.common.translator.base_test_translator import validate_service_translations
from zepben.evolve.services.customer.customer_service_comparator import CustomerServiceComparator

T = TypeVar("T", bound=IdentifiedObject)

types_to_test = {

    ######################
    # IEC61968 CUSTOMERS #
    ######################

    "create_customer": create_customer(),
    "create_customer_agreement": create_customer_agreement(),
    "create_pricing_structure": create_pricing_structure(),
    "create_tariffs": create_tariffs(),

}


@given(**types_to_test)
def test_customer_service_translations(**kwargs):
    validate_service_translations(CustomerService, CustomerServiceComparator(), **kwargs)
