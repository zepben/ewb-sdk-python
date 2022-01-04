#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import integers, data

from test.cim.common_testing_functions import verify
from zepben.evolve import ShuntCompensatorInfo

from test.cim.iec61968.assets.test_asset_info import asset_info_kwargs, asset_info_args, verify_asset_info_constructor_default, \
    verify_asset_info_constructor_kwargs, verify_asset_info_constructor_args
from test.cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER
from zepben.evolve.model.cim.iec61968.assetinfo.create_asset_info_components import create_shunt_compensator_info


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
    sci2 = create_shunt_compensator_info()
    verify_default_shunt_compensator_info(sci)
    verify_default_shunt_compensator_info(sci2)


def verify_default_shunt_compensator_info(sci):
    verify_asset_info_constructor_default(sci)
    assert sci.max_power_loss is None
    assert sci.rated_current is None
    assert sci.rated_reactive_power is None
    assert sci.rated_voltage is None


# noinspection PyShadowingNames
@given(data())
def test_shunt_compensator_info_constructor_kwargs(data):
    verify(
        [ShuntCompensatorInfo, create_shunt_compensator_info],
        data, shunt_compensator_info_kwargs, verify_shunt_compensator_info_value
    )


def verify_shunt_compensator_info_value(sci, max_power_loss, rated_current, rated_reactive_power, rated_voltage, **kwargs):
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
