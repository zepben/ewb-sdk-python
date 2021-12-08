#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import lists, builds

from test.cim.extract_testing_args import extract_testing_args
from test.cim.collection_validator import validate_collection_unordered
from test.cim.iec61968.assets.test_asset_info import asset_info_kwargs, verify_asset_info_constructor_default, \
    verify_asset_info_constructor_kwargs, verify_asset_info_constructor_args, asset_info_args
from zepben.evolve import TransformerTankInfo, TransformerEndInfo, PowerTransformerInfo
from zepben.evolve.model.cim.iec61968.assetinfo.create_asset_info_components import create_transformer_tank_info

transformer_tank_info_kwargs = {
    **asset_info_kwargs,
    "power_transformer_info": builds(PowerTransformerInfo),
    "transformer_end_infos": lists(builds(TransformerEndInfo), max_size=2)
}

transformer_tank_info_args = [*asset_info_args, PowerTransformerInfo(), [TransformerEndInfo(), TransformerEndInfo()]]


def test_transformer_tank_info_constructor_default():
    tti = TransformerTankInfo()
    tti2 = create_transformer_tank_info()
    validate_default_transformer_tank_info(tti)
    validate_default_transformer_tank_info(tti2)


def validate_default_transformer_tank_info(tti):
    verify_asset_info_constructor_default(tti)
    assert not list(tti.transformer_end_infos)


@given(**transformer_tank_info_kwargs)
def test_transformer_tank_info_constructor_kwargs(power_transformer_info, transformer_end_infos, **kwargs):
    args = extract_testing_args(locals())
    tti = TransformerTankInfo(**args, **kwargs)
    validate_transformer_tank_info_values(tti, **args, **kwargs)


@given(**transformer_tank_info_kwargs)
def test_transformer_tank_info_creator(transformer_end_infos, **kwargs):
    args = extract_testing_args(locals())
    tti = create_transformer_tank_info(**args, **kwargs)
    validate_transformer_tank_info_values(tti, **args, **kwargs)


def validate_transformer_tank_info_values(tti, transformer_end_infos, **kwargs):
    verify_asset_info_constructor_kwargs(tti, **kwargs)
    assert list(tti.transformer_end_infos) == transformer_end_infos


def test_transformer_tank_info_constructor_args():
    tti = TransformerTankInfo(*transformer_tank_info_args)

    verify_asset_info_constructor_args(tti)
    assert list(tti.transformer_end_infos) == transformer_tank_info_args[-1]


def test_transformer_tank_info_collection():
    # noinspection PyArgumentList
    validate_collection_unordered(TransformerTankInfo,
                                  lambda mrid, _: TransformerEndInfo(mrid),
                                  TransformerTankInfo.num_transformer_end_infos,
                                  TransformerTankInfo.get_transformer_end_info,
                                  TransformerTankInfo.transformer_end_infos,
                                  TransformerTankInfo.add_transformer_end_info,
                                  TransformerTankInfo.remove_transformer_end_info,
                                  TransformerTankInfo.clear_transformer_end_infos)
