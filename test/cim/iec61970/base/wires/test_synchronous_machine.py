#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.fill_fields import synchronous_machine_kwargs
from cim.iec61970.base.wires.test_rotating_machine import rotating_machine_args, \
    verify_rotating_machine_constructor_default, verify_rotating_machine_constructor_kwargs, verify_rotating_machine_constructor_args
from cim.private_collection_validator import validate_unordered
from zepben.ewb import SynchronousMachine, SynchronousMachineKind, ReactiveCapabilityCurve

synchronous_machine_args = [*rotating_machine_args, [ReactiveCapabilityCurve(mrid="rcc1"), ReactiveCapabilityCurve(mrid="rcc2")], 1.1, 2, True, 3.3, 4.4, 5.5,
                            6.6, 7, 8.8, 9, 10.10, 11.11, 12.12, 13.13, 14.14, 15.15, 16.16, 17.17, 18.18, SynchronousMachineKind.generatorOrMotor,
                            SynchronousMachineKind.generator]


def verify_synchronous_machine_constructor_default():
    sm = SynchronousMachine()

    verify_rotating_machine_constructor_default(sm)
    assert not list(sm.curves)
    assert sm.base_q is None
    assert sm.condenser_p is None
    assert not sm.earthing
    assert sm.earthing_star_point_r is None
    assert sm.earthing_star_point_x is None
    assert sm.ikk is None
    assert sm.max_q is None
    assert sm.max_u is None
    assert sm.min_q is None
    assert sm.min_u is None
    assert sm.mu is None
    assert sm.r is None
    assert sm.r0 is None
    assert sm.r2 is None
    assert sm.sat_direct_subtrans_x is None
    assert sm.sat_direct_sync_x is None
    assert sm.sat_direct_trans_x is None
    assert sm.x0 is None
    assert sm.x2 is None
    assert sm.type is SynchronousMachineKind.UNKNOWN
    assert sm.operating_mode is SynchronousMachineKind.UNKNOWN


# noinspection PyShadowingBuiltins
@given(**synchronous_machine_kwargs())
def verify_synchronous_machine_constructor_kwargs(
    curves,
    base_q,
    condenser_p,
    earthing,
    earthing_star_point_r,
    earthing_star_point_x,
    ikk,
    max_q,
    max_u,
    min_q,
    min_u,
    mu,
    r,
    r0,
    r2,
    sat_direct_subtrans_x,
    sat_direct_sync_x,
    sat_direct_trans_x,
    x0,
    x2,
    type,
    operating_mode,
    **kwargs
):
    sm = SynchronousMachine(
        curves=curves,
        base_q=base_q,
        condenser_p=condenser_p,
        earthing=earthing,
        earthing_star_point_r=earthing_star_point_r,
        earthing_star_point_x=earthing_star_point_x,
        ikk=ikk,
        max_q=max_q,
        max_u=max_u,
        min_q=min_q,
        min_u=min_u,
        mu=mu,
        r=r,
        r0=r0,
        r2=r2,
        sat_direct_subtrans_x=sat_direct_subtrans_x,
        sat_direct_sync_x=sat_direct_sync_x,
        sat_direct_trans_x=sat_direct_trans_x,
        x0=x0,
        x2=x2,
        type=type,
        operating_mode=operating_mode,
        **kwargs
    )

    verify_rotating_machine_constructor_kwargs(sm, **kwargs)
    assert sm.curves == curves
    assert sm.base_q == base_q
    assert sm.condenser_p == condenser_p
    assert sm.earthing == earthing
    assert sm.earthing_star_point_r == earthing_star_point_r
    assert sm.earthing_star_point_x == earthing_star_point_x
    assert sm.ikk == ikk
    assert sm.max_q == max_q
    assert sm.max_u == max_u
    assert sm.min_q == min_q
    assert sm.min_u == min_u
    assert sm.mu == mu
    assert sm.r == r
    assert sm.r0 == r0
    assert sm.r2 == r2
    assert sm.sat_direct_subtrans_x == sat_direct_subtrans_x
    assert sm.sat_direct_sync_x == sat_direct_sync_x
    assert sm.sat_direct_trans_x == sat_direct_trans_x
    assert sm.x0 == x0
    assert sm.x2 == x2
    assert sm.type == type
    assert sm.operating_mode == operating_mode


def verify_synchronous_machine_constructor_args():
    sm = SynchronousMachine(*synchronous_machine_args)

    verify_rotating_machine_constructor_args(sm)
    assert synchronous_machine_args[-22:] == [
        list(sm.curves),
        sm.base_q,
        sm.condenser_p,
        sm.earthing,
        sm.earthing_star_point_r,
        sm.earthing_star_point_x,
        sm.ikk,
        sm.max_q,
        sm.max_u,
        sm.min_q,
        sm.min_u,
        sm.mu,
        sm.r,
        sm.r0,
        sm.r2,
        sm.sat_direct_subtrans_x,
        sm.sat_direct_sync_x,
        sm.sat_direct_trans_x,
        sm.x0,
        sm.x2,
        sm.type,
        sm.operating_mode
    ]


def test_curves_collection():
    validate_unordered(
        SynchronousMachine,
        ReactiveCapabilityCurve,
        SynchronousMachine.curves,
        SynchronousMachine.num_curves,
        SynchronousMachine.get_curve,
        SynchronousMachine.add_curve,
        SynchronousMachine.remove_curve,
        SynchronousMachine.clear_curves
    )
