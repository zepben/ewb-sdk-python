#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from zepben.evolve import ReactiveCapabilityCurve

from cim.iec61970.base.core.test_curve import curve_kwargs, curve_args, verify_curve_constructor_default, verify_curve_constructor_kwargs, \
    verify_curve_constructor_args

reactive_capability_curve_kwargs = curve_kwargs
reactive_capability_curve_args = curve_args


def verify_reactive_capability_curve_constructor_default():
    verify_curve_constructor_default(ReactiveCapabilityCurve())


@given(**reactive_capability_curve_kwargs)
def verify_reactive_capability_curve_constructor_kwargs(**kwargs):
    verify_curve_constructor_kwargs(ReactiveCapabilityCurve(**kwargs), **kwargs)


def verify_reactive_capability_curve_constructor_args():
    verify_curve_constructor_args(ReactiveCapabilityCurve(*reactive_capability_curve_args))
