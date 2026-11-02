#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from cim.iec61970.base.core.test_conducting_equipment import verify_conducting_equipment_constructor_default, verify_conducting_equipment_constructor_kwargs
from zepben.ewb import EarthFaultCompensator


def verify_earth_fault_compensator_constructor_default(efc: EarthFaultCompensator):
    verify_conducting_equipment_constructor_default(efc)
    assert efc.r is None


def verify_earth_fault_compensator_constructor_kwargs(efc: EarthFaultCompensator, r, **kwargs):
    verify_conducting_equipment_constructor_kwargs(efc, **kwargs)
    assert efc.r == r
