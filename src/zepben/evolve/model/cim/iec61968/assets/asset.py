#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, Generator, List, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import AssetOrganisationRole

from zepben.evolve.model.cim.iec61968.common.location import Location
from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.evolve.util import get_by_mrid, nlen, ngen, safe_remove

__all__ = ["Asset", "AssetContainer"]


class Asset(IdentifiedObject):
    """
    Tangible resource of the utility, including power system equipment, various end devices, cabinets, buildings,
    etc. For electrical network equipment, the role of the asset is defined through PowerSystemResource and its
    subclasses, defined mainly in the Wires model (refer to IEC61970-301 and model package IEC61970::Wires). Asset
    description places emphasis on the physical characteristics of the equipment fulfilling that role.
    """

    location: Optional[Location] = None
    """`zepben.evolve.cim.iec61968.common.location.Location` of this asset"""

    _organisation_roles: Optional[List[AssetOrganisationRole]] = None

    def __init__(self, organisation_roles: List[AssetOrganisationRole] = None, **kwargs):
        super(Asset, self).__init__(**kwargs)
        if organisation_roles:
            for role in organisation_roles:
                self.add_organisation_role(role)

    def num_organisation_roles(self) -> int:
        """
        Get the number of `AssetOrganisationRole`s associated with this `Asset`.
        """
        return nlen(self._organisation_roles)

    @property
    def organisation_roles(self) -> Generator[AssetOrganisationRole, None, None]:
        """
        The `AssetOrganisationRole`s of this `Asset`.
        """
        return ngen(self._organisation_roles)

    def get_organisation_role(self, mrid: str) -> AssetOrganisationRole:
        """
        Get the `AssetOrganisationRole` for this asset identified by `mrid`.

        `mrid` the mRID of the required `AssetOrganisationRole`
        Returns The `AssetOrganisationRole` with the specified `mrid`.
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._organisation_roles, mrid)

    def add_organisation_role(self, role: AssetOrganisationRole) -> Asset:
        """
        `role` The `AssetOrganisationRole` to
        associate with this `Asset`.
        Returns A reference to this `Asset` to allow fluent use.
        Raises `ValueError` if another `AssetOrganisationRole` with the same `mrid` already exists in this `Asset`
        """
        if self._validate_reference(role, self.get_organisation_role, "An AssetOrganisationRole"):
            return self

        self._organisation_roles = list() if self._organisation_roles is None else self._organisation_roles
        self._organisation_roles.append(role)
        return self

    def remove_organisation_role(self, role: AssetOrganisationRole) -> Asset:
        """
        Disassociate an `AssetOrganisationRole` from this `Asset`.

        `role` the `AssetOrganisationRole` to
        disassociate with this `Asset`.
        Raises `ValueError` if `role` was not associated with this `Asset`.
        Returns A reference to this `Asset` to allow fluent use.
        """
        self._organisation_roles = safe_remove(self._organisation_roles, role)
        return self

    def clear_organisation_roles(self) -> Asset:
        """
        Clear all organisation roles.
        Returns self
        """
        self._organisation_roles = None
        return self


class AssetContainer(Asset):
    """
    Asset that is aggregation of other assets such as conductors, transformers, switchgear, land, fences, buildings,
    equipment, vehicles, etc.
    """
    pass
