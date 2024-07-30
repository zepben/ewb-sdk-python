#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis.strategies import integers, builds

from cim.iec61970.base.core.test_equipment import equipment_kwargs, verify_equipment_constructor_default, \
    verify_equipment_constructor_kwargs, verify_equipment_constructor_args, equipment_args
from zepben.evolve import PowerElectronicsUnit, PowerElectronicsConnection
from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER

power_electronics_unit_kwargs = {
    **equipment_kwargs,
    "power_electronics_connection": builds(PowerElectronicsConnection),
    "max_p": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "min_p": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
}

power_electronics_unit_args = [*equipment_args, PowerElectronicsConnection(), 1, 2]


def verify_power_electronics_unit_constructor_default(peu: PowerElectronicsUnit):
    verify_equipment_constructor_default(peu)
    assert peu.power_electronics_connection is None
    assert peu.max_p is None
    assert peu.min_p is None


def verify_power_electronics_unit_constructor_kwargs(peu: PowerElectronicsUnit, power_electronics_connection, max_p, min_p, **kwargs):
    verify_equipment_constructor_kwargs(peu, **kwargs)
    assert peu.power_electronics_connection == power_electronics_connection
    assert peu.max_p == max_p
    assert peu.min_p == min_p


def verify_power_electronics_unit_constructor_args(peu: PowerElectronicsUnit):
    verify_equipment_constructor_args(peu)
    assert peu.power_electronics_connection is power_electronics_unit_args[-3]
    assert peu.max_p == power_electronics_unit_args[-2]
    assert peu.min_p == power_electronics_unit_args[-1]
