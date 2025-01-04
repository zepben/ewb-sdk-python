#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import floats, integers, sampled_from
from zepben.evolve import SVCControlMode, StaticVarCompensator

from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER, FLOAT_MAX, FLOAT_MIN
from cim.iec61970.base.wires.test_regulating_cond_eq import regulating_cond_eq_kwargs, verify_regulating_cond_eq_constructor_default, \
    verify_regulating_cond_eq_constructor_kwargs, verify_regulating_cond_eq_constructor_args, regulating_cond_eq_args

static_var_compensator_kwargs = {
    **regulating_cond_eq_kwargs,
    "capacitive_rating": floats(min_value=0, max_value=FLOAT_MAX),
    "inductive_rating": floats(min_value=FLOAT_MIN, max_value=0),
    "q": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "svc_control_mode": sampled_from(SVCControlMode),
    "voltage_set_point": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
}

static_var_compensator_args = [*regulating_cond_eq_args, 1.0, -1.0, 2.0, SVCControlMode.voltage, 3]


def test_static_var_compensator_constructor_default():
    svc = StaticVarCompensator()
    verify_regulating_cond_eq_constructor_default(svc)
    assert svc.capacitive_rating is None
    assert svc.inductive_rating is None
    assert svc.q is None
    assert svc.svc_control_mode == SVCControlMode.UNKNOWN
    assert svc.voltage_set_point is None


@given(**static_var_compensator_kwargs)
def test_static_var_compensator_constructor_kwargs(capacitive_rating, inductive_rating, q, svc_control_mode, voltage_set_point, **kwargs):
    svc = StaticVarCompensator(
        capacitive_rating=capacitive_rating,
        inductive_rating=inductive_rating,
        q=q,
        svc_control_mode=svc_control_mode,
        voltage_set_point=voltage_set_point,
        **kwargs
    )
    verify_regulating_cond_eq_constructor_kwargs(svc, **kwargs)
    assert svc.capacitive_rating == capacitive_rating
    assert svc.inductive_rating == inductive_rating
    assert svc.q == q
    assert svc.svc_control_mode == svc_control_mode
    assert svc.voltage_set_point == voltage_set_point


def test_shunt_compensator_constructor_args():
    svc = StaticVarCompensator(*static_var_compensator_args)

    verify_regulating_cond_eq_constructor_args(svc)
    assert static_var_compensator_args[-5:] == [
        svc.capacitive_rating,
        svc.inductive_rating,
        svc.q,
        svc.svc_control_mode,
        svc.voltage_set_point,
    ]
