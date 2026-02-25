#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import text
from zepben.ewb.model.cim.iec61968.common.street_detail import StreetDetail

from cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE

street_detail_kwargs = {
    "building_name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "floor_identification": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "number": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "suite_number": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "type": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "display_address": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
}

street_detail_args = ["a", "b", "c", "d", "e", "f", "g"]


def test_street_detail_constructor_default():
    sd = StreetDetail()

    assert sd.building_name is None
    assert sd.floor_identification is None
    assert sd.name is None
    assert sd.number is None
    assert sd.suite_number is None
    assert sd.type is None
    assert sd.display_address is None


@given(**street_detail_kwargs)
def test_street_detail_constructor_kwargs(building_name, floor_identification, name, number, suite_number, type, display_address, **kwargs):
    assert not kwargs

    sd = StreetDetail(
        building_name=building_name,
        floor_identification=floor_identification,
        name=name,
        number=number,
        suite_number=suite_number,
        type=type,
        display_address=display_address
    )

    assert sd.building_name == building_name
    assert sd.floor_identification == floor_identification
    assert sd.name == name
    assert sd.number == number
    assert sd.suite_number == suite_number
    assert sd.type == type
    assert sd.display_address == display_address


def test_street_detail_constructor_args():
    sd = StreetDetail(*street_detail_args)

    assert street_detail_args[-7:] == [
        sd.building_name,
        sd.floor_identification,
        sd.name,
        sd.number,
        sd.suite_number,
        sd.type,
        sd.display_address
    ]


def test_all_fields_empty():
    assert StreetDetail().all_fields_empty()

    assert not StreetDetail(building_name="value").all_fields_empty()
    assert not StreetDetail(floor_identification="value").all_fields_empty()
    assert not StreetDetail(name="value").all_fields_empty()
    assert not StreetDetail(number="value").all_fields_empty()
    assert not StreetDetail(suite_number="value").all_fields_empty()
    assert not StreetDetail(type="value").all_fields_empty()
    assert not StreetDetail(display_address="value").all_fields_empty()
