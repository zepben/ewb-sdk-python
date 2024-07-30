#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.iec61970.base.auxiliaryequipment.test_auxiliary_equipment import auxiliary_equipment_kwargs, verify_auxiliary_equipment_constructor_default, \
    verify_auxiliary_equipment_constructor_kwargs, verify_auxiliary_equipment_constructor_args, auxiliary_equipment_args
from zepben.evolve import FaultIndicator

fault_indicator_kwargs = auxiliary_equipment_kwargs
fault_indicator_args = auxiliary_equipment_args


def test_fault_indicator_constructor_default():
    verify_auxiliary_equipment_constructor_default(FaultIndicator())


@given(**fault_indicator_kwargs)
def test_fault_indicator_constructor_kwargs(**kwargs):
    # noinspection PyArgumentList
    verify_auxiliary_equipment_constructor_kwargs(FaultIndicator(**kwargs), **kwargs)


def test_fault_indicator_constructor_args():
    # noinspection PyArgumentList
    verify_auxiliary_equipment_constructor_args(FaultIndicator(*fault_indicator_args))
