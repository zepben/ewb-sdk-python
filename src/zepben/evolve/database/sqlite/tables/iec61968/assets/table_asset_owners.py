#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_organisation_roles import TableAssetOrganisationRoles

__all__ = ["TableAssetOwners"]


class TableAssetOwners(TableAssetOrganisationRoles):

    @property
    def name(self) -> str:
        return "asset_owners"
