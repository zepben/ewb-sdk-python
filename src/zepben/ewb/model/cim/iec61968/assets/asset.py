#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Asset"]

from typing import Optional, List, TYPE_CHECKING
from abc import ABCMeta
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.boilerplate.collections.lazy_mrid_list import LazyMridList
from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.assets.asset_organisation_role import AssetOrganisationRole
    from zepben.ewb.model.cim.iec61968.common.location import Location
    from zepben.ewb.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource


@zb_dataclass
class Asset(IdentifiedObject, metaclass=ABCMeta):
    """
    Tangible resource of the utility, including power system equipment, various end devices, cabinets, buildings,
    etc. For electrical network equipment, the role of the asset is defined through PowerSystemResource and its
    subclasses, defined mainly in the Wires model (refer to IEC61970-301 and model package IEC61970::Wires). Asset
    description places emphasis on the physical characteristics of the equipment fulfilling that role.
    """

    location: Optional[Location] = None
    """`zepben.ewb.model.cim.iec61968.common.location.Location` of this asset"""

    _organisation_roles: Optional[List[AssetOrganisationRole]] = field(default=None)

    _power_system_resources: Optional[List[PowerSystemResource]] = field(default=None)

    organisation_roles: MridCollection[AssetOrganisationRole] = LazyMridList(
        _organisation_roles,
        "An AssetOrganisationRole",
    )

    power_system_resources: MridCollection[PowerSystemResource] = LazyMridList(
        _power_system_resources,
        "An PowerSystemResource",
    )


    # region deprecated list boilerplate
    # region organisation_roles boilerplate

    @deprecated("Use len(obj.organisation_roles) instead.")
    def num_organisation_roles(self) -> int:
        return len(self.organisation_roles)

    @deprecated("Use obj.organisation_roles.get_by_mrid(mrid) instead.")
    def get_organisation_role(self, mrid: str) -> AssetOrganisationRole:
        return self.organisation_roles.get_by_mrid(mrid)

    @deprecated("Use obj.organisation_roles.append(role) instead.")
    def add_organisation_role(self, role: AssetOrganisationRole) -> Asset:
        self.organisation_roles.append(role)
        return self

    @deprecated("Use obj.organisation_roles.remove(role) instead.")
    def remove_organisation_role(self, role: AssetOrganisationRole) -> Asset:
        self.organisation_roles.remove(role)
        return self

    @deprecated("Use obj.organisation_roles.clear() instead.")
    def clear_organisation_roles(self) -> Asset:
        self.organisation_roles.clear()
        return self

    # endregion organisation_roles boilerplate

    # region power_system_resources boilerplate

    @deprecated("Use len(obj.power_system_resources) instead.")
    def num_power_system_resources(self) -> int:
        return len(self.power_system_resources)

    @deprecated("Use obj.power_system_resources.get_by_mrid(mrid) instead.")
    def get_power_system_resource(self, mrid: str) -> PowerSystemResource:
        return self.power_system_resources.get_by_mrid(mrid)

    @deprecated("Use obj.power_system_resources.append(resource) instead.")
    def add_power_system_resource(self, resource: PowerSystemResource) -> Asset:
        self.power_system_resources.append(resource)
        return self

    @deprecated("Use obj.power_system_resources.remove(resource) instead.")
    def remove_power_system_resource(self, resource: PowerSystemResource) -> Asset:
        self.power_system_resources.remove(resource)
        return self

    @deprecated("Use obj.power_system_resources.clear() instead.")
    def clear_power_system_resources(self) -> Asset:
        self.power_system_resources.clear()
        return self

    # endregion power_system_resources boilerplate

    # endregion deprecated list boilerplate
