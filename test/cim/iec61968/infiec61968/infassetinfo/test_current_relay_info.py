#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import text, lists, floats

from cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE, FLOAT_MIN, FLOAT_MAX
from cim.iec61968.assets.test_asset_info import asset_info_kwargs, asset_info_args, verify_asset_info_constructor_default, verify_asset_info_constructor_kwargs, \
    verify_asset_info_constructor_args
from zepben.evolve import CurrentRelayInfo

current_relay_info_kwargs = {
    **asset_info_kwargs,
    "curve_setting": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "reclose_delays": lists(floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))

}

current_relay_info_args = [*asset_info_args, "a", [0.1, 0.2, 0.3]]


def test_current_relay_info_constructor_default():
    cri = CurrentRelayInfo()

    verify_asset_info_constructor_default(cri)
    assert cri.curve_setting is None
    assert not list(cri.reclose_delays)


@given(**current_relay_info_kwargs)
def test_current_relay_info_constructor_kwargs(curve_setting, reclose_delays, **kwargs):
    cri = CurrentRelayInfo(
        curve_setting=curve_setting,
        reclose_delays=reclose_delays,
        **kwargs
    )

    verify_asset_info_constructor_kwargs(cri, **kwargs)
    assert cri.curve_setting == curve_setting
    assert list(cri.reclose_delays) == reclose_delays


def test_current_relay_info_constructor_args():
    cri = CurrentRelayInfo(*current_relay_info_args)

    verify_asset_info_constructor_args(cri)
    assert cri.curve_setting == current_relay_info_args[-2]
    assert list(cri.reclose_delays) == current_relay_info_args[-1]
