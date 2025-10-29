#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.iec61970.base.auxiliaryequipment.test_auxiliary_equipment import auxiliary_equipment_kwargs, verify_auxiliary_equipment_constructor_default, \
    verify_auxiliary_equipment_constructor_kwargs, verify_auxiliary_equipment_constructor_args, auxiliary_equipment_args
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.fault_indicator import FaultIndicator

fault_indicator_kwargs = auxiliary_equipment_kwargs
fault_indicator_args = auxiliary_equipment_args


def test_fault_indicator_constructor_default():
    verify_auxiliary_equipment_constructor_default(FaultIndicator())


@given(**fault_indicator_kwargs)
def test_fault_indicator_constructor_kwargs(**kwargs):
    verify_auxiliary_equipment_constructor_kwargs(FaultIndicator(**kwargs), **kwargs)


from pytest import mark
@mark.skip(reason="Args are deprecated")
def test_fault_indicator_constructor_args():
    verify_auxiliary_equipment_constructor_args(FaultIndicator(*fault_indicator_args))
