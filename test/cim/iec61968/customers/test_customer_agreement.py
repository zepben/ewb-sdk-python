#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import lists, builds

from util import mrid_strategy
from zepben.ewb import CustomerAgreement, Customer, PricingStructure, generate_id

from cim.iec61968.common.test_agreement import agreement_kwargs, verify_agreement_constructor_default, verify_agreement_constructor_kwargs, \
    verify_agreement_constructor_args, agreement_args
from cim.private_collection_validator import validate_unordered

customer_agreement_kwargs = {
    **agreement_kwargs,
    "customer": builds(Customer, mrid=mrid_strategy),
    "pricing_structures": lists(builds(PricingStructure, mrid=mrid_strategy), max_size=2)
}

customer_agreement_args = [*agreement_args, Customer(mrid=generate_id()), [PricingStructure(mrid=generate_id())]]


def test_customer_agreement_constructor_default():
    ca = CustomerAgreement(mrid=generate_id())

    verify_agreement_constructor_default(ca)
    assert not ca.customer
    assert not list(ca.pricing_structures)


@given(**customer_agreement_kwargs)
def test_customer_agreement_constructor_kwargs(customer, pricing_structures, **kwargs):
    ca = CustomerAgreement(
        customer=customer,
        pricing_structures=pricing_structures,
        **kwargs
    )

    verify_agreement_constructor_kwargs(ca, **kwargs)
    assert ca.customer == customer
    assert list(ca.pricing_structures) == pricing_structures


def test_customer_agreement_constructor_args():
    ca = CustomerAgreement(*customer_agreement_args)

    verify_agreement_constructor_args(ca)
    assert [
        ca.customer,
        list(ca.pricing_structures)
    ] == customer_agreement_args[-2:]


def test_pricing_structures_collection():
    validate_unordered(
        CustomerAgreement,
        lambda mrid: PricingStructure(mrid),
        CustomerAgreement.pricing_structures,
        CustomerAgreement.num_pricing_structures,
        CustomerAgreement.get_pricing_structure,
        CustomerAgreement.add_pricing_structure,
        CustomerAgreement.remove_pricing_structure,
        CustomerAgreement.clear_pricing_structures
    )
