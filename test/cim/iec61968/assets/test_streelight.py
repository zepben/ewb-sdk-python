#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, sampled_from, integers

from test.cim.extract_testing_args import extract_testing_args
from test.cim.iec61968.assets.test_asset import asset_kwargs, verify_asset_constructor_default, \
    verify_asset_constructor_kwargs, verify_asset_constructor_args, asset_args
from test.cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER
from zepben.evolve import Streetlight, Pole, StreetlightLampKind
from zepben.evolve.model.cim.iec61968.assets.create_assets_components import create_streetlight

streetlight_kwargs = {
    **asset_kwargs,
    "pole": builds(Pole),
    "light_rating": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "lamp_kind": sampled_from(StreetlightLampKind)
}

streetlight_args = [*asset_args, Pole(), 1, StreetlightLampKind.HIGH_PRESSURE_SODIUM]


def test_streetlight_constructor_default():
    sl = Streetlight()
    sl2 = create_streetlight()
    validate_default_streetlight(sl)
    validate_default_streetlight(sl2)


def validate_default_streetlight(sl):
    verify_asset_constructor_default(sl)
    assert not sl.pole
    assert sl.light_rating is None
    assert sl.lamp_kind == StreetlightLampKind.UNKNOWN


@given(**streetlight_kwargs)
def test_streetlight_constructor_kwargs(pole, light_rating, lamp_kind, **kwargs):
    args = extract_testing_args(locals())
    sl = Streetlight(**args, **kwargs)
    validate_streetlight_values(sl, **args, **kwargs)


@given(**streetlight_kwargs)
def test_streetlight_creator(pole, light_rating, lamp_kind, **kwargs):
    args = extract_testing_args(locals())
    sl = create_streetlight(**args, **kwargs)
    validate_streetlight_values(sl, **args, **kwargs)


def validate_streetlight_values(sl, pole, light_rating, lamp_kind, **kwargs):
    verify_asset_constructor_kwargs(sl, **kwargs)
    assert sl.pole == pole
    assert sl.light_rating == light_rating
    assert sl.lamp_kind == lamp_kind


def test_streetlight_constructor_args():
    sl = Streetlight(*streetlight_args)

    verify_asset_constructor_args(sl)
    assert sl.pole == streetlight_args[-3]
    assert sl.light_rating == streetlight_args[-2]
    assert sl.lamp_kind == streetlight_args[-1]


def test_auto_two_way_connections_for_street_light_constructor():
    p = Pole()
    s = create_streetlight(pole=p)

    assert p.get_streetlight(s.mrid) == s
