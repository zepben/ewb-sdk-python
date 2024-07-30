#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import text, lists, floats, booleans

from cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE, FLOAT_MIN, FLOAT_MAX
from cim.collection_validator import validate_collection_ordered
from cim.iec61968.assets.test_asset_info import asset_info_kwargs, asset_info_args, verify_asset_info_constructor_default, verify_asset_info_constructor_kwargs, \
    verify_asset_info_constructor_args
from zepben.evolve import RelayInfo

relay_info_kwargs = {
    **asset_info_kwargs,
    "curve_setting": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "reclose_fast": booleans(),
    "reclose_delays": lists(floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))

}

relay_info_args = [*asset_info_args, "a", True, [0.1, 0.2, 0.3]]


def test_relay_info_constructor_default():
    ri = RelayInfo()

    verify_asset_info_constructor_default(ri)
    assert ri.curve_setting is None
    assert ri.reclose_fast is None
    assert not list(ri.reclose_delays)


@given(**relay_info_kwargs)
def test_relay_info_constructor_kwargs(curve_setting, reclose_fast, reclose_delays, **kwargs):
    ri = RelayInfo(
        curve_setting=curve_setting,
        reclose_fast=reclose_fast,
        reclose_delays=reclose_delays,
        **kwargs
    )

    verify_asset_info_constructor_kwargs(ri, **kwargs)
    assert ri.curve_setting == curve_setting
    assert ri.reclose_fast == reclose_fast
    assert list(ri.reclose_delays) == reclose_delays


def test_relay_info_constructor_args():
    ri = RelayInfo(*relay_info_args)

    verify_asset_info_constructor_args(ri)
    assert ri.curve_setting == relay_info_args[-3]
    assert ri.reclose_fast == relay_info_args[-2]
    assert list(ri.reclose_delays) == relay_info_args[-1]


def test_relay_info_reclose_delays():
    validate_collection_ordered(RelayInfo,
                                lambda i, _: float(i),
                                RelayInfo.num_delays,
                                RelayInfo.get_delay,
                                RelayInfo.reclose_delays,
                                RelayInfo.add_delay,
                                RelayInfo.add_delay,
                                RelayInfo.remove_delay,
                                RelayInfo.clear_delays
                                )
