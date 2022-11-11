#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.auxiliaryequipment.test_auxiliary_equipment import auxiliary_equipment_kwargs, verify_auxiliary_equipment_constructor_default, \
    verify_auxiliary_equipment_constructor_kwargs, verify_auxiliary_equipment_constructor_args, auxiliary_equipment_args
from zepben.evolve import Sensor

sensor_kwargs = auxiliary_equipment_kwargs
sensor_args = auxiliary_equipment_args


def verify_sensor_constructor_default(sn: Sensor):
    verify_auxiliary_equipment_constructor_default(sn)


def verify_sensor_constructor_kwargs(sn: Sensor, **kwargs):
    verify_auxiliary_equipment_constructor_kwargs(sn, **kwargs)


def verify_sensor_constructor_args(sn: Sensor):
    verify_auxiliary_equipment_constructor_args(sn)
