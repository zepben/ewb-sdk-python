#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import text

from test.cim_creators import ALPHANUM, TEXT_MAX_SIZE
from zepben.evolve import StreetDetail

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
    sa = StreetDetail()

    assert sa.building_name == ""
    assert sa.floor_identification == ""
    assert sa.name == ""
    assert sa.number == ""
    assert sa.suite_number == ""
    assert sa.type == ""
    assert sa.display_address == ""


@given(**street_detail_kwargs)
def test_street_detail_constructor_kwargs(building_name, floor_identification, name, number, suite_number, street_type, display_address, **kwargs):
    assert not kwargs

    # noinspection PyArgumentList
    sa = StreetDetail(
        building_name=building_name,
        floor_identification=floor_identification,
        name=name,
        number=number,
        suite_number=suite_number,
        type=street_type,
        display_address=display_address
    )

    assert sa.building_name == building_name
    assert sa.floor_identification == floor_identification
    assert sa.name == name
    assert sa.number == number
    assert sa.suite_number == suite_number
    assert sa.type == street_type
    assert sa.display_address == display_address


def test_street_detail_constructor_args():
    # noinspection PyArgumentList
    sa = StreetDetail(*street_detail_args)

    assert sa.building_name == street_detail_args[-7]
    assert sa.floor_identification == street_detail_args[-6]
    assert sa.name == street_detail_args[-5]
    assert sa.number == street_detail_args[-4]
    assert sa.suite_number == street_detail_args[-3]
    assert sa.type == street_detail_args[-2]
    assert sa.display_address == street_detail_args[-1]
