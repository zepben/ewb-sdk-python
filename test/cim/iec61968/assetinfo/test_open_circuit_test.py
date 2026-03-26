#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.fill_fields import open_circuit_test_kwargs
from cim.iec61968.assetinfo.test_transformer_test import verify_transformer_test_constructor_default, \
    verify_transformer_test_constructor_kwargs, verify_transformer_test_constructor_args, transformer_test_args
from zepben.ewb import OpenCircuitTest, generate_id

open_circuit_test_args = [*transformer_test_args, 1, 2, 3, 4, 5.5]


def test_open_circuit_test_constructor_default():
    test = OpenCircuitTest(mrid=generate_id())

    verify_transformer_test_constructor_default(test)
    assert test.energised_end_step is None
    assert test.energised_end_voltage is None
    assert test.open_end_step is None
    assert test.open_end_voltage is None
    assert test.phase_shift is None


@given(**open_circuit_test_kwargs())
def test_open_circuit_test_constructor_kwargs(energised_end_step, energised_end_voltage, open_end_step, open_end_voltage, phase_shift, **kwargs):
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
    test = OpenCircuitTest(*open_circuit_test_args)

    verify_transformer_test_constructor_args(test)
    assert open_circuit_test_args[-5:] == [
        test.energised_end_step,
        test.energised_end_voltage,
        test.open_end_step,
        test.open_end_voltage,
        test.phase_shift
    ]
