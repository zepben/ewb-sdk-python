#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import text
from test.cim import extract_testing_args
from test.cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE
from test.cim.extract_testing_args import extract_testing_args
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
    validate_default_town_detail(td)
    validate_default_town_detail(td2)


def validate_default_town_detail(td):
    assert td.name is None
    assert td.state_or_province is None


# noinspection PyArgumentList
@given(**town_detail_kwargs)
def test_town_detail_constructor_kwargs(name, state_or_province, **kwargs):
    args = extract_testing_args(locals())
    assert not kwargs

    td = TownDetail(**args)
    validate_town_detail_values(td, **args)


@given(**town_detail_kwargs)
def test_town_detail_creator(name, state_or_province, **kwargs):
    args = extract_testing_args(locals())
    assert not kwargs

    td = create_town_detail(**args)
    validate_town_detail_values(td, **args)


def validate_town_detail_values(td, name, state_or_province):
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

