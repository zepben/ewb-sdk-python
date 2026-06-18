#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from cim.fill_fields import telephone_number_kwargs
from hypothesis import given

from zepben.ewb import TelephoneNumber

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


@given(**telephone_number_kwargs())
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
