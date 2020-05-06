"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""


from dataclasses import dataclass

from zepben.cimbend.cim.iec61968.common.organisation_role import OrganisationRole

__all__ = ["AssetOrganisationRole", "AssetOwner"]


class AssetOrganisationRole(OrganisationRole):
    """ Role an organisation plays with respect to asset. """
    pass


@dataclass
class AssetOwner(AssetOrganisationRole):
    """ Owner of the Asset """
    pass

