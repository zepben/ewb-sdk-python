#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import datetime

from hypothesis.strategies import booleans, lists, builds, datetimes

from cim.collection_validator import validate_collection_unordered
from cim.iec61970.base.core.test_power_system_resource import power_system_resource_kwargs, verify_power_system_resource_constructor_default, \
    verify_power_system_resource_constructor_kwargs, verify_power_system_resource_constructor_args, power_system_resource_args
from cim.cim_creators import sampled_equipment_container, sampled_hvlv_feeder
from zepben.evolve import Equipment, UsagePoint, OperationalRestriction, Feeder, EquipmentContainer

equipment_kwargs = {
    **power_system_resource_kwargs,
    "in_service": booleans(),
    "normally_in_service": booleans(),
    "commissioned_date": datetimes(),
    "usage_points": lists(builds(UsagePoint), max_size=2),
    "equipment_containers": lists(sampled_equipment_container(True), max_size=2),
    "operational_restrictions": lists(builds(OperationalRestriction), max_size=2),
    "current_containers": lists(sampled_hvlv_feeder(True), max_size=2),
}

equipment_args = [*power_system_resource_args, False, False, datetime.datetime(2023, 1, 2), [UsagePoint(), UsagePoint()],
                  [EquipmentContainer(), EquipmentContainer()],
                  [OperationalRestriction(), OperationalRestriction()], [Feeder(), Feeder()]]


def verify_equipment_constructor_default(eq: Equipment):
    verify_power_system_resource_constructor_default(eq)
    assert eq.in_service
    assert eq.normally_in_service
    assert not eq.commissioned_date
    assert not list(eq.usage_points)
    assert not list(eq.containers)
    assert not list(eq.operational_restrictions)
    assert not list(eq.current_containers)


def verify_equipment_constructor_kwargs(eq: Equipment, in_service, normally_in_service, commissioned_date, usage_points, equipment_containers, operational_restrictions,
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
    assert eq.in_service == equipment_args[-7]
    assert eq.normally_in_service == equipment_args[-6]
    assert eq.commissioned_date == equipment_args[-5]
    assert list(eq.usage_points) == equipment_args[-4]
    assert list(eq.containers) == equipment_args[-3]
    assert list(eq.operational_restrictions) == equipment_args[-2]
    assert list(eq.current_containers) == equipment_args[-1]


def test_usage_points_collection():
    validate_collection_unordered(Equipment,
                                  lambda mrid, _: UsagePoint(mrid),
                                  Equipment.num_usage_points,
                                  Equipment.get_usage_point,
                                  Equipment.usage_points,
                                  Equipment.add_usage_point,
                                  Equipment.remove_usage_point,
                                  Equipment.clear_usage_points)


def test_equipment_containers_collection():
    validate_collection_unordered(Equipment,
                                  lambda mrid, _: EquipmentContainer(mrid),
                                  Equipment.num_containers,
                                  Equipment.get_container,
                                  Equipment.containers,
                                  Equipment.add_container,
                                  Equipment.remove_container,
                                  Equipment.clear_containers)


def test_operational_restrictions_collection():
    validate_collection_unordered(Equipment,
                                  lambda mrid, _: OperationalRestriction(mrid),
                                  Equipment.num_operational_restrictions,
                                  Equipment.get_operational_restriction,
                                  Equipment.operational_restrictions,
                                  Equipment.add_operational_restriction,
                                  Equipment.remove_operational_restriction,
                                  Equipment.clear_operational_restrictions)


def test_current_containers_collection():
    validate_collection_unordered(Equipment,
                                  lambda mrid, _: EquipmentContainer(mrid),
                                  Equipment.num_current_containers,
                                  Equipment.get_current_container,
                                  Equipment.current_containers,
                                  Equipment.add_current_container,
                                  Equipment.remove_current_container,
                                  Equipment.clear_current_containers)
