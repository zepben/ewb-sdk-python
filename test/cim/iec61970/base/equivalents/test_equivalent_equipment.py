#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.core.test_conducting_equipment import conducting_equipment_kwargs, verify_conducting_equipment_constructor_default, \
    verify_conducting_equipment_constructor_kwargs, verify_conducting_equipment_constructor_args, conducting_equipment_args
from zepben.evolve import EquivalentEquipment

equivalent_equipment_kwargs = conducting_equipment_kwargs
equivalent_equipment_args = conducting_equipment_args


def verify_equivalent_equipment_constructor_default(ee: EquivalentEquipment):
    verify_conducting_equipment_constructor_default(ee)


def verify_equivalent_equipment_constructor_kwargs(ee: EquivalentEquipment, **kwargs):
    verify_conducting_equipment_constructor_kwargs(ee, **kwargs)


def verify_equivalent_equipment_constructor_args(ee: EquivalentEquipment):
    verify_conducting_equipment_constructor_args(ee)
