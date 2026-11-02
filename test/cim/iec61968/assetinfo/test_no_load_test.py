#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.fill_fields import no_load_test_kwargs
from cim.iec61968.assetinfo.test_transformer_test import verify_transformer_test_constructor_default, \
    verify_transformer_test_constructor_kwargs
from zepben.ewb import NoLoadTest, generate_id


def test_no_load_test_constructor_default():
    nlt = NoLoadTest(mrid=generate_id())

    verify_transformer_test_constructor_default(nlt)
    assert nlt.energised_end_voltage is None
    assert nlt.exciting_current is None
    assert nlt.exciting_current_zero is None
    assert nlt.loss is None
    assert nlt.loss_zero is None


@given(**no_load_test_kwargs())
def test_no_load_test_constructor_kwargs(energised_end_voltage, exciting_current, exciting_current_zero, loss, loss_zero, **kwargs):
    nlt = NoLoadTest(
        energised_end_voltage=energised_end_voltage,
        exciting_current=exciting_current,
        exciting_current_zero=exciting_current_zero,
        loss=loss,
        loss_zero=loss_zero,
        **kwargs,
    )

    verify_transformer_test_constructor_kwargs(nlt, **kwargs)
    assert nlt.energised_end_voltage == energised_end_voltage
    assert nlt.exciting_current == exciting_current
    assert nlt.exciting_current_zero == exciting_current_zero
    assert nlt.loss == loss
    assert nlt.loss_zero == loss_zero
