#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import booleans, text

from cim.cim_creators import ALPHANUM
from zepben.ewb import ElectronicAddress


electronic_address_kwargs = {
    'is_primary': booleans(),
    'description': text(alphabet=ALPHANUM),
    'email1': text(alphabet=ALPHANUM),
}


electronic_address_args = ['email1', False, 'descript']


def test_electronic_address_constructor_default():
    e = ElectronicAddress()

    assert e.is_primary is None
    assert e.description is None
    assert e.email1 is None


@given(**electronic_address_kwargs)
def test_electronic_address_constructor_kwargs(is_primary, description, email1):
    e = ElectronicAddress(is_primary=is_primary, description=description, email1=email1)

    assert e.is_primary == is_primary
    assert e.description == description
    assert e.email1 == email1


def test_electronic_address_constructor_args():
    e = ElectronicAddress(*electronic_address_args)

    assert e.email1 == electronic_address_args[-3]
    assert e.is_primary == electronic_address_args[-2]
    assert e.description == electronic_address_args[-1]
