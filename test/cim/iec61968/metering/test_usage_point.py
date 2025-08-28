#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import builds, lists, booleans, text, integers, sampled_from
from zepben.ewb import Location, Equipment, PhaseCode
from zepben.ewb.model.cim.iec61968.metering.usage_point import UsagePoint
from zepben.ewb.model.cim.iec61968.metering.end_device import EndDevice

from cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE, MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER
from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from cim.private_collection_validator import validate_unordered_1234567890

usage_point_kwargs = {
    **identified_object_kwargs,
    "usage_point_location": builds(Location),
    "is_virtual": booleans(),
    "connection_category": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "rated_power": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "approved_inverter_capacity": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "phase_code": sampled_from(PhaseCode),
    "equipment": lists(builds(Equipment)),
    "end_devices": lists(builds(EndDevice))
}

usage_point_args = [*identified_object_args, Location(), True, "1", 1, 2, PhaseCode.XYN, [Equipment()], [EndDevice()]]


def test_usage_point_constructor_default():
    up = UsagePoint()

    verify_identified_object_constructor_default(up)
    assert up.usage_point_location is None
    assert up.is_virtual is None
    assert up.connection_category is None
    assert up.rated_power is None
    assert up.approved_inverter_capacity is None
    assert not list(up.equipment)
    assert not list(up.end_devices)


@given(**usage_point_kwargs)
def test_usage_point_constructor_kwargs(
    usage_point_location,
    is_virtual,
    connection_category,
    rated_power,
    approved_inverter_capacity,
    phase_code,
    equipment,
    end_devices,
    **kwargs
):
    up = UsagePoint(usage_point_location=usage_point_location,
                    is_virtual=is_virtual,
                    connection_category=connection_category,
                    rated_power=rated_power,
                    approved_inverter_capacity=approved_inverter_capacity,
                    phase_code=phase_code,
                    equipment=equipment,
                    end_devices=end_devices,
                    **kwargs)

    verify_identified_object_constructor_kwargs(up, **kwargs)
    assert up.usage_point_location == usage_point_location
    assert up.is_virtual == is_virtual
    assert up.connection_category == connection_category
    assert up.rated_power == rated_power
    assert up.approved_inverter_capacity == approved_inverter_capacity
    assert up.phase_code == phase_code
    assert list(up.equipment) == equipment
    assert list(up.end_devices) == end_devices


def test_usage_point_constructor_args():
    up = UsagePoint(*usage_point_args)

    verify_identified_object_constructor_args(up)

    assert usage_point_args[-8:] == [
        up.usage_point_location,
        up.is_virtual,
        up.connection_category,
        up.rated_power,
        up.approved_inverter_capacity,
        up.phase_code,
        list(up.equipment),
        list(up.end_devices)
    ]


def test_equipment_collection():
    validate_unordered_1234567890(
        UsagePoint,
        lambda mrid: Equipment(mrid),
        UsagePoint.equipment,
        UsagePoint.num_equipment,
        UsagePoint.get_equipment,
        UsagePoint.add_equipment,
        UsagePoint.remove_equipment,
        UsagePoint.clear_equipment
    )


def test_end_devices_collection():
    validate_unordered_1234567890(
        UsagePoint,
        lambda mrid: EndDevice(mrid),
        UsagePoint.end_devices,
        UsagePoint.num_end_devices,
        UsagePoint.get_end_device,
        UsagePoint.add_end_device,
        UsagePoint.remove_end_device,
        UsagePoint.clear_end_devices
    )
