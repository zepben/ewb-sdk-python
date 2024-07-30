#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.auxiliaryequipment.test_auxiliary_equipment import auxiliary_equipment_kwargs, verify_auxiliary_equipment_constructor_default, \
    verify_auxiliary_equipment_constructor_kwargs, verify_auxiliary_equipment_constructor_args, auxiliary_equipment_args
from hypothesis.strategies import lists, builds

from cim.collection_validator import validate_collection_unordered
from zepben.evolve import Sensor, ProtectionRelayFunction

sensor_kwargs = {
    **auxiliary_equipment_kwargs,
    "relay_functions": lists(builds(ProtectionRelayFunction), max_size=2)
}

sensor_args = [*auxiliary_equipment_args, [ProtectionRelayFunction()]]


def verify_sensor_constructor_default(sn: Sensor):
    verify_auxiliary_equipment_constructor_default(sn)
    assert len(list(sn.relay_functions)) == 0


def verify_sensor_constructor_kwargs(sn: Sensor, relay_functions, **kwargs):
    verify_auxiliary_equipment_constructor_kwargs(sn, **kwargs)

    assert list(sn.relay_functions) == relay_functions


def verify_sensor_constructor_args(sn: Sensor):
    verify_auxiliary_equipment_constructor_args(sn)
    assert list(sn.relay_functions) == sensor_args[-1]


def test_relay_functions_collection():
    validate_collection_unordered(Sensor,
                                  lambda mrid, _: ProtectionRelayFunction(mrid),
                                  Sensor.num_relay_functions,
                                  Sensor.get_relay_function,
                                  Sensor.relay_functions,
                                  Sensor.add_relay_function,
                                  Sensor.remove_relay_function,
                                  Sensor.clear_relay_function)
