#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import lists, builds
from zepben.ewb import TransformerTankInfo, TransformerEndInfo, PowerTransformerInfo

from cim.iec61968.assets.test_asset_info import asset_info_kwargs, verify_asset_info_constructor_default, \
    verify_asset_info_constructor_kwargs, verify_asset_info_constructor_args, asset_info_args
from cim.private_collection_validator import validate_unordered_1234567890

transformer_tank_info_kwargs = {
    **asset_info_kwargs,
    "power_transformer_info": builds(PowerTransformerInfo),
    "transformer_end_infos": lists(builds(TransformerEndInfo), max_size=2)
}

transformer_tank_info_args = [*asset_info_args, PowerTransformerInfo(), [TransformerEndInfo(), TransformerEndInfo()]]


def test_transformer_tank_info_constructor_default():
    tti = TransformerTankInfo()

    verify_asset_info_constructor_default(tti)
    assert not list(tti.transformer_end_infos)


@given(**transformer_tank_info_kwargs)
def test_transformer_tank_info_constructor_kwargs(power_transformer_info, transformer_end_infos, **kwargs):
    tti = TransformerTankInfo(power_transformer_info=power_transformer_info, transformer_end_infos=transformer_end_infos, **kwargs)

    verify_asset_info_constructor_kwargs(tti, **kwargs)
    assert list(tti.transformer_end_infos) == transformer_end_infos


from pytest import mark
@mark.skip(reason="Args are deprecated")
def test_transformer_tank_info_constructor_args():
    tti = TransformerTankInfo(*transformer_tank_info_args)

    verify_asset_info_constructor_args(tti)
    assert transformer_tank_info_args[-1:] == [
        list(tti.transformer_end_infos)
    ]


def test_transformer_tank_info_collection():
    validate_unordered_1234567890(
        TransformerTankInfo,
        lambda mrid: TransformerEndInfo(mrid),
        TransformerTankInfo.transformer_end_infos,
        TransformerTankInfo.num_transformer_end_infos,
        TransformerTankInfo.get_transformer_end_info,
        TransformerTankInfo.add_transformer_end_info,
        TransformerTankInfo.remove_transformer_end_info,
        TransformerTankInfo.clear_transformer_end_infos
    )
