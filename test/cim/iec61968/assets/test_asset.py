#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis.strategies import builds, lists

from util import mrid_strategy
from zepben.ewb import Asset, Location, AssetOrganisationRole, PowerSystemResource, generate_id

from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from cim.private_collection_validator import validate_unordered

asset_kwargs = {
    **identified_object_kwargs,
    "location": builds(Location, mrid=mrid_strategy),
    "organisation_roles": lists(builds(AssetOrganisationRole, mrid=mrid_strategy), max_size=2),
    "power_system_resources": lists(builds(PowerSystemResource, mrid=mrid_strategy), max_size=2)
}

asset_args = [*identified_object_args, Location(mrid=generate_id()), [AssetOrganisationRole(mrid=generate_id())], [PowerSystemResource(mrid=generate_id())]]


def verify_asset_constructor_default(a: Asset):
    verify_identified_object_constructor_default(a)
    assert not a.location
    assert not list(a.organisation_roles)
    assert not list(a.power_system_resources)


def verify_asset_constructor_kwargs(a: Asset, location, organisation_roles, power_system_resources, **kwargs):
    verify_identified_object_constructor_kwargs(a, **kwargs)
    assert a.location == location
    assert list(a.organisation_roles) == organisation_roles
    assert list(a.power_system_resources) == power_system_resources


def verify_asset_constructor_args(a: Asset):
    verify_identified_object_constructor_args(a)
    assert asset_args[-3:] == [
        a.location,
        list(a.organisation_roles),
        list(a.power_system_resources)
    ]


def test_organisation_roles_collection():
    validate_unordered(
        Asset,
        lambda mrid: AssetOrganisationRole(mrid),
        Asset.organisation_roles,
        Asset.num_organisation_roles,
        Asset.get_organisation_role,
        Asset.add_organisation_role,
        Asset.remove_organisation_role,
        Asset.clear_organisation_roles
    )


def test_power_system_resources_collection():
    validate_unordered(
        Asset,
        lambda mrid: PowerSystemResource(mrid),
        Asset.power_system_resources,
        Asset.num_power_system_resources,
        Asset.get_power_system_resource,
        Asset.add_power_system_resource,
        Asset.remove_power_system_resource,
        Asset.clear_power_system_resources
    )
