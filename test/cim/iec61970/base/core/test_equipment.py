#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import datetime

from hypothesis.strategies import booleans, lists, builds, datetimes

from cim.cim_creators import sampled_equipment_container, sampled_hvlv_feeder
from cim.iec61970.base.core.test_power_system_resource import power_system_resource_kwargs, verify_power_system_resource_constructor_default, \
    verify_power_system_resource_constructor_kwargs, verify_power_system_resource_constructor_args, power_system_resource_args
from cim.private_collection_validator import validate_unordered
from util import mrid_strategy
from zepben.ewb import Equipment, OperationalRestriction, EquipmentContainer, generate_id
from zepben.ewb.model.cim.iec61968.metering.usage_point import UsagePoint
from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder

equipment_kwargs = {
    **power_system_resource_kwargs,
    "in_service": booleans(),
    "normally_in_service": booleans(),
    "commissioned_date": datetimes(),
    "usage_points": lists(builds(UsagePoint, mrid=mrid_strategy), max_size=2),
    "equipment_containers": lists(sampled_equipment_container(True), max_size=2),
    "operational_restrictions": lists(builds(OperationalRestriction, mrid=mrid_strategy), max_size=2),
    "current_containers": lists(sampled_hvlv_feeder(True), max_size=2),
}

equipment_args = [
    *power_system_resource_args,
    False,
    False,
    datetime.datetime(2023, 1, 2),
    [UsagePoint(mrid=generate_id()), UsagePoint(mrid=generate_id())],
    [EquipmentContainer(mrid=generate_id()), EquipmentContainer(mrid=generate_id())],
    [OperationalRestriction(mrid=generate_id()), OperationalRestriction(mrid=generate_id())],
    [Feeder(mrid=generate_id()), Feeder(mrid=generate_id())]
]


def verify_equipment_constructor_default(eq: Equipment):
    verify_power_system_resource_constructor_default(eq)
    assert eq.in_service
    assert eq.normally_in_service
    assert not eq.commissioned_date
    assert not list(eq.usage_points)
    assert not list(eq.containers)
    assert not list(eq.operational_restrictions)
    assert not list(eq.current_containers)


def verify_equipment_constructor_kwargs(eq: Equipment, in_service, normally_in_service, commissioned_date, usage_points, equipment_containers,
                                        operational_restrictions,
                                        current_containers, **kwargs):
    verify_power_system_resource_constructor_kwargs(eq, **kwargs)
    assert eq.in_service == in_service
    assert eq.normally_in_service == normally_in_service
    assert eq.commissioned_date == commissioned_date
    assert list(eq.usage_points) == usage_points
    assert list(eq.containers) == equipment_containers
    assert list(eq.operational_restrictions) == operational_restrictions
    assert list(eq.current_containers) == current_containers


def verify_equipment_constructor_args(eq: Equipment):
    verify_power_system_resource_constructor_args(eq)
    assert equipment_args[-7:] == [
        eq.in_service,
        eq.normally_in_service,
        eq.commissioned_date,
        list(eq.usage_points),
        list(eq.containers),
        list(eq.operational_restrictions),
        list(eq.current_containers)
    ]


def test_usage_points_collection():
    validate_unordered(
        Equipment,
        lambda mrid: UsagePoint(mrid),
        Equipment.usage_points,
        Equipment.num_usage_points,
        Equipment.get_usage_point,
        Equipment.add_usage_point,
        Equipment.remove_usage_point,
        Equipment.clear_usage_points
    )


def test_equipment_containers_collection():
    validate_unordered(
        Equipment,
        lambda mrid: EquipmentContainer(mrid),
        Equipment.containers,
        Equipment.num_containers,
        Equipment.get_container,
        Equipment.add_container,
        Equipment.remove_container,
        Equipment.clear_containers
    )


def test_operational_restrictions_collection():
    validate_unordered(
        Equipment,
        lambda mrid: OperationalRestriction(mrid),
        Equipment.operational_restrictions,
        Equipment.num_operational_restrictions,
        Equipment.get_operational_restriction,
        Equipment.add_operational_restriction,
        Equipment.remove_operational_restriction,
        Equipment.clear_operational_restrictions
    )


def test_current_containers_collection():
    validate_unordered(
        Equipment,
        lambda mrid: EquipmentContainer(mrid),
        Equipment.current_containers,
        Equipment.num_current_containers,
        Equipment.get_current_container,
        Equipment.add_current_container,
        Equipment.remove_current_container,
        Equipment.clear_current_containers
    )
