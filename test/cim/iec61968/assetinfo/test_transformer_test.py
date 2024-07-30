#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis.strategies import integers, floats

from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER, FLOAT_MIN, FLOAT_MAX
from zepben.evolve import TransformerTest

transformer_test_kwargs = {
    **identified_object_kwargs,
    "base_power": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "temperature": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

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
    assert tt.base_power == transformer_test_args[-2]
    assert tt.temperature == transformer_test_args[-1]
