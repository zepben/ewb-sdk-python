#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.core.test_identified_object import verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from cim.private_collection_validator import validate_unordered
from zepben.ewb import PowerSystemResource, Location, PowerTransformerInfo, Asset, generate_id

power_system_resource_args = [
    *identified_object_args,
    Location(mrid=generate_id()),
    PowerTransformerInfo(mrid=generate_id()),
    1,
    [Asset(mrid=generate_id())]
]


def verify_power_system_resource_constructor_default(psr: PowerSystemResource):
    verify_identified_object_constructor_default(psr)
    assert psr.location is None
    assert psr.asset_info is None
    assert psr.num_controls is None
    assert not list(psr.assets)


def verify_power_system_resource_constructor_kwargs(psr: PowerSystemResource, location, num_controls, assets, asset_info = None, **kwargs):
    verify_identified_object_constructor_kwargs(psr, **kwargs)
    assert psr.location is location
    assert psr.asset_info is asset_info
    assert psr.num_controls == num_controls
    assert list(psr.assets) == assets


def verify_power_system_resource_constructor_args(psr: PowerSystemResource):
    verify_identified_object_constructor_args(psr)
    assert power_system_resource_args[-4:] == [
        psr.location,
        psr.asset_info,
        psr.num_controls,
        list(psr.assets)
    ]


def test_assets_collection():
    validate_unordered(
        PowerSystemResource,
        Asset,
        PowerSystemResource.assets,
        PowerSystemResource.num_assets,
        PowerSystemResource.get_asset,
        PowerSystemResource.add_asset,
        PowerSystemResource.remove_asset,
        PowerSystemResource.clear_assets
    )
