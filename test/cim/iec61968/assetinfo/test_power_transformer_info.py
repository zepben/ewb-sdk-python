#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given

from test.cim.constructor_validation import *
from zepben.evolve import PowerTransformerInfo, TransformerTankInfo
from test.cim.collection_validator import validate_collection_unordered

pti_args = (
    *ai_args,
    [TransformerTankInfo("tti1"), TransformerTankInfo("tti2")]
)

pti_kwargs = {
    **ai_kwargs,
    "transformer_tank_infos": lists(builds(TransformerTankInfo), max_size=2)
}


@given(**pti_kwargs)
def test_pti_constructor_kwargs(transformer_tank_infos, **kwargs):
    pti = PowerTransformerInfo(transformer_tank_infos=transformer_tank_infos)
    assert [tti for tti in pti.transformer_tank_infos] == transformer_tank_infos
    verify_asset_info_constructor(clazz=PowerTransformerInfo, **kwargs)


def test_pti_constructor_args():
    pti = PowerTransformerInfo(*pti_args)
    assert pti._transformer_tank_infos == pti_args[-1]
    verify_ai_args(pti)


def test_transformer_tank_info_collection():
    validate_collection_unordered(PowerTransformerInfo,
                                  lambda mrid, _: TransformerTankInfo(mrid),
                                  PowerTransformerInfo.num_transformer_tank_infos,
                                  PowerTransformerInfo.get_transformer_tank_info,
                                  lambda it: PowerTransformerInfo.transformer_tank_infos.fget(it),
                                  PowerTransformerInfo.add_transformer_tank_info,
                                  PowerTransformerInfo.remove_transformer_tank_info,
                                  PowerTransformerInfo.clear_transformer_tank_infos)
