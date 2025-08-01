#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis.strategies import text, builds, lists

from cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE
from cim.iec61968.assets.test_asset_container import asset_container_kwargs, verify_asset_container_constructor_default, \
    verify_asset_container_constructor_kwargs, verify_asset_container_constructor_args, asset_container_args
from cim.private_collection_validator import validate_unordered_1234567890
from zepben.ewb import Location
from zepben.ewb.model.cim.iec61968.metering.end_device_function import EndDeviceFunction
from zepben.ewb.model.cim.iec61968.metering.usage_point import UsagePoint
from zepben.ewb.model.cim.iec61968.metering.end_device import EndDevice

end_device_kwargs = {
    **asset_container_kwargs,
    "customer_mrid": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "service_location": builds(Location),
    "usage_points": lists(builds(UsagePoint), max_size=2)
}

end_device_args = [*asset_container_args, "a", Location(), [UsagePoint]]


def verify_end_device_constructor_default(ed: EndDevice):
    verify_asset_container_constructor_default(ed)
    assert not ed.customer_mrid
    assert not ed.service_location
    assert not list(ed.usage_points)


def verify_end_device_constructor_kwargs(ed: EndDevice, customer_mrid, service_location, usage_points, **kwargs):
    verify_asset_container_constructor_kwargs(ed, **kwargs)
    assert ed.customer_mrid == customer_mrid
    assert ed.service_location == service_location
    assert list(ed.usage_points) == usage_points


def verify_end_device_constructor_args(ed: EndDevice):
    verify_asset_container_constructor_args(ed)
    assert end_device_args[-3:] == [
        ed.customer_mrid,
        ed.service_location,
        list(ed.usage_points)
    ]


def test_usage_points_collection():
    validate_unordered_1234567890(
        EndDevice,
        lambda mrid: UsagePoint(mrid),
        EndDevice.usage_points,
        EndDevice.num_usage_points,
        EndDevice.get_usage_point,
        EndDevice.add_usage_point,
        EndDevice.remove_usage_point,
        EndDevice.clear_usage_points
    )


def test_end_device_function_collection():
    validate_unordered_1234567890(
        EndDevice,
        lambda mrid: EndDeviceFunction(mrid),
        EndDevice.functions,
        EndDevice.num_functions,
        EndDevice.get_function,
        EndDevice.add_function,
        EndDevice.remove_function,
        EndDevice.clear_functions
    )
