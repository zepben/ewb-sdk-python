#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import builds, floats, integers, text

from cim.cim_creators import FLOAT_MIN, FLOAT_MAX, MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER, ALPHANUM, TEXT_MAX_SIZE
from cim.iec61968.assets.test_asset_info import asset_info_kwargs, verify_asset_info_constructor_default, \
    verify_asset_info_constructor_kwargs, verify_asset_info_constructor_args, asset_info_args
from zepben.evolve import PotentialTransformerInfo, PowerTransformerInfo, Ratio

potential_transformer_info_kwargs = {
    **asset_info_kwargs,
    "accuracy_class": builds(PowerTransformerInfo),
    "nominal_ratio": builds(Ratio, floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
    "primary_ratio": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "pt_class": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "rated_voltage": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "secondary_ratio": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

# noinspection PyArgumentList
potential_transformer_info_args = [*asset_info_args, "a", Ratio(1.1, 2.2), 3.3, "b", 4, 5.5]


def test_potential_transformer_info_constructor_default():
    vti = PotentialTransformerInfo()

    verify_asset_info_constructor_default(vti)
    assert vti.accuracy_class is None
    assert vti.nominal_ratio is None
    assert vti.primary_ratio is None
    assert vti.pt_class is None
    assert vti.rated_voltage is None
    assert vti.secondary_ratio is None


@given(**potential_transformer_info_kwargs)
def test_potential_transformer_info_constructor_kwargs(accuracy_class, nominal_ratio, primary_ratio, pt_class, rated_voltage, secondary_ratio, **kwargs):
    vti = PotentialTransformerInfo(
        accuracy_class=accuracy_class,
        nominal_ratio=nominal_ratio,
        primary_ratio=primary_ratio,
        pt_class=pt_class,
        rated_voltage=rated_voltage,
        secondary_ratio=secondary_ratio,
        **kwargs
    )

    verify_asset_info_constructor_kwargs(vti, **kwargs)
    assert vti.accuracy_class == accuracy_class
    assert vti.nominal_ratio == nominal_ratio
    assert vti.primary_ratio == primary_ratio
    assert vti.pt_class == pt_class
    assert vti.rated_voltage == rated_voltage
    assert vti.secondary_ratio == secondary_ratio


def test_potential_transformer_info_constructor_args():
    vti = PotentialTransformerInfo(*potential_transformer_info_args)

    verify_asset_info_constructor_args(vti)
    assert vti.accuracy_class == potential_transformer_info_args[-6]
    assert vti.nominal_ratio == potential_transformer_info_args[-5]
    assert vti.primary_ratio == potential_transformer_info_args[-4]
    assert vti.pt_class == potential_transformer_info_args[-3]
    assert vti.rated_voltage == potential_transformer_info_args[-2]
    assert vti.secondary_ratio == potential_transformer_info_args[-1]
