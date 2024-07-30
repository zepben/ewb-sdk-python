#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import builds, floats, integers, text

from cim.cim_creators import FLOAT_MIN, FLOAT_MAX, MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER, ALPHANUM, TEXT_MAX_SIZE
from cim.iec61968.assets.test_asset_info import asset_info_kwargs, verify_asset_info_constructor_default, \
    verify_asset_info_constructor_kwargs, verify_asset_info_constructor_args, asset_info_args
from zepben.evolve import CurrentTransformerInfo, Ratio

current_transformer_info_kwargs = {
    **asset_info_kwargs,
    "accuracy_class": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "accuracy_limit": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "core_count": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "ct_class": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "knee_point_voltage": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "max_ratio": builds(Ratio, floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
    "nominal_ratio": builds(Ratio, floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
    "primary_ratio": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "rated_current": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "secondary_fls_rating": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "secondary_ratio": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "usage": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
}

# noinspection PyArgumentList
current_transformer_info_args = [*asset_info_args, "a", 1.1, 2, "b", 3, Ratio(4.4, 5.5), Ratio(6.6, 7.7), 8.8, 9, 10, 11.11, "c"]


def test_current_transformer_info_constructor_default():
    cti = CurrentTransformerInfo()

    verify_asset_info_constructor_default(cti)
    assert cti.accuracy_class is None
    assert cti.accuracy_limit is None
    assert cti.core_count is None
    assert cti.ct_class is None
    assert cti.knee_point_voltage is None
    assert cti.max_ratio is None
    assert cti.nominal_ratio is None
    assert cti.primary_ratio is None
    assert cti.rated_current is None
    assert cti.secondary_fls_rating is None
    assert cti.secondary_ratio is None
    assert cti.usage is None


@given(**current_transformer_info_kwargs)
def test_current_transformer_info_constructor_kwargs(accuracy_class, accuracy_limit, core_count, ct_class, knee_point_voltage, max_ratio, nominal_ratio,
                                                     primary_ratio, rated_current, secondary_fls_rating, secondary_ratio, usage, **kwargs):
    cti = CurrentTransformerInfo(
        accuracy_class=accuracy_class,
        accuracy_limit=accuracy_limit,
        core_count=core_count,
        ct_class=ct_class,
        knee_point_voltage=knee_point_voltage,
        max_ratio=max_ratio,
        nominal_ratio=nominal_ratio,
        primary_ratio=primary_ratio,
        rated_current=rated_current,
        secondary_fls_rating=secondary_fls_rating,
        secondary_ratio=secondary_ratio,
        usage=usage,
        **kwargs
    )

    verify_asset_info_constructor_kwargs(cti, **kwargs)
    assert cti.accuracy_class == accuracy_class
    assert cti.accuracy_limit == accuracy_limit
    assert cti.core_count == core_count
    assert cti.ct_class == ct_class
    assert cti.knee_point_voltage == knee_point_voltage
    assert cti.max_ratio == max_ratio
    assert cti.nominal_ratio == nominal_ratio
    assert cti.primary_ratio == primary_ratio
    assert cti.rated_current == rated_current
    assert cti.secondary_fls_rating == secondary_fls_rating
    assert cti.secondary_ratio == secondary_ratio
    assert cti.usage == usage


def test_current_transformer_info_constructor_args():
    cti = CurrentTransformerInfo(*current_transformer_info_args)

    verify_asset_info_constructor_args(cti)
    assert cti.accuracy_class == current_transformer_info_args[-12]
    assert cti.accuracy_limit == current_transformer_info_args[-11]
    assert cti.core_count == current_transformer_info_args[-10]
    assert cti.ct_class == current_transformer_info_args[-9]
    assert cti.knee_point_voltage == current_transformer_info_args[-8]
    assert cti.max_ratio == current_transformer_info_args[-7]
    assert cti.nominal_ratio == current_transformer_info_args[-6]
    assert cti.primary_ratio == current_transformer_info_args[-5]
    assert cti.rated_current == current_transformer_info_args[-4]
    assert cti.secondary_fls_rating == current_transformer_info_args[-3]
    assert cti.secondary_ratio == current_transformer_info_args[-2]
    assert cti.usage == current_transformer_info_args[-1]
