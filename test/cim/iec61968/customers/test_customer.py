#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import lists, builds, sampled_from

from test.cim.extract_testing_args import extract_testing_args
from test.cim.collection_validator import validate_collection_unordered
from test.cim.iec61968.common.test_organisation_role import organisation_role_kwargs, verify_organisation_role_constructor_default, \
    verify_organisation_role_constructor_kwargs, \
    verify_organisation_role_constructor_args, organisation_role_args
from zepben.evolve import Customer, CustomerKind, CustomerAgreement
from zepben.evolve.model.cim.iec61968.customers.create_customers_components import create_customer

customer_kwargs = {
    **organisation_role_kwargs,
    "kind": sampled_from(CustomerKind),
    "customer_agreements": lists(builds(CustomerAgreement), max_size=2)
}

customer_args = [*organisation_role_args, CustomerKind.residential, [CustomerAgreement()]]


def test_customer_constructor_default():
    c = Customer()
    c2 = create_customer()
    validate_default_customer(c)
    validate_default_customer(c2)


def validate_default_customer(c):
    verify_organisation_role_constructor_default(c)
    assert c.kind == CustomerKind.UNKNOWN
    assert not list(c.agreements)


@given(**customer_kwargs)
def test_customer_constructor_kwargs(kind, customer_agreements, **kwargs):
    args = extract_testing_args(locals())
    c = Customer(**args, **kwargs)
    validate_customer_values(c, **args, **kwargs)


@given(**customer_kwargs)
def test_customer_creator(kind, customer_agreements, **kwargs):
    args = extract_testing_args(locals())
    c = create_customer(**args, **kwargs)
    validate_customer_values(c, **args, **kwargs)


def validate_customer_values(c, kind, customer_agreements, **kwargs):
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


def test_auto_two_way_connections_for_customer_constructor():
    ca = CustomerAgreement()
    c = create_customer(customer_agreements=[ca])

    assert ca.customer == c
