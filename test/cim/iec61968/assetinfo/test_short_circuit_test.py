#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.fill_fields import short_circuit_test_kwargs
from cim.iec61968.assetinfo.test_transformer_test import verify_transformer_test_constructor_default, \
    verify_transformer_test_constructor_kwargs
from zepben.ewb import ShortCircuitTest, generate_id


def test_short_circuit_test_constructor_default():
    sct = ShortCircuitTest(mrid=generate_id())

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


@given(**short_circuit_test_kwargs())
def test_short_circuit_test_constructor_kwargs(
    current, energised_end_step, grounded_end_step, leakage_impedance, leakage_impedance_zero, loss, loss_zero,
    power, voltage, voltage_ohmic_part, **kwargs,
):
    sct = ShortCircuitTest(
        current=current,
        energised_end_step=energised_end_step,
        grounded_end_step=grounded_end_step,
        leakage_impedance=leakage_impedance,
        leakage_impedance_zero=leakage_impedance_zero,
        loss=loss,
        loss_zero=loss_zero,
        power=power,
        voltage=voltage,
        voltage_ohmic_part=voltage_ohmic_part,
        **kwargs,
    )

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
