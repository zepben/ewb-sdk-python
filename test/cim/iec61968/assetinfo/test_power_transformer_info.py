#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import lists, builds

from test.cim import extract_testing_args
from test.cim.collection_validator import validate_collection_unordered
from test.cim.iec61968.assets.test_asset_info import asset_info_kwargs, verify_asset_info_constructor_default, \
    verify_asset_info_constructor_kwargs, verify_asset_info_constructor_args, asset_info_args
from zepben.evolve import PowerTransformerInfo, TransformerTankInfo
from zepben.evolve.model.cim.iec61968.assetinfo.create_asset_info_components import create_power_transformer_info

power_transformer_info_kwargs = {
    **asset_info_kwargs,
    "transformer_tank_infos": lists(builds(TransformerTankInfo), max_size=2)
}

power_transformer_info_args = [*asset_info_args, [TransformerTankInfo(), TransformerTankInfo()]]


def test_power_transformer_info_constructor_default():
    pti = PowerTransformerInfo()
    pti2 = create_power_transformer_info()
    validate_default_power_transformer_info(pti)
    validate_default_power_transformer_info(pti2)


def validate_default_power_transformer_info(pti):
    verify_asset_info_constructor_default(pti)
    assert not list(pti.transformer_tank_infos)


@given(**power_transformer_info_kwargs)
def test_power_transformer_info_constructor_kwargs(transformer_tank_infos, **kwargs):
    args = extract_testing_args(locals())
    pti = PowerTransformerInfo(**args, **kwargs)
    validate_power_transformer_info_value(pti, **args, **kwargs)


@given(**power_transformer_info_kwargs)
def test_power_transformer_info_creator(transformer_tank_infos, **kwargs):
    args = extract_testing_args(locals())
    pti = create_power_transformer_info(**args, **kwargs)
    validate_power_transformer_info_value(pti, **args, **kwargs)


def validate_power_transformer_info_value(pti, transformer_tank_infos, **kwargs):
    verify_asset_info_constructor_kwargs(pti, **kwargs)
    assert list(pti.transformer_tank_infos) == transformer_tank_infos


def test_power_transformer_info_constructor_args():
    pti = PowerTransformerInfo(*power_transformer_info_args)

    verify_asset_info_constructor_args(pti)
    assert list(pti.transformer_tank_infos) == power_transformer_info_args[-1]


def test_transformer_tank_info_collection():
    validate_collection_unordered(PowerTransformerInfo,
                                  lambda mrid, _: TransformerTankInfo(mrid),
                                  PowerTransformerInfo.num_transformer_tank_infos,
                                  PowerTransformerInfo.get_transformer_tank_info,
                                  PowerTransformerInfo.transformer_tank_infos,
                                  PowerTransformerInfo.add_transformer_tank_info,
                                  PowerTransformerInfo.remove_transformer_tank_info,
                                  PowerTransformerInfo.clear_transformer_tank_infos)
