#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import lists, builds

from test.cim.collection_validator import validate_collection_unordered
from test.cim.constructor_validation import ai_kwargs, verify_asset_info_constructor, verify_ai_args, ai_args
from zepben.evolve import TransformerEndInfo, TransformerTankInfo

tti_args = (*ai_args, [TransformerEndInfo("tei1"), TransformerEndInfo("tei1")])

tti_kwargs = {
    **ai_kwargs,
    "transformer_end_infos": lists(builds(TransformerEndInfo), max_size=2)
}


@given(**tti_kwargs)
def test_tti_constructor_kwargs(transformer_end_infos, **kwargs):
    tti = TransformerTankInfo(transformer_end_infos=transformer_end_infos)
    assert [tei for tei in tti.transformer_end_infos] == transformer_end_infos
    verify_asset_info_constructor(clazz=TransformerTankInfo, **kwargs)


def test_tti_constructor_args():
    tti = TransformerTankInfo(*tti_args)
    assert tti._transformer_end_infos == tti_args[-1]
    verify_ai_args(tti)


def test_transformer_end_info_collection():
    validate_collection_unordered(TransformerTankInfo,
                                  lambda mrid, _: TransformerEndInfo(mrid),
                                  TransformerTankInfo.num_transformer_end_infos,
                                  TransformerTankInfo.get_transformer_end_info,
                                  lambda it: TransformerTankInfo.transformer_end_infos.fget(it),
                                  TransformerTankInfo.add_transformer_end_info,
                                  TransformerTankInfo.remove_transformer_end_info,
                                  TransformerTankInfo.clear_transformer_end_infos)
