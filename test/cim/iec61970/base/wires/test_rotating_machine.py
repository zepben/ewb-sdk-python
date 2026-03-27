#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from cim.iec61970.base.wires.test_regulating_cond_eq import regulating_cond_eq_args, \
    verify_regulating_cond_eq_constructor_default, verify_regulating_cond_eq_constructor_kwargs, verify_regulating_cond_eq_constructor_args
from zepben.ewb import RotatingMachine

rotating_machine_args = [*regulating_cond_eq_args, 1.1, 2.2, 3, 4.4, 5.5]


def verify_rotating_machine_constructor_default(rm: RotatingMachine):
    verify_regulating_cond_eq_constructor_default(rm)
    assert rm.rated_power_factor is None
    assert rm.rated_s is None
    assert rm.rated_u is None
    assert rm.p is None
    assert rm.q is None


def verify_rotating_machine_constructor_kwargs(rm: RotatingMachine, rated_power_factor, rated_s, rated_u, p, q, **kwargs):
    verify_regulating_cond_eq_constructor_kwargs(rm, **kwargs)
    assert rm.rated_power_factor == rated_power_factor
    assert rm.rated_s == rated_s
    assert rm.rated_u == rated_u
    assert rm.p == p
    assert rm.q == q


def verify_rotating_machine_constructor_args(rm: RotatingMachine):
    verify_regulating_cond_eq_constructor_args(rm)
    assert rotating_machine_args[-5:] == [
        rm.rated_power_factor,
        rm.rated_s,
        rm.rated_u,
        rm.p,
        rm.q
    ]
