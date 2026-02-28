#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import text

from cim.cim_creators import ALPHANUM
from zepben.ewb import TelephoneNumber


telephone_number_kwargs = {
    'area_code': text(alphabet=ALPHANUM),
    'city_code': text(alphabet=ALPHANUM),
    'country_code': text(alphabet=ALPHANUM),
    'dial_out': text(alphabet=ALPHANUM),
    'extension': text(alphabet=ALPHANUM),
    'international_prefix': text(alphabet=ALPHANUM),
    'local_number': text(alphabet=ALPHANUM),
    'is_primary': text(alphabet=ALPHANUM),
    'description': text(alphabet=ALPHANUM),
}


telephone_number_args = ['area_code', 'city_code', 'country_code', 'dial_out', 'extension',
                         'international_prefix', 'itu_phone', None, 'local_number',
                         'is_primary', 'description']


def test_telephone_number_constructor_default():
    t = TelephoneNumber()

    assert t.area_code is None
    assert t.city_code is None
    assert t.country_code is None
    assert t.dial_out is None
    assert t.extension is None
    assert t.international_prefix is None
    assert t.itu_phone is None
    assert t.partial_itu_phone is None
    assert t.local_number is None
    assert t.is_primary is None
    assert t.description is None


@given(**telephone_number_kwargs)
def test_telephone_number_constructor_kwargs(
    area_code,
    city_code,
    country_code,
    dial_out,
    extension,
    international_prefix,
    local_number,
    is_primary,
    description
):
    t = TelephoneNumber(
        area_code=area_code,
        city_code=city_code,
        country_code=country_code,
        dial_out=dial_out,
        extension=extension,
        international_prefix=international_prefix,
        local_number=local_number,
        is_primary=is_primary,
        description=description
    )


    assert t.area_code == area_code
    assert t.city_code == city_code
    assert t.country_code == country_code
    assert t.dial_out == dial_out
    assert t.extension == extension
    assert t.international_prefix == international_prefix
    assert t.local_number == local_number
    assert t.is_primary == is_primary
    assert t.description == description


def test_telephone_number_constructor_args():
    t = TelephoneNumber(*telephone_number_args)

    assert t.area_code == telephone_number_args[-11]
    assert t.city_code == telephone_number_args[-10]
    assert t.country_code == telephone_number_args[-9]
    assert t.dial_out == telephone_number_args[-8]
    assert t.extension == telephone_number_args[-7]
    assert t.international_prefix == telephone_number_args[-6]
    assert t.itu_phone == telephone_number_args[-5]
    assert t.local_number == telephone_number_args[-3]
    assert t.is_primary == telephone_number_args[-2]
    assert t.description == telephone_number_args[-1]
