#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import builds, lists

from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from zepben.evolve import UsagePoint, Location, Equipment, EndDevice

usage_point_kwargs = {
    **identified_object_kwargs,
    "usage_point_location": builds(Location),
    "equipment": lists(builds(Equipment)),
    "end_devices": lists(builds(EndDevice))
}

usage_point_args = [*identified_object_args, Location(), [Equipment()], [EndDevice()]]


def test_usage_point_constructor_default():
    up = UsagePoint()

    verify_identified_object_constructor_default(up)
    assert not up.usage_point_location
    assert not list(up.equipment)
    assert not list(up.end_devices)


@given(**usage_point_kwargs)
def test_usage_point_constructor_kwargs(usage_point_location, equipment, end_devices, **kwargs):
    up = UsagePoint(usage_point_location=usage_point_location,
                    equipment=equipment,
                    end_devices=end_devices,
                    **kwargs)

    verify_identified_object_constructor_kwargs(up, **kwargs)
    assert up.usage_point_location == usage_point_location
    assert list(up.equipment) == equipment
    assert list(up.end_devices) == end_devices


def test_usage_point_constructor_args():
    up = UsagePoint(*usage_point_args)

    verify_identified_object_constructor_args(up)
    assert up.usage_point_location == usage_point_args[-3]
    assert list(up.equipment) == usage_point_args[-2]
    assert list(up.end_devices) == usage_point_args[-1]
