#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.core.test_conducting_equipment import verify_conducting_equipment_constructor_default, \
    verify_conducting_equipment_constructor_kwargs
from zepben.ewb import EnergyConnection


def verify_energy_connection_constructor_default(ec: EnergyConnection):
    verify_conducting_equipment_constructor_default(ec)


def verify_energy_connection_constructor_kwargs(ec: EnergyConnection, **kwargs):
    verify_conducting_equipment_constructor_kwargs(ec, **kwargs)
