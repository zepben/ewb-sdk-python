#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.iec61970.base.wires.test_switch import verify_switch_constructor_default, verify_switch_constructor_kwargs, verify_switch_constructor_args, \
    switch_kwargs, switch_args
from hypothesis.strategies import builds

from zepben.evolve import Fuse, ProtectionRelayFunction

fuse_kwargs = {
    **switch_kwargs,
    "function": builds(ProtectionRelayFunction)
}
fuse_args = [*switch_args, ProtectionRelayFunction()]


def test_fuse_constructor_default():
    f = Fuse()
    verify_switch_constructor_default(f)
    assert f.function is None


@given(**fuse_kwargs)
def test_fuse_constructor_kwargs(function, **kwargs):
    f = Fuse(function=function, **kwargs)
    verify_switch_constructor_kwargs(f, **kwargs)
    assert f.function == function


def test_fuse_constructor_args():
    f = Fuse(*fuse_args)
    verify_switch_constructor_args(f)
    assert f.function == fuse_args[-1]
