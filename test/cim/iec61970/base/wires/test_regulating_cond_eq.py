#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis.strategies import booleans

from test.cim.iec61970.base.wires.test_energy_connection import energy_connection_kwargs, verify_energy_connection_constructor_default, \
    verify_energy_connection_constructor_kwargs, verify_energy_connection_constructor_args, energy_connection_args
from zepben.evolve import RegulatingCondEq

regulating_cond_eq_kwargs = {
    **energy_connection_kwargs,
    "control_enabled": booleans()
}

regulating_cond_eq_args = [*energy_connection_args, False]


def verify_regulating_cond_eq_constructor_default(rce: RegulatingCondEq):
    verify_energy_connection_constructor_default(rce)
    assert rce.control_enabled


def verify_regulating_cond_eq_constructor_kwargs(rce: RegulatingCondEq, control_enabled, **kwargs):
    verify_energy_connection_constructor_kwargs(rce, **kwargs)
    assert rce.control_enabled == control_enabled


def verify_regulating_cond_eq_constructor_args(rce: RegulatingCondEq):
    verify_energy_connection_constructor_args(rce)
    assert rce.control_enabled == regulating_cond_eq_args[-1]
