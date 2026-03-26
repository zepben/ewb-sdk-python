#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from cim.iec61970.base.core.test_identified_object import verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from zepben.ewb import TransformerTest

transformer_test_args = [*identified_object_args, 1, 2.2]


def verify_transformer_test_constructor_default(tt: TransformerTest):
    verify_identified_object_constructor_default(tt)
    assert tt.base_power is None
    assert tt.temperature is None


def verify_transformer_test_constructor_kwargs(tt: TransformerTest, base_power, temperature, **kwargs):
    verify_identified_object_constructor_kwargs(tt, **kwargs)
    assert tt.base_power == base_power
    assert tt.temperature == temperature


def verify_transformer_test_constructor_args(tt: TransformerTest):
    verify_identified_object_constructor_args(tt)
    assert transformer_test_args[-2:] == [
        tt.base_power,
        tt.temperature
    ]
