#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61968.common.test_organisation_role import organisation_role_kwargs, verify_organisation_role_constructor_default, \
    verify_organisation_role_constructor_kwargs, verify_organisation_role_constructor_args, organisation_role_args
from zepben.evolve import AssetOrganisationRole

asset_organisation_role_kwargs = organisation_role_kwargs
asset_organisation_role_args = organisation_role_args


def verify_asset_organisation_role_constructor_default(aor: AssetOrganisationRole):
    verify_organisation_role_constructor_default(aor)


def verify_asset_organisation_role_constructor_kwargs(aor: AssetOrganisationRole, **kwargs):
    verify_organisation_role_constructor_kwargs(aor, **kwargs)


def verify_asset_organisation_role_constructor_args(aor: AssetOrganisationRole):
    verify_organisation_role_constructor_args(aor)
