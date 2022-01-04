#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import builds, lists, booleans, text, data
from test.cim.common_testing_functions import verify
from test.cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE
from test.cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from zepben.evolve import UsagePoint, Location, Equipment, EndDevice
from zepben.evolve.model.cim.iec61968.metering.create_metering_components import create_usage_point

usage_point_kwargs = {
    **identified_object_kwargs,
    "usage_point_location": builds(Location),
    "is_virtual": booleans(),
    "connection_category": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "equipment": lists(builds(Equipment)),
    "end_devices": lists(builds(EndDevice))
}

usage_point_args = [*identified_object_args, Location(), True, "1", [Equipment()], [EndDevice()]]


def test_usage_point_constructor_default():
    up = UsagePoint()
    up2 = create_usage_point()
    verify_default_usage_point(up)
    verify_default_usage_point(up2)


def verify_default_usage_point(up):
    verify_identified_object_constructor_default(up)
    assert not up.usage_point_location
    assert not up.is_virtual
    assert not up.connection_category
    assert not list(up.equipment)
    assert not list(up.end_devices)


# noinspection PyShadowingNames
@given(data())
def test_usage_point_constructor_kwargs(data):
    verify(
        [UsagePoint, create_usage_point],
        data, usage_point_kwargs, verify_usage_point_values
    )


def verify_usage_point_values(up, usage_point_location, is_virtual, connection_category, equipment, end_devices, **kwargs):
    verify_identified_object_constructor_kwargs(up, **kwargs)
    assert up.usage_point_location == usage_point_location
    assert up.is_virtual == is_virtual
    assert up.connection_category == connection_category
    assert list(up.equipment) == equipment
    assert list(up.end_devices) == end_devices


def test_usage_point_constructor_args():
    up = UsagePoint(*usage_point_args)

    verify_identified_object_constructor_args(up)
    assert up.usage_point_location == usage_point_args[-5]
    assert up.is_virtual == usage_point_args[-4]
    assert up.connection_category == usage_point_args[-3]
    assert list(up.equipment) == usage_point_args[-2]
    assert list(up.end_devices) == usage_point_args[-1]


def test_auto_two_way_connections_for_usage_point_constructor():
    e = Equipment()
    ed = EndDevice()
    up = create_usage_point(equipment=[e], end_devices=[ed])

    assert e.get_usage_point(up.mrid) == up
    assert ed.get_usage_point(up.mrid) == up
