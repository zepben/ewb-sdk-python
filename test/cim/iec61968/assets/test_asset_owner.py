#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import data

from cim.common_testing_functions import verify
from test.cim.iec61968.assets.test_asset_organisation_role import asset_organisation_role_kwargs, verify_asset_organisation_role_constructor_default, \
    verify_asset_organisation_role_constructor_kwargs, verify_asset_organisation_role_constructor_args, asset_organisation_role_args
from zepben.evolve import AssetOwner, create_name, create_name_type
from zepben.evolve.model.cim.iec61968.assets.create_assets_components import create_asset_owner

asset_owner_kwargs = asset_organisation_role_kwargs
asset_owner_args = asset_organisation_role_args


def test_asset_owner_constructor_default():
    verify_asset_organisation_role_constructor_default(AssetOwner())
    verify_asset_organisation_role_constructor_default(create_asset_owner())


# noinspection PyShadowingNames
@given(data())
def test_asset_owner_constructor_kwargs(data):
    verify(
        [AssetOwner, create_asset_owner],
        data, asset_owner_kwargs, verify_asset_organisation_role_constructor_kwargs
    )


def test_asset_owner_constructor_args():
    # noinspection PyArgumentList
    verify_asset_organisation_role_constructor_args(AssetOwner(*asset_owner_args))


def test_auto_two_way_connections_for_asset_owner_constructor():
    name = create_name(name='name', type=create_name_type(name='nameType'))
    ao = create_asset_owner(names=[name])

    assert name.identified_object == ao
