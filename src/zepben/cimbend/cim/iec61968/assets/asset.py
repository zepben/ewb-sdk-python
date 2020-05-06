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

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Set, Generator

from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.cimbend.util import get_by_mrid, nlen, require, contains_mrid, ngen

__all__ = ["Asset", "AssetContainer"]


@dataclass
class Asset(IdentifiedObject):
    """
    Tangible resource of the utility, including power system equipment, various end devices, cabinets, buildings,
    etc. For electrical network equipment, the role of the asset is defined through PowerSystemResource and its
    subclasses, defined mainly in the Wires model (refer to IEC61970-301 and model package IEC61970::Wires). Asset
    description places emphasis on the physical characteristics of the equipment fulfilling that role.

    Attributes:
        _organisation_roles: The :class:`asset_organisation_role.AssetOrganisationRole`s for this ``Asset``
    """

    _organisation_roles: Optional[Set[AssetOrganisationRole]] = None

    @property
    def num_organisation_roles(self) -> int:
        """
        Get the number of entries in the :class:`zepben.cimbend.iec61968.assets.asset_organisation_role
        .AssetOrganisationRole` collection.
        """
        return nlen(self._organisation_roles)

    @property
    def organisation_roles(self) -> Generator[AssetOrganisationRole, None, None]:
        """
        :return: Generator over the ``AssetOrganisationRole``s of this ``Asset``.
        """
        return ngen(self._organisation_roles)

    def get_organisation_role(self, mrid: str) -> AssetOrganisationRole:
        """
        Get the ``AssetOrganisationRole`` for this asset identified by ``mrid``.

        :param mrid: the mRID of the required :class:`zepben.cimbend.iec61968.assets.asset_organisation_role
        .AssetOrganisationRole`
        :return: The :class:`zepben.cimbend.iec61968.assets.asset_organisation_role.AssetOrganisationRole` with the
        specified ``mrid``.
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._organisation_roles, mrid)

    def add_organisation_role(self, role: AssetOrganisationRole) -> Asset:
        """
        :param role: the :class:`zepben.cimbend.iec61968.assets.asset_organisation_role.AssetOrganisationRole` to
        associate with this ``Asset``.
        :return: A reference to this ``Asset`` to allow fluent use.
        """
        require(not contains_mrid(self._organisation_roles, role.mrid),
                lambda: f"An organisation role with mRID {role.mrid} already exists in {str(self)}.")
        self._organisation_roles = set() if self._organisation_roles is None else self._organisation_roles
        self._organisation_roles.add(role)
        return self

    def remove_organisation_role(self, role: AssetOrganisationRole) -> Asset:
        """
        :param role: the :class:`zepben.cimbend.iec61968.assets.asset_organisation_role.AssetOrganisationRole` to
        disassociate with this ``Asset``.
        :raises: KeyError if ``role`` was not associated with this ``Asset``.
        """
        if self._organisation_roles is not None:
            self._organisation_roles.remove(role)
            if not self._organisation_roles:
                self._organisation_roles = None
        else:
            raise KeyError(role)

        return self

    def clear_organisation_roles(self) -> Asset:
        """
        Clear all organisation roles.
        :return: self
        """
        self._organisation_roles = None
        return self


class AssetContainer(Asset):
    """
    Asset that is aggregation of other assets such as conductors, transformers, switchgear, land, fences, buildings,
    equipment, vehicles, etc.
    """
    pass
