#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import integers, floats

from test.cim.extract_testing_args import extract_testing_args
from test.cim.iec61968.assetinfo.test_transformer_test import transformer_test_kwargs, verify_transformer_test_constructor_default, \
    verify_transformer_test_constructor_kwargs, verify_transformer_test_constructor_args, transformer_test_args
from test.cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER, FLOAT_MIN, FLOAT_MAX
from zepben.evolve import ShortCircuitTest
from zepben.evolve.model.cim.iec61968.assetinfo.create_asset_info_components import create_short_circuit_test

short_circuit_test_kwargs = {
    **transformer_test_kwargs,
    "current": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "energised_end_step": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "grounded_end_step": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "leakage_impedance": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "leakage_impedance_zero": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "loss": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "loss_zero": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "power": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "voltage": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "voltage_ohmic_part": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

short_circuit_test_args = [*transformer_test_args, 1.1, 2, 3, 4.4, 5.5, 6, 7, 8, 9.9, 10.01]


def test_short_circuit_test_constructor_default():
    sct = ShortCircuitTest()
    sct2 = create_short_circuit_test()
    validate_default_short_circuit(sct)
    validate_default_short_circuit(sct2)


def validate_default_short_circuit(sct):
    verify_transformer_test_constructor_default(sct)
    assert sct.current is None
    assert sct.energised_end_step is None
    assert sct.grounded_end_step is None
    assert sct.leakage_impedance is None
    assert sct.leakage_impedance_zero is None
    assert sct.loss is None
    assert sct.loss_zero is None
    assert sct.power is None
    assert sct.voltage is None
    assert sct.voltage_ohmic_part is None


@given(**short_circuit_test_kwargs)
def test_short_circuit_test_constructor_kwargs(current, energised_end_step, grounded_end_step, leakage_impedance, leakage_impedance_zero, loss, loss_zero,
                                               power, voltage, voltage_ohmic_part, **kwargs):
    args = extract_testing_args(locals())
    sct = ShortCircuitTest(**args, **kwargs)
    validate_short_circuit_test_values(sct, **args, **kwargs)


@given(**short_circuit_test_kwargs)
def test_short_circuit_test_creator(current, energised_end_step, grounded_end_step, leakage_impedance, leakage_impedance_zero, loss, loss_zero,
                                    power, voltage, voltage_ohmic_part, **kwargs):
    args = extract_testing_args(locals())
    sct = ShortCircuitTest(**args, **kwargs)
    validate_short_circuit_test_values(sct, **args, **kwargs)


def validate_short_circuit_test_values(sct, current, energised_end_step, grounded_end_step, leakage_impedance, leakage_impedance_zero, loss, loss_zero, power,
                                       voltage, voltage_ohmic_part, **kwargs):
    verify_transformer_test_constructor_kwargs(sct, **kwargs)
    assert sct.current == current
    assert sct.energised_end_step == energised_end_step
    assert sct.grounded_end_step == grounded_end_step
    assert sct.leakage_impedance == leakage_impedance
    assert sct.leakage_impedance_zero == leakage_impedance_zero
    assert sct.loss == loss
    assert sct.loss_zero == loss_zero
    assert sct.power == power
    assert sct.voltage == voltage
    assert sct.voltage_ohmic_part == voltage_ohmic_part


def test_short_circuit_test_constructor_args():
    # noinspection PyArgumentList
    sct = ShortCircuitTest(*short_circuit_test_args)

    verify_transformer_test_constructor_args(sct)
    assert sct.current == short_circuit_test_args[-10]
    assert sct.energised_end_step == short_circuit_test_args[-9]
    assert sct.grounded_end_step == short_circuit_test_args[-8]
    assert sct.leakage_impedance == short_circuit_test_args[-7]
    assert sct.leakage_impedance_zero == short_circuit_test_args[-6]
    assert sct.loss == short_circuit_test_args[-5]
    assert sct.loss_zero == short_circuit_test_args[-4]
    assert sct.power == short_circuit_test_args[-3]
    assert sct.voltage == short_circuit_test_args[-2]
    assert sct.voltage_ohmic_part == short_circuit_test_args[-1]
