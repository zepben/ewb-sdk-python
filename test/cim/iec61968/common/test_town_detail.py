#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import text
from zepben.ewb.model.cim.iec61968.common.town_detail import TownDetail

from cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE

town_detail_kwargs = {
    "name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "state_or_province": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
}

town_detail_args = ["a", "b"]


def test_town_detail_constructor_default():
    td = TownDetail()

    assert td.name is None
    assert td.state_or_province is None


@given(**town_detail_kwargs)
def test_town_detail_constructor_kwargs(name, state_or_province, **kwargs):
    assert not kwargs

    td = TownDetail(name=name, state_or_province=state_or_province)

    assert td.name == name
    assert td.state_or_province == state_or_province


def test_town_detail_constructor_args():
    td = TownDetail(*town_detail_args)

    assert town_detail_args[-2:] == [
        td.name,
        td.state_or_province
    ]


def test_all_fields_empty():
    assert TownDetail().all_fields_null_or_empty()
    assert TownDetail("", "").all_fields_null_or_empty()

    assert not TownDetail(name="value").all_fields_null_or_empty()
    assert not TownDetail(state_or_province="value").all_fields_null_or_empty()
