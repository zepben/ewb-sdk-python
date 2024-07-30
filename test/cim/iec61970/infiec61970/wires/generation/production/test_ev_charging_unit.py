#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.iec61970.base.wires.generation.production.test_power_electronics_unit import verify_power_electronics_unit_constructor_default, \
    verify_power_electronics_unit_constructor_args, verify_power_electronics_unit_constructor_kwargs, power_electronics_unit_kwargs, power_electronics_unit_args
from zepben.evolve import EvChargingUnit

ev_charging_unit_kwargs = power_electronics_unit_kwargs
ev_charging_unit_args = power_electronics_unit_args


def test_ev_charging_unit_constructor_default():
    verify_power_electronics_unit_constructor_default(EvChargingUnit())


@given(**ev_charging_unit_kwargs)
def test_ev_charging_unit_constructor_kwargs(**kwargs):
    verify_power_electronics_unit_constructor_kwargs(EvChargingUnit(**kwargs), **kwargs)


def test_ev_charging_unit_constructor_args():
    verify_power_electronics_unit_constructor_args(EvChargingUnit(*ev_charging_unit_args))
