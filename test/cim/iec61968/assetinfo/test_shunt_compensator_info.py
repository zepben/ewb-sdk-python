#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import integers
from zepben.evolve import ShuntCompensatorInfo

from cim.iec61968.assets.test_asset_info import asset_info_kwargs, asset_info_args, verify_asset_info_constructor_default, \
    verify_asset_info_constructor_kwargs, verify_asset_info_constructor_args
from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER

shunt_compensator_info_kwargs = {
    **asset_info_kwargs,
    "max_power_loss": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "rated_current": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "rated_reactive_power": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "rated_voltage": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
}

shunt_compensator_info_args = [*asset_info_args, 1, 2, 3, 4]


def test_shunt_compensator_info_constructor_default():
    sci = ShuntCompensatorInfo()

    verify_asset_info_constructor_default(sci)
    assert sci.max_power_loss is None
    assert sci.rated_current is None
    assert sci.rated_reactive_power is None
    assert sci.rated_voltage is None


@given(**shunt_compensator_info_kwargs)
def test_shunt_compensator_info_constructor_kwargs(max_power_loss, rated_current, rated_reactive_power, rated_voltage, **kwargs):
    # noinspection PyArgumentList
    sci = ShuntCompensatorInfo(max_power_loss=max_power_loss,
                               rated_current=rated_current,
                               rated_reactive_power=rated_reactive_power,
                               rated_voltage=rated_voltage,
                               **kwargs)

    verify_asset_info_constructor_kwargs(sci, **kwargs)
    assert sci.max_power_loss == max_power_loss
    assert sci.rated_current == rated_current
    assert sci.rated_reactive_power == rated_reactive_power
    assert sci.rated_voltage == rated_voltage


def test_shunt_compensator_info_constructor_args():
    # noinspection PyArgumentList
    sci = ShuntCompensatorInfo(*shunt_compensator_info_args)

    verify_asset_info_constructor_args(sci)
    assert sci.max_power_loss == shunt_compensator_info_args[-4]
    assert sci.rated_current == shunt_compensator_info_args[-3]
    assert sci.rated_reactive_power == shunt_compensator_info_args[-2]
    assert sci.rated_voltage == shunt_compensator_info_args[-1]
