#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import integers, floats

from cim.iec61968.assetinfo.test_transformer_test import transformer_test_kwargs, verify_transformer_test_constructor_default, \
    verify_transformer_test_constructor_kwargs, verify_transformer_test_constructor_args, transformer_test_args
from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER, FLOAT_MIN, FLOAT_MAX
from zepben.evolve import OpenCircuitTest

open_circuit_test_kwargs = {
    **transformer_test_kwargs,
    "energised_end_step": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "energised_end_voltage": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "open_end_step": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "open_end_voltage": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "phase_shift": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

open_circuit_test_args = [*transformer_test_args, 1, 2, 3, 4, 5.5]


def test_open_circuit_test_constructor_default():
    test = OpenCircuitTest()

    verify_transformer_test_constructor_default(test)
    assert test.energised_end_step is None
    assert test.energised_end_voltage is None
    assert test.open_end_step is None
    assert test.open_end_voltage is None
    assert test.phase_shift is None


@given(**open_circuit_test_kwargs)
def test_open_circuit_test_constructor_kwargs(energised_end_step, energised_end_voltage, open_end_step, open_end_voltage, phase_shift, **kwargs):
    # noinspection PyArgumentList
    test = OpenCircuitTest(energised_end_step=energised_end_step,
                           energised_end_voltage=energised_end_voltage,
                           open_end_step=open_end_step,
                           open_end_voltage=open_end_voltage,
                           phase_shift=phase_shift,
                           **kwargs)

    verify_transformer_test_constructor_kwargs(test, **kwargs)
    assert test.energised_end_step == energised_end_step
    assert test.energised_end_voltage == energised_end_voltage
    assert test.open_end_step == open_end_step
    assert test.open_end_voltage == open_end_voltage
    assert test.phase_shift == phase_shift


def test_open_circuit_test_constructor_args():
    # noinspection PyArgumentList
    test = OpenCircuitTest(*open_circuit_test_args)

    verify_transformer_test_constructor_args(test)
    assert test.energised_end_step == open_circuit_test_args[-5]
    assert test.energised_end_voltage == open_circuit_test_args[-4]
    assert test.open_end_step == open_circuit_test_args[-3]
    assert test.open_end_voltage == open_circuit_test_args[-2]
    assert test.phase_shift == open_circuit_test_args[-1]
