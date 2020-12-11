#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.model.cim.iec61968.common.organisation_role import OrganisationRole

__all__ = ["AssetOrganisationRole", "AssetOwner"]


class AssetOrganisationRole(OrganisationRole):
    """ Role an organisation plays with respect to asset. """
    pass


class AssetOwner(AssetOrganisationRole):
    """ Owner of the Asset """
    pass

