#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.core.test_conducting_equipment import verify_conducting_equipment_constructor_default, \
    verify_conducting_equipment_constructor_kwargs
from zepben.ewb import EquivalentEquipment


def verify_equivalent_equipment_constructor_default(ee: EquivalentEquipment):
    verify_conducting_equipment_constructor_default(ee)


def verify_equivalent_equipment_constructor_kwargs(ee: EquivalentEquipment, **kwargs):
    verify_conducting_equipment_constructor_kwargs(ee, **kwargs)
