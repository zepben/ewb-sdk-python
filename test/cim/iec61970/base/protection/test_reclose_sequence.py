#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import integers, floats

from cim.cim_creators import FLOAT_MIN, FLOAT_MAX, MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER
from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, identified_object_args, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args
from zepben.evolve import RecloseSequence

reclose_sequence_kwargs = {
    **identified_object_kwargs,
    "reclose_delay": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "reclose_step": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
}

reclose_sequence_args = [*identified_object_args, 1.1, 2]


def test_reclose_sequence_constructor_default():
    rs = RecloseSequence()

    verify_identified_object_constructor_default(rs)
    assert rs.reclose_delay is None
    assert rs.reclose_step is None


@given(**reclose_sequence_kwargs)
def test_reclose_sequence_constructor_kwargs(reclose_delay, reclose_step, **kwargs):
    rs = RecloseSequence(
        reclose_delay=reclose_delay,
        reclose_step=reclose_step,
        **kwargs
    )

    verify_identified_object_constructor_kwargs(rs, **kwargs)
    assert rs.reclose_delay == reclose_delay
    assert rs.reclose_step == reclose_step


def test_reclose_sequence_constructor_args():
    rs = RecloseSequence(*reclose_sequence_args)

    verify_identified_object_constructor_args(rs)
    assert rs.reclose_delay == reclose_sequence_args[-2]
    assert rs.reclose_step == reclose_sequence_args[-1]
