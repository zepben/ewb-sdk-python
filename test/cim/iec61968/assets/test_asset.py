#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis.strategies import builds, lists
from zepben.evolve import Asset, Location, AssetOrganisationRole

from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from cim.private_collection_validator import validate_unordered_1234567890

asset_kwargs = {
    **identified_object_kwargs,
    "location": builds(Location),
    "organisation_roles": lists(builds(AssetOrganisationRole), max_size=2)
}

asset_args = [*identified_object_args, Location(), [AssetOrganisationRole()]]


def verify_asset_constructor_default(a: Asset):
    verify_identified_object_constructor_default(a)
    assert not a.location
    assert not list(a.organisation_roles)


def verify_asset_constructor_kwargs(a: Asset, location, organisation_roles, **kwargs):
    verify_identified_object_constructor_kwargs(a, **kwargs)
    assert a.location == location
    assert list(a.organisation_roles) == organisation_roles


def verify_asset_constructor_args(a: Asset):
    verify_identified_object_constructor_args(a)
    assert asset_args[-2:] == [
        a.location,
        list(a.organisation_roles)
    ]


def test_organisation_roles_collection():
    validate_unordered_1234567890(
        Asset,
        lambda mrid: AssetOrganisationRole(mrid),
        Asset.organisation_roles,
        Asset.num_organisation_roles,
        Asset.get_organisation_role,
        Asset.add_organisation_role,
        Asset.remove_organisation_role,
        Asset.clear_organisation_roles
    )
