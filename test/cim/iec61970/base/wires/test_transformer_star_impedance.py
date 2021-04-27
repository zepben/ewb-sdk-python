#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import floats, builds

from test.cim_creators import FLOAT_MIN, FLOAT_MAX
from test.cim.constructor_validation import io_kwargs, io_args, verify_io_args, verify_identifed_object_constructor
from zepben.evolve import TransformerStarImpedance, TransformerEndInfo

tsi_args = (
    *io_args, 0.0, 1.0, 2.0, 3.0, TransformerEndInfo(mrid="test_transformer_end_info")
)

tsi_kwargs = {
    **io_kwargs,
    "r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "r0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "transformer_end_info": builds(TransformerEndInfo)
}


def test_tsi_constructor_args():
    tsi = TransformerStarImpedance(*tsi_args)
    assert tsi.transformer_end_info == tsi_args[-1]
    assert tsi.x0 == tsi_args[-2]
    assert tsi.x == tsi_args[-3]
    assert tsi.r0 == tsi_args[-4]
    assert tsi.r == tsi_args[-5]
    verify_io_args(tsi)


@given(**tsi_kwargs)
def test_tsi_constructor_kwargs(r, r0, x, x0, transformer_end_info, **kwargs):
    tsi = TransformerStarImpedance()
    assert tsi.r == 0.0
    assert tsi.r0 == 0.0
    assert tsi.x == 0.0
    assert tsi.x0 == 0.0
    assert tsi.transformer_end_info is None

    tsi = TransformerStarImpedance(r=r, r0=r0, x=x, x0=x0, transformer_end_info=transformer_end_info)
    assert tsi.r == r
    assert tsi.r0 == r0
    assert tsi.x == x
    assert tsi.x0 == x0
    assert tsi.transformer_end_info is transformer_end_info

    verify_identifed_object_constructor(clazz=TransformerStarImpedance, **kwargs)


