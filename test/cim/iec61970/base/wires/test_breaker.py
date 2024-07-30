#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import floats

from cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from cim.iec61970.base.wires.test_protected_switch import verify_protected_switch_constructor_default, \
    verify_protected_switch_constructor_kwargs, verify_protected_switch_constructor_args, protected_switch_kwargs, protected_switch_args
from zepben.evolve import Breaker, Substation, Terminal, Feeder

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


def test_is_substation_breaker_when_associated_with_a_substation_equipment():
    br = Breaker()

    assert not br.is_substation_breaker, "is_substation_breaker should return False for Breakers without containers"

    br.add_container(Substation())

    assert br.is_substation_breaker, "is_substation_breaker should return True for Breakers with a Substation container"


def test_is_feeder_head_breaker_when_a_terminal_is_a_feeder_head_terminal():
    br = Breaker().add_terminal(Terminal()).add_terminal(Terminal())
    fdr = Feeder(normal_head_terminal=Terminal())

    assert not br.is_feeder_head_breaker, "is_feeder_head_breaker should return False for Breakers without feeder head terminals"

    br.add_container(fdr)
    assert not br.is_feeder_head_breaker, "is_feeder_head_breaker should not return True because a Breaker has a Feeder as a container"

    br.add_terminal(fdr.normal_head_terminal)
    assert br.is_feeder_head_breaker, "is_feeder_head_breaker should return True for Breakers with a feeder head terminal"
