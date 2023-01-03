#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import floats

from cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from cim.iec61970.base.wires.test_protected_switch import verify_protected_switch_constructor_default, \
    verify_protected_switch_constructor_kwargs, verify_protected_switch_constructor_args, protected_switch_kwargs, protected_switch_args
from zepben.evolve.model.cim.iec61970.base.wires.breaker import Breaker

breaker_kwargs = {
    **protected_switch_kwargs,
    "in_transit_time": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}
breaker_args = [*protected_switch_args, 1.1]


def test_breaker_constructor_default():
    br = Breaker()
    verify_protected_switch_constructor_default(br)

    assert br.in_transit_time is None


@given(**breaker_kwargs)
def test_breaker_constructor_kwargs(in_transit_time, **kwargs):
    br = Breaker(in_transit_time=in_transit_time, **kwargs)
    verify_protected_switch_constructor_kwargs(br, **kwargs)

    assert br.in_transit_time == in_transit_time


def test_breaker_constructor_args():
    br = Breaker(*breaker_args)
    verify_protected_switch_constructor_args(br)

    assert br.in_transit_time == breaker_args[-1]
