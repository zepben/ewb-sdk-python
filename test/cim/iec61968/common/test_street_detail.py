#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import text

from cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE
from zepben.evolve import StreetDetail

street_detail_kwargs = {
    "building_name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "floor_identification": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "number": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "suite_number": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "street_type": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "display_address": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
}

street_detail_args = ["a", "b", "c", "d", "e", "f", "g"]


def test_street_detail_constructor_default():
    sd = StreetDetail()

    assert sd.building_name == ""
    assert sd.floor_identification == ""
    assert sd.name == ""
    assert sd.number == ""
    assert sd.suite_number == ""
    assert sd.type == ""
    assert sd.display_address == ""


@given(**street_detail_kwargs)
def test_street_detail_constructor_kwargs(building_name, floor_identification, name, number, suite_number, street_type, display_address, **kwargs):
    assert not kwargs

    # noinspection PyArgumentList
    sd = StreetDetail(
        building_name=building_name,
        floor_identification=floor_identification,
        name=name,
        number=number,
        suite_number=suite_number,
        type=street_type,
        display_address=display_address
    )

    assert sd.building_name == building_name
    assert sd.floor_identification == floor_identification
    assert sd.name == name
    assert sd.number == number
    assert sd.suite_number == suite_number
    assert sd.type == street_type
    assert sd.display_address == display_address


def test_street_detail_constructor_args():
    # noinspection PyArgumentList
    sd = StreetDetail(*street_detail_args)

    assert sd.building_name == street_detail_args[-7]
    assert sd.floor_identification == street_detail_args[-6]
    assert sd.name == street_detail_args[-5]
    assert sd.number == street_detail_args[-4]
    assert sd.suite_number == street_detail_args[-3]
    assert sd.type == street_detail_args[-2]
    assert sd.display_address == street_detail_args[-1]


# noinspection PyArgumentList
def test_all_fields_empty():
    assert StreetDetail().all_fields_empty()

    assert not StreetDetail(building_name="value").all_fields_empty()
    assert not StreetDetail(floor_identification="value").all_fields_empty()
    assert not StreetDetail(name="value").all_fields_empty()
    assert not StreetDetail(number="value").all_fields_empty()
    assert not StreetDetail(suite_number="value").all_fields_empty()
    assert not StreetDetail(type="value").all_fields_empty()
    assert not StreetDetail(display_address="value").all_fields_empty()
