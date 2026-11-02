#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.core.test_equipment import verify_equipment_constructor_default, \
    verify_equipment_constructor_kwargs
from zepben.ewb import PowerElectronicsUnit


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
