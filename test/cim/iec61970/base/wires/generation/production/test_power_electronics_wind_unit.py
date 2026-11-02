#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.fill_fields import power_electronics_wind_unit_kwargs
from cim.iec61970.base.wires.generation.production.test_power_electronics_unit import \
    verify_power_electronics_unit_constructor_default, verify_power_electronics_unit_constructor_kwargs
from zepben.ewb import PowerElectronicsWindUnit, generate_id


def test_power_electronics_wind_unit_constructor_default():
    verify_power_electronics_unit_constructor_default(PowerElectronicsWindUnit(mrid=generate_id()))


@given(**power_electronics_wind_unit_kwargs())
def test_power_electronics_wind_unit_constructor_kwargs(**kwargs):
    verify_power_electronics_unit_constructor_kwargs(PowerElectronicsWindUnit(**kwargs), **kwargs)
