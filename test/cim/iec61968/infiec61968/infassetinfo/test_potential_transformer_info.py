#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given

from cim.fill_fields import potential_transformer_info_kwargs
from cim.iec61968.assets.test_asset_info import verify_asset_info_constructor_default, \
    verify_asset_info_constructor_kwargs, verify_asset_info_constructor_args, asset_info_args
from zepben.ewb import PotentialTransformerInfo, Ratio, generate_id

# noinspection PyArgumentList
potential_transformer_info_args = [*asset_info_args, "a", Ratio(1.1, 2.2), 3.3, "b", 4, 5.5]


def test_potential_transformer_info_constructor_default():
    vti = PotentialTransformerInfo(mrid=generate_id())

    verify_asset_info_constructor_default(vti)
    assert vti.accuracy_class is None
    assert vti.nominal_ratio is None
    assert vti.primary_ratio is None
    assert vti.pt_class is None
    assert vti.rated_voltage is None
    assert vti.secondary_ratio is None


@given(**potential_transformer_info_kwargs())
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
    assert potential_transformer_info_args[-6:] == [
        vti.accuracy_class,
        vti.nominal_ratio,
        vti.primary_ratio,
        vti.pt_class,
        vti.rated_voltage,
        vti.secondary_ratio
    ]
