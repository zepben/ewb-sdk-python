#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.fill_fields import static_var_compensator_kwargs
from cim.iec61970.base.wires.test_regulating_cond_eq import verify_regulating_cond_eq_constructor_default, \
    verify_regulating_cond_eq_constructor_kwargs
from zepben.ewb import SVCControlMode, StaticVarCompensator, generate_id


def test_static_var_compensator_constructor_default():
    svc = StaticVarCompensator(mrid=generate_id())
    verify_regulating_cond_eq_constructor_default(svc)
    assert svc.capacitive_rating is None
    assert svc.inductive_rating is None
    assert svc.q is None
    assert svc.svc_control_mode == SVCControlMode.UNKNOWN
    assert svc.voltage_set_point is None


@given(**static_var_compensator_kwargs())
def test_static_var_compensator_constructor_kwargs(capacitive_rating, inductive_rating, q, svc_control_mode, voltage_set_point, **kwargs):
    svc = StaticVarCompensator(
        capacitive_rating=capacitive_rating,
        inductive_rating=inductive_rating,
        q=q,
        svc_control_mode=svc_control_mode,
        voltage_set_point=voltage_set_point,
        **kwargs,
    )
    verify_regulating_cond_eq_constructor_kwargs(svc, **kwargs)
    assert svc.capacitive_rating == capacitive_rating
    assert svc.inductive_rating == inductive_rating
    assert svc.q == q
    assert svc.svc_control_mode == svc_control_mode
    assert svc.voltage_set_point == voltage_set_point
