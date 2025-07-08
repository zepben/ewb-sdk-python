#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import lists, builds, sampled_from, text

from cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE
from zepben.ewb import Customer, CustomerKind, CustomerAgreement

from cim.iec61968.common.test_organisation_role import organisation_role_kwargs, verify_organisation_role_constructor_default, \
    verify_organisation_role_constructor_kwargs, \
    verify_organisation_role_constructor_args, organisation_role_args
from cim.private_collection_validator import validate_unordered_1234567890

customer_kwargs = {
    **organisation_role_kwargs,
    "kind": sampled_from(CustomerKind),
    "special_need": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "customer_agreements": lists(builds(CustomerAgreement), max_size=2)
}

customer_args = [*organisation_role_args, CustomerKind.residential, "special", [CustomerAgreement()]]


def test_customer_constructor_default():
    c = Customer()

    verify_organisation_role_constructor_default(c)
    assert c.kind == CustomerKind.UNKNOWN
    assert c.special_need is None
    assert not list(c.agreements)


@given(**customer_kwargs)
def test_customer_constructor_kwargs(kind, special_need, customer_agreements, **kwargs):
    c = Customer(
        kind=kind,
        special_need=special_need,
        customer_agreements=customer_agreements,
        **kwargs
    )

    verify_organisation_role_constructor_kwargs(c, **kwargs)
    assert c.kind == kind
    assert c.special_need == special_need
    assert list(c.agreements) == customer_agreements


def test_customer_constructor_args():
    c = Customer(*customer_args)

    verify_organisation_role_constructor_args(c)
    assert customer_args[-3:] == [
        c.kind,
        c.special_need,
        list(c.agreements)
    ]


def test_customer_agreements_collection():
    validate_unordered_1234567890(
        Customer,
        lambda mrid: CustomerAgreement(mrid),
        Customer.agreements,
        Customer.num_agreements,
        Customer.get_agreement,
        Customer.add_agreement,
        Customer.remove_agreement,
        Customer.clear_agreements
    )
