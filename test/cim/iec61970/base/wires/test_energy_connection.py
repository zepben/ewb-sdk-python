#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.core.test_conducting_equipment import conducting_equipment_kwargs, verify_conducting_equipment_constructor_default, \
    verify_conducting_equipment_constructor_kwargs, verify_conducting_equipment_constructor_args, conducting_equipment_args
from zepben.evolve import EnergyConnection

energy_connection_kwargs = conducting_equipment_kwargs
energy_connection_args = conducting_equipment_args


def verify_energy_connection_constructor_default(ec: EnergyConnection):
    verify_conducting_equipment_constructor_default(ec)


def verify_energy_connection_constructor_kwargs(ec: EnergyConnection, **kwargs):
    verify_conducting_equipment_constructor_kwargs(ec, **kwargs)


def verify_energy_connection_constructor_args(ec: EnergyConnection):
    verify_conducting_equipment_constructor_args(ec)
