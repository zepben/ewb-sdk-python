#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import floats

from cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from cim.iec61968.assets.test_asset_info import asset_info_kwargs, asset_info_args, verify_asset_info_constructor_default, verify_asset_info_constructor_kwargs, \
    verify_asset_info_constructor_args
from zepben.evolve import SwitchInfo

switch_info_kwargs = {
    **asset_info_kwargs,
    "rated_interrupting_time": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

switch_info_args = [*asset_info_args, 1.1]


def test_switch_info_constructor_default():
    si = SwitchInfo()

    verify_asset_info_constructor_default(si)
    assert si.rated_interrupting_time is None


@given(**switch_info_kwargs)
def test_switch_info_constructor_kwargs(rated_interrupting_time, **kwargs):
    si = SwitchInfo(
        rated_interrupting_time=rated_interrupting_time,
        **kwargs
    )

    verify_asset_info_constructor_kwargs(si, **kwargs)
    assert si.rated_interrupting_time == rated_interrupting_time


def test_switch_info_constructor_args():
    si = SwitchInfo(*switch_info_args)

    verify_asset_info_constructor_args(si)
    assert si.rated_interrupting_time == switch_info_args[-1]
