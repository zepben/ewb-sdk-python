#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import lists, builds
from zepben.ewb import PowerTransformerInfo, TransformerTankInfo

from cim.iec61968.assets.test_asset_info import asset_info_kwargs, verify_asset_info_constructor_default, \
    verify_asset_info_constructor_kwargs, verify_asset_info_constructor_args, asset_info_args
from cim.private_collection_validator import validate_unordered_1234567890

power_transformer_info_kwargs = {
    **asset_info_kwargs,
    "transformer_tank_infos": lists(builds(TransformerTankInfo), max_size=2)
}

power_transformer_info_args = [*asset_info_args, [TransformerTankInfo(), TransformerTankInfo()]]


def test_power_transformer_info_constructor_default():
    pti = PowerTransformerInfo()

    verify_asset_info_constructor_default(pti)
    assert not list(pti.transformer_tank_infos)


@given(**power_transformer_info_kwargs)
def test_power_transformer_info_constructor_kwargs(transformer_tank_infos, **kwargs):
    pti = PowerTransformerInfo(transformer_tank_infos=transformer_tank_infos, **kwargs)

    verify_asset_info_constructor_kwargs(pti, **kwargs)
    assert list(pti.transformer_tank_infos) == transformer_tank_infos


def test_power_transformer_info_constructor_args():
    pti = PowerTransformerInfo(*power_transformer_info_args)

    verify_asset_info_constructor_args(pti)
    assert power_transformer_info_args[-1:] == [
        list(pti.transformer_tank_infos)
    ]


def test_transformer_tank_info_collection():
    validate_unordered_1234567890(
        PowerTransformerInfo,
        lambda mrid: TransformerTankInfo(mrid),
        PowerTransformerInfo.transformer_tank_infos,
        PowerTransformerInfo.num_transformer_tank_infos,
        PowerTransformerInfo.get_transformer_tank_info,
        PowerTransformerInfo.add_transformer_tank_info,
        PowerTransformerInfo.remove_transformer_tank_info,
        PowerTransformerInfo.clear_transformer_tank_infos
    )
