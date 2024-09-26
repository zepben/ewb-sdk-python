#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis.strategies import floats, one_of, none
from zepben.evolve import EarthFaultCompensator

from cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from cim.iec61970.base.core.test_conducting_equipment import conducting_equipment_kwargs, conducting_equipment_args, \
    verify_conducting_equipment_constructor_default, verify_conducting_equipment_constructor_kwargs, verify_conducting_equipment_constructor_args

earth_fault_compensator_kwargs = {
    **conducting_equipment_kwargs,
    "r": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))
}

earth_fault_compensator_args = [*conducting_equipment_args, 1.0]


def verify_earth_fault_compensator_constructor_default(efc: EarthFaultCompensator):
    verify_conducting_equipment_constructor_default(efc)
    assert efc.r is None


def verify_earth_fault_compensator_constructor_kwargs(efc: EarthFaultCompensator, r, **kwargs):
    verify_conducting_equipment_constructor_kwargs(efc, **kwargs)
    assert efc.r == r


def verify_earth_fault_compensator_constructor_args(efc: EarthFaultCompensator):
    verify_conducting_equipment_constructor_args(efc)
    assert earth_fault_compensator_args[-1:] == [
        efc.r
    ]
