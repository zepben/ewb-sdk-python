#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from test.cim.iec61968.assets.test_asset_organisation_role import asset_organisation_role_kwargs, verify_asset_organisation_role_constructor_default, \
    verify_asset_organisation_role_constructor_kwargs, verify_asset_organisation_role_constructor_args, asset_organisation_role_args
from zepben.evolve import AssetOwner
from zepben.evolve.model.cim.iec61968.assets.create_assets_components import create_asset_owner

asset_owner_kwargs = asset_organisation_role_kwargs
asset_owner_args = asset_organisation_role_args


def test_asset_owner_constructor_default():
    verify_asset_organisation_role_constructor_default(AssetOwner())
    verify_asset_organisation_role_constructor_default(create_asset_owner())


@given(**asset_owner_kwargs)
def test_asset_owner_constructor_kwargs(**kwargs):
    # noinspection PyArgumentList
    verify_asset_organisation_role_constructor_kwargs(AssetOwner(**kwargs), **kwargs)


@given(**asset_owner_kwargs)
def test_asset_owner_creator(**kwargs):
    # noinspection PyArgumentList
    verify_asset_organisation_role_constructor_kwargs(create_asset_owner(**kwargs), **kwargs)


def test_asset_owner_constructor_args():
    # noinspection PyArgumentList
    verify_asset_organisation_role_constructor_args(AssetOwner(*asset_owner_args))
