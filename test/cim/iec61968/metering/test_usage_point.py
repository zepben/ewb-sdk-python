#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given

from cim.fill_fields import usage_point_kwargs
from cim.iec61970.base.core.test_identified_object import verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs
from cim.private_collection_validator import validate_unordered
from util import assert_or_empty
from zepben.ewb import Equipment, generate_id
from zepben.ewb.model.cim.extensions.iec61968.common.contact_details import ContactDetails
from zepben.ewb.model.cim.iec61968.metering.end_device import EndDevice
from zepben.ewb.model.cim.iec61968.metering.usage_point import UsagePoint


def test_usage_point_constructor_default():
    up = UsagePoint(mrid=generate_id())

    verify_identified_object_constructor_default(up)
    assert up.usage_point_location is None
    assert up.is_virtual is None
    assert up.connection_category is None
    assert up.rated_power is None
    assert up.approved_inverter_capacity is None
    assert not list(up.equipment)
    assert not list(up.end_devices)


@given(**usage_point_kwargs())
def test_usage_point_constructor_kwargs(
    usage_point_location,
    is_virtual,
    connection_category,
    rated_power,
    approved_inverter_capacity,
    phase_code,
    equipment,
    end_devices,
    contacts,
    **kwargs,
):
    up = UsagePoint(
        usage_point_location=usage_point_location,
        is_virtual=is_virtual,
        connection_category=connection_category,
        rated_power=rated_power,
        approved_inverter_capacity=approved_inverter_capacity,
        phase_code=phase_code,
        equipment=equipment,
        end_devices=end_devices,
        contacts=contacts,
        **kwargs,
    )

    verify_identified_object_constructor_kwargs(up, **kwargs)
    assert up.usage_point_location == usage_point_location
    assert up.is_virtual == is_virtual
    assert up.connection_category == connection_category
    assert up.rated_power == rated_power
    assert up.approved_inverter_capacity == approved_inverter_capacity
    assert up.phase_code == phase_code
    assert_or_empty(up.equipment, equipment)
    assert_or_empty(up.end_devices, end_devices)
    assert_or_empty(up.contacts, contacts)


def test_equipment_collection():
    validate_unordered(
        UsagePoint,
        Equipment,
        UsagePoint.equipment,
        UsagePoint.num_equipment,
        UsagePoint.get_equipment,
        UsagePoint.add_equipment,
        UsagePoint.remove_equipment,
        UsagePoint.clear_equipment,
    )


def test_end_devices_collection():
    validate_unordered(
        UsagePoint,
        EndDevice,
        UsagePoint.end_devices,
        UsagePoint.num_end_devices,
        UsagePoint.get_end_device,
        UsagePoint.add_end_device,
        UsagePoint.remove_end_device,
        UsagePoint.clear_end_devices,
    )


def test_contacts_collection():
    validate_unordered(
        UsagePoint,
        ContactDetails,
        UsagePoint.contacts,
        UsagePoint.num_contacts,
        UsagePoint.get_contact,
        UsagePoint.add_contact,
        UsagePoint.remove_contact,
        UsagePoint.clear_contacts,
    )
