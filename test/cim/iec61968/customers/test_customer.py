#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import lists, builds, sampled_from

from cim.collection_validator import validate_collection_unordered
from cim.iec61968.common.test_organisation_role import organisation_role_kwargs, verify_organisation_role_constructor_default, \
    verify_organisation_role_constructor_kwargs, \
    verify_organisation_role_constructor_args, organisation_role_args
from zepben.evolve import Customer, CustomerKind, CustomerAgreement

customer_kwargs = {
    **organisation_role_kwargs,
    "kind": sampled_from(CustomerKind),
    "customer_agreements": lists(builds(CustomerAgreement), max_size=2)
}

customer_args = [*organisation_role_args, CustomerKind.residential, [CustomerAgreement()]]


def test_customer_constructor_default():
    c = Customer()

    verify_organisation_role_constructor_default(c)
    assert c.kind == CustomerKind.UNKNOWN
    assert not list(c.agreements)


@given(**customer_kwargs)
def test_customer_constructor_kwargs(kind, customer_agreements, **kwargs):
    c = Customer(
        kind=kind,
        customer_agreements=customer_agreements,
        **kwargs
    )

    verify_organisation_role_constructor_kwargs(c, **kwargs)
    assert c.kind == kind
    assert list(c.agreements) == customer_agreements


def test_customer_constructor_args():
    c = Customer(*customer_args)

    verify_organisation_role_constructor_args(c)
    assert c.kind == customer_args[-2]
    assert list(c.agreements) == customer_args[-1]


def test_customer_agreements_collection():
    validate_collection_unordered(Customer,
                                  lambda mrid, _: CustomerAgreement(mrid),
                                  Customer.num_agreements,
                                  Customer.get_agreement,
                                  Customer.agreements,
                                  Customer.add_agreement,
                                  Customer.remove_agreement,
                                  Customer.clear_agreements)
