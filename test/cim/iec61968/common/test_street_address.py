#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import builds, text
from test.cim import extract_testing_args
from test.cim.extract_testing_args import extract_testing_args
from test.cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE
from zepben.evolve import StreetAddress, TownDetail, StreetDetail
from zepben.evolve.model.cim.iec61968.common.create_common_components import create_street_address


street_address_kwargs = {
    "postal_code": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "town_detail": builds(TownDetail),
    "po_box": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "street_detail": builds(StreetDetail)
}

street_address_args = ["a", TownDetail(), "b", StreetDetail()]


def test_street_address_constructor_default():
    sa = StreetAddress()
    sa2 = create_street_address()
    validate_default_street_address(sa)
    validate_default_street_address(sa2)


def validate_default_street_address(sa):
    assert sa.postal_code == ""
    assert sa.po_box == ""
    assert not sa.town_detail
    assert not sa.street_detail


# noinspection PyArgumentList
@given(**street_address_kwargs)
def test_street_address_constructor_kwargs(postal_code, town_detail, po_box, street_detail, **kwargs):
    args = extract_testing_args(locals())
    assert not kwargs

    sa = StreetAddress(**args)
    validate_street_address_values(sa, **args)


@given(**street_address_kwargs)
def test_street_address_creator(postal_code, town_detail, po_box, street_detail, **kwargs):
    args = extract_testing_args(locals())
    assert not kwargs

    sa = create_street_address(**args)
    validate_street_address_values(sa, **args)


def validate_street_address_values(sa, postal_code, po_box, street_detail, town_detail):
    assert sa.postal_code == postal_code
    assert sa.town_detail == town_detail
    assert sa.po_box == po_box
    assert sa.street_detail == street_detail


def test_street_address_constructor_args():
    # noinspection PyArgumentList
    sa = StreetAddress(*street_address_args)

    assert sa.postal_code == street_address_args[-4]
    assert sa.town_detail == street_address_args[-3]
    assert sa.po_box == street_address_args[-2]
    assert sa.street_detail == street_address_args[-1]
