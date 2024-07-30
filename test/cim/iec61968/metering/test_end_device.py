#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis.strategies import text, builds, lists

from cim.collection_validator import validate_collection_unordered
from cim.iec61968.assets.test_asset_container import asset_container_kwargs, verify_asset_container_constructor_default, \
    verify_asset_container_constructor_kwargs, verify_asset_container_constructor_args, asset_container_args
from cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE
from zepben.evolve import EndDevice, Location, UsagePoint

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
    assert ed.customer_mrid == end_device_args[-3]
    assert ed.service_location == end_device_args[-2]
    assert list(ed.usage_points) == end_device_args[-1]


def test_usage_points_collection():
    validate_collection_unordered(EndDevice,
                                  lambda mrid, _: UsagePoint(mrid),
                                  EndDevice.num_usage_points,
                                  EndDevice.get_usage_point,
                                  EndDevice.usage_points,
                                  EndDevice.add_usage_point,
                                  EndDevice.remove_usage_point,
                                  EndDevice.clear_usage_points)
