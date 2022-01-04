#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import text, data
from test.cim.common_testing_functions import verify
from test.cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE
from zepben.evolve import TownDetail
from zepben.evolve.model.cim.iec61968.common.create_common_components import create_town_detail

town_detail_kwargs = {
    "name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "state_or_province": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
}

town_detail_args = ["a", "b"]


def test_town_detail_constructor_default():
    td = TownDetail()
    td2 = create_town_detail()
    verify_default_town_detail(td)
    verify_default_town_detail(td2)


def verify_default_town_detail(td):
    assert td.name is None
    assert td.state_or_province is None


# noinspection PyShadowingNames
@given(data())
def test_town_detail_constructor_kwargs(data):
    verify(
        [TownDetail, create_town_detail],
        data, town_detail_kwargs, verify_town_detail_values
    )


def verify_town_detail_values(td, name, state_or_province):
    assert td.name == name
    assert td.state_or_province == state_or_province


def test_town_detail_constructor_args():
    # noinspection PyArgumentList
    td = TownDetail(*town_detail_args)

    assert td.name == town_detail_args[-2]
    assert td.state_or_province == town_detail_args[-1]


# noinspection PyArgumentList
def test_all_fields_empty():
    assert TownDetail().all_fields_null_or_empty()
    assert TownDetail("", "").all_fields_null_or_empty()

    assert not TownDetail(name="value").all_fields_null_or_empty()
    assert not TownDetail(state_or_province="value").all_fields_null_or_empty()

