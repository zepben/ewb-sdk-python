#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, sampled_from, integers

from cim.iec61968.assets.test_asset import asset_kwargs, verify_asset_constructor_default, \
    verify_asset_constructor_kwargs, verify_asset_constructor_args, asset_args
from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER
from zepben.evolve import Streetlight, Pole, StreetlightLampKind

streetlight_kwargs = {
    **asset_kwargs,
    "pole": builds(Pole),
    "light_rating": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "lamp_kind": sampled_from(StreetlightLampKind)
}

streetlight_args = [*asset_args, Pole(), 1, StreetlightLampKind.HIGH_PRESSURE_SODIUM]


def test_streetlight_constructor_default():
    p = Streetlight()

    verify_asset_constructor_default(p)
    assert not p.pole
    assert p.light_rating is None
    assert p.lamp_kind == StreetlightLampKind.UNKNOWN


@given(**streetlight_kwargs)
def test_streetlight_constructor_kwargs(pole, light_rating, lamp_kind, **kwargs):
    p = Streetlight(pole=pole,
                    light_rating=light_rating,
                    lamp_kind=lamp_kind,
                    **kwargs)

    verify_asset_constructor_kwargs(p, **kwargs)
    assert p.pole == pole
    assert p.light_rating == light_rating
    assert p.lamp_kind == lamp_kind


def test_streetlight_constructor_args():
    p = Streetlight(*streetlight_args)

    verify_asset_constructor_args(p)
    assert p.pole == streetlight_args[-3]
    assert p.light_rating == streetlight_args[-2]
    assert p.lamp_kind == streetlight_args[-1]
