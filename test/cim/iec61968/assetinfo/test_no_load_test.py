#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import integers, floats

from cim.iec61968.assetinfo.test_transformer_test import transformer_test_kwargs, verify_transformer_test_constructor_default, \
    verify_transformer_test_constructor_kwargs, verify_transformer_test_constructor_args, transformer_test_args
from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER, FLOAT_MIN, FLOAT_MAX
from zepben.evolve import NoLoadTest

no_load_test_kwargs = {
    **transformer_test_kwargs,
    "energised_end_voltage": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "exciting_current": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "exciting_current_zero": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "loss": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "loss_zero": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
}

no_load_test_args = [*transformer_test_args, 1, 2.2, 3.3, 4, 5]


def test_no_load_test_constructor_default():
    nlt = NoLoadTest()

    verify_transformer_test_constructor_default(nlt)
    assert nlt.energised_end_voltage is None
    assert nlt.exciting_current is None
    assert nlt.exciting_current_zero is None
    assert nlt.loss is None
    assert nlt.loss_zero is None


@given(**no_load_test_kwargs)
def test_no_load_test_constructor_kwargs(energised_end_voltage, exciting_current, exciting_current_zero, loss, loss_zero, **kwargs):
    # noinspection PyArgumentList
    nlt = NoLoadTest(energised_end_voltage=energised_end_voltage,
                     exciting_current=exciting_current,
                     exciting_current_zero=exciting_current_zero,
                     loss=loss,
                     loss_zero=loss_zero,
                     **kwargs)

    verify_transformer_test_constructor_kwargs(nlt, **kwargs)
    assert nlt.energised_end_voltage == energised_end_voltage
    assert nlt.exciting_current == exciting_current
    assert nlt.exciting_current_zero == exciting_current_zero
    assert nlt.loss == loss
    assert nlt.loss_zero == loss_zero


def test_no_load_test_constructor_args():
    # noinspection PyArgumentList
    nlt = NoLoadTest(*no_load_test_args)

    verify_transformer_test_constructor_args(nlt)
    assert nlt.energised_end_voltage == no_load_test_args[-5]
    assert nlt.exciting_current == no_load_test_args[-4]
    assert nlt.exciting_current_zero == no_load_test_args[-3]
    assert nlt.loss == no_load_test_args[-2]
    assert nlt.loss_zero == no_load_test_args[-1]
